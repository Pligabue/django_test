# Generated by Django 2.2.5 on 2019-09-29 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0005_coach'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coach',
            name='team',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournament.Team'),
        ),
    ]
