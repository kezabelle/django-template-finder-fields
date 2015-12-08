# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import templatefinderfields


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0006_testmodel_another_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='testtemplatemodel',
            name='empty_template',
            field=templatefinderfields.TemplateCharField(default='glorp', pattern='*.trololol', max_length=255),
            preserve_default=False,
        ),
    ]
