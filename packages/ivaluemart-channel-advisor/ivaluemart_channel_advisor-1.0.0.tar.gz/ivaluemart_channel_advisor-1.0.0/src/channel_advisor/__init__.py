import logging
from urllib import request, parse
import requests
import json

from channel_advisor import helper


def get_access_token(headers, payload):
    url = "https://api.channeladvisor.com/oauth2/token"
    response = post(payload, url, headers)
    if response is not None:
        return response['access_token']

    return None


def post(payload, url, headers=None):
    if headers is None:
        req = request.Request(url=url, data=(parse.urlencode(payload).encode()), method="POST")
    else:
        req = request.Request(url=url, data=(parse.urlencode(payload).encode()), headers=headers, method="POST")
    response = request.urlopen(req)
    if response.status == 200:
        return json.loads(response.read())
    return None


def get_product_id(token, sku):
    url = "https://api.channeladvisor.com/v1/Products?access_token=" + token + "&" + helper.ca_filter(
        sku) + "&$select=ID"
    response = helper.get_response(url)
    if response is not None:
        if len(response['value']) > 0:
            return response['value'][0]['ID']
        else:
            logging.warning("SKU : " + sku + " doesn't exist in channel advisor.")


def get_fba_product_id(token, asin):
    url = "https://api.channeladvisor.com/v1/Products?access_token=" + token + "&" + helper.ca_filter(asin, "ASIN") + \
          "&$select=sku,ID"
    response = helper.get_response(url)
    skus = response['value']
    for sku in skus:
        if 'merchant' not in sku['Sku']:
            return sku['ID']
    return None


def get_product_by_id(token, product_id):
    url = "https://api.channeladvisor.com/v1/Products(" + product_id + ")?access_token=" + token
    return helper.get_response(url)


def get_bundle_components(token, product_id):
    url = "https://api.channeladvisor.com/v1/Products(" + str(
        product_id) + ")/BundleComponents?access_token=" + token + \
          "&$select=ComponentID,ComponentSku,ProductId,Quantity"
    return helper.get_response(url)


def get_components(token, product_id):
    components = []
    res = get_bundle_components(token, product_id)
    values = res['value']
    for value_ in values:
        components.append([value_['ComponentSku'], value_['ComponentID']])
    return components


def add_or_update_attribute(token, product_id, attribute_name, attribute_value):
    payload = {
        'ProductID': product_id,
        'Name': attribute_name,
        'Value': attribute_value
    }
    headers = {
        "Content-Type": "application/json"
    }
    url = "https://api.channeladvisor.com/v1/AttributeValues?access_token=" + token
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        return True
    logging.error(
        "Failed to update attribute " + attribute_name + " with value " + attribute_value + " Response status is : " +
        str(response.status_code))
    return False


def get_product_with_attributes_by_id(token, product_id):
    url = "https://api.channeladvisor.com/v1/Products(" + product_id + ")?access_token=" + token + "&$expand=Attributes"
    return helper.get_response(url)


def get_product_quantity(token, product_id):
    url = "https://api.channeladvisor.com/v1/Products(" + product_id + ")/DCQuantities?access_token=" + token
    return helper.get_response(url)


def delete_product(token, product_id):
    url = "https://api.channeladvisor.com/v1/Products(" + product_id + ")?access_token=" + token
    response = requests.request("DELETE", url)
    if 200 <= response.status_code < 300:
        logging.info("Successfully deleted product_id : " + product_id)
        return True

    logging.error("Failed to deleted product_id : " + product_id + ". Status: " + str(response.status_code))
    logging.error("Detail response is : " + str(response.json()))
    return False


