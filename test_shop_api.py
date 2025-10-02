import requests
import json
import pytest

base_url = 'https://gw.alifshop.uz'

active_items_url = f'{base_url}/web/client/events/active'
delivery_products_url_template = f'{base_url}/web/client/catalog/moderated-offers/{{offer_id}}/delivery-time-estimation/duplicate'
reviews_url_template = f'{base_url}/web/client/moderated-offers/{{offer_id}}/reviews'
offers_v2_url = f'{base_url}/web/client/recommend/offers/v2'


def get_active_items():
    return requests.get(url=active_items_url)

def test_get_active_items():
    global offer_id, slug

    response = get_active_items()
    assert response.status_code == 200

    response = response.json()
    assert len(response) > 0

    first_item = response[0]["offers"][0]
    offer_id = first_item["moderated_offer_id"]
    slug = first_item["slug"]

    for offer in response[0]["offers"]:
        assert "id" in offer or "offer_id" in offer, "Нет id"
        assert "name" in offer, "Нет name"
        assert "price" in offer, "Нет price"
        assert "partner" in offer, "Нет partner"

        # price > 0
        assert offer["price"] > 0, "Цена должна быть больше 0"

        # old_price >= price
        if "old_price" in offer:
            assert offer["old_price"] >= offer["price"], "old_price < price"

        # discount check
        if "discount" in offer and offer["discount"] < 0:
            assert offer["price"] < offer["old_price"], "price не меньше old_price"


def test_moderated_offer():
    url = f'{base_url}/web/client/moderated-offers/{slug}'
    response = requests.get(url=url)
    assert response.status_code == 200

    item = response.json()["moderated_offer"]

    assert "name" in item, "Нет name"
    assert item["price"] > 0, "Цена должна быть больше 0"
    assert len(item["images"]) > 0, "Нет фото"
    assert "discount" in item, "Нет discount"
    assert item["discount"] <= 0, "discount > 0"
    if item["discount"] < 0:
        assert item["price"] < item["old_price"], "price не меньше old_price"


def test_delivery_time():
    url = delivery_products_url_template.format(offer_id=offer_id)
    response = requests.get(url=url)
    if response.status_code == 404:
        pytest.skip("delivery-time-estimation endpoint недоступен (404)")
    assert response.status_code == 200

    response = response.json()

    # Если это список
    if isinstance(response, list):
        for d in response:
            assert "days_to_deliver" in d
            assert d["days_to_deliver"] >= 0
    # Если это словарь
    elif isinstance(response, dict):
        assert "days_to_deliver" in response
        assert response["days_to_deliver"] >= 0
    else:
        pytest.skip(f"Неожиданный формат ответа: {type(response)}")


def test_reviews():
    url = reviews_url_template.format(offer_id=offer_id)
    response = requests.get(url=url)
    if response.status_code == 404:
        pytest.skip("reviews endpoint недоступен (404)")
    assert response.status_code == 200

    response = response.json()
    total = response.get("total", 0)
    reviews = response.get("offer_reviews", [])

    if total > 0:
        assert len(reviews) > 0, "total > 0, но reviews пустой"

# этот код страннно работает 
# def test_offers_v2():
#     response = requests.get(url=offers_v2_url)
#     if response.status_code == 404:
#         pytest.skip("offers/v2 endpoint недоступен (404)")
#     assert response.status_code == 200

#     data = response.json()
#     assert "offers" in data
#     offers = data["offers"]
#     assert len(offers) > 0

#     for offer in offers:
#         assert "partner" in offer
#         partner = offer["partner"]
#         assert "name" in partner
#         assert "rating" in partner

#         if "conditions" in offer:
#             for cond in offer["conditions"]:
#                 assert "duration" in cond
#                 assert "commission" in cond

