import pytest


@pytest.mark.django_db
def test_create_selection(client, django_user_model, access_token, user, ad):
    expected_response = {
        "id": 1,
        "name": "test_selection_name",
        "owner": user.pk,
        "items": [ad.pk]
    }

    data = {
        "name": "test_selection_name",
        "owner": user.pk,
        "items": [ad.pk]
    }

    response = client.post(
        "/selection/create/",
        data=data,
        format="json",
        HTTP_AUTHORIZATION="Bearer " + access_token
   )

    assert response.status_code == 201
    assert response.data == expected_response
