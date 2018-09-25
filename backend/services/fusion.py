import os

import logging
from datetime import datetime

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class BaseBackend:
    def __init__(self, api_base_url, api_key):
        self.api_base_url = api_base_url
        self.api_key = api_key

    def api_get(self, endpoint, **kwargs):
        return self._request('get', endpoint, params=kwargs)

    def api_post(self, endpoint, data):
        return self._request('post', endpoint, json=data)

    def api_put(self, endpoint, data):
        return self._request('put', endpoint, json=data)

    def api_delete(self, endpoint):
        return self._request('delete', endpoint)

    def _request(self, method, endpoint, **kwargs):
        headers = {'Authorization': 'Token ' + self.api_key}
        res = requests.request(method, os.path.join(self.api_base_url, endpoint), headers=headers, **kwargs)
        logger.info("{} {}".format(method.upper(), res.url))

        res.raise_for_status()

        if not res.content:
            return {}

        return res.json()


class PageResults:
    def __init__(self, *, results, page, total_rows, total_pages, prev_page, next_page):
        self.results = results
        self.page = page
        self.total_rows = total_rows
        self.total_pages = total_pages
        self.prev_page = prev_page
        self.next_page = next_page

    @staticmethod
    def from_response(data, parsed_results):
        return PageResults(results=parsed_results,
                           page=data.get('page', 1),
                           total_rows=data.get('total_count', 0),
                           total_pages=data.get('total_pages', 0),
                           prev_page=data.get('prev').get('href', '') if data.get('prev') else None,
                           next_page=data.get('next').get('href', '') if data.get('next') else None)


class FusionBackend(BaseBackend):
    def __init__(self):
        # TODO: use fusion service and address instead of config?
        super().__init__(settings.SERVICES['fusion']['api_base_url'], settings.SERVICES['fusion']['api_key'])

    def query_newspaper_list(self, page, page_size):
        res = self.api_get('newspapers/', page=page, page_size=page_size)
        return PageResults.from_response(res, [Newspaper(row) for row in res['results']])

    def query_reports(self, start, end):
        res = self.api_get('reporting/newspapers/', report_start=start, report_end=end)
        return [Report(row) for row in res['results']]

    def query_newspaper_report(self, newspaper, start, end):
        res = self.api_get('reporting/newspapers/' + newspaper, report_start=start, report_end=end)
        return Report(res)

    def query_adfusion_feed_list(self, page, page_size, *, search='', order_by=''):
        data = self.api_get('adfusion/feeds/', page=page, page_size=page_size, search=search, order_by=order_by)
        return PageResults.from_response(data, [AdFeed(feed) for feed in data['results']])

    def query_adfusion_feed_detail(self, id):
        res = self.api_get('adfusion/feeds/{}/'.format(id))
        return AdFeed(res)

    def create_adfusion_feed(self, data):
        return AdFeed(self.api_post('adfusion/feeds/', data))

    def update_adfusion_feed(self, id, data):
        return AdFeed(self.api_put('adfusion/feeds/{}/'.format(id), data))

    def delete_adfusion_feed(self, id):
        self.api_delete('adfusion/feeds/{}/'.format(id))

    def query_adfusion_category_list(self, page, page_size, *, newspaper='', search='', order_by=''):
        data = self.api_get('adfusion/categories/',
                            page=page,
                            page_size=page_size,
                            newspaper=newspaper,
                            search=search,
                            order_by=order_by)

        return PageResults.from_response(data, [AdCategory(cat) for cat in data['results']])

    def query_adfusion_category_detail(self, id):
        res = self.api_get('adfusion/categories/{}/'.format(id))
        return AdCategory(res)

    def create_adfusion_category(self, data):
        return AdCategory(self.api_post('adfusion/categories/', data))

    def update_adfusion_category(self, id, data):
        return AdCategory(self.api_put('adfusion/categories/{}/'.format(id), data))

    def delete_adfusion_category(self, id):
        self.api_delete('adfusion/categories/{}/'.format(id))

    def query_adfusion_widget_list(self, page, page_size, *, newspaper='', search='', order_by=''):
        data = self.api_get('adfusion/widgets/',
                            page=page,
                            page_size=page_size,
                            newspaper=newspaper,
                            search=search,
                            order_by=order_by)
        return PageResults.from_response(data, [AdWidget(widget) for widget in data['results']])

    def query_adfusion_widget_detail(self, id):
        res = self.api_get('adfusion/widgets/{}/'.format(id))
        return AdWidget(res)

    def create_adfusion_widget(self, data):
        return AdWidget(self.api_post('adfusion/widgets/', data))

    def update_adfusion_widget(self, id, data):
        return AdWidget(self.api_put('adfusion/widgets/{}/'.format(id), data))

    def delete_adfusion_widget(self, id):
        self.api_delete('adfusion/widgets/{}/'.format(id))


