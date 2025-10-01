from decimal import Decimal

import pytest

from network.admin import clear_debt
from network.models import NetworkUnit


@pytest.mark.django_db
def test_admin_action_clear_debt():
    factory = NetworkUnit.objects.create(
        name="Завод",
        email="f@example.com",
        country="Korea",
        city="Suwon",
        street="Main",
        house_number="1",
        debt=Decimal("0.00"),
    )
    retail = NetworkUnit.objects.create(
        name="Розница",
        email="r@example.com",
        country="Georgia",
        city="Tbilisi",
        street="Rustaveli",
        house_number="10",
        supplier=factory,
        debt=Decimal("123.45"),
    )

    qs = NetworkUnit.objects.filter(id__in=[factory.id, retail.id])
    clear_debt(modeladmin=None, request=None, queryset=qs)

    retail.refresh_from_db()
    factory.refresh_from_db()
    assert retail.debt == Decimal("0.00")
    assert factory.debt == Decimal("0.00")
