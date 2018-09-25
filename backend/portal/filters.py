from django.db.models import Q, FieldDoesNotExist
from dry_rest_permissions.generics import DRYPermissionFiltersBase


class PermissionForPublicationFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the publication's users.
        """

        # Staff can always see everything
        if request.user.is_staff:
            return queryset

        user_publications = [m.publication for m in request.user.membership_set.select_related('publication')]

        # TODO: This is rather pointless for our simple relations for now but later on can make sense, still we will need to refactor this to a better form
        q = Q()
        try:
            # This is just a check to see if we have publication field for our model
            queryset.model._meta.get_field('publication')
            q |= Q(publication__in=user_publications)
        except FieldDoesNotExist:
            try:
                queryset.model._meta.get_field('file')
                q |= Q(file__publication__in=user_publications)
            except FieldDoesNotExist:
                try:
                    queryset.model._meta.get_field('service')
                    q |= Q(service__publication__in=user_publications)
                except FieldDoesNotExist:
                    pass
        return queryset.filter(q)


class PublisherListFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the publication's users.
        """

        # Staff can always see everything
        if request.user.is_staff:
            return queryset

        # Publication.objects.filter(membership__user=request.user)
        return queryset.filter(members__user=request.user)


class PublicationListFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        """
        Limits all list requests to only be seen by the publication's users.
        """

        # Staff can always see everything
        if request.user.is_staff:
            return queryset

        # Publication.objects.filter(membership__user=request.user)
        return queryset.filter(membership__user=request.user)