def reset_buffer(token, product_id, updated_quantity):
    buffer = 3
    if updated_quantity <= 3:
        buffer = updated_quantity - 1

    data = {
        "Value": {
            "Attributes": [{
                "Name": "Buffer Quantity Amount",
                "Value": str(buffer)
            }]
        }
    }

    logging.debug('payload for product id ' + product_id + ' is : ' + str(data))

    headers = {"Content-Type": "application/json"}
    url = "https://api.channeladvisor.com/v1/Products(" + product_id + ")/UpdateAttributes?access_token=" + token
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    if 200 <= response.status_code < 300:
        logging.info("Successfully reset buffer for product_id: " + product_id)
        return True

    logging.error(
        "Failed to  update reset buffer for product_id: " + product_id + ". Status: " + str(response.status_code))
    logging.error("Detail response is : " + str(response.json()))
    return False


def update_buffer(token, product_id, buffer):
    data = {
        "Value": {
            "Attributes":
                [{
                    "Name": "Buffer Quantity Amount",
                    "Value": str(buffer)
                }]
        }
    }

    logging.debug('payload for product id ' + product_id + ' is : ' + str(data))

    headers = {"Content-Type": "application/json"}
    url = "https://api.channeladvisor.com/v1/Products(" + product_id + ")/UpdateAttributes?access_token=" + token
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    if 200 <= response.status_code < 300:
        logging.info("Successfully update buffer for product_id: " + product_id)
        return True

    logging.error(
        "Failed to update buffer for product_id: " + product_id + ". Status: " + str(response.status_code))
    logging.error("Detail response is : " + str(response.json()))
    return False


def update_dimensions(token, product_id, height, length, width, weight, location):
    payload = {
        "Height": height,
        "Length": length,
        "Width": width,
        "Weight": weight,
        "WarehouseLocation": location
    }
    headers = {
        "Content-Type": "application/json"
    }
    url = "https://api.channeladvisor.com/v1/Products(" + product_id + ")?access_token=" + token
    response = requests.request("PATCH", url, headers=headers, data=json.dumps(payload))
    logging.debug(response)

    if 200 <= response.status_code < 300:
        return True
    logging.error("Failed to update dimensions. Response status is : " +
                  str(response.status_code))
    return False


def update_quantity(token, sku, product_id, quantity, dc_id):
    data = {
        "Value": {
            "UpdateType": "InStock",
            "Updates": [{
                "DistributionCenterID": str(dc_id),
                "Quantity": quantity
            }]
        }
    }
    headers = {"Content-Type": "application/json"}
    url = "https://api.channeladvisor.com/v1/Products(" + product_id + ")/UpdateQuantity?access_token=" + token
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    if 200 <= response.status_code < 300:
        logging.info(f"Successfully updated quantity {quantity} for sku : " + sku)
        return quantity

    logging.error(f"Failed to  update quantity {quantity} for sku : " + sku + ". Status: " + str(response.status_code))
    logging.error("Detail response is : " + str(response.json()))
    return 0


def get_product_id_by_supplier_sku(token, mpn):
    url = "https://api.channeladvisor.com/v1/Products?access_token=" + token + "&" + parse.urlencode(
        {
            "$filter": "Attributes/Any (c:c/Name eq 'Supplier SKU' and c/Value eq '" + mpn + "') and startswith(SKU, 'merchant-')"
        }) + "&$select=ID,Sku,UPC"
    return helper.get_response(url)['value']


def get_product_id_by_mpn(token, mpn):
    url = "https://api.channeladvisor.com/v1/Products?access_token=" + token + "&" + parse.urlencode(
        {"$filter": "MPN eq '" + mpn + "' and startswith(SKU, 'merchant-')"}) + "&$select=ID,Sku,UPC"
    return helper.get_response(url)['value']


def get_sku_by_upc(token, upc):
    url = "https://api.channeladvisor.com/v1/Products?access_token=" + token + "&" + parse.urlencode(
        {
            "$filter": "UPC eq '" + upc + "' and startswith(SKU, 'merchant-')"}) + \
          "&$select=SKU,MPN"
    return helper.get_response(url)['value']
