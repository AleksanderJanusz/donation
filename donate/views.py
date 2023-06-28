from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from donate.models import *


class LandingPage(View):
    def get(self, request):
        institution_per_page = 5  # CONNECTED WITH INSTITUTION API

        total_quantities = sum([donation.quantity for donation in Donation.objects.all()])
        total_supported_institutions = Donation.objects.distinct('institution_id').count()

        foundations = Institution.objects.filter(type=0)
        paginator_found = Paginator(foundations, institution_per_page)
        foundations_page = paginator_found.get_page(1)
        found_pages = [page for page in paginator_found.page_range]

        organizations = Institution.objects.filter(type=1)
        paginator_org = Paginator(organizations, institution_per_page)
        organizations_page = paginator_org.get_page(1)
        org_pages = [page for page in paginator_org.page_range]

        collections = Institution.objects.filter(type=2)
        paginator_col = Paginator(collections, institution_per_page)
        collections_page = paginator_col.get_page(1)
        col_pages = [page for page in paginator_col.page_range]

        return render(request, 'donate/index.html', {'bags': total_quantities,
                                                     'total_institutions': total_supported_institutions,
                                                     'foundations': foundations_page,
                                                     'found_pages': found_pages,
                                                     'organizations': organizations_page,
                                                     'org_pages': org_pages,
                                                     'collections': collections_page,
                                                     'col_pages': col_pages})


class AddDonation(View):
    def get(self, request):
        return render(request, 'donate/form.html')


class InstitutionPaginatorAPI(View):
    def get(self, request):
        inst_type = request.GET.get('type')
        page = request.GET.get('page')
        paginator = Paginator(Institution.objects.filter(type=inst_type), 5).get_page(page)
        result = [{'name': inst.name, 'description': inst.description,
                   'categories': " ".join([i.name if i == inst.categories.last()
                                           else i.name + ',' for i in inst.categories.all()])} for inst in paginator]
        return JsonResponse(result, safe=False)
