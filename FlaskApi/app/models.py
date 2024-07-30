from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class CVE(db.Model):
    __tablename__ = 'CVE'
    cve_id = db.Column(db.String(255), primary_key=True)
    sourceIdentifier = db.Column(db.String(255), nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    lastModified = db.Column(db.DateTime, nullable=False)
    vulnStatus = db.Column(db.String(255), nullable=False)
    descriptions = db.relationship('Descriptions', backref='cve', lazy=True)
    cvssmetrics = db.relationship('CVSSMetric', backref='cve', lazy=True)
    weaknesses = db.relationship('Weaknesses', backref='cve', lazy=True)
    configurations = db.relationship('Configurations', backref='cve', lazy=True)

class Descriptions(db.Model):
    __tablename__ = 'Descriptions'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cve_id = db.Column(db.String(255), db.ForeignKey('CVE.cve_id'))
    lang = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Text)

class SourceType(db.Model):
    __tablename__ = 'Source_type'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(15), nullable=False)
    cvssmetrics = db.relationship('CVSSMetric', backref='source_type', lazy=True)

class CVSSMetric(db.Model):
    __tablename__ = 'CVSSMetric'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cve_id = db.Column(db.String(255), db.ForeignKey('CVE.cve_id'))
    source_type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Source_type.id'))
    version = db.Column(db.Float, nullable=False)
    exploitabilityScore = db.Column(db.Float, nullable=False)
    impactScore = db.Column(db.Float, nullable=False)
    attackVector = db.Column(db.String(50))
    vectorString = db.Column(db.String(255))
    baseScore = db.Column(db.Float, nullable=False)
    baseSeverity = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<CVSSMetric {self.id}>'

class Weaknesses(db.Model):
    __tablename__ = 'Weaknesses'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cve_id = db.Column(db.String(255), db.ForeignKey('CVE.cve_id'))
    source = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(15), nullable=False)
    weaknesses_descriptions = db.relationship('WeaknessesDescriptions', backref='weakness', lazy=True)

class WeaknessesDescriptions(db.Model):
    __tablename__ = 'Weaknesses_Descriptions'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    weakness_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Weaknesses.id'))
    lang = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Text, nullable=False)

class Configurations(db.Model):
    __tablename__ = 'Configurations'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cve_id = db.Column(db.String(255), db.ForeignKey('CVE.cve_id'))
    operator = db.Column(db.String(10))
    nodes = db.relationship('Nodes', backref='configuration', lazy=True)

class Nodes(db.Model):
    __tablename__ = 'Nodes'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    configuration_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Configurations.id'))
    operator = db.Column(db.String(10), nullable=False)
    negate = db.Column(db.Boolean, nullable=False)
    cpe_matches = db.relationship('CpeMatch', backref='node', lazy=True)

class CpeMatch(db.Model):
    __tablename__ = 'CpeMatch'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Nodes.id'))
    vulnerable = db.Column(db.Boolean, nullable=False)
    criteria = db.Column(db.String(255), nullable=False)
    matchCriteriaId = db.Column(UUID(as_uuid=True), nullable=False)

class MatchString(db.Model):
    __tablename__ = 'MatchString'
    matchCriteriaId = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    criteria = db.Column(db.String(255), nullable=False)
    lastModified = db.Column(db.DateTime, nullable=False)
    cpeLastModified = db.Column(db.DateTime)
    created = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    matches = db.relationship('Matches', backref='match_string', lazy=True)

class Matches(db.Model):
    __tablename__ = 'Matches'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    matchCriteriaId = db.Column(UUID(as_uuid=True), db.ForeignKey('MatchString.matchCriteriaId'))
    cpeName = db.Column(db.String(255), nullable=False)
    cpeNameId = db.Column(UUID(as_uuid=True), db.ForeignKey('CPE.cpeNameId'))

class CPE(db.Model):
    __tablename__ = 'CPE'
    cpeNameId = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cpeName = db.Column(db.String(255), nullable=False)
    deprecated = db.Column(db.Boolean, nullable=False)
    lastModified = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    titles = db.relationship('Titles', backref='cpe', lazy=True)
    matches = db.relationship('Matches', backref='cpe', lazy=True)

class Titles(db.Model):
    __tablename__ = 'Titles'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cpeNameId = db.Column(UUID(as_uuid=True), db.ForeignKey('CPE.cpeNameId'))
    title = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Text, nullable=False)
