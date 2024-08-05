-- loading CSV data into PostgreSql Database

copy CVE(cve_id, sourceIdentifier, published, lastModified, vulnStatus)
from '.../DataCollection/cve_csv_data/cve.csv' delimiter '|' csv header;

COPY Descriptions(id, cve_id, lang, value) 
FROM '.../DataCollection/cve_csv_data/descriptions.csv' DELIMITER '|' CSV HEADER;

COPY CVSSMetric(id, cve_id, source_type_id, version, exploitabilityScore, impactScore, attackVector, vectorString, baseScore, baseSeverity) 
FROM '.../DataCollection/cve_csv_data/cvss_metric.csv' DELIMITER '|' CSV HEADER;

COPY Source_type(id, source, type) 
FROM '.../DataCollection/cve_csv_data/source_type.csv' DELIMITER '|' CSV HEADER;

COPY Weaknesses(id, cve_id, source, type) 
FROM 'D.../DataCollection/cve_csv_data/weaknesses.csv' DELIMITER '|' CSV HEADER;

COPY Weaknesses_Descriptions(id, weakness_id, lang, value) 
FROM '.../DataCollection/cve_csv_data/weaknesses_descriptions.csv' DELIMITER '|' CSV HEADER;

COPY Configurations(id, cve_id, operator) 
FROM '.../DataCollection/cve_csv_data/configurations.csv' DELIMITER '|' CSV HEADER;

COPY Nodes(id, configuration_id, operator, negate) 
FROM '.../DataCollection/cve_csv_data/nodes.csv' DELIMITER '|' CSV HEADER;

COPY CpeMatch(id, node_id, vulnerable, criteria, matchCriteriaId) 
FROM '.../DataCollection/cve_csv_data/cpe_match.csv' DELIMITER '|' CSV HEADER;


COPY MatchString(matchCriteriaId, criteria, lastModified, cpeLastModified, created, status) 
FROM '.../DataCollectorAPI/DataCollection/cpematch_csv_data/matchString.csv' DELIMITER '|' CSV HEADER;

COPY Matches(id, matchCriteriaId, cpeName, cpeNameId) 
FROM '.../DataCollectorAPI/DataCollection/cpematch_csv_data/matches.csv' DELIMITER '|' CSV HEADER;


COPY CPE(cpeNameId, cpeName, deprecated, lastModified, created) 
FROM '.../DataCollectorAPI/DataCollection/cpe_csv_data/cpe.csv' DELIMITER '|' CSV HEADER;

COPY Titles(id, cpeNameId, title, value) 
FROM '.../DataCollectorAPI/DataCollection/cpe_csv_data/titles.csv' DELIMITER '|' CSV HEADER;