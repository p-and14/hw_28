import pytest

from ads.serializers import AdDetailSerializer


@pytest.mark.django_db
def test_detail_ad(client, ad, access_token):
    expected_response = AdDetailSerializer(ad).data

    response = client.get(f"/ad/{ad.pk}/", HTTP_AUTHORIZATION="Bearer " + access_token)

    assert response.status_code == 200
    assert response.data == expected_response
