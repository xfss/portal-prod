import re
from datetime import date, time
from datetime import datetime, timedelta

import pytz
import requests
from babel.dates import format_date
from requests import HTTPError


class PaperlitApiError(Exception):
    pass


class PaperlitApi:
    # We can't use our own domain which goes through cloudflare because cloudflare will timeout slow requests, which
    # can happen for big PDFs.
    # PAPERLIT_API_URL = "https://eedition-api.localpoint.ch/v8/"
    # PAPERLIT_API_URL = "https://api-ne.paperlit.com/v8/"

    def __init__(self, paperlit_api_url):
        self.paperlit_api_url = paperlit_api_url
        if not self.paperlit_api_url.endswith('/'):
            self.paperlit_api_url = f'{self.paperlit_api_url}/'

        self.access_token = ''

    def login(self, email, password, company):
        res = self.post('users/token/get', {
            'email': email,
            'password': password,
            'company': company,
        })

        self.access_token = res['items'][0]['accessToken']

    def post(self, endpoint, data):
        return self._request('POST', endpoint, data)

    def get(self, endpoint):
        return self._request('GET', endpoint)

    def delete(self, endpoint):
        return self._request('DELETE', endpoint)

    def _request(self, method, endpoint, json=None):
        # TODO: use urllib to join url parts!
        response = requests.request(method, f'{self.paperlit_api_url}{endpoint}', json=json, headers={
            'Authorization': 'Bearer ' + self.access_token,
        })
        response.raise_for_status()
        content = response.json()

        return content.get('data')


def upload_paperlit_pdf(paperlit_api_url, file_url, original_filename, api_email, api_password, api_company, project_id, publication_id, publish_offset=timedelta(), default_paid=False):
    """
    Uploads a given PDF to PaperLit by copying it to a public path and calling the PaperLit API.

    :param paperlit_api_url: url of paperlit api
    :param file_url: public url of file
    :param original_filename: original filename of file
    :param api_email: API credentials
    :param api_password: API credentials
    :param api_company: API credentials
    :param project_id: PaperLit project id
    :param publication_id: PaperLit publication id
    :param publish_offset: Offset in timedelta for the publishedOn field (based on edition date 00:00 AM)
    :param default_paid: If the `isForSale` flag for an issue should be set to True by default or not
    """
    api = PaperlitApi(paperlit_api_url)
    api.login(api_email, api_password, api_company)

    edition_date = _parse_edition_date(original_filename)
    project = api.get('projects/{}'.format(project_id))['items'][0]

    published_on = datetime.combine((edition_date or date.today()), time(0, 0))
    published_on += publish_offset
    published_on = pytz.timezone('Europe/Zurich').localize(published_on)

    issue = api.post('projects/{}/issues/{}'.format(project_id, publication_id), {
        "issueName": _generate_issue_name(project['languages'][0], edition_date or date.today()),
        "publishedOn": published_on.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:00'),
        "caption": None,
        "isForSale": default_paid,
    })

    issue_id = issue['items'][0]['issueId']
    unique_id = issue['items'][0]['uniqueId']

    try:
        # The file must be accessible at this point. The variant will only be created if the PDF can be downloaded.
        result = api.post('projects/{}/issues/{}/variants'.format(project_id, unique_id), {
            'fileUrl': file_url,
            'uploadFilename': original_filename,
            'platform': 'universal',
            'type': 'pdf',
            'narrowDimension': 0,
            'wideDimension': 0,
            'hasPreview': False,
            'previewPages': []
        })
        return ''
    except HTTPError as e:
        return e
    except Exception as e:
        api.delete('projects/{}/issues/{}/{}'.format(project_id, publication_id, issue_id))
        raise e


def _parse_edition_date(filename):
    match = re.search(r'(?:^|_)(20[0-9]{2})([0-1][0-9])([0-3][0-9])_', filename)

    if match:
        return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return None


def _generate_issue_name(language, edition_date):
    weekday = format_date(edition_date, 'EEEE', language)[:2].capitalize()
    return edition_date.strftime(weekday + '. %d.%m.%Y')
