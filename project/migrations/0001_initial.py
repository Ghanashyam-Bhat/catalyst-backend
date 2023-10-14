# Generated by Django 4.2.2 on 2023-08-07 21:28

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
            name='project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=25)),
                ('details', models.CharField(max_length=500)),
                ('withCollege', models.BooleanField()),
                ('link', models.URLField(blank=True, default='')),
                ('category', models.CharField(max_length=15, null=True)),
                ('completion', models.IntegerField(default=0)),
                ('approval', models.IntegerField(default=0)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.department')),
                ('guide', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home.faculty')),
                ('hackathon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='subjectTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.faculty')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.subject')),
            ],
            options={
                'unique_together': {('faculty', 'subject')},
            },
        ),
        migrations.CreateModel(
            name='studentProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='project.project')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.student')),
            ],
            options={
                'unique_together': {('project', 'student')},
            },
        ),
    ]