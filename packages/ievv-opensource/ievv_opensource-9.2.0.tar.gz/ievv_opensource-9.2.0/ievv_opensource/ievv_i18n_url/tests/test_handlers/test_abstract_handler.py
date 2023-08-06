from unittest import mock

from django import test
from ievv_opensource.ievv_i18n_url import active_i18n_url_translation
from ievv_opensource.ievv_i18n_url.base_url import BaseUrl
from ievv_opensource.ievv_i18n_url.handlers import AbstractHandler
from ievv_opensource.ievv_i18n_url.handlers.abstract_handler import \
    UrlTransformError


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

    def test_is_default_languagecode(self):
        active_i18n_url_translation.activate(active_languagecode='de', default_languagecode='nb')
        self.assertTrue(AbstractHandler().is_default_languagecode('nb'))
        self.assertFalse(AbstractHandler().is_default_languagecode('de'))

    def test_default_languagecode(self):
        active_i18n_url_translation.activate(active_languagecode='de', default_languagecode='nb')
        self.assertEqual(AbstractHandler().default_languagecode, 'nb')

    def test_active_languagecode(self):
        active_i18n_url_translation.activate(active_languagecode='de', default_languagecode='nb')
        self.assertEqual(AbstractHandler().active_languagecode, 'de')

    def test_active_languagecode_or_none_if_default(self):
        active_i18n_url_translation.activate(active_languagecode='de', default_languagecode='de')
        self.assertIsNone(AbstractHandler().active_languagecode_or_none_if_default)

    def test_active_base_url(self):
        active_i18n_url_translation.activate(active_base_url='https://active.example.com')
        self.assertEqual(AbstractHandler().active_base_url, 'https://active.example.com')

    def test_get_supported_languagecodes(self):
        self.assertEqual(AbstractHandler.get_all_supported_languagecodes(), {'en', 'nb', 'de'})

    def test_is_supported_languagecode(self):
        self.assertTrue(AbstractHandler.is_supported_languagecode('de'))
        self.assertFalse(AbstractHandler.is_supported_languagecode('se'))

    def test_get_translated_label_for_languagecode(self):
        active_i18n_url_translation.activate(active_languagecode='nb')
        self.assertEqual(AbstractHandler().get_translated_label_for_languagecode('de'), 'Tysk')

    def test_get_untranslated_label_for_languagecode(self):
        self.assertEqual(AbstractHandler().get_untranslated_label_for_languagecode('de'), 'German')

    def test_get_local_label_for_languagecode(self):
        self.assertEqual(AbstractHandler().get_local_label_for_languagecode('de'), 'Deutsch')

    def test_get_icon_cssclass_for_languagecode(self):
        self.assertIsNone(AbstractHandler().get_icon_cssclass_for_languagecode('en'))

    def test_get_icon_svg_image_url_for_languagecode(self):
        self.assertIsNone(AbstractHandler().get_icon_svg_image_url_for_languagecode('en'))

    def test_get_translation_to_activate_for_languagecode(self):
        self.assertEqual(AbstractHandler().get_translation_to_activate_for_languagecode('en'), 'en')

    @test.override_settings(
        STATIC_URL='/static',
        MEDIA_URL='/media',
    )
    def test_is_translatable_urlpath(self):
        self.assertTrue(AbstractHandler.is_translatable_urlpath(BaseUrl(), '/my/path'))
        self.assertFalse(AbstractHandler.is_translatable_urlpath(BaseUrl(), '/media/stuff'))
        self.assertFalse(AbstractHandler.is_translatable_urlpath(BaseUrl(), '/static/stuff'))

    def test_detect_preferred_languagecode_for_user(self):
        self.assertIsNone(AbstractHandler.detect_preferred_languagecode_for_user(user=mock.MagicMock()))

    def test_detect_default_languagecode(self):
        self.assertEqual(AbstractHandler.detect_default_languagecode(BaseUrl()), 'en')

        with test.override_settings(LANGUAGE_CODE='nb'):
            self.assertEqual(AbstractHandler.detect_default_languagecode(BaseUrl()), 'nb')

    def test_get_urlpath_prefix_for_languagecode(self):
        self.assertEqual(AbstractHandler().get_urlpath_prefix_for_languagecode(BaseUrl(), 'en'), '')

    def test_transform_urlpath_to_languagecode_named_url_no_translation(self):
        self.assertEqual(
            AbstractHandler.transform_urlpath_to_languagecode(
                base_url=BaseUrl('https://example.com'),
                path='/ievv_i18n_url_testapp/my/named/untranslated_example',
                from_languagecode='en',
                to_languagecode='nb'),
            '/ievv_i18n_url_testapp/my/named/untranslated_example')

    def test_transform_urlpath_to_languagecode_named_url_translation(self):
        self.assertEqual(
            AbstractHandler.transform_urlpath_to_languagecode(
                base_url=BaseUrl('https://example.com'),
                path='/ievv_i18n_url_testapp/my/named/translated_example',
                from_languagecode='en',
                to_languagecode='nb'),
            '/ievv_i18n_url_testapp/mitt/navngitte/oversatte-eksempel')

    # def test_transform_urlpath_to_languagecode_unnamed_url_no_translation(self):
    #     self.assertEqual(
    #         AbstractHandler.transform_urlpath_to_languagecode(
    #             base_url=BaseUrl('https://example.com'),
    #             path='/ievv_i18n_url_testapp/my/unnamed/untranslated_example',
    #             from_languagecode='en',
    #             to_languagecode='nb'),
    #         '/ievv_i18n_url_testapp/my/unnamed/untranslated_example')

    # def test_transform_urlpath_to_languagecode_unnamed_url_translation(self):
    #     self.assertEqual(
    #         AbstractHandler.transform_urlpath_to_languagecode(
    #             base_url=BaseUrl('https://example.com'),
    #             path='/ievv_i18n_url_testapp/my/unnamed/translated_example',
    #             from_languagecode='en',
    #             to_languagecode='nb'),
    #         '/ievv_i18n_url_testapp/mitt/ikke-navngitte/oversatte_eksempel')

    def test_transform_urlpath_to_languagecode_invalid_path(self):
        with self.assertRaises(UrlTransformError):
            AbstractHandler.transform_urlpath_to_languagecode(
                base_url=BaseUrl('https://example.com'),
                path='/some/random/invalid/path',
                from_languagecode='en',
                to_languagecode='nb')
