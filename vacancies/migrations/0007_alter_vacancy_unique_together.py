# Generated by Django 3.2.5 on 2021-11-23 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vacancies", "0006_rename_site_type_id_vacancy_site_type"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="vacancy",
            unique_together={("site_type_id", "vacancy_id")},
        ),
    ]
