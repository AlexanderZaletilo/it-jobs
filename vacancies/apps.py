from django.apps import AppConfig
import sys


class VacanciesConfig(AppConfig):
    name = "vacancies"

    def ready(self):
        if 'runserver' not in sys.argv:
            return True

        currencies = ['USD', 'RUB', 'BYN', 'EUR']
        sites = ['rabota_by', 'dev_by']
        from vacancies.models import Currency, SiteType

        Currency.objects.bulk_create([
                 Currency(name=item) for item in currencies
            ], ignore_conflicts=True)

        SiteType.objects.bulk_create([
            SiteType(name=item) for item in sites
        ], ignore_conflicts=True)
