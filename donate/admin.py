from django.contrib import admin
from donate.models import Category, Institution, Donation

admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)
