import allure

def attach_reqres(response):
    request = response.request

    allure.attach(request.method, name='Метод Запроса',
                  attachment_type=allure.attachment_type.TEXT)

    allure.attach(request.url, name='URL Запроса',
                  attachment_type=allure.attachment_type.TEXT)