# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import templatefinderfields


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testtemplatemodel',
            name='template',
            field=templatefinderfields.TemplateCharField(default='test.html', pattern='*.html', max_length=255),
            preserve_default=False,
        ),
    ]
