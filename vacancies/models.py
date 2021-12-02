import uuid

from django.contrib.auth.models import User
from django.db import models

User._meta.get_field("email")._unique = True
User._meta.get_field("email").blank = False
User._meta.get_field("email").null = False


class Company(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    logo = models.ImageField(default="company.png", null=True, blank=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    location = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, blank=True)
    employee_count = models.IntegerField(null=True, blank=True)

    external_site = models.ForeignKey(
        "SiteType", on_delete=models.SET_NULL, null=True, blank=True
    )
    external_logo_url = models.URLField(null=True, blank=True)
    external_url = models.URLField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("external_site_id", "external_url")
        index_together = [["external_site_id", "last_updated"]]

    def __str__(self):
        return str(self.name)


class Specialty(models.Model):
    code = models.CharField(max_length=32)
    title = models.CharField(max_length=32, db_index=True)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.code)


class Currency(models.Model):
    name = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return str(self.name)


class SiteType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)


class Vacancy(models.Model):
    title = models.CharField(max_length=65535, db_index=True)
    is_internal = models.BooleanField(default=True)
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)

    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.CASCADE,
        related_name="vacancies",
        null=True,
        blank=True,
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="vacancies",
        null=True,
        blank=True,
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="vacancies",
        null=True,
        blank=True,
    )

    url = models.URLField(null=True, blank=True)

    site_type = models.ForeignKey(
        SiteType,
        on_delete=models.CASCADE,
        related_name="vacancies",
        null=True,
        blank=True,
    )
    vacancy_id = models.PositiveBigIntegerField(null=True, blank=True)
    hash = models.BinaryField(null=True, blank=True, max_length=16)

    address = models.CharField(null=True, blank=True, max_length=65535)
    experience = models.CharField(null=True, blank=True, max_length=255)
    skills = models.CharField(null=True, blank=True, max_length=65535, db_index=True)
    employment_mode = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)

    posted = models.DateField(null=True, blank=True)
    published_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        unique_together = ("site_type_id", "vacancy_id")


class Application(models.Model):
    written_username = models.CharField(max_length=32, null=True, blank=True)
    written_phone = models.CharField(max_length=32, null=True, blank=True)
    written_cover_letter = models.CharField(max_length=120, null=True, blank=True)
    vacancy = models.ForeignKey(
        Vacancy, on_delete=models.CASCADE, related_name="applications", null=True, blank=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applications", null=True, blank=True
    )

    def __str__(self):
        return str(self.written_username)


class StatusModel(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return str(self.title)


class GradeModel(models.Model):
    title = models.CharField(max_length=32)
    code = models.CharField(max_length=32)

    def __str__(self):
        return str(self.title)


class Resume(models.Model):
    verified = models.BooleanField(default=False)
    token = models.TextField(default="")
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default="check.png", null=True, blank=True)
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, null=True, blank=True)
    status = models.ForeignKey(
        StatusModel,
        on_delete=models.CASCADE,
        related_name="resume",
        null=True,
        blank=True,
    )
    salary = models.IntegerField(null=True, blank=True)
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.CASCADE,
        related_name="resume",
        null=True,
        blank=True,
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="resumes",
        null=True,
        blank=True,
    )
    phone = models.CharField(max_length=32, null=True, blank=True)
    grade = models.ForeignKey(
        GradeModel,
        on_delete=models.CASCADE,
        related_name="resume",
        null=True,
        blank=True,
    )
    education = models.CharField(max_length=500, null=True, blank=True)
    experience = models.CharField(max_length=32, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    portfolio = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)
