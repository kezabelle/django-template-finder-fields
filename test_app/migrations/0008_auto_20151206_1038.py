# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import templatefinderfields


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0007_testmodel_empty_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testtemplatemodel',
            name='another_template',
            field=templatefinderfields.TemplateCharField(pattern='*.html', max_length=255, blank=True),
        ),
    ]
