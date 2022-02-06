from .api_connector import ApiConnector
from leads.settings import settings


class HTTPError(Exception):
    pass


class NovaPoshtaClient(ApiConnector):

    def __init__(self):
        self.token = settings.NOVA_POSHTA_CLIENT_TOKEN
        self.url = "https://api.novaposhta.ua/v2.0/json/"
        self.headers = {'Content-type': 'application/json'}
        self.method = "POST"

    def get_city_ref(self, city_name):
        body = {'apiKey': self.token,
                'modelName': 'Address',
                'calledMethod': 'searchSettlements',
                "methodProperties": {
                    "CityName": city_name,
                    "Limit": 1
                }
                }
        response = self.make_request(body=body, url=self.url, method=self.method, headers=self.headers)
        if not response['success']:
            return print('Ошибка')

        city_ref = response.get('data')[0].get('Addresses')[0].get("Ref")
        return city_ref

    def get_ttn_information(self, ttn):
        body = {'apiKey': self.token,
                'modelName': "TrackingDocument",
                'calledMethod': "getStatusDocuments",
                "methodProperties": {
                    "Documents": [
                        {
                            "DocumentNumber": ttn,
                            "Phone": ""
                        },
                    ]
                }
                }
        response = self.make_request(body=body, url=self.url, method=self.method, headers=self.headers)

        if not response['success']:
            return print('Ошибка')

        result = {
            "redelivery": response.get('data')[0].get('Redelivery'),
            'RedeliverySum': response.get('data')[0].get('RedeliverySum'),
            'ScheduledDeliveryDate': response.get('data')[0].get('ScheduledDeliveryDate'),
            'DocumentCost': response.get('data')[0].get('DocumentCost'),
            'Status': response.get('data')[0].get('Status'),
            'StatusCode': response.get('data')[0].get('StatusCode'),
        }
        return result


