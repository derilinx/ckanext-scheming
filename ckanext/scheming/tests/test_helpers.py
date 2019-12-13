#!/usr/bin/env python
# encoding: utf-8
from nose.tools import assert_equals
from mock import patch

from ckanext.scheming.helpers import (
    scheming_language_text,
    scheming_field_required,
    scheming_get_preset,
    scheming_get_presets
)


class TestLanguageText(object):
    @patch('ckanext.scheming.helpers.gettext')
    def test_pass_through_gettext(self, gettext):
        gettext.side_effect = lambda x: x + '1'
        assert_equals('hello1', scheming_language_text('hello'))

    def test_only_one_language(self):
        assert_equals('hello', scheming_language_text(
            {'zh': 'hello'},
            prefer_lang='en'))

    def test_matching_language(self):
        assert_equals('hello', scheming_language_text(
            {'en': 'hello', 'aa': 'aaaa'},
            prefer_lang='en'))

    def test_first_when_no_matching_language(self):
        assert_equals('hello', scheming_language_text(
            {'aa': 'hello', 'bb': 'no'},
            prefer_lang='en'))

    def test_decodes_utf8(self):
        assert_equals('\xa1Hola!', scheming_language_text('\xc2\xa1Hola!'))

    @patch('ckanext.scheming.helpers.lang')
    def test_no_user_lang(self, lang):
        lang.side_effect = Exception()
        assert_equals('hello', scheming_language_text(
            {'en': 'hello', 'aa': 'aaaa'}))


class TestFieldRequired(object):
    def test_explicit_required_true(self):
        assert_equals(True, scheming_field_required({'required': True}))

    def test_explicit_required_false(self):
        assert_equals(False, scheming_field_required({'required': False}))

    def test_not_empty_in_validators(self):
        assert_equals(True, scheming_field_required({
            'validators': 'not_empty unicode'}))

    def test_not_empty_not_in_validators(self):
        assert_equals(False, scheming_field_required({
            'validators': 'maybe_not_empty'}))


class TestGetPreset(object):
    def test_scheming_get_presets(self):
        presets = scheming_get_presets()
        assert_equals(sorted((
            'title',
            'tag_string_autocomplete',
            'select',
            'resource_url_upload',
            'resource_format_autocomplete',
            'multiple_select',
            'multiple_checkbox',
            'date',
            'datetime',
            'dataset_slug',
            'dataset_organization'
        )), sorted(presets.keys()))

    def test_scheming_get_preset(self):
        preset = scheming_get_preset('date')
        assert_equals(sorted((
            ('display_snippet', 'date.html'),
            ('form_snippet', 'date.html'),
            ('validators', 'scheming_required isodate convert_to_json_if_date')
        )), sorted(preset.items()))
