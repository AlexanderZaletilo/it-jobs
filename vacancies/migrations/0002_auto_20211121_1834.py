# Generated by Django 3.2.5 on 2021-11-21 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='SiteType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='vacancy',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='company_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='company_name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='employment_mode',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='experience',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='hash',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='is_internal',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='posted',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='vacancy_id',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='vacancies.company'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary_max',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary_min',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='skills',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='specialty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='vacancies.specialty'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='title',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='vacancies.currency'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='site_type_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='vacancies.sitetype'),
        ),
        migrations.AlterUniqueTogether(
            name='vacancy',
            unique_together={('site_type_id', 'vacancy_id')},
        ),
    ]