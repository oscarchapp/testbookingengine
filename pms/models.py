import inspect
from django.core.exceptions import ValidationError
from django.db import models
from datetime import date
from .managers import BookingManager
# Create your models here.


class CheckContraintsMixin:
    def clean_fields(self, exclude=None):
        '''
        Gets all class-functions which start with 'clean_' and applies them performing constraint checking.
        This emulates form field validation in models in order to follow "fat models-skinny views" approach.
        excepts:
            if any of the _check functions raises ValidationError, 
            this functions raises ValidationError showing all the errors
        '''
        CLEAN_FUNC_PREFIX = 'clean_'
        exclude_set = {f"{CLEAN_FUNC_PREFIX}{f}" for f in exclude}  # clean_attr, clean_attr2...
        instance_objects = self.__class__.__dict__.items()
        # filtering our instance functions
        check_funcs = (func for func_name, func in instance_objects
                       if inspect.isfunction(func)
                       and func_name.startswith(CLEAN_FUNC_PREFIX)
                       and func_name not in exclude_set)
        validation_errors = {}
        for func in check_funcs:
            try:
                # trying each _check function
                func(self)
            except ValidationError as e:
                validation_errors.update(e)

        if validation_errors:
            raise ValidationError(validation_errors)

        super().clean_fields(exclude)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


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


class Booking(CheckContraintsMixin, models.Model):
    MAX_ALLOWED_DATE = date(2022, 12, 31)
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

    # managers
    objects = BookingManager()
    
    def __str__(self):
        return self.code

    @staticmethod
    def format_dates(date: date) -> str:
        return date.strftime('%d/%m/%Y')

    @staticmethod
    def _booking_days(start_date, end_date):
        delta = start_date - end_date
        return delta.days + 1  # adding 1 as checkin:2023/01/01, checkout:2023/01/01 is 1 day

    def _calculate_price(self):
        return Booking._booking_days(self.checkin, self.checkout) * self.room.room_type.price

    def clean_checkin(self):
        delta = self.MAX_ALLOWED_DATE - self.checkin
        if delta.days < 0:
            formatted_str = Booking.format_dates(self.MAX_ALLOWED_DATE)
            raise ValidationError({"checkin": f"La fecha de checkin no puede ser posterior a {formatted_str}"})
        return self.checkin

    def clean_checkout(self):
        delta = self.MAX_ALLOWED_DATE - self.checkout
        if delta.days < 0:
            formatted_str = Booking.format_dates(self.MAX_ALLOWED_DATE)
            raise ValidationError({"checkout": f"La fecha de checkout no puede ser posterior a {formatted_str}"})
        return self.checkout

    def clean(self):
        errors = {}
        # check dates range has a positive number of days
        delta = self.checkout - self.checkin
        if delta.days < 0:
            checking_str = Booking.format_dates(self.checkin)
            checkout_str = Booking.format_dates(self.checkout)
            errors['checkout'] = f"La fecha de checkout {checkout_str} no puede ser anterior a la fecha de checkin {checking_str}."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.total = self._calculate_price()
        super().save(*args, **kwargs)
