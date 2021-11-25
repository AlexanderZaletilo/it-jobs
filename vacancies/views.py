import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView, View

from .forms import *
from core.base.send_emails import send_verification_email_link
from .models import Specialty, Application
from .token import account_activation_token

logger = logging.getLogger(__name__)


def SearchView(request):
    template_name = "search.html"
    q = request.GET.get("q", "")
    results = Vacancy.objects.all()
    if q:
        results = Vacancy.objects.select_related("specialty", "company").annotate(
            search=SearchVector("title", "specialty__title", "company__name", "skills")
        ).filter(search=q)
        return render(request, template_name, {"results": results, "query": q})
    return render(request, template_name, {"results": results})


class CompanyListView(ListView):
    model = Company
    template_name = "company_list.html"
    context_object_name = "objects"


class About(View):
    def get(self, request):
        return render(request, "about.html")


def create_my_vacancy(request):
    form = VacancyForm()
    if request.method == "POST":
        form = VacancyForm(request.POST)
        if form.is_valid():
            Vacancy.objects.create(
                title=request.POST.get("title"),
                specialty_id=request.POST.get("specialty"),
                company=Company.objects.get(owner=request.user),
                skills=request.POST.get("skills"),
                description=request.POST.get("description"),
                salary_min=request.POST.get("salary_min"),
                salary_max=request.POST.get("salary_max"),
            )
            return redirect("/mycompany/vacancies")
    context = {"form": form}
    return render(request, "vacancy-create.html", context=context)


def update_my_vacancy(request, vacancy_id):
    vacancy = Vacancy.objects.filter(id=vacancy_id).first()
    if vacancy == None:
        logger.warning("Запрос несуществующей вакансии!")
        raise Http404
    form = VacancyForm(instance=vacancy)
    if "update" in request.POST:
        form = VacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            messages.info(request, "Ваша вакансия обновлена!")
            form.save()
    elif "delete" in request.POST:
        vacancy = Vacancy.objects.get(id=vacancy_id)
        vacancy.delete()
        return redirect("/mycompany/vacancies")

    context = {
        "form": form,
        "applications": Vacancy.objects.get(id=vacancy_id).applications.all(),
    }
    return render(request, "vacancy-edit.html", context=context)


def MyCompanyVacancyView(request):
    template_name = "vacancy-list.html"
    context = {"objects": Vacancy.objects.filter(company__owner=request.user)}
    return render(request, template_name, context=context)


def MyCompany(request):
    if not Company.objects.select_related("owner").filter(owner=request.user):
        if request.method == "POST":
            Company.objects.create(owner=request.user)
            return render(request, "company-edit.html")
        else:
            return render(request, "company-create.html")
    else:
        company = Company.objects.select_related("owner").get(owner=request.user)
        form = MyCompanyForm(instance=company)
        if request.method == "POST":
            form = MyCompanyForm(request.POST, request.FILES, instance=company)
            if form.is_valid():
                messages.info(request, "Информация о вашей компании успешно обновлена!")
                form.save()

        context = {"form": form, "logo": company.logo}
        return render(request, "company-edit.html", context)


def AccountSettings(request):
    user = request.user.resume
    form = ProfileForm(instance=user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

    context = {"form": form}
    return render(request, "profile.html", context)


@login_required
def ResumeEdit(request):
    user = request.user.resume
    form = ResumeForm(instance=user)
    if request.method == "POST":
        form = ResumeForm(request.POST, instance=user)
        if form.is_valid():
            messages.info(request, "Ваше резюме обновлено!")
            form.save()

    context = {"form": form}
    return render(request, "resume-edit.html", context)


def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get("username")
                resume = Resume.objects.create(
                    user=user,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    verified=True,
                    token=account_activation_token.make_token(user),
                )
                resume.save()
                send_verification_email_link.delay(
                    to_email=user.email,
                    to_name=user.first_name,
                    link=f'http://localhost:8000/{user.resume.token}/verify/',
                    firstname=user.first_name,
                )
                messages.success(request, "Аккаунт был создан для " + username)
                return HttpResponseRedirect(reverse_lazy("login"))
        context = {"form": form}
        return render(request, "register.html", context)


def LoginPage(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not user.resume.verified:
                    messages.info(
                        request, "Ваш аккаунт не активирован, проверьте вашу почту !"
                    )
                    return render(request, "login.html")
                login(request, user=user)
                return HttpResponseRedirect(reverse_lazy("MainPage"))
            else:
                messages.info(request, "Неверный логин или пароль")

        context = {}
        return render(request, "login.html", context)


def LogoutPage(request):
    logout(request)
    return redirect("/")


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "login.html"


class MyLogoutView(LogoutView):
    redirect_authenticated_user = False


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = "login"
    template_name = "register.html"


class MainView(ListView):
    template_name = "index.html"
    model = Vacancy

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = Specialty.objects.annotate(
            count=Count("vacancies")
        ).order_by("-count")
        context["companies"] = Company.objects.annotate(
            count=Count("vacancies")
        ).order_by("-count")
        return context


class ListVacancies(ListView):
    context_object_name = "objects"
    template_name = "vacancies.html"
    queryset = Vacancy.objects.select_related("company", "specialty").all()


class VacancyBySpecialization(ListView):
    template_name = "vacancies.html"
    queryset = Vacancy.objects.select_related("company", "specialty")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = self.get_queryset().filter(
            specialty__code=self.kwargs["title"]
        )
        context["specialties"] = Specialty.objects.get(code=self.kwargs["title"])
        return context


class DetailCompany(ListView):
    model = Company
    template_name = "company.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = get_object_or_404(Company, id=self.kwargs["id"])
        context["vacancies"] = Vacancy.objects.select_related("company", "specialty").filter(
            company=get_object_or_404(Company.objects.prefetch_related("vacancies"), id=self.kwargs["id"])
        )
        return context


def detail_vacancies(request, id):
    context = {"object": get_object_or_404(Vacancy.objects.select_related("company", "specialty"), id=id)}
    if request.user.is_authenticated:
        form = ResumeForm(instance=request.user.resume)
        if request.method == "POST":
            Application.objects.create(
                written_username=request.user.username,
                written_phone=request.user.resume.phone,
                written_cover_letter=request.user.resume.education,
                vacancy=get_object_or_404(Vacancy, id=id),
                user=request.user,
            )
            return render(request, template_name="sent.html")
        context = {
            "object": get_object_or_404(Vacancy.objects.select_related("company", "specialty"), id=id),
            "form": form}

    return render(request, "vacancy.html", context=context)


def verify(request, token):
    user = User.objects.get(resume__token=token)
    if account_activation_token.check_token(user, token):
        user.resume.verified = True
        user.resume.save()
    return redirect('MainPage')


def custom_handler404(request, exception):
    return render(request, "404.html", status=404)


def custom_handler500(request):
    return render(request, "500.html", status=500)
