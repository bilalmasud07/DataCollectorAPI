import collections

Params = collections.OrderedDict()

Params['CPE_INFO'] = {
    'URL': 'https://services.nvd.nist.gov/rest/json/cpes/2.0/',
}
Params['STORE_DATA'] = {
    'cpe': 'cpe.csv',
    'titles': 'titles.csv'
}
Params['SUB_DIR'] = {
    'dir_name': 'cpe_csv_data'
}
Params['HEADERS'] = {
    'cpe': ['cpeNameId', 'cpeName', 'deprecated', 'lastModified', 'created'],
    'titles': ['id', 'cpeNameId', 'title', 'lang']
}