from django.contrib import admin

from .forms import *
from .models import Currency, SiteType
from .models import Specialty, Application
from .models import StatusModel, GradeModel


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("user", "verified")


admin.site.register(Resume, CustomUserAdmin)
admin.site.register(Vacancy)
admin.site.register(GradeModel)
admin.site.register(StatusModel)
admin.site.register(Company)
admin.site.register(Specialty)
admin.site.register(Application)
admin.site.register(Currency)
admin.site.register(SiteType)
