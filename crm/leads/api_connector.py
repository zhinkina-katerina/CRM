import requests


class HTTPError(Exception):
    pass


class ApiConnector():
    def make_request(self, headers, url, method, body=None):
        if method == 'GET':
            response = requests.get(url, headers=headers)
        if method == 'POST':
            response = requests.post(url, json=body, headers=headers)
        if response.status_code != 200:
            raise HTTPError('{}: {}'.format(response.status_code, response.reason))

        return response.json()
