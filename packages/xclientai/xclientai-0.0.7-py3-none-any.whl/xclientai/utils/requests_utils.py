import requests
from requests.adapters import HTTPAdapter, Retry
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def do_request(
    url, 
    http_method, 
    json_data=None, 
    headers=None,
    params=None
):
    session = requests.Session()
    retries = Retry(
        total=5,
        status_forcelist=[ 500, 502, 503, 504 ]
    )
    
    session.mount("http://", HTTPAdapter(max_retries=retries))
    
    params_fn = {
        "url": url, 
        "json": json_data,
        "timeout": 300,
        "headers": headers,
        "verify": False,
        "params": params
    }
    
    if http_method == "get":
        response = session.get(**params_fn)
    elif http_method == "post":
        response = session.post(**params_fn)
    elif http_method == "patch":
        response = session.patch(**params_fn)
    elif http_method == "delete":
        response = session.delete(**params_fn)
    elif http_method == "put":
        response = session.put(**params_fn)
    
    error = False
    try:
        response.raise_for_status()
    except Exception as ex:
        error = True
        
    if error:
        raise Exception(response.json()["message"])
    
    return response