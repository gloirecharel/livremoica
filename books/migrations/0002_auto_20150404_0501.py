# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='owner',
            field=models.ForeignKey(
                related_name='books',
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE  # Ajout obligatoire ici
            ),
            preserve_default=True,
        ),
    ]
