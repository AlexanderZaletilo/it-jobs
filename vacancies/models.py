from django.contrib.auth.models import User
from django.db import models

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False


class Company(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True, db_index=True)
    logo = models.ImageField(default='company.png', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, )
    location = models.CharField(max_length=32, null=True)
    description = models.CharField(max_length=32, null=True)
    employee_count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Specialty(models.Model):
    code = models.CharField(max_length=32)
    title = models.CharField(max_length=32, db_index=True)
    picture = models.ImageField()

    def __str__(self):
        return self.code


class Vacancy(models.Model):
    title = models.CharField(max_length=124, db_index=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.CharField(max_length=124, db_index=True)
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField(max_length=32)
    written_phone = models.CharField(max_length=32)
    written_cover_letter = models.CharField(max_length=120)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return self.written_username


class StatusModel(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class GradeModel(models.Model):
    title = models.CharField(max_length=32)
    code = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class Resume(models.Model):
    verified = models.BooleanField(default=False)
    token = models.TextField(default='')
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default="check.png", null=True, blank=True)
    first_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32, null=True)
    status = models.ForeignKey(StatusModel, on_delete=models.CASCADE, related_name='resume', null=True)
    salary = models.IntegerField(null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='resume', null=True)
    phone = models.CharField(max_length=32, null=True)
    grade = models.ForeignKey(GradeModel, on_delete=models.CASCADE, related_name='resume', null=True)
    education = models.CharField(max_length=500, null=True)
    experience = models.CharField(max_length=32, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    portfolio = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.user.username
