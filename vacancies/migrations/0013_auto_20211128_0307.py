# Generated by Django 3.2.5 on 2021-11-28 00:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("vacancies", "0012_auto_20211126_2131"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resume",
            name="education",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="resume",
            name="experience",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="resume",
            name="first_name",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="resume",
            name="grade",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="resume",
                to="vacancies.grademodel",
            ),
        ),
        migrations.AlterField(
            model_name="resume",
            name="last_name",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="resume",
            name="phone",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="resume",
            name="portfolio",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="resume",
            name="salary",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="resume",
            name="specialty",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="resume",
                to="vacancies.specialty",
            ),
        ),
        migrations.AlterField(
            model_name="resume",
            name="status",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="resume",
                to="vacancies.statusmodel",
            ),
        ),
    ]
