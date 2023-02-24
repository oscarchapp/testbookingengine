from datetime import datetime, timedelta

from pms.models import Room_type, Room, Booking
from pms.reservation_code.generate import get


class MockData:
    @staticmethod
    def start_mock_data():
        room_type = Room_type.objects.create(name="Doble", price=20, max_guests=2)
        r1 = Room.objects.create(room_type=room_type, name='1.1', description='UNA HAB')
        r2 = Room.objects.create(room_type=room_type, name='1.2', description='DOS HAB')
        r3 = Room.objects.create(room_type=room_type, name='2.1', description='HAB')
        r4 = Room.objects.create(room_type=room_type, name='11', description='HAB 11')
        b1 = Booking.objects.create(checkin=datetime.today(),
                                    checkout=datetime.today() + timedelta(days=8), room=r1, guests=1, total=20,
                                    code=get())
        b2 = Booking.objects.create(checkin=datetime.today(),
                                    checkout=datetime.today() + timedelta(days=1), room=r2, guests=2, total=20,
                                    code=get())
        b3 = Booking.objects.create(checkin=datetime.today(),
                                    checkout=datetime.today() + timedelta(days=5), room=r3, guests=1, total=20,
                                    code=get())
        b4 = Booking.objects.create(checkin=datetime.today() - timedelta(days=10),
                                    checkout=datetime.today() - timedelta(days=5), room=r3, guests=1, total=20,
                                    code=get())
        b5 = Booking.objects.create(checkin=datetime.today() + timedelta(days=20),
                                    checkout=datetime.today() + timedelta(days=22), room=r3, guests=1, total=20,
                                    code=get())
