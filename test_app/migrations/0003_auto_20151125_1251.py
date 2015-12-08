# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import templatefinderfields


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_testmodel_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testtemplatemodel',
            name='template',
            field=templatefinderfields.TemplateCharField(pattern='*.htm*', max_length=255, display_names={'test.html': 'LOL'}),
        ),
    ]
