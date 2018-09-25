from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse


def get_backend_link(obj, reverse_url_name):
    url_path = reverse(reverse_url_name, args=(obj.id,))
    return urljoin(f'{settings.PROTOCOL}://{settings.HOSTNAME}', url_path)


def get_frontend_link(obj):
    from portal.models import Publication
    from status.models import Service, File, FileEvent

    url = None
    if isinstance(obj, Publication):
        return urljoin(f'{settings.PROTOCOL}://{settings.FRONTEND_HOSTNAME}/publication/', str(obj.id))
    if isinstance(obj, Service):
        return urljoin(f'{settings.PROTOCOL}://{settings.FRONTEND_HOSTNAME}/services/', str(obj.id))
    if isinstance(obj, File):
        return urljoin(f'{settings.PROTOCOL}://{settings.FRONTEND_HOSTNAME}/files/', str(obj.id))
    if isinstance(obj, FileEvent):
        return urljoin_multi_path(f'{settings.PROTOCOL}://{settings.FRONTEND_HOSTNAME}/files/', str(obj.file.id), 'events')

    return url


def urljoin_multi_path(base_url, *args):
    current_url = base_url
    for path in args:
        # Extra slash needed as urljoin will overwrite base url path's last segment, on the other hand double slashes are taken care of it
        current_url = urljoin(f'{current_url}/', path)
    return current_url
