from django.db import models, transaction

from .models import Room

class RoomManager(models.Manager):

    def filter_rooms_by_name(self, room_name_filter):
        """
        Filtering room name with 'icontains' so the name includes the search word in any position, case insensitive
        """
        return Room.objects.filter(name__icontains=room_name_filter).values("name", "room_type__name", "id")
