"""Helper functions for emails."""
import json
from os import listdir, path as os_path
from email.mime.image import MIMEImage

import html2text
from django.conf import settings
from django.utils.safestring import mark_safe


def file_to_mimeimage(path):
    """Convert local file to MIMEIMage."""
    if not os_path.exists(path):
        return ''

    with open(path, 'rb') as fp:
        return MIMEImage(fp.read())


def dict_to_html(dict):
    """Convert a dict to html."""
    html = ''
    for key in dict:
        html += '{}: {}<br>'.format(key, dict[key])
    return html


def format_details(details, type=''):
    """Convert received `details` to html or markdown."""
    try:
        dict = json.loads(details)
    except (json.decoder.JSONDecodeError, TypeError):
        return details
    else:
        html_details = mark_safe(dict_to_html(dict))
        if type == 'html':
            return html_details
        elif type == 'md':
            return html2text.html2text(html_details)
        elif type == 'dict':
            return dict


def details_is_dict(details):
    """Check if details can be converted to dict."""
    try:
        details_as_dict = json.loads(details)
    except json.decoder.JSONDecodeError:
        return False
    return details_as_dict


def format_default_email_images(metadata):
    """
    Setup metadata keys with default email template items.

    This depends on the `collecstatic` have already been run.
    """
    logo_path = os_path.join(
        settings.STATIC_ROOT,
        'portal/images/localpoint-logo.png'
    )

    icon_folder = os_path.join(
        settings.STATIC_ROOT,
        'portal/images/email-icons/'
    )

    icons_data = {}
    for filename in listdir(icon_folder):
        path = os_path.join(icon_folder, filename)
        if not os_path.isfile(path):
            continue

        name = os_path.basename(path).replace('-', '_').split('.')[0]
        icons_data[name] = path

    metadata.update({
        'logo_cid': os_path.basename(logo_path),
        'logo_path': logo_path,
        'icons_data': icons_data,
        'localpoint_address': settings.LOCALPOINT_ADDRESS,
        'localpoint_phone': settings.LOCALPOINT_PHONE,
        'localpoint_email': settings.LOCALPOINT_EMAIL,
    })

    return metadata


def email_html_to_text(html):
    """Convert HTML to text for emails."""
    h = html2text.HTML2Text()
    h.unicode_snob = True
    h.ignore_links = True
    h.images_to_alt = True
    h.ignore_tables = True
    return h.handle(html)
