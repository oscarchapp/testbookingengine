import factory
from pms.models import Room_type, Room, Booking


class RoomTypeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Room_type

    price = factory.Faker("pydecimal", left_digits=6, right_digits=2, positive=True)
    name = factory.Iterator(['type 1', 'type 2', 'type 2'])
    max_guests = factory.Faker('pyint', min_value=1, max_value=10)


class RoomFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Room

    room_type = factory.SubFactory(RoomTypeFactory)
    name = factory.Faker("text", max_nb_chars=100)
    description = factory.Faker("text", max_nb_chars=500)


class BookingFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Booking

    state = Booking.NEW
    total = factory.Faker("pydecimal", left_digits=6, right_digits=2, positive=True)
    code = factory.Faker("pystr", max_chars=8)
    guests = factory.Faker("pyint", min_value=1, max_value=10)
    room = factory.SubFactory(RoomFactory)