from decimal import Decimal
from unittest import mock

import pytest

from pms.views import DashboardView


@pytest.mark.django_db
def test_get_current_reservation_with_null():
    current_reservation = DashboardView().get_current_reservation()
    assert current_reservation == 100
