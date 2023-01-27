from django_unicorn.components import UnicornView
from pms.models import Room

class LiveSearchRoomView(UnicornView):
    search = ""
    room = Room.objects.all().values("name", "room_type__name", "id")
    def get_rooms(self):
        return self.room.filter(name__icontains=self.search)
    