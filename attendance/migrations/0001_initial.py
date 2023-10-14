# Generated by Django 4.2.2 on 2023-08-07 21:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='attendaceRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('signed', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(4)])),
                ('total', models.IntegerField(default=0)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.student')),
            ],
        ),
        migrations.CreateModel(
            name='subjectAttendaceRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjectRequest', to='attendance.attendacerequest')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.subject')),
            ],
        ),
        migrations.CreateModel(
            name='studentcourse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sem', models.IntegerField()),
                ('attendance', models.FloatField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.subject')),
            ],
        ),
        migrations.CreateModel(
            name='declaration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('signed', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(3)])),
                ('doc', models.ImageField(upload_to='uploads')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.student')),
            ],
        ),
        migrations.CreateModel(
            name='fam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.faculty')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fams', to='home.student')),
            ],
            options={
                'unique_together': {('faculty', 'student')},
            },
        ),
    ]
