# Generated by Django 2.2.5 on 2019-09-29 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tournament', '0002_auto_20190916_2304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coach',
            name='name',
        ),
        migrations.RemoveField(
            model_name='coach',
            name='surname',
        ),
        migrations.AddField(
            model_name='coach',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='coach',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournament.Team'),
        ),
    ]