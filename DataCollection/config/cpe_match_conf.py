import collections

Params = collections.OrderedDict()

Params['CPE_MATCH_INFO'] = {
    'URL': 'https://services.nvd.nist.gov/rest/json/cpematch/2.0/',
}
Params['STORE_DATA'] = {
    'matchString': 'matchString.csv',
    'matches': 'matches.csv'
}
Params['SUB_DIR'] = {
    'dir_name': 'cpematch_csv_data'
}
Params['HEADERS'] = {
    'matchString': ['matchCriteriaId', 'criteria', 'lastModified', 'cpeLastModified', 'created', 'status'],
    'matches': ['id', 'matchCriteriaId', 'cpeName', 'cpeNameId']
}