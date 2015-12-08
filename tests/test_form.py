# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.forms import modelform_factory
from test_app.models import TestTemplateModel


def test_modelform():
    factory = modelform_factory(TestTemplateModel, exclude=())
    form = factory()
    assert form.fields['template'].widget ==''
    assert form.fields['another_template'].widget ==''
    assert form.fields['empty_template'].widget ==''
