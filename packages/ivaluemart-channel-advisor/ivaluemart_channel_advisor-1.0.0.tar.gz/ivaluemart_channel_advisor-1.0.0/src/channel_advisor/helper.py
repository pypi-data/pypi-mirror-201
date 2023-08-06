import logging
from time import sleep
from urllib import request, parse
import json

RETRY_GET_RESPONSE_AFTER = 30


def ca_filter(value, name="Sku"):
    return parse.urlencode({"$filter": name + " eq '" + value + "'"})


def get_response(url, retries=0):
    logging.debug(f'get_response retries {retries}')
    try:
        req = request.Request(url=url)
        response = request.urlopen(req)
        if response.status == 200:
            return json.loads(response.read())
    except ConnectionResetError:
        if retries >= 2:
            logging.error(f'Received ConnectionResetError on url {url}')
            raise ConnectionResetError
        else:
            logging.debug(f'sleep for 30 seconds after ConnectionResetError')
            sleep(RETRY_GET_RESPONSE_AFTER)
            return get_response(url, retries + 1)