import django_filters
from pms.models import Room


class RoomFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Nombre')

    class Meta:
        model = Room
        fields = ['name']
