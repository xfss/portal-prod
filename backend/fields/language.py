import pendulum
from django.utils import formats
from rest_framework.fields import DateField, DateTimeField

from helpers.language import get_user_timezone


class LocalizedDateField(DateField):
    def to_representation(self, value):
        """
        Serialize the object's class name.
        """
        result = formats.localize(value, use_l10n=True)

        return result


class LocalizedDateTimeField(DateTimeField):
    def to_representation(self, value):
        """
        Serialize the object's class name.
        """
        timezone = get_user_timezone(self.context['request'])
        dt = pendulum.instance(value)
        dt = dt.in_timezone(timezone)
        result = formats.localize(dt, use_l10n=True)

        return result
