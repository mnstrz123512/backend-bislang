# Generated by Django 5.0.4 on 2024-05-23 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_type_achievement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(upload_to='games/images'),
        ),
        migrations.DeleteModel(
            name='UserProgress',
        ),
    ]
