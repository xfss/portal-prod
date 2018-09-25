from django.conf import settings
from django.contrib.auth import get_user_model
from dry_rest_permissions.generics import DRYObjectPermissions
from rest_framework import views, viewsets, authentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from helpers.language import get_user_lang
from portal.filters import PublicationListFilterBackend, PublisherListFilterBackend
from portal.models import Publication, LocaleSettingsBase, Publisher, PublicationConfigRule
from portal.serializers import UserSerializer, PublicationSerializer, PublisherSerializer, PublicationConfigRuleSerializer

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class CurrentLanguageView(views.APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request):
        return Response(
            {"language": get_user_lang(request)},
        )


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (IsAuthenticated, DRYObjectPermissions,)
    filter_backends = (PublisherListFilterBackend,)


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = (IsAuthenticated, DRYObjectPermissions,)
    filter_backends = (PublicationListFilterBackend,)


class PublicationConfigRuleViewSet(viewsets.ModelViewSet):
    queryset = PublicationConfigRule.objects.all()
    serializer_class = PublicationConfigRuleSerializer
    permission_classes = (IsAuthenticated, DRYObjectPermissions,)


@api_view(['GET'])
@permission_classes((AllowAny,))
def languages(request):
    return Response([{'text': i[1], 'value': str(i[0])} for i in settings.LANGUAGES])


@api_view(['GET'])
@permission_classes((AllowAny,))
def timezones(request):
    return Response([{'text': i[1], 'value': str(i[0])} for i in LocaleSettingsBase.TIMEZONE_CHOICES])
