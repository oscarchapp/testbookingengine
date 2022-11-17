import pytest
from django.db.models import QuerySet

from pms.views import RoomsView


@pytest.mark.django_db
def test_get_room_queryset():
    request = {'value_to_search': 'ROOM'}
    room = RoomsView().get_queryset(request)
    assert isinstance(room, QuerySet)
