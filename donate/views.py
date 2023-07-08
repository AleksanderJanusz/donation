from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from donate.forms import DonationForm
from donate.models import *
from django.urls import reverse


class LandingPage(View):
    def get(self, request):
        institution_per_page = 5  # CONNECTED WITH INSTITUTION API

        total_quantities = sum([donation.quantity for donation in Donation.objects.all()])
        total_supported_institutions = Donation.objects.distinct('institution_id').count()

        foundations = Institution.objects.filter(type=0).order_by('name')
        paginator_found = Paginator(foundations, institution_per_page)
        foundations_page = paginator_found.get_page(1)
        found_pages = [page for page in paginator_found.page_range]

        organizations = Institution.objects.filter(type=1).order_by('name')
        paginator_org = Paginator(organizations, institution_per_page)
        organizations_page = paginator_org.get_page(1)
        org_pages = [page for page in paginator_org.page_range]

        collections = Institution.objects.filter(type=2).order_by('name')
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


class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all().order_by('name')
        form = DonationForm()
        return render(request, 'donate/form_try.html', {'categories': categories,
                                                        "institutions": institutions,
                                                        'form': form})

    def post(self, request):
        categories_id = request.POST.getlist('categories')
        categories = [Category.objects.get(pk=int(category)) for category in categories_id]
        institutions = request.POST.getlist('organization')
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.institution = Institution.objects.get(pk=int(institutions[0]))
            donation.user = request.user
            donation.save()
            donation.categories.set(categories)
            Donation.objects.filter(pk=donation.pk).update(status_change_date=None)
            return render(request, 'donate/form-confirmation.html')

        categories = Category.objects.all()
        institutions = Institution.objects.all().order_by('name')
        return render(request, 'donate/form_try.html/', {'categories': categories,
                                                         "institutions": institutions,
                                                         'form': form})


class InstitutionPaginatorAPI(View):
    def get(self, request):
        inst_type = request.GET.get('type')
        page = request.GET.get('page')
        paginator = Paginator(Institution.objects.filter(type=inst_type), 5).get_page(page)
        result = [{'name': inst.name, 'description': inst.description,
                   'categories': " ".join([i.name if i == inst.categories.last()
                                           else i.name + ',' for i in inst.categories.all()])} for inst in paginator]
        return JsonResponse(result, safe=False)


class Profil(LoginRequiredMixin, View):
    def get(self, request):
        donation = Donation.objects.filter(user_id=request.user.id).order_by('is_taken', 'status_change_date',
                                                                             'pick_up_date')
        return render(request, 'donate/profile.html', {'donations': donation})

    def post(self, request):
        change = request.POST.get('change')
        donate = Donation.objects.get(pk=change)
        donate.is_taken = not donate.is_taken
        donate.save()
        url = reverse('profile') + '#help'
        return redirect(url)


class DonateDetails(View):
    def get(self, request, pk):
        donate = Donation.objects.get(pk=pk)
        return render(request, 'donate/donate_details.html', {'donate': donate})
