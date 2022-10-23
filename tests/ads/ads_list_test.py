import pytest

from ads.serializers import AdListSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_list_ads(client):
    ads = AdFactory.create_batch(2)

    expected_response = {
        "count": 2,
        "next": None,
        "previous": None,
        "results": AdListSerializer(ads, many=True).data
    }

    response = client.get("/ad/")

    assert response.status_code == 200
    assert response.data == expected_response
