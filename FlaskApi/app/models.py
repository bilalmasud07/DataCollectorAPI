from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class CVE(db.Model):
    __tablename__ = 'cve'
    cve_id = db.Column(db.String(255), primary_key=True)
    sourceidentifier = db.Column(db.String(255), nullable=False)
    published = db.Column(db.TIMESTAMP, nullable=False)
    lastmodified = db.Column(db.TIMESTAMP, nullable=False)
    vulnstatus = db.Column(db.String(255), nullable=False)

class Descriptions(db.Model):
    __tablename__ = 'descriptions'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    cve_id = db.Column(db.String(255), db.ForeignKey('cve.cve_id'))
    lang = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Text)

class CVSSMetric(db.Model):
    __tablename__ = 'cvssmetric'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    cve_id = db.Column(db.String(255), db.ForeignKey('cve.cve_id'))
    source_type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('source_type.id'))
    version = db.Column(db.Float, nullable=False)
    exploitabilityscore = db.Column(db.Float, nullable=False)
    impactscore = db.Column(db.Float, nullable=False)
    attackvector = db.Column(db.String(50))
    vectorstring = db.Column(db.String(255))
    basescore = db.Column(db.Float, nullable=False)
    baseseverity = db.Column(db.String(20), nullable=False)

class SourceType(db.Model):
    __tablename__ = 'source_type'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    source = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(15), nullable=False)

class Weaknesses(db.Model):
    __tablename__ = 'weaknesses'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    cve_id = db.Column(db.String(255), db.ForeignKey('cve.cve_id'))
    source = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(15), nullable=False)

class WeaknessesDescriptions(db.Model):
    __tablename__ = 'weaknesses_descriptions'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    weakness_id = db.Column(UUID(as_uuid=True), db.ForeignKey('weaknesses.id'))
    lang = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Text, nullable=False)

class Configurations(db.Model):
    __tablename__ = 'configurations'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    cve_id = db.Column(db.String(255), db.ForeignKey('cve.cve_id'))
    operator = db.Column(db.String(10))

class Nodes(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    configuration_id = db.Column(UUID(as_uuid=True), db.ForeignKey('configurations.id'))
    operator = db.Column(db.String(10), nullable=False)
    negate = db.Column(db.Boolean, nullable=False)

class CpeMatch(db.Model):
    __tablename__ = 'cpematch'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    node_id = db.Column(UUID(as_uuid=True), db.ForeignKey('nodes.id'))
    vulnerable = db.Column(db.Boolean, nullable=False)
    criteria = db.Column(db.String(255), nullable=False)
    matchcriteriaid = db.Column(UUID(as_uuid=True), nullable=False)

class MatchString(db.Model):
    __tablename__ = 'matchstring'
    matchcriteriaid = db.Column(UUID(as_uuid=True), primary_key=True)
    criteria = db.Column(db.String(255), nullable=False)
    lastmodified = db.Column(db.TIMESTAMP, nullable=False)
    cpeLastmodified = db.Column(db.TIMESTAMP)
    created = db.Column(db.TIMESTAMP, nullable=False)
    status = db.Column(db.String(20), nullable=False)

class Matches(db.Model):
    __tablename__ = 'matches'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    matchcriteriaid = db.Column(UUID(as_uuid=True), db.ForeignKey('matchstring.matchCriteriaId'))
    cpeName = db.Column(db.String(255), nullable=False)
    cpeNameId = db.Column(UUID(as_uuid=True), db.ForeignKey('cpe.cpeNameId'))

class CPE(db.Model):
    __tablename__ = 'cpe'
    cpenameid = db.Column(UUID(as_uuid=True), primary_key=True)
    cpename = db.Column(db.String(255), nullable=False)
    deprecated = db.Column(db.Boolean, nullable=False)
    lastmodified = db.Column(db.TIMESTAMP, nullable=False)
    created = db.Column(db.TIMESTAMP, nullable=False)

class Titles(db.Model):
    __tablename__ = 'titles'
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    cpenameid = db.Column(UUID(as_uuid=True), db.ForeignKey('cpe.cpeNameId'))
    title = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Text, nullable=False)
