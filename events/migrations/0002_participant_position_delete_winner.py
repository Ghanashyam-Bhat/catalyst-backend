# Generated by Django 4.2.2 on 2023-10-14 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='position',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='winner',
        ),
    ]
