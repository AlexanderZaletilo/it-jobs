# Generated by Django 3.2.5 on 2021-12-01 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0015_auto_20211128_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resumes', to='vacancies.currency'),
        ),
    ]