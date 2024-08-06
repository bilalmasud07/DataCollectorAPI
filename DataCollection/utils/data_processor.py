import uuid
import logging

def generate_uuid():
    return str(uuid.uuid4())

# CVE specific processing
def process_cve_data(cve_data):
    log = logging.getLogger(__name__)

    """Process CVE data and return rows for each CSV file."""
    cve_rows = []
    description_rows = []
    cvss_metric_rows = []
    source_type_rows = []
    weaknesses_rows = []
    weaknesses_description_rows = []
    configurations_rows = []
    nodes_rows = []
    cpe_match_rows = []
    
    for vul in cve_data:
        cve = vul['cve']
        cve_rows.append([
            cve['id'],
            cve['sourceIdentifier'],
            cve['published'],
            cve['lastModified'],
            cve['vulnStatus']
        ])
        for desc in cve['descriptions']:
            description_rows.append([
                generate_uuid(),
                cve['id'],
                desc['lang'],
                desc['value']
            ])
        metrics = cve.get('metrics', {})
        selected_metric = metrics.get('cvssMetricV31', []) or metrics.get('cvssMetricV30', [])
        if not selected_metric:
            selected_metric = metrics.get('cvssMetricV2', [])
        
        for metric in selected_metric:
            cvss = metric['cvssData']
            base_severity = metric.get('baseSeverity', None)
            base_severity = base_severity or cvss.get('baseSeverity', None)
            cvss_metric_id = generate_uuid()
            source_type_id = generate_uuid()
            cvss_metric_rows.append([
                    cvss_metric_id,
                    cve['id'],
                    source_type_id,
                    cvss['version'],
                    metric['exploitabilityScore'],
                    metric['impactScore'],
                    cvss.get('accessVector') or cvss.get('attackVector'),
                    cvss['vectorString'],
                    cvss['baseScore'],
                    base_severity
                ])
            source_type_rows.append([
                    source_type_id,
                    metric['source'],
                    metric['type']
                ])
        for weakness in cve.get('weaknesses', []):
            weakness_id = generate_uuid()
            weaknesses_rows.append([
                weakness_id,
                cve['id'],
                weakness['source'],
                weakness['type']
            ])
            for desc in weakness['description']:
                weaknesses_description_rows.append([
                    generate_uuid(),  # Unique ID for the description
                    weakness_id,
                    desc['lang'],
                    desc['value']
                ])
        for config in cve.get('configurations', []):
            config_id = generate_uuid()
            configurations_rows.append([
                config_id,  # Unique ID for the configuration
                cve['id'],
                config.get('operator', None)
            ])
            for node in config['nodes']:
                node_id = generate_uuid()
                nodes_rows.append([
                    node_id,  # Unique ID for the node
                    config_id,
                    node.get('operator', None),
                    node.get('negate', None)
                ])
                for match in node['cpeMatch']:
                    cpe_match_rows.append([
                        generate_uuid(),
                        node_id,
                        match['vulnerable'],
                        match['criteria'],
                        match['matchCriteriaId']
                    ])

    return {
        'cve': cve_rows,
        'descriptions': description_rows,
        'cvss_metric': cvss_metric_rows,
        'source_type': source_type_rows,
        'weaknesses': weaknesses_rows,
        'weaknesses_descriptions': weaknesses_description_rows,
        'configurations': configurations_rows,
        'nodes': nodes_rows,
        'cpe_match': cpe_match_rows
    }
    return processed_data

# CPE specific processing
def process_cpe_info(product):
    log = logging.getLogger(__name__)

    """Process CPE data and return rows for each CSV file."""
    # Extract relevant information
    cpe_rows = []
    title_rows = []

    for prod in product:
        cpe = prod["cpe"]
        cpe_rows.append([
            cpe['cpeNameId'],
            cpe['cpeName'],
            cpe['deprecated'],
            cpe['lastModified'],
            cpe['created']
        ])
        for title in cpe['titles']:
            title_rows.append([
                generate_uuid(),
                cpe['cpeNameId'],
                title['title'],
                title['lang']
            ])
    
    return {
        'cpe': cpe_rows,
        'titles': title_rows
    }

# CPE Match specific processing
def process_cpe_match_info(match_strings):
    log = logging.getLogger(__name__)

    """Process CPE data and return rows for each CSV file."""
    # Extract relevant information
    matchString_rows = []
    matches_rows = []

    for match_string in match_strings:
        match_string = match_string['matchString']
        matchString_rows.append([
            match_string['matchCriteriaId'],
            match_string['criteria'],
            match_string['lastModified'],
            match_string.get('cpeLastModified', None),
            match_string['created'],
            match_string['status']
        ])
        for match in match_string.get('matches', []):
            matches_rows.append([
                generate_uuid(),
                match_string['matchCriteriaId'],
                match['cpeName'],
                match['cpeNameId']
            ])
    
    return {
        'matchString': matchString_rows,
        'matches': matches_rows
    }
