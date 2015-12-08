# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import templatefinderfields


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0004_remove_testmodel_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='testtemplatemodel',
            name='template',
            field=templatefinderfields.TemplateCharField(default='test2.html', pattern='*', max_length=255),
            preserve_default=False,
        ),
    ]
