# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from django.db.models import Model
from templatefinderfields import TemplateCharField


class TestTemplateModel(Model):
    template = TemplateCharField(pattern='*')
    another_template = TemplateCharField(pattern='*.html', blank=True)
    empty_template = TemplateCharField(pattern='*.trololol')
    class Meta:
        db_table = 'test_app_test_model'
