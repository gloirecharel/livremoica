# Generated by Django 5.1.1 on 2025-07-11 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookrequests', '0004_merge_20250710_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrequest',
            name='status',
            field=models.IntegerField(choices=[(0, 'request pending'), (1, 'request accepted'), (2, 'request rejected'), (3, 'being delivered to borrower'), (4, 'with borrower'), (5, 'done reading'), (6, 'being delivered to owner'), (7, 'returned')], default=0),
        ),
    ]
