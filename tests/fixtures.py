import pytest


@pytest.fixture()
@pytest.mark.django_db
def access_token(client, django_user_model):
    username = "test_username"
    password = "test_password"
    birth_date = "2000-01-01"
    email = "test_mail@mail.ru"

    django_user_model.objects.create_user(
        username=username,
        password=password,
        role="админ",
        birth_date=birth_date,
        email=email
    )

    response = client.post(
        "/user/token/",
        data={"username": username, "password": password},
        format='json'
    )

    return response.data["access"]
