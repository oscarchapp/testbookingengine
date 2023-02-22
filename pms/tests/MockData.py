from pms.models import Room_type, Room


class MockData:
    @staticmethod
    def startMockData():
        type_room = Room_type.objects.create(name="Doble", price=20, max_guests=2)
        Room.objects.create(room_type=type_room, name='1.1', description='UNA HAB')
        Room.objects.create(room_type=type_room, name='1.2', description='DOS HAB')
        Room.objects.create(room_type=type_room, name='2.1', description='HAB')
        Room.objects.create(room_type=type_room, name='11', description='HAB 11')