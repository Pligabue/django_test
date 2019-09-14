# Generated by Django 2.2.5 on 2019-09-13 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_team_1', models.IntegerField()),
                ('score_team_2', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='coach',
            old_name='bday',
            new_name='birthday',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='bday',
            new_name='birthday',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='goal_diff',
            new_name='goal_difference',
        ),
        migrations.CreateModel(
            name='Game_Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Game')),
                ('player_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Player')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='team_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='tournament.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='team_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='tournament.Team'),
        ),
    ]