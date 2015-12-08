# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pickle
from django.core.exceptions import ValidationError
import pytest
from test_app.models import TestTemplateModel


def test_can_pickle_with_weirdly_wrapped_info_method():
    lol = TestTemplateModel()
    lol2 = pickle.loads(pickle.dumps(lol))
    assert len(lol2.get_template_info()) == len(lol.get_template_info())


def test_info_methods_return_expected_lengths():
    lol = TestTemplateModel()
    assert len(lol.get_template_info()) == 38
    assert len(lol.get_another_template_info()) == 37


def test_info_methods_include_expected_keys():
    lol = TestTemplateModel()
    expected = ('path', 'selected', 'description', '_meta')
    assert tuple(lol.get_template_info()[0].keys()) == expected


def test_info_methods_include_expected_paths():
    lol = TestTemplateModel()
    paths = tuple(x['path'] for x in lol.get_template_info())  # noqa
    # paths was only to ensure repeated calls work.
    paths2 = tuple(x['path'] for x in lol.get_template_info())
    assert 'admin/change_form.html' in paths2
    assert 'registration/password_reset_subject.txt' in paths2


def test_info_methods_exclude_expected_paths():
    lol = TestTemplateModel()
    paths = tuple(x['path'] for x in lol.get_template_info())
    assert 'registration/password_reset_subject.txt' in paths
    paths2 = tuple(x['path'] for x in lol.get_another_template_info())
    assert 'registration/password_reset_subject.txt' not in paths2


def test_cleaning_error():
    lol = TestTemplateModel(another_template='guess.json')
    with pytest.raises(ValidationError):
        lol.full_clean(exclude=['empty_template', 'template'])


def test_cleaning():
    lol = TestTemplateModel(another_template='admin/change_form.html')
    lol.full_clean(exclude=['empty_template', 'template'])
