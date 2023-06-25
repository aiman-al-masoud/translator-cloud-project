# To run the tests in this file:
# 
# pytest name_of_file.py
#

import argostranslate
import argostranslate.package
import argostranslate.translate


def translate(_from, to, from_text, expected):

    installed_languages = argostranslate.translate.get_installed_languages()
    installed_lang_codes = {l.code for l in installed_languages}

    if _from not in installed_lang_codes:
        return False

    if to not in installed_lang_codes:
        return False

    from_lang = list(filter(lambda x: x.code == _from, installed_languages))[0]
    to_lang = list(filter(lambda x: x.code == to, installed_languages))[0]

    translation = from_lang.get_translation(to_lang)

    return translation.translate(from_text) == expected

    

def test_one():
    assert translate('it', 'en', 'ciao mondo', 'hello world')

def test_two():
    assert translate('en', 'it', 'hello world', 'ciao mondo')





