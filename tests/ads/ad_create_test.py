import pytest

from tests.factories import CategoryFactory


@pytest.mark.django_db
def test_create_ad(client, django_user_model, user):
    expected_response = {
        "id": 1,
        "name": "test_ad_name",
        "author": user.pk,
        "price": 100,
        "description": None,
        "is_published": False,
        "image": None,
        "category": 1
    }

    cat = CategoryFactory.create()
    data = {
        "name": "test_ad_name",
        "author": user.pk,
        "price": 100,
        "category": cat.pk
    }
    response = client.post("/ad/create/", data=data, format="json")

    assert response.status_code == 201
    assert response.data == expected_response
