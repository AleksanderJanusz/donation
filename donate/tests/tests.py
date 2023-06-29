import pytest
from django.test import Client
from django.urls import reverse
import math
from donate.models import Institution, Donation


@pytest.mark.django_db
def test_index_view_bags_and_institutions_counter(ten_donations_to_five_institutions):
    client = Client()
    url = reverse('index')
    response = client.get(url)
    total_quantities = sum([donation.quantity for donation in Donation.objects.all()])
    total_supported_institutions = Donation.objects.distinct('institution_id').count()

    assert total_quantities == response.context['bags']
    assert total_supported_institutions == response.context['total_institutions']
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("inst, context1, context2",
                         [(Institution.objects.filter(type=0), 'foundations', 'found_pages'),
                          (Institution.objects.filter(type=1), 'organizations', 'org_pages'),
                          (Institution.objects.filter(type=2), 'collections', 'col_pages')])
def test_index_view_pages_and_institutions(ten_donations_to_five_institutions, inst, context1, context2):
    client = Client()
    url = reverse('index')
    response = client.get(url)
    pages = [i + 1 for i in range(0, math.ceil(len(inst) / 5))]
    institutions = inst[:5]

    assert response.status_code == 200
    assert institutions == response.context[context1].object_list
    assert pages == response.context[context2]


@pytest.mark.django_db
@pytest.mark.parametrize("test_type", [0, 1, 2])
def test_institutions_api_type0(institutions_with_categories, test_type):
    client = Client()
    url = reverse('inst_api')
    response = client.get(url + f'?page=1&type={test_type}')
    first_inst = Institution.objects.filter(type=test_type).first()

    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0]['name'] == first_inst.name
    assert response.json()[0]['description'] == first_inst.description
    assert len(response.json()[0]['categories'].split()) == len(first_inst.categories.all())
