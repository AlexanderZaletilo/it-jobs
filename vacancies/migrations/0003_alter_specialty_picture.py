# Generated by Django 3.2.5 on 2021-11-22 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vacancies", "0002_auto_20211121_1834"),
    ]

    operations = [
        migrations.AlterField(
            model_name="specialty",
            name="picture",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
