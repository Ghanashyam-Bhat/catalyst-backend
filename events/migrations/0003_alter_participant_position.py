# Generated by Django 4.2.2 on 2023-10-15 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_participant_position_delete_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='position',
            field=models.FloatField(default=0),
        ),
    ]
