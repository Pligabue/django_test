# Generated by Django 2.2.5 on 2019-09-29 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0006_auto_20190929_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coach',
            name='team',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coach', to='tournament.Team'),
        ),
    ]
