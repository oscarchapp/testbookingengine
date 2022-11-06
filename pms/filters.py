import django_filters
from pms.models import Room


class RoomFilter(django_filters.FilterSet):
    """Room name filter. Example search 
    for Room1 to get Room1.1 Room1.2 ...
    """
    name = django_filters.CharFilter(lookup_expr='istartswith',label='Name')
    
    class Meta:
        model = Room
        fields = ['name']
        