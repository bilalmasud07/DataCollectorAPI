import requests
import logging

def fetch_data(api_url, api_key, start_index=0):
    log = logging.getLogger(__name__)
    params = {'startIndex': start_index}
    headers = {"apiKey": api_key}

    try:
        response = requests.get(api_url, headers=headers, params=params)
        log.info(f"Response: {response}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        log.error(f"HTTP error occurred: {http_err}")
        raise
    except requests.exceptions.RequestException as req_err:
        log.error(f"Request failed: {req_err}")
        raise
