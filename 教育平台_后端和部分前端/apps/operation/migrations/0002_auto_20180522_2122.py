# Generated by Django 2.0.5 on 2018-05-22 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfavorite',
            old_name='Fav_type',
            new_name='fav_type',
        ),
    ]
