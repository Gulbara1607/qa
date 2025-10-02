import requests
import json
from config import *

base_url = "https://gw.alifshop.uz"
active_items_url = f"{base_url}/web/client/events/active"
get_item = f"{base_url}/web/client/moderated-offers"
search_url = f"{base_url}/web/client/search/full-text"
get_cart_url = f"{base_url}/web/client/cart/view-cart/duplicate"
add_cart_url = f"{base_url}/web/client/cart/moderated-items"
remove_item_url = f"{base_url}/web/client/cart/remove-item"
user_events_url = f"{base_url}/web/client/users/events"


def get_active_items():
    response = requests.get(url=f"{base_url}/web/client/events/active")
    return response

def get_item(item_slug):
    response = requests.get(url=f"{base_url}/web/client/moderated-offers/{item_slug}")
    return response

def search_items(item_name: str):
    body = {
        "query": item_name
    }
    response = requests.post(url=f"{base_url}/web/client/search/full-text", json=body)
    return response

def get_cart(cookie=None):
    if cookie is None:
        response = requests.get(f"{base_url}/web/client/cart/view-cart/duplicate")
    else:
        headers = {
            'Cookie': f"cart={cookie};"
        }
        response = requests.get(url=f"{base_url}/web/client/cart/view-cart/duplicate", headers=headers)
    return response

def add_to_cart(cookie: str, offer_id: str, condition_id: int, quantity=1):
    headers = {
        'Cookie': f"cart={cookie};"
    }
    body = {
        "moderated_offer_id": offer_id,
        "condition_id": condition_id,
        "quantity": quantity
    }
    response = requests.post(
        url=f"{base_url}/web/client/cart/moderated-items",
        json=body,
        headers=headers
    )
    # print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    return response