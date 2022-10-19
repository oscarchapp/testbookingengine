import django_filters

from pms.models import Room


class RoomFilter(django_filters.FilterSet):

    class Meta:
        model = Room
        fields = {
            'name': ['icontains']
        }
