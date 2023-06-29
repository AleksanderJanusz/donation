from random import randint

import pytest

from donate.models import Category, Institution, Donation


@pytest.fixture
def categories():
    return [Category.objects.create(name=f'name{i}') for i in range(0, 10)]


@pytest.fixture
def institutions():
    foundations = [Institution.objects.create(name=f'foundation{i}',
                                              description=f'description foundation{i}',
                                              type=0) for i in range(0, 10)]
    organizations = [Institution.objects.create(name=f'organization{i}',
                                                description=f'description organization{i}',
                                                type=1) for i in range(0, 10)]
    collections = [Institution.objects.create(name=f'collections{i}',
                                              description=f'description collections{i}',
                                              type=2) for i in range(0, 10)]

    return foundations + organizations + collections


@pytest.fixture
def institutions_with_categories(institutions, categories):
    lst = []
    for institution in institutions:
        institution.categories.set(categories[:randint(0, len(categories))])
        lst.append(institution)
    return lst


@pytest.fixture
def ten_donations_to_five_institutions(institutions_with_categories):
    institutions = Institution.objects.all()
    return [Donation.objects.create(quantity=3, address=f'address{i}',
                                    phone_number='+48 123 456 789', city=f'city{i}',
                                    zip_code=f'01-2{i}', pick_up_date='2023-10-28',
                                    pick_up_time='16:10:00', pick_up_comment=f'comment{i}',
                                    institution_id=institutions[i//2].id) for i in range(0, 10)]
