# Generated by Django 5.0.4 on 2024-05-30 16:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_gameuserprogressproxy'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='game',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='games.type'),
        ),
    ]
