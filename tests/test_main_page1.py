import pytest
import requests
import json
from utils.main_page.api import get_cart, get_active_items, add_to_cart 
import allure

from utils.main_page.functions import attach_reqres

# from utils.functions import attach_requests

@allure.parent_suite("Главная страница")
@allure.suite("Проверка добавления товаров в корзину без регистраци")
@allure.title("Получение товаров")
def test_get_active():
    
    
    global offers_id, slug, condition_id
    
    with allure.step("отправка запроса на получение товаров"):
        response = get_active_items()
        attach_reqres(response=response)
        
    with allure.step("проверка статуса ответа"):
         assert response.status_code == 200
    
    response = response.json()
    
    with allure.step("проверка что в ответе есть товары"):
        assert len(response) > 0
        
    first_item=response[0]["offers"][0]
    
    offers_id=first_item["moderated_offer_id"]
    slug=first_item["slug"]
    condition_id=first_item["condition"]["id"]

@allure.parent_suite("Главная страница")
@allure.suite("Проверка добавления товаров в корзину без регистраци")
@allure.title("Получение session_id из куки")

def test_get_session_id():
    global cookie

    with allure.step("отправка запроса на получение товаров"):
        response = get_cart()
        
        
        
    with allure.step("проверка статуса ответа"):
        assert response.status_code == 200
        
    with allure.step("проверка статуса ответа"):
        cookie = response.cookies.get_dict()['cart']
    assert isinstance(cookie, str), f'Тип куки на самом деле {type(cookie)}'


@allure.parent_suite("Главная страница")
@allure.suite("Проверка добавления товаров в корзину без регистраци")
@allure.title("Добавление товаров в корзину")
def test_add_item():
    
    response = add_to_cart(cookie=cookie, offer_id=offers_id, condition_id=condition_id)
   
    
    with allure.step("отправка запроса на получение товаров"):
        response = get_active_items()
        

    assert response.status_code == 200
         
    response = response.json()
    print(json.dumps(response, indent=4))

# def view_cart():
#     response = add_cart(cookie=cookie, offer_id=offers_id, condition_id=condition_id)

# @pytest.mark.parametrize('item', ['iPhone', 'samsung', '8716248712648712648172648127','xiaomi'])
# def test_search(item):
#     search_body = {
#         "query": item
#     }
#
#     response = requests.post(url=search_url, json=search_body)
#     res_json = response.json()
#
#     items_list = res_json["items"]
#
#     print(f'{items_list}\n\n')
#
#     assert response.status_code == 200
#     assert len(items_list) > 0, "Ничего не нашлось"


# def url_generator(slug):
#     return f'{get_item}/{slug}'


# def test_active_items():
#     global item_slug
#
#     response = requests.get(url=active_items_url)
#
#     assert response.status_code == 200
#
#     response = response.json()
#
#     item_slug = response[0]['offers'][0]['slug']
#     print(item_slug)
#
#
# def test_get_item():
#     url = url_generator(item_slug)
#
#     response = requests.get(url=url)
#
#     print(response.json())
