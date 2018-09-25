import base64

import requests


class AboDbApiError(Exception):
    pass


class AboDbApi:
    def __init__(self, abodb_url, api_key):
        self.api_url = abodb_url + '/hub/'
        self.api_key = api_key

    def post(self, endpoint, data):
        return self._request('POST', endpoint, data)

    def _request(self, method, endpoint, data=None):
        res = requests.request(method, self.api_url + endpoint, data=data, headers={
            'X-Api-Key': self.api_key,
        })

        try:
            res = res.json()
        except:
            raise AboDbApiError("Unknown error: {}".format(res.text))

        if res.get('error'):
            raise AboDbApiError("AboDB error: {}".format(res.get('error')))

        return res


def upload_abodb_csv(file_object, abodb_url, api_key, publisher_code):
    """
    Uploads a CSV to AboDB.

    :param file_object: content of csv file
    :param abodb_url: The URL to AboDB
    :param api_key: API key for AboDB
    :param publisher_code: Publisher code such as `avs`, `fru`, etc.
    """
    api = AboDbApi(abodb_url, api_key)

    csv_content = base64.b64encode(file_object.read()).decode()
    # csv_content = file_object.read()

    return api.post('import/csv', {
        'publisher_code': publisher_code,
        'csv': csv_content,
    })
