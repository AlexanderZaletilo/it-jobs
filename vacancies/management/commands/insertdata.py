import os
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from . import data
from vacancies.models import Specialty, Company, Vacancy


class Command(BaseCommand):
    def handle(self, *args, **options):
        specialties = [Specialty(
            code=specialty.get("code"),
            title=specialty.get("title"),
            picture=specialty.get("picture"),
        ) for specialty in data.specialties]

        companies = [
            Company(
                name=company.get("title"),
                employee_count=company.get("employee_count"),
                location=company.get("location"),
                description=company.get("description"),
                logo=company.get("logo"),
            )
            for company in data.companies
        ]

        vacancies = [
            Vacancy(
                title=vacancy.get("title"),
                specialty_id=vacancy.get("specialty"),
                company_id=vacancy.get("company"),
                salary_min=vacancy.get("salary_from"),
                salary_max=vacancy.get("salary_to"),
                posted=vacancy.get("posted"),
                skills=vacancy.get("skills"),
                description=vacancy.get("description"),
            )
            for vacancy in data.jobs
        ]
        Specialty.objects.bulk_create(specialties)
        Company.objects.bulk_create(companies)
        Vacancy.objects.bulk_create(vacancies)
