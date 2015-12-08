# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
# from functools import partial
from django.contrib.admin.widgets import AdminTextInputWidget
from django.db.models import BLANK_CHOICE_DASH
from fnmatch import fnmatch
from django.core.exceptions import ValidationError
import os
from django import forms
# from django.core import checks
from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
# from django.utils.functional import curry
from templatefinder import find_all_templates, template_choices
#
# W001 = partial(checks.Warning,
#     msg="TemplateChoiceField could not find any template files",
#     id='templatefinderfields.E001',
# )



class FilenameMatchValidator(object):
    __slots__ = ('pattern', 'message', 'code', 'evaluated')

    def __init__(self, pattern, message=None, code='invalid'):
        self.pattern = pattern
        self.message = message or _('Enter a valid value.')
        self.code = code
        self.evaluated = None

    def get_matches(self):
        if self.evaluated is None:
            self.evaluated = find_all_templates(pattern=self.pattern)
        return self.evaluated

    def __repr__(self):
        fields = ("%s='%s'" % (str(x), force_text(getattr(self, x)))
                  for x in self.__slots__ if x != 'evaluated')
        return '%(mod)s.%(cls)s(%(fields)s)' % {
            'mod': self.__module__,
            'cls': self.__class__.__name__,
            'fields': ', '.join(fields),
        }

    def __call__(self, value):
        # Attempt to emulate the find_all_templates filtering without actually
        # asking for the matching files.
        basename = os.path.basename(value)
        consider = (fnmatch(value, self.pattern),
                    fnmatch(basename, self.pattern))
        error = ValidationError(message=self.message, code=self.code, params={
            'pattern': self.pattern,
        })
        if not any(consider):
            raise error
        matches = self.get_matches()
        if value not in matches:
            raise error
        return True


class TemplateCharField(models.CharField):
    """
    lol = TemplateChoiceField(pattern='*.html',
                              display_names={'lol.html': 'LOL'})
    """
    def __init__(self, pattern, display_names=None, *args, **kwargs):
        self._pattern = pattern
        self._display_names = display_names
        if 'choices' in kwargs:
            raise TypeError("`choices` should not be set directly, use "
                            "`pattern` and `display_names` instead")
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        super(TemplateCharField, self).__init__(*args, **kwargs)
        self.fnmatcher = FilenameMatchValidator(pattern=self._pattern)
        self.validators.append(self.fnmatcher)
    #
    # This slows stuff down :(
    #
    # def check(self, **kwargs):
    #     errors = super(TemplateCharField, self).check(**kwargs)
    #     errors.extend(self._check_templates_exist(**kwargs))
    #     return errors
    #
    # def _check_templates_exist(self, **kwargs):
    #     if not self._templates:
    #         return [
    #             W001(hint="%r doesn't match anything?" % self._pattern,
    #                  obj=self)
    #         ]
    #     return []

    def deconstruct(self):
        name, path, args, kwargs = super(TemplateCharField, self).deconstruct()
        kwargs['pattern'] = self._pattern
        if self._display_names is not None:
            kwargs['display_names'] = self._display_names
        if 'choices' in kwargs:
            kwargs.pop('choices')
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {
            'pattern': self._pattern,
            'display_names': self._display_names,
            'form_class': TemplateChoiceField,
            'matches': self.fnmatcher.get_matches(),
            # 'required': not self.blank,
        }
        if 'widget' in kwargs:
            if kwargs['widget']().__class__ == AdminTextInputWidget:
                kwargs.pop('widget')
        defaults.update(kwargs)
        # skip the max_length
        return super(models.CharField, self).formfield(**defaults)

    def contribute_to_class(self, cls, name, virtual_only=False):
        super(TemplateCharField, self).contribute_to_class(
            cls=cls, name=name, virtual_only=virtual_only)

        def wrapper(instance):
            def yielder(selected, choices, attname):
                for value, key in choices:
                    yield {
                        'description': key,
                        'path': value,
                        'selected': selected == value,
                        '_meta': {
                            'attribute': attname,
                            'extension': os.path.splitext(value)[1] or None,
                            'basename': os.path.basename(value),
                            'dirname': os.path.dirname(value) or None,
                            'segments': value.split(os.path.sep),
                        }
                    }
            attname = self.get_attname()
            choices = template_choices(
                templates=self.fnmatcher.get_matches(),
                display_names=self._display_names)
            value = getattr(instance, attname)
            return tuple(yielder(selected=value, choices=choices, attname=attname))
        setattr(cls, 'get_%s_info' % self.name, wrapper)


class TemplateChoiceField(forms.TypedChoiceField):
    def __init__(self, pattern, display_names=None, *args, **kwargs):
        if 'coerce' in kwargs:
            raise TypeError("`coerce` should not be set directly")
        kwargs['coerce'] = force_text
        self._pattern = pattern
        self._display_names = display_names
        if 'matches' in kwargs:
            self._templates = kwargs.pop('matches')
        else:
           self._templates = find_all_templates(pattern=pattern)
        super(TemplateChoiceField, self).__init__(*args, **kwargs)
        choices = list(template_choices(
            templates=self._templates, display_names=self._display_names))
        if not self.required or len(choices) == 0:
            choices = BLANK_CHOICE_DASH + choices
        self.choices = choices

    def __repr__(self):
        return ('%(mod)s.%(cls)s(pattern="%(pat)s", display_names=%(names)r, '
                'required=%(required)r)' % {
                    'mod': self.__module__,
                    'cls': self.__class__.__name__,
                    'pat': self._pattern,
                    'names': self._display_names,
                    'required': self.required,
                })
