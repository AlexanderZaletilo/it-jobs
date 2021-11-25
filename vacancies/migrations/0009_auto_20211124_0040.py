# Generated by Django 3.2.5 on 2021-11-23 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vacancies", "0008_auto_20211123_2359"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vacancy",
            name="address",
            field=models.CharField(blank=True, max_length=65535, null=True),
        ),
        migrations.AlterField(
            model_name="vacancy",
            name="company_name",
            field=models.CharField(
                blank=True, db_index=True, max_length=65535, null=True
            ),
        ),
        migrations.AlterField(
            model_name="vacancy",
            name="skills",
            field=models.CharField(
                blank=True, db_index=True, max_length=65535, null=True
            ),
        ),
        migrations.AlterField(
            model_name="vacancy",
            name="title",
            field=models.CharField(db_index=True, max_length=65535),
        ),
    ]
