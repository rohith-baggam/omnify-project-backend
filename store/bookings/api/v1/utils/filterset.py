import django_filters
from store.bookings.models import BookingsModel


class BookingsModelFilterSet(django_filters.FilterSet):
    client_email = django_filters.CharFilter(
        field_name="client__email", lookup_expr="icontains"
    )

    class Meta:
        model = BookingsModel
        fields = ["client_email"]
