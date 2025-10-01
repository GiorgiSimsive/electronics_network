import pytest
from django.core.exceptions import ValidationError

from network.models import NetworkUnit


@pytest.mark.django_db
def test_levels_and_depth_validation():
    factory = NetworkUnit.objects.create(
        name="Завод",
        email="f@example.com",
        country="Korea",
        city="Suwon",
        street="Main",
        house_number="1",
    )
    retail = NetworkUnit.objects.create(
        name="Розница",
        email="r@example.com",
        country="Georgia",
        city="Tbilisi",
        street="Rustaveli",
        house_number="10",
        supplier=factory,
    )
    ip = NetworkUnit.objects.create(
        name="ИП",
        email="ip@example.com",
        country="Georgia",
        city="Batumi",
        street="Chavchavadze",
        house_number="7",
        supplier=retail,
    )

    assert factory.level == 0
    assert retail.level == 1
    assert ip.level == 2

    with pytest.raises(ValidationError):
        NetworkUnit.objects.create(
            name="Слишком глубоко",
            email="x@example.com",
            country="Georgia",
            city="Kutaisi",
            street="A",
            house_number="1",
            supplier=ip,
        )
