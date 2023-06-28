from random import randint

import pytest

from donate.models import Category, Institution


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
