from django.contrib import admin
from django.urls import path

from vacancies.views import *

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
    path("mycompany/vacancies/", MyCompanyVacancyView.as_view()),
    path("mycompany/vacancies/create", create_my_vacancy),
    path("mycompany/vacancies/<int:vacancy_id>", update_my_vacancy),
    path("search/", SearchView),
    path("<token>/verify/", verify, name="verify"),
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
