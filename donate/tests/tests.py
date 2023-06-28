import pytest
from django.test import Client
from django.urls import reverse

from donate.models import Institution


@pytest.mark.django_db
def test_index_view(institutions_with_categories):
    client = Client()
    url = reverse('index')
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("test_type", [0, 1, 2])
def test_institutions_api_type0(institutions_with_categories, test_type):
    client = Client()
    url = reverse('inst_api')
    response = client.get(url+f'?page=1&type={test_type}')
    first_inst = Institution.objects.filter(type=test_type).first()

    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0]['name'] == first_inst.name
    assert response.json()[0]['description'] == first_inst.description
    assert len(response.json()[0]['categories'].split()) == len(first_inst.categories.all())