class Edition:
    def __init__(self, edition):
        self.id = edition['id']
        self.edition_date = datetime.strptime(edition['edition_date'], "%Y-%m-%d").date()

        if 'ads' in edition:
            self.ads = AdReportStats(edition['ads'])

        if 'news' in edition:
            self.news = NewsReportStats(edition['news'])


class Report:
    def __init__(self, report):
        self.ads = AdReportStats(report['ads'])
        self.news = NewsReportStats(report.get('news'))
        self.newspaper = Newspaper(report['newspaper'])
        self.editions = [Edition(e) for e in report.get('editions', [])]


class Newspaper:
    def __init__(self, newspaper):
        self.code = newspaper['code']
        self.name = newspaper['name']

    def __str__(self):
        return self.name_and_code

    @property
    def name_and_code(self):
        if not self.name:
            return self.code
        return "{} ({})".format(self.name, self.code)


class AdReportStats:
    def __init__(self, stats):
        if stats:
            self.total = stats['total']
            self.published_revenue = stats['published_revenue']
            self.published_nonrevenue = stats['published_nonrevenue']
            self.nonpublished_revenue = stats['nonpublished_revenue']
            self.nonpublished_nonrevenue = stats['nonpublished_nonrevenue']
        else:
            self.total = 0
            self.published_revenue = 0
            self.published_nonrevenue = 0
            self.nonpublished_revenue = 0
            self.nonpublished_nonrevenue = 0


class NewsReportStats:
    def __init__(self, stats):
        if stats:
            self.total_pages = stats.get('total_pages', 0)
            self.news_pages = stats.get('news_pages', 0)
        else:
            self.total_pages = 0
            self.news_pages = 0


class AdCategory:
    def __init__(self, category):
        self.id = category['id']
        self.name = category['name']
        self.newspaper = Newspaper(category['newspaper']) if 'newspaper' in category else None
        self.exclude_from_tv = category.get('exclude_from_tv')

    def __str__(self):
        return "{} - {}".format(self.newspaper.code, self.name)


class AdFeed:
    def __init__(self, feed):
        if feed:
            self.id = feed['id']
            self.name = feed['name']
            self.sort = feed.get('sort', '')
            self.sources = [AdFeedSource(source) for source in feed.get('sources', [])]
            self.json_url = feed.get('json_url', '')
            self.xml_url = feed.get('xml_url', '')
            self.tv_url = feed.get('tv_url', '')
        else:
            self.id = ''
            self.name = ''
            self.sort = ''
            self.sources = []
            self.json_url = ''
            self.xml_url = ''
            self.tv_url = ''

    def __str__(self):
        return self.name


class AdFeedSource:
    def __init__(self, source):
        self.id = source['id']
        self.newspaper = Newspaper(source['newspaper'])
        self.categories = [AdCategory(category) for category in source['categories']]
        self.max_edition_age = source['max_edition_age']
        self.editions_count = source['editions_count']
        self.min_ad_count = source['min_ad_count']

    def __str__(self):
        return "{} - {}".format(self.newspaper, ', '.join(cat.name for cat in self.categories))


class AdWidget:
    def __init__(self, widget):
        self.id = widget['id']
        self.name = widget['name']
        self.feed = AdFeed(widget['feed'])
        self.lp_ad_duration = widget['lp_ad_duration']
        self.preview_url = widget.get('preview_url', '')

    def __str__(self):
        return self.name
