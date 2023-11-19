from django.db import models
from django.db.models import Q, Sum
from datetime import date



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

    @classmethod
    def get_percent_occupation(cls):
        """
        Get percentage occupation
        Warning: Future reservations are ignored
        """
        today = date.today()
        occupied_rooms = len(
            set(
                Booking.objects.exclude(state=Booking.DELETED)
                .filter(Q(checkin__lte=today, checkout__gte=today))
                .values_list("room", flat=True)
            )
        )
        rooms_quantity = cls.objects.all().count()
        return 0 if rooms_quantity == 0 else (occupied_rooms / rooms_quantity) * 100

    def __str__(self):
        return self.name


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

    @classmethod
    def get_news(cls, count_only=False):
        """
        get bookings created today
        """
        queryset = cls.objects.filter(created__date=date.today())
        return queryset.count() if count_only else queryset.all()

    @classmethod
    def get_incoming(cls, count_only=False):
        """
        get incoming guests
        """
        queryset = cls.objects.filter(checkin=date.today()).exclude(state=cls.DELETED)
        return queryset.count() if count_only else queryset.all()

    @classmethod
    def get_outcoming(cls, count_only=False):
        """
        get outcoming guests
        """
        queryset = cls.objects.filter(checkout=date.today()).exclude(state=cls.DELETED)
        return queryset.count() if count_only else queryset.all()

    @classmethod
    def get_invoiced(cls):
        """
        get invoiced
        """
        return cls.objects.filter(
            created__date=date.today()
        ).exclude(state=cls.DELETED).aggregate(Sum('total'))

    def __str__(self):
        return self.code
