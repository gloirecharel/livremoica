# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20150404_0501'),
    ]

    operations = [
            migrations.AddField(
            model_name='book',
            name='summary',
            field=models.TextField(default='Résumé non disponible'),
            preserve_default=True,
        )

    ]
