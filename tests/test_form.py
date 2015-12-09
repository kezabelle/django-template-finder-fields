# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.forms import modelform_factory, Select
from templatefinderfields import TemplateChoiceField
from test_app.models import TestTemplateModel


def test_modelform_widget():
    factory = modelform_factory(TestTemplateModel, exclude=())
    form = factory()
    assert isinstance(form.fields['template'].widget, Select)
    assert isinstance(form.fields['another_template'].widget, Select)
    assert isinstance(form.fields['empty_template'].widget, Select)


def test_modelform_fieldtype():
    factory = modelform_factory(TestTemplateModel, exclude=())
    form = factory()
    assert isinstance(form.fields['template'], TemplateChoiceField)
    assert isinstance(form.fields['another_template'], TemplateChoiceField)
    assert isinstance(form.fields['empty_template'], TemplateChoiceField)


def test_modelform_choices():
    factory = modelform_factory(TestTemplateModel, exclude=())
    form = factory()
    # This includes a .txt file
    assert len(form.fields['template'].choices) == 38
    # This includes the blank choice.
    assert len(form.fields['another_template'].choices) == 38
    # This also contains a blank dash.
    assert len(form.fields['empty_template'].choices) == 1
