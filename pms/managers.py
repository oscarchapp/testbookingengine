from datetime import date
from django.db import models
from django.db.models import Q
from django.db.models.functions import Coalesce

class BookingManager(models.Manager):
    def with_counts(self):
        return self.annotate(
            num_responses=Coalesce(models.Count("response"), 0)
        )

    def is_room_available(self, booking, from_date: date, to_date: date) -> bool:
        room = booking.room
        qset = super().get_queryset()
        # bookings whose checkin/checkout dates intersect our desired from_date/to_date range
        checkin_conflict = Q(checkin__range=[from_date, to_date])
        checkout_conflict = Q(checkout__range=[from_date, to_date])
        search_date_conflicts = checkin_conflict | checkout_conflict
        qset_conflicts = qset.filter(search_date_conflicts, room=room, state=self.model.NEW)
        # excluding our own booking dates in order to allow reservation period extension/reduction
        qset_cleaned = qset_conflicts.exclude(code=booking.code)
        # if queryset with conflict is bigger than 0 it means there exist conflicts
        return len(qset_cleaned) == 0
