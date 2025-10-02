import requests
import json

base_url = 'https://gw.alifshop.uz'

active_items_url = f'{base_url}/web/client/events/active'
get_item_url = f'{base_url}/web/client/cart/view-cart'
popular_url = f'{base_url}/web/client/brands/popular'
reviews_url = f'{base_url}/web/client/users/events'
delivery_products_url = f'{base_url}/web/client/delivery-time-estimation/longest/duplicate'


def get_active_items():
    response = requests.get(url=f"{active_items_url}")
    
    return response

def test_get_active_items():
    global offer_id, slug, condition_id
    
    response = get_active_items()
    
    assert response.status_code == 200
    
    response = response.json()
    assert len(response) > 0

    first_item = response[0]["offers"][0]
    
    offer_id = first_item["moderated_offer_id"]
    slug = first_item["slug"]
    condition_id = first_item["condition"]["id"]
    
    
    offers = response[0]["offers"]
    
    for offer in offers:
        assert "offer_id" in offer, "Ожидали поле offer_id в offer"
        assert "name" in offer, "Ожидали поле name в offer"
        assert "price" in offer, "Ожидали поле price в offer"
        assert "partner" in offer, "Ожидали поле partner в offer"
        assert offer["price"] > 0
        if "old_price" in offer:
            offer["old_price"] >= offer["price"], "old_price меньше чем price"
            
            # print(response)

""" 
def get_item(item_slug):
    response = requests.get(url=f"{get_item_url}/{item_slug}")
     """
    
def url_generator(slug):
    return f'{get_item_url}/{slug}'

     
def test_item():
    link = url_generator(slug)
    response = requests.get(url=link)
    
    assert response.status_code == 200
    
    response = response.json()
    assert len(response) > 0
    
    item = response["moderated_offer"]
    assert "name" in item, "Ожидали поле name в moderated_offer"
    assert item["price"] >= 0, "price меньше, либо равна 0"
    assert len(item["images"]) > 0, "В продукте нет картинок"
    assert item["discount"] <= 0, "discount больше нуля"
    if item["discount"] < 0:
        item["price"] < item["old_price"], "old_price меньше чем price"

  

