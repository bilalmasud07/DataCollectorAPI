-- cve info

CREATE TABLE CVE (
    cve_id VARCHAR(255) PRIMARY KEY,
    sourceIdentifier VARCHAR(255) NOT NULL,
    published TIMESTAMP NOT NULL,
    lastModified TIMESTAMP NOT NULL,
    vulnStatus VARCHAR(255) NOT NULL
);

CREATE TABLE Descriptions (
    id UUID PRIMARY KEY,
    cve_id VARCHAR(255) REFERENCES CVE(cve_id),
    lang VARCHAR(10) NOT NULL,
    value TEXT
);


CREATE TABLE CVSSMetric (
    id UUID PRIMARY KEY,
    cve_id VARCHAR(255) REFERENCES CVE(cve_id),
    source_type_id UUID REFERENCES Source_type(id),
    version FLOAT NOT NULL,
    exploitabilityScore FLOAT NOT NULL,
    impactScore FLOAT NOT NULL,
    attackVector VARCHAR(50),
    vectorString VARCHAR(255),
    baseScore FLOAT NOT NULL,
    baseSeverity VARCHAR(20) NOT NULL
);

CREATE TABLE Source_type (
    id UUID PRIMARY KEY,
    source VARCHAR(255) NOT NULL,
    type VARCHAR(15) NOT NULL
);

CREATE TABLE Weaknesses (
    id UUID PRIMARY KEY,
    cve_id VARCHAR(255) REFERENCES CVE(cve_id),
    source VARCHAR(255) NOT NULL,
    type VARCHAR(15) NOT NULL
);

CREATE TABLE Weaknesses_Descriptions (
    id UUID PRIMARY KEY,
    weakness_id UUID REFERENCES Weaknesses(id),
    lang VARCHAR(10) NOT NULL,
    value TEXT NOT NULL
);

CREATE TABLE Configurations (
    id UUID PRIMARY KEY,
    cve_id VARCHAR(255) REFERENCES CVE(cve_id),
    operator VARCHAR(10)
);

CREATE TABLE Nodes (
    id UUID PRIMARY KEY,
    configuration_id UUID REFERENCES Configurations(id),
    operator VARCHAR(10) NOT NULL,
    negate BOOLEAN NOT NULL
);

CREATE TABLE CpeMatch (
    id UUID PRIMARY KEY,
    node_id UUID REFERENCES Nodes(id),
    vulnerable BOOLEAN NOT NULL,
    criteria VARCHAR(255) NOT NULL,
    matchCriteriaId UUID not NULL
);

-- cpematch info

CREATE TABLE MatchString (
	matchCriteriaId UUID PRIMARY KEY,
	criteria VARCHAR(255) NOT NULL,
	lastModified TIMESTAMP NOT NULL,
	cpeLastModified TIMESTAMP,
    created TIMESTAMP NOT null,
    status VARCHAR(20) NOT null
);

CREATE TABLE Matches (
    id UUID PRIMARY KEY,
    matchCriteriaId UUID REFERENCES MatchString(matchCriteriaId),
    cpeName VARCHAR(255) NOT NULL,
    cpeNameId UUID REFERENCES CPE(cpeNameId)
);


-- products info

CREATE TABLE CPE (
    cpeNameId UUID PRIMARY KEY,
    cpeName VARCHAR(255) NOT NULL,
    deprecated BOOLEAN NOT NULL,
    lastModified TIMESTAMP NOT NULL,
    created TIMESTAMP NOT NULL
);

CREATE TABLE Titles (
    id UUID PRIMARY KEY,
    cpeNameId UUID REFERENCES CPE(cpeNameId),
    title VARCHAR(255) NOT NULL,
    value TEXT NOT NULL
);

