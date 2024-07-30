import collections

Params = collections.OrderedDict()

Params['CVE_INFO'] = {
    'URL': 'https://services.nvd.nist.gov/rest/json/cves/2.0/',
}
Params['STORE_DATA'] = {
    'cve': 'cve.csv',
    'descriptions': 'descriptions.csv',
    'cvss_metric': 'cvss_metric.csv',
    'source_type': 'source_type.csv',
    'weaknesses': 'weaknesses.csv',
    'weaknesses_descriptions': 'weaknesses_descriptions.csv',
    'configurations': 'configurations.csv',
    'nodes': 'nodes.csv',
    'cpe_match': 'cpe_match.csv'
}
Params['SUB_DIR'] = {
    'dir_name': 'cve_csv_data'
}
Params['HEADERS'] = {
    'cve': ['cve_id', 'sourceIdentifier', 'published', 'lastModified', 'vulnStatus'],
    'descriptions': ['id', 'cve_id', 'lang', 'value'],
    'cvss_metric': [
        'id', 'cve_id', 'source_type_id', 'version', 'exploitabilityScore', 'impactScore', 'attackVector',
        'vectorString', 'baseScore', 'baseSeverity'
    ],
    'source_type': ['id', 'source', 'type'],
    'weaknesses': ['id', 'cve_id', 'source', 'type'],
    'weaknesses_descriptions': ['id', 'weakness_id', 'lang', 'value'],
    'configurations': ['id', 'cve_id', 'operator'],
    'nodes': ['id', 'configuration_id', 'operator', 'negate'],
    'cpe_match': ['id', 'node_id', 'vulnerable', 'criteria', 'matchCriteriaId']
}