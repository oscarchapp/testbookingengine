from django.db import models
from .form_dates import Ymd
from django.db.models import F, Count
# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)  # TODO:ADD REGEX FOR PHONE VALIDATION

    def __str__(self):
        return self.name


class Room_type(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    max_guests = models.IntegerField()

    def __str__(self):
        return self.name


class Room(models.Model):
    room_type = models.ForeignKey(Room_type, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    @classmethod
    def filter_rooms(cls, name_to_filter):
        return cls.objects.filter(name__contains= name_to_filter).values("name", "room_type__name", "id")


class Booking(models.Model):
    NEW = 'NEW'
    DELETED = 'DEL'
    STATE_CHOICES = [
        (NEW, 'Nueva'),
        (DELETED, 'Cancelada'),
    ]
    state = models.CharField(
        max_length=3,
        choices=STATE_CHOICES,
        default=NEW,
    )
    checkin = models.DateField()
    checkout = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    guests = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    total = models.FloatField()
    code = models.CharField(max_length=8)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    @classmethod
    def percentage_usage(cls):
        ''' Calculates the percentage of rooms booked
        '''
        from datetime import date
        today = date.today().strftime("%Y-%m-%d")
        rooms_booked = cls.objects.filter(checkout__gte= today,checkin__lte= today).count()
        rooms_available = Room.objects.all().count()
        return "{:.2f}".format(rooms_booked/rooms_available)

    @classmethod
    def verify_availability_of_change(cls, query):
        '''
            Verifys if there is any available room for the dates selected and same amount of guests
        '''
        checkin = Ymd.Ymd(query['checkin'])
        checkout = Ymd.Ymd(query['checkout'])
        total_days = checkout - checkin
        # get available rooms and total according to dates and guests
        filters = {
            'room_type': query['guests']
        }
        exclude = {
            'booking__checkin__lte': query['checkout'],
            'booking__checkout__gte': query['checkin'],
            'booking__state__exact': "NEW"
        }
        #verify the amount of rooms frees after the checkout date
        rooms = (Room.objects
                 .filter(**filters)
                 .exclude(**exclude)
                 .values("id", "name")
                 .annotate(total=total_days * F('room_type__price'))
                 .order_by("room_type__max_guests", "name")
                 )

        if len(rooms) >0:
            return True , rooms.first()['id']
        else:
            return False , 0

    @classmethod
    def verify_same_room(cls, query):
        '''
            Verifys if the same room is available in the days selectes, verifys the chechin with the checkout
        '''
        rooms_booked = cls.objects.filter(room_id= query['room_id'],checkin__lte= query['checkout']).values('code')
        if len(rooms_booked)<1:
            return True
        elif len(rooms_booked) == 1:
            if rooms_booked[0]['code'] == query['code']:
                return True
        return False