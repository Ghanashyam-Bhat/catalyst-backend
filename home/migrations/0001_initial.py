# Generated by Django 4.2.2 on 2023-08-07 21:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='department',
            fields=[
                ('id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='faculty',
            fields=[
                ('id', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25)),
                ('access', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='subject',
            fields=[
                ('id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=15)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.department')),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('srn', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25)),
                ('sem', models.IntegerField()),
                ('cgpa', models.FloatField()),
                ('crypto', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.department')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='chairperson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.faculty'),
        ),
        migrations.CreateModel(
            name='club',
            fields=[
                ('id', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.faculty')),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.student')),
            ],
        ),
    ]
