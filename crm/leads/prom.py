from .api_connector import ApiConnector
from ..settings import settings


class HTTPError(Exception):
    pass


class PromClient(ApiConnector):

    def __init__(self):
        self.url = 'https://my.prom.ua'
        self.headers = {'Authorization': f'Bearer {settings.PROM_CLIENT_TOKEN}',
                   'Content-type': 'application/json'}

    def get_order_list(self):
        url_options = '/api/v1/orders/list'
        url = self.url+url_options
        method = 'GET'

        return self.make_request(url=url,  method=method, headers=self.headers)

