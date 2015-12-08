# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from django.core.exceptions import ValidationError
import pytest
from templatefinderfields import FilenameMatchValidator


def test_repr():
    x = FilenameMatchValidator(pattern='*.html')
    repr(x)  # ensure generator exp is consumable repeatedly
    expected = ("templatefinderfields.FilenameMatchValidator(pattern='*.html', "
                "message='Enter a valid value.', code='invalid')")
    assert repr(x) == expected


def test_invalid():
    x = FilenameMatchValidator(pattern='*.html')
    with pytest.raises(ValidationError):
        x('glimp.x')


def test_valid():
    x = FilenameMatchValidator(pattern='*.html')
    assert x('admin/pagination.html') is True

