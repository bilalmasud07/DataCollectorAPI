from flask import jsonify, Response
from app.models import CVE, CVSSMetric, CpeMatch, Nodes, Configurations, SourceType, Matches, MatchString, CPE, Titles, Descriptions, Weaknesses, WeaknessesDescriptions
import logging
from sqlalchemy.sql import text
from datetime import datetime, timezone
import json
from sqlalchemy import func
from collections import defaultdict

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
            # Query to join necessary tables
            cpe_data = db.session.query(
                CPE,
                Titles
            ).outerjoin(Titles, Titles.cpenameid == CPE.cpenameid)\
            .filter(CPE.cpenameid == cpename_id)\
            .all()
            logging.info(f"cpe_data: {cpe_data}")
            if not cpe_data:
                return jsonify({"error": f"CPE with ID {cpename_id} not found."}), 404

            # Create the cpe object
            cpe = cpe_data[0][0]
            titles = [title for cpe, title in cpe_data if title]

            data = {
                "totalResults": len(cpe_data),
                "format": "NVD_CPE",
                "version": "2.0",
                "timestamp": formatted_time,
                "products": [
                    {
                        "cpe": {
                            "deprecated": cpe.deprecated,
                            "cpeName": cpe.cpename,
                            "cpeNameid": str(cpe.cpenameid).upper(),
                            "lastModified": cpe.lastmodified.isoformat(timespec='milliseconds') if cpe.lastmodified else None,
                            "created": cpe.created.isoformat(timespec='milliseconds') if cpe.created else None,
                            "titles": [
                                {"title": title.title, "title": title.title} for title in titles
                            ]
                        }
                    }
                ]
            }
            response = Response(json.dumps(data), mimetype='application/json')
            return response, 200
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
            data = {
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
            }
            response = Response(json.dumps(data), mimetype='application/json')
            return response, 200
        except Exception as e:
            logging.error(f"Error in get_cve: {e}")
            return jsonify({"error": "Internal Server Error"}), 500


    @app.route('/severity_distribution', methods=['GET'])
    def severity_distribution():
        try:
            logging.info("Executing a query for: severity_distribution")
            
            # Ensure the date is a datetime object
            cutoff_date = datetime.strptime('2024-05-02', '%Y-%m-%d')

            result = db.session.query(
                CVE.cve_id,
                CVSSMetric.exploitabilityscore
            ).join(CVSSMetric, CVSSMetric.cve_id == CVE.cve_id)\
            .filter(CVE.lastmodified < cutoff_date)\
            .filter(CVE.vulnstatus != 'Rejected')\
            .order_by(CVSSMetric.exploitabilityscore.desc(), CVE.cve_id)\
            .limit(10).all()

            data = [{'cve_id': row.cve_id, 'exploitabilityScore': row.exploitabilityscore} for row in result]
            response = Response(json.dumps(data), mimetype='application/json')
            return response, 200
        except Exception as e:
            logging.error(f"Error in severity_distribution: {e}")
            return jsonify({"error": "Internal Server Error"}), 500


    @app.route('/worst_products_platforms', methods=['GET'])
    def worst_products_platforms():
        try:
            cutoff_date = datetime.strptime('2024-05-02', '%Y-%m-%d')

            result = db.session.query(
                CPE.cpename.label('product'),
                func.count(CPE.cpename).label('total_known_vulnerabilities')
            ).join(Titles, Titles.cpenameid == CPE.cpenameid)\
            .join(Matches, Matches.cpenameid == CPE.cpenameid)\
            .join(MatchString, MatchString.matchcriteriaid == Matches.matchcriteriaid)\
            .join(CpeMatch, CpeMatch.matchcriteriaid == MatchString.matchcriteriaid)\
            .join(Nodes, CpeMatch.node_id == Nodes.id)\
            .join(Configurations, Nodes.configuration_id == Configurations.id)\
            .join(CVE, Configurations.cve_id == CVE.cve_id)\
            .filter(CVE.lastmodified < cutoff_date)\
            .filter(CVE.vulnstatus != 'Rejected')\
            .filter(CPE.deprecated == False)\
            .group_by(CPE.cpename)\
            .order_by(func.count(CPE.cpename).desc())\
            .limit(10).all()

            data = [{'product': row.product, 'total_known_vulnerabilities': row.total_known_vulnerabilities} for row in result]
            response = Response(json.dumps(data), mimetype='application/json')
            return response, 200

        except Exception as e:
            logging.error(f"Error in worst_products_platforms: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    @app.route('/top_vulnerabilities_highest_impact', methods=['GET'])
    def top_vulnerabilities_highest_impact():
        try:
            logging.info("Executing a query for: top_vulnerabilities_highest_impact")
            # Ensure the date is a datetime object
            cutoff_date = datetime.strptime('2024-05-02', '%Y-%m-%d')

            result = db.session.query(
                CVE.cve_id,
                CVSSMetric.impactscore
            ).join(CVSSMetric, CVSSMetric.cve_id == CVE.cve_id)\
            .filter(CVE.lastmodified < cutoff_date)\
            .filter(CVE.vulnstatus != 'Rejected')\
            .order_by(CVSSMetric.impactscore.desc(), CVE.cve_id)\
            .limit(10).all()

            data = [{'cve_id': row.cve_id, 'impactScore': row.impactscore} for row in result]
            response = Response(json.dumps(data), mimetype='application/json')
            return response, 200
        except Exception as e:
            logging.error(f"Error in top_vulnerabilities_highest_impact: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    @app.route('/top_vulnerabilities_highest_exploitability', methods=['GET'])
    def top_vulnerabilities_highest_exploitability():
        try:
            cutoff_date = datetime.strptime('2024-05-02', '%Y-%m-%d')

            result = db.session.query(
                CVE.cve_id,
                CVSSMetric.exploitabilityscore
            ).join(CVSSMetric, CVSSMetric.cve_id == CVE.cve_id)\
            .filter(CVE.lastmodified < cutoff_date)\
            .filter(CVE.vulnstatus != 'Rejected')\
            .order_by(CVSSMetric.exploitabilityscore.desc(), CVE.cve_id)\
            .limit(10).all()

            data = [{'cve_id': row.cve_id, 'exploitabilityscore': row.exploitabilityscore} for row in result]
            response = Response(json.dumps(data), mimetype='application/json')
            return response, 200

        except Exception as e:
            logging.error(f"Error in top_vulnerabilities_highest_exploitability: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    @app.route('/top_attack_vectors', methods=['GET'])
    def top_attack_vectors():
        try:
            cutoff_date = datetime.strptime('2024-05-02', '%Y-%m-%d')

            result = db.session.query(
                CVSSMetric.attackvector,
                func.count(CVSSMetric.attackvector).label('total_count')
            ).join(CVE, CVSSMetric.cve_id == CVE.cve_id)\
            .filter(CVE.lastmodified < cutoff_date)\
            .filter(CVE.vulnstatus != 'Rejected')\
            .group_by(CVSSMetric.attackvector)\
            .order_by(func.count(CVSSMetric.attackvector).desc())\
            .limit(10).all()

            data = [{'attackVector': row.attackvector, 'total_count': row.total_count} for row in result]
            response = Response(json.dumps(data), mimetype='application/json')
            return response, 200

        except Exception as e:
            logging.error(f"Error in top_attack_vectors: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    @app.route('/matchCriteriaId=<uuid:matchcriteriaid>', methods=['GET'])
    def match_strings(matchcriteriaid):
        try:
            # Query to join necessary tables
            result = db.session.query(
                MatchString,
                Matches
            ).join(Matches, MatchString.matchcriteriaid == Matches.matchcriteriaid)\
            .filter(MatchString.matchcriteriaid == matchcriteriaid)\
            .all()

            match_strings_dict = defaultdict(list)
            for match_string, match in result:
                match_strings_dict[match_string].append(match)
            logging.info(f"match_strings_dict: {match_strings_dict}")
            match_strings = []
            for match_string_id, matches in match_strings_dict.items():
                match_string = match_string_id  # Get the MatchString instance from the first match
                match_strings.append({
                    "matchString": {
                        "matchCriteriaId": str(match_string.matchcriteriaid).upper(),
                        "criteria": match_string.criteria,
                        "lastModified": match_string.lastmodified.isoformat(timespec='milliseconds') if match_string.lastmodified else None,
                        "cpeLastModified": match_string.cpelastmodified.isoformat(timespec='milliseconds') if match_string.cpelastmodified else None,
                        "created": match_string.created.isoformat(timespec='milliseconds') if match_string.created else None,
                        "status": match_string.status,
                        "matches": [
                            {
                                "cpeName": match.cpename,
                                "cpeNameId": str(match.cpenameid).upper()
                            } for match in matches
                        ]
                    }
                })

            data = {
                "totalResults": len(match_strings),
                "format": "NVD_CPEMatchString",
                "version": "2.0",
                "timestamp": datetime.now().isoformat(timespec='milliseconds'),
                "matchStrings": match_strings
            }

            response = Response(json.dumps(data), mimetype='application/json')
            return response, 200

        except Exception as e:
            logging.error(f"Error in match_strings: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    logging.info("Routes have been registered successfully.")
