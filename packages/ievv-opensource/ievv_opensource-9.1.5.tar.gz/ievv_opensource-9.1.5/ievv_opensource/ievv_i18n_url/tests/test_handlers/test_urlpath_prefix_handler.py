from unittest import mock

from django import test
from ievv_opensource.ievv_i18n_url import active_i18n_url_translation
from ievv_opensource.ievv_i18n_url.base_url import BaseUrl
from ievv_opensource.ievv_i18n_url.handlers.urlpath_prefix_handler import \
    UrlpathPrefixHandler


class UrlpathPrefixExtraPrefixHandler(UrlpathPrefixHandler):
    LANGUAGECODE_URLPATH_PREFIX = 'l/s'


@test.override_settings(
    LANGUAGE_CODE='en',
    LANGUAGES=(
        ('en', 'English'),
        ('nb', 'Norwegian'),
        ('de', 'German'),
    ),
    IEVV_I18N_URL_FALLBACK_BASE_URL='https://example.com'
)
class TestAbstractHandler(test.TestCase):
    def setUp(self):
        active_i18n_url_translation.activate()

    def test_get_urlpath_prefix_for_languagecode(self):
        self.assertEqual(UrlpathPrefixHandler.get_urlpath_prefix_for_languagecode(BaseUrl(), 'nb'), 'nb')
        self.assertEqual(UrlpathPrefixHandler.get_urlpath_prefix_for_languagecode(BaseUrl(), 'en'), '')
        self.assertEqual(UrlpathPrefixExtraPrefixHandler.get_urlpath_prefix_for_languagecode(BaseUrl(), 'en'), '')
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler.get_urlpath_prefix_for_languagecode(BaseUrl(), 'nb'),
            'l/s/nb')

    def test_strip_languagecode_from_urlpath(self):
        self.assertEqual(
            UrlpathPrefixHandler._strip_languagecode_from_urlpath(BaseUrl(), 'nb', '/nb/my/view'),
            '/my/view')
        self.assertEqual(
            UrlpathPrefixHandler._strip_languagecode_from_urlpath(BaseUrl(), 'nb', '/x/nb/my/view'),
            '/x/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler._strip_languagecode_from_urlpath(BaseUrl(), 'en', '/en/my/view'),
            '/en/my/view')
        self.assertEqual(
            UrlpathPrefixHandler._strip_languagecode_from_urlpath(BaseUrl(), 'xx', '/xx/my/view'),
            '/xx/my/view')

        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler._strip_languagecode_from_urlpath(BaseUrl(), 'nb', '/l/s/nb/my/view'),
            '/my/view')
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler._strip_languagecode_from_urlpath(BaseUrl(), 'nb', '/x/l/s/nb/my/view'),
            '/x/l/s/nb/my/view')
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler._strip_languagecode_from_urlpath(BaseUrl(), 'en', '/l/s/en/my/view'),
            '/l/s/en/my/view')
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler._strip_languagecode_from_urlpath(BaseUrl(), 'xx', '/l/s/xx/my/view'),
            '/l/s/xx/my/view')

    def test_get_languagecode_from_url(self):
        self.assertEqual(UrlpathPrefixHandler.get_languagecode_from_url('http://example.com/nb/my/view'), 'nb')
        self.assertEqual(UrlpathPrefixHandler.get_languagecode_from_url('http://example.com/x/nb/my/view'), 'en')
        self.assertEqual(UrlpathPrefixHandler.get_languagecode_from_url('http://example.com/sv/my/view'), 'en')

        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler.get_languagecode_from_url('http://example.com/l/s/nb/my/view'), 'nb')
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler.get_languagecode_from_url('http://example.com/x/l/s/nb/my/view'), 'en')
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler.get_languagecode_from_url('http://example.com/l/s/sv/my/view'), 'en')

    def test_detect_current_languagecode(self):
        class MockRequest:
            def __init__(self, path):
                self.path = path

            def build_absolute_uri(self):
                return f'http://example.com{self.path}'

        self.assertEqual(
            UrlpathPrefixHandler.detect_current_languagecode(BaseUrl(), MockRequest('/nb/my/view')),
            'nb')
        self.assertEqual(
            UrlpathPrefixHandler.detect_current_languagecode(BaseUrl(), MockRequest('/x/nb/my/view')),
            'en')
        self.assertEqual(
            UrlpathPrefixHandler.detect_current_languagecode(BaseUrl(), MockRequest('/sv/my/view')),
            'en')

        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler.detect_current_languagecode(BaseUrl(), MockRequest('/l/s/nb/my/view')),
            'nb')
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler.detect_current_languagecode(BaseUrl(), MockRequest('/x/l/s/nb/my/view')),
            'en')
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler.detect_current_languagecode(BaseUrl(), MockRequest('/l/s/sv/my/view')),
            'en')

    def test_build_urlpath(self):
        self.assertEqual(
            UrlpathPrefixHandler().build_urlpath('/my/view'),
            '/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_urlpath('/my/view', languagecode='nb'),
            '/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_urlpath('/my/view', languagecode='en'),
            '/my/view')

    def test_build_urlpath_nondefault_active_languagecode(self):
        active_i18n_url_translation.activate(active_languagecode='nb')
        self.assertEqual(
            UrlpathPrefixHandler().build_urlpath('/my/view'),
            '/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_urlpath('/my/view', languagecode='nb'),
            '/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_urlpath('/my/view', languagecode='en'),
            '/my/view')

    def test_build_absolute_url(self):
        self.assertEqual(
            UrlpathPrefixHandler().build_absolute_url('/my/view'),
            'https://example.com/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_absolute_url('/my/view', languagecode='nb'),
            'https://example.com/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_absolute_url('/my/view', languagecode='en'),
            'https://example.com/my/view')

    def test_build_absolute_url_nondefault_active_languagecode(self):
        active_i18n_url_translation.activate(active_languagecode='nb')
        self.assertEqual(
            UrlpathPrefixHandler().build_absolute_url('/my/view'),
            'https://example.com/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_absolute_url('/my/view', languagecode='nb'),
            'https://example.com/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_absolute_url('/my/view', languagecode='en'),
            'https://example.com/my/view')

    def test_transform_url_to_languagecode_simple(self):
        # active_i18n_url_translation.activate(active_languagecode='nb')
        self.assertEqual(
            UrlpathPrefixHandler.transform_url_to_languagecode('https://example.com/my/view', 'nb'),
            'https://example.com/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler.transform_url_to_languagecode('https://example.com/my/view', 'nb'),
            'https://example.com/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler.transform_url_to_languagecode('https://example.com/nb/my/view', 'en'),
            'https://example.com/my/view')
        self.assertEqual(
            UrlpathPrefixHandler.transform_url_to_languagecode('https://example.com/nb/my/view', 'nb'),
            'https://example.com/nb/my/view')

        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler.transform_url_to_languagecode('https://example.com/l/s/nb/my/view', 'en'),
            'https://example.com/my/view')
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler.transform_url_to_languagecode('https://example.com/my/view', 'nb'),
            'https://example.com/l/s/nb/my/view')

    def test_transform_url_to_languagecode_translate_path(self):
        self.assertEqual(
            UrlpathPrefixHandler.transform_url_to_languagecode(
                'https://example.com/ievv_i18n_url_testapp/my/named/untranslated_example', 'nb'),
            'https://example.com/nb/ievv_i18n_url_testapp/my/named/untranslated_example')
        self.assertEqual(
            UrlpathPrefixHandler.transform_url_to_languagecode(
                'https://example.com/ievv_i18n_url_testapp/my/named/translated_example', 'nb'),
            'https://example.com/nb/ievv_i18n_url_testapp/mitt/navngitte/oversatte-eksempel')
        self.assertEqual(
            UrlpathPrefixHandler.transform_url_to_languagecode(
                'https://example.com/nb/ievv_i18n_url_testapp/mitt/navngitte/oversatte-eksempel', 'de'),
            'https://example.com/de/ievv_i18n_url_testapp/mein/benanntes/ubersetztes-beispiel')
