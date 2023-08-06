Testapp for the i18n url handlers.

It is here to provide some plain django views to reverse and test with translations of the URL paths/regexes.

To build/update the translations, use:

```
$ cd ievv_opensource/ievv_i18n_url/tests/ievv_i18n_url_testapp/
$ django-admin makemessages
... translate in locale/nb/LC_MESSAGES/django.po ...
... translate in locale/de/LC_MESSAGES/django.po ...
$ django-admin compilemessages
```