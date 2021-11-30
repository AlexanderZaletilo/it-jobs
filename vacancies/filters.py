import django_filters
from django_filters import RangeFilter

from .models import Vacancy


class VacancyFilter(django_filters.FilterSet):
    salary_min__gt = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gt')
    salary_max__lt = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lt')

    class Meta:
        model = Vacancy
        fields = {
            'currency',
        }
