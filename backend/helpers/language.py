from copy import deepcopy

from django.conf import settings

from portal.models import Publication


def get_most_relevant_language(language_sources):
    remaining_languages = deepcopy(language_sources)
    language_order_of_precedence = getattr(settings, 'LANGUAGE_ORDER_OF_PRECEDENCE', [])
    for source in language_order_of_precedence:
        lang = language_sources.get(source)
        if lang:
            return lang
        elif lang in remaining_languages:
            del remaining_languages[lang]
    else:
        return next((v for k, v in remaining_languages.items() if v))


def get_user_lang(request):
    language_sources = {
        'user': None,
        'publication': None,
        'publisher': None,
        'request': request._request.LANGUAGE_CODE,
        'default': getattr(settings, 'LANGUAGE_CODE', 'en')
    }
    if not request.user.is_anonymous:
        language_sources['user'] = request.user.settings.language
        user_publications = Publication.objects.filter(membership__user=request.user)
        if len(user_publications) == 1:
            language_sources['publication'] = user_publications[0].language
        elif len(user_publications) > 1:
            # TODO: get publisher lang here if user have
            pass

    return get_most_relevant_language(language_sources)


def get_publication_lang(publication):
    language_sources = {
        'publication': publication.language if publication else None,
        'publisher': None,
        'default': getattr(settings, 'LANGUAGE_CODE', 'en')
    }

    return get_most_relevant_language(language_sources)


# TODO: generalize this as this is the same method for getting lang and timezones based on precedence?
def get_most_relevant_timezone(timezone_sources):
    remaining_timezones = deepcopy(timezone_sources)
    timezone_order_of_precedence = getattr(settings, "TIMEZONE_ORDER_OF_PRECEDENCE", [])
    for source in timezone_order_of_precedence:
        timezone = timezone_sources.get(source)
        if timezone:
            return timezone
        elif timezone in remaining_timezones:
            del remaining_timezones[timezone]
    else:
        return next((v for k, v in remaining_timezones.items() if v))


def get_user_timezone(request):
    timezone_sources = {
        'user': None,
        'publication': None,
        'publisher': None,
        # TODO: research if we get something like this or not?
        # 'request': request._request.TIMEZONE,
        'default': getattr(settings, 'TIMEZONE', 'utc')
    }
    if not request.user.is_anonymous:
        timezone_sources['user'] = request.user.settings.get_timezone_display()
        user_publications = Publication.objects.filter(membership__user=request.user)
        if len(user_publications) == 1:
            timezone_sources['publication'] = user_publications[0].get_timezone_display()
        elif len(user_publications) > 1:
            # TODO: get publisher timezone here if user have
            pass

    return get_most_relevant_timezone(timezone_sources)


def get_publication_timezone(publication):
    timezone_sources = {
        'publication': publication.get_timezone_display() if publication else None,
        'publisher': None,
        'default': getattr(settings, 'TIMEZONE', 'utc')
    }

    return get_most_relevant_timezone(timezone_sources)
