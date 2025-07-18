# Generated by Django 5.1.1 on 2025-07-05 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='book',
            name='unavailable_until',
            field=models.DateField(blank=True, null=True),
        ),
    ]
