from flask import request, jsonify
#from app import db
from app.models import CVE, CVSSMetric, CpeMatch, Nodes, Configurations, SourceType, Matches, MatchString, CPE, Titles, Descriptions
import logging
from sqlalchemy.sql import text
from datetime import datetime

def register_routes(app, db):
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({"message": "Welcome to the CVE API!"}), 200

    @app.route('/test_db', methods=['GET'])
    def test_db():
        try:
            query = text("SELECT * FROM cve LIMIT 10;")
            result = db.session.execute(query).fetchall()
            #data = [dict(row) for row in result]
            data = [{'cve_id': row.cve_id, 'sourceIdentifier': row.sourceidentifier} for row in result]
            return jsonify(data), 200
        except Exception as e:
            logging.error(f"Error in test_db: {e}")
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
