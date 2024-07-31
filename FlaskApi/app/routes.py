from flask import jsonify
from app.models import CVE, CVSSMetric, CpeMatch, Nodes, Configurations, SourceType, Matches, MatchString, CPE, Titles, Descriptions, Weaknesses, WeaknessesDescriptions
import logging
from sqlalchemy.sql import text
from datetime import datetime, timezone
from collections import OrderedDict

# Get the current UTC time with timezone awareness
current_utc_time = datetime.now(timezone.utc)

# Format it as requested
formatted_time = current_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]


def register_routes(app, db):
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({"message": "Welcome to the CVE API!"}), 200

    @app.route('/Product_ID=<uuid:cpename_id>', methods=['GET'])
    def get_cpe(cpename_id):
        try:
            query = text("SELECT * FROM CPE WHERE cpeNameId = :cpename_id")
            result = db.session.execute(query, {'cpename_id': cpename_id}).fetchone()
            if result:
                data = OrderedDict({
                    'cpenameid': result.cpenameid,
                    'cpename': result.cpename,
                    'deprecated': result.deprecated,
                    'lastmodified': result.lastmodified,
                    'created': result.created
                })
                return jsonify(data), 200
            else:
                return jsonify({"error": f"CPE with cpeNameId {cpename_id} not found."}), 404
        except Exception as e:
            logging.error(f"Error in get_cpe: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    @app.route('/CVE_ID=<string:cveid>', methods=['GET'])
    def get_cve(cveid):
        try:
            cve = db.session.query(CVE).filter_by(cve_id=cveid).first()
            if not cve:
                return jsonify({"error": f"CVE with ID {cveid} not found."}), 404

            descriptions = db.session.query(Descriptions).filter_by(cve_id=cveid).all()
            cvss_metrics = db.session.query(CVSSMetric).filter_by(cve_id=cveid).all()
            weaknesses = db.session.query(Weaknesses).filter_by(cve_id=cveid).all()
            configurations = db.session.query(Configurations).filter_by(cve_id=cveid).all()

            metrics_data = {
                "cvssMetricV2": [
                    {
                        "source": source_type.source,
                        "type": source_type.type,
                        "cvssData": {
                            "version": metric.version,
                            "vectorString": metric.vectorString,
                            "accessVector": metric.attackVector,
                            "baseScore": metric.baseScore
                        },
                        "baseSeverity": metric.baseSeverity,
                        "exploitabilityScore": metric.exploitabilityScore,
                        "impactScore": metric.impactScore
                    } for metric in cvss_metrics if metric.version == 2 for source_type in [db.session.query(SourceType).filter_by(id=metric.source_type_id).first()]
                ],
                "cvssMetricV3": [
                    {
                        "source": source_type.source,
                        "type": source_type.type,
                        "cvssData": {
                            "version": metric.version,
                            "vectorString": metric.vectorstring,
                            "accessVector": metric.attackvector,
                            "baseSeverity": metric.baseseverity,
                            "baseScore": metric.basescore
                        },
                        "exploitabilityScore": metric.exploitabilityscore,
                        "impactScore": metric.impactscore
                    } for metric in cvss_metrics if metric.version >= 3 for source_type in [db.session.query(SourceType).filter_by(id=metric.source_type_id).first()]
                ] # for metric in cvss_metrics for source_type in db.session.query(SourceType).filter_by(id=metric.source_type_id).all()
            }
            logging.info(f"metric: {metrics_data}")
            data = OrderedDict({
                    "resultsPerPage": 1,
                    "startIndex": 0,
                    "totalResults": 1,
                    "format": "NVD_CVE",
                    "version": "2.0",
                    "timestamp": formatted_time,
                    "vulnerabilities": [
                    {
                        "cve": {
                            "id": cve.cve_id,
                            "sourceIdentifier": cve.sourceidentifier,
                            "published": cve.published.isoformat(timespec='milliseconds') if cve.published else None,
                            "lastModified": cve.lastmodified.isoformat(timespec='milliseconds') if cve.lastmodified else None,
                            "vulnStatus": cve.vulnstatus,
                            "descriptions": [
                                {"lang": desc.lang, "value": desc.value} for desc in descriptions
                            ],
                            # "metrics": {
                            #     "cvssMetricV2": [
                            #         {
                            #             "source": source_type.source,
                            #             "type": source_type.type,
                            #             "cvssData": {
                            #                 "version": metric.version,
                            #                 "vectorString": metric.vectorstring,
                            #                 "attackVector": metric.attackvector,
                            #                 "baseScore": metric.basescore
                            #             },
                            #             "baseSeverity": metric.baseseverity,
                            #             "exploitabilityScore": metric.exploitabilityscore,
                            #             "impactScore": metric.impactscore
                            #         } for metric in cvss_metrics for source_type in db.session.query(SourceType).filter_by(id=metric.source_type_id).all()
                            #     ]
                            # },
                            "metrics": {
                                k: v for k, v in metrics_data.items() if v  # Only include if the list is not empty
                            },
                            "weaknesses": [
                                {
                                    "source": weakness.source,
                                    "type": weakness.type,
                                    "description": [
                                        {"lang": desc.lang, "value": desc.value} for desc in db.session.query(WeaknessesDescriptions).filter_by(weakness_id=weakness.id).all()
                                    ]
                                } for weakness in weaknesses
                            ],
                            "configurations": [
                                {
                                    "nodes": [
                                        {
                                            "operator": node.operator,
                                            "negate": node.negate,
                                            "cpeMatch": [
                                                {
                                                    "vulnerable": match.vulnerable,
                                                    "criteria": match.criteria,
                                                    "matchCriteriaId": str(match.matchcriteriaid).upper()
                                                } for match in db.session.query(CpeMatch).filter_by(node_id=node.id).all()
                                            ]
                                        } for node in db.session.query(Nodes).filter_by(configuration_id=config.id).all()
                                    ]
                                } for config in configurations
                            ]
                        }
                    }
                ]
            })
            return jsonify(data), 200
        except Exception as e:
            logging.error(f"Error in get_cve: {e}")
            return jsonify({"error": "Internal Server Error"}), 500


    @app.route('/severity_distribution', methods=['GET'])
    def severity_distribution():
        try:
            logging.info("Executing a query for: severity_distribution")
            # query = text("""
            #                 SELECT cvsm.baseSeverity as baseseverity, COUNT(*) as total_severties
            #                 FROM CVSSMetric cvsm
            #                 join Source_type st on cvsm.source_type_id = st.id
            #                 JOIN CVE ON cvsm.cve_id = CVE.cve_id
            #                 WHERE CVE.lastmodified < '2024-05-02' and cve.vulnstatus != 'Rejected' and st.type = 'Primary'
            #                 GROUP by baseseverity
            #                 order by baseseverity;
            # """)
            
            # result = db.session.execute(query).fetchall()

            # logging.info(f"Result of severity_distribution query: {result}")

            # data = [{'severity': row.baseseverity, 'total_severties': row.total_severties} for row in result]
            # return jsonify(data), 200
            
            # Ensure the date is a datetime object
            cutoff_date = datetime.strptime('2024-05-02', '%Y-%m-%d')

            result = db.session.query(
                CVE.cve_id,
                CVSSMetric.exploitabilityScore
            ).join(CVSSMetric, CVSSMetric.cve_id == CVE.cve_id)\
            .filter(CVE.lastModified < cutoff_date)\
            .filter(CVE.vulnStatus != 'Rejected')\
            .order_by(CVSSMetric.exploitabilityScore.desc(), CVE.cve_id)\
            .limit(10).all()

            data = [{'cve_id': row.cve_id, 'exploitabilityScore': row.exploitabilityScore} for row in result]
            return jsonify(data), 200

        except Exception as e:
            logging.error(f"Error in severity_distribution: {e}")
            return jsonify({"error": "Internal Server Error"}), 500


    @app.route('/worst_products_platforms', methods=['GET'])
    def worst_products_platforms():
        try:
            logging.info("Executing a query for: worst_products_platforms")
            query = text("""
                            select cp.cpename as product, count(*) as total_known_vulnerabilities
                            from cpe cp
                            inner join Titles t on t.cpenameid = cp.cpenameid 
                            inner join matches m on m.cpenameid = cp.cpenameid 
                            inner join matchstring ms on ms.matchcriteriaid = m.matchcriteriaid 
                            inner join cpematch cpm on cpm.matchcriteriaid = ms.matchcriteriaid 
                            inner join nodes n on cpm.node_id = n.id 
                            inner join configurations conf on n.configuration_id = conf.id 
                            inner join cve cv on conf.cve_id = cv.cve_id 
                            WHERE cv.lastModified < '2024-05-02' and cv.vulnstatus != 'Rejected'
                            group by cp.cpename 
                            order by total_known_vulnerabilities desc;
            """)
            
            result = db.session.execute(query).fetchall()

            logging.info(f"Result of worst_products_platforms query: {result}")

            data = [{'product': row.product, 'total_known_vulnerabilities': row.total_known_vulnerabilities} for row in result]
            return jsonify(data), 200

        except Exception as e:
            logging.error(f"Error in worst_products_platforms: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    @app.route('/top_vulnerabilities_highest_impact', methods=['GET'])
    def top_vulnerabilities_highest_impact():
        try:
            logging.info("Executing a query for: top_vulnerabilities_highest_impact")
            query = text("""
                            SELECT c.cve_id, cvsm.impactScore as impactScore
                            FROM CVSSMetric cvsm
                            JOIN CVE c ON cvsm.cve_id = c.cve_id
                            WHERE c.lastmodified < '2024-05-02' and c.vulnstatus != 'Rejected'
                            ORDER BY cvsm.impactScore DESC, c.cve_id
                            LIMIT 10;
            """)
            
            result = db.session.execute(query).fetchall()

            logging.info(f"Result of top_vulnerabilities_highest_impact query: {result}")

            data = [{'cve_id': row.cve_id, 'impactScore': row.impactscore} for row in result]
            return jsonify(data), 200

        except Exception as e:
            logging.error(f"Error in top_vulnerabilities_highest_impact: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    @app.route('/top_vulnerabilities_highest_exploitability', methods=['GET'])
    def top_vulnerabilities_highest_exploitability():
        try:
            logging.info("Executing a query for: top_vulnerabilities_highest_exploitability")
            query = text("""
                        SELECT c.cve_id, cvsm.exploitabilityscore as exploitabilityscore
                        FROM CVSSMetric cvsm
                        JOIN CVE c ON cvsm.cve_id = c.cve_id
                        WHERE c.lastmodified < '2024-05-02' and c.vulnstatus != 'Rejected'
                        ORDER BY cvsm.exploitabilityScore DESC, c.cve_id
                        LIMIT 10;
            """)
            
            result = db.session.execute(query).fetchall()

            logging.info(f"Result of top_vulnerabilities_highest_exploitability query: {result}")

            data = [{'cve_id': row.cve_id, 'exploitabilityscore': row.exploitabilityscore} for row in result]
            return jsonify(data), 200

        except Exception as e:
            logging.error(f"Error in top_vulnerabilities_highest_exploitability: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    @app.route('/top_attack_vectors', methods=['GET'])
    def top_attack_vectors():
        try:
            logging.info("Executing a query for: top_attack_vectors")
            query = text("""
                            SELECT cvsm.attackVector, COUNT(*) as total_count
                            FROM CVSSMetric cvsm
                            JOIN CVE c ON cvsm.cve_id = c.cve_id
                            WHERE c.lastmodified < '2024-05-02' and c.vulnstatus != 'Rejected'
                            GROUP BY attackVector
                            ORDER BY total_count DESC
                            LIMIT 10;
            """)
            
            result = db.session.execute(query).fetchall()

            logging.info(f"Result of top_attack_vectors query: {result}")

            data = [{'attackVector': row.attackvector, 'total_count': row.total_count} for row in result]
            return jsonify(data), 200

        except Exception as e:
            logging.error(f"Error in top_attack_vectors: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    logging.info("Routes have been registered successfully.")
