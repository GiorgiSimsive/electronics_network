from decimal import Decimal

import pytest

from network.models import NetworkUnit, Product


@pytest.mark.django_db
def test_api_permissions_only_staff(api_client, regular_user):
    api_client.login(username="user", password="pass12345")
    resp = api_client.get("/api/suppliers/")
    assert resp.status_code in (401, 403)
    api_client.logout()


@pytest.mark.django_db
def test_api_create_filter_and_forbid_debt_update(api_client, staff_user):
    api_client.login(username="staff", password="pass12345")

    factory = NetworkUnit.objects.create(
        name="Завод",
        email="f@example.com",
        country="Korea",
        city="Suwon",
        street="Main",
        house_number="1",
    )
    p = Product.objects.create(name="Smartphone", model="X1", release_date="2025-01-01")

    payload = {
        "name": "Розница",
        "email": "r@example.com",
        "country": "Georgia",
        "city": "Tbilisi",
        "street": "Rustaveli",
        "house_number": "10",
        "supplier": factory.id,
        "products": [p.id],
        "debt": "12500.50",
    }
    resp = api_client.post("/api/suppliers/", data=payload, format="json")
    assert resp.status_code == 201, resp.content
    item_id = resp.data["id"]

    resp = api_client.get("/api/suppliers/?country=Georgia")
    assert resp.status_code == 200
    assert any(x["id"] == item_id for x in resp.data)

    resp = api_client.patch(f"/api/suppliers/{item_id}/", data={"debt": "0.00", "city": "Batumi"}, format="json")
    assert resp.status_code == 200
    created = NetworkUnit.objects.get(id=item_id)
    assert created.city == "Batumi"
    assert created.debt == Decimal("12500.50")

    api_client.logout()
