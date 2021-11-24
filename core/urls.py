import functools
import time

from django.contrib import admin
from django.db import connection, reset_queries
from django.urls import path

from vacancies.views import *


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")

        return result

    return inner_func


handler404 = custom_handler404
handler500 = custom_handler500
urlpatterns = [
    path("", MainView.as_view(), name="MainPage"),
    path("about/", About.as_view()),
    path("admin/", admin.site.urls),
    path("vacancies/", ListVacancies.as_view()),
    path("vacancies/<int:id>/", detail_vacancies),
    path("vacancies/cat/<title>/", VacancyBySpecialization.as_view()),
    path("companies/<int:id>/", DetailCompany.as_view()),
    path("mycompany/vacancies/", MyCompanyVacancyView),
    path("mycompany/vacancies/create", create_my_vacancy),
    path("mycompany/vacancies/<int:vacancy_id>", update_my_vacancy),
    path("search/", SearchView),
]

urlpatterns += [
    path("companies/", CompanyListView.as_view()),
    path("mycompany/", MyCompany, name="MyCompany"),
    path("profile", AccountSettings, name="profile"),
    path("logout", LogoutPage, name="logout"),
    path("login", LoginPage, name="login"),
    path("register/", RegisterPage, name="register"),
    path("myresume/", ResumeEdit, name="myresume"),
]
