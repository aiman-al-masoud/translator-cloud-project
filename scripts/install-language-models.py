#!/bin/python3

import argostranslate.package, argostranslate.translate, argparse

# Download and install Argos Translate package
def install_languages(from_code, to_code):
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    available_package = list(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)[0]
    download_path = available_package.download()
    argostranslate.package.install_from_path(download_path)

# Translate
def translate_test(from_code, to_code, test_text):
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = list(filter(
        lambda x: x.code == from_code,
        installed_languages))[0]
    to_lang = list(filter(
        lambda x: x.code == to_code,
        installed_languages))[0]
    translation = from_lang.get_translation(to_lang)
    translatedText = translation.translate(test_text)
    print(translatedText)

def main():
    parser = argparse.ArgumentParser(description='Script useful to download and install Argos Translate package')
    parser.add_argument("--start", "-f", help="language to start with", required=True)
    parser.add_argument("--to", "-t", help="language in which I want to translate", required=True)
    parser.add_argument("--test_text", "-txt", help="text to test", required=True)

    args = parser.parse_args()
    install_languages(args.start, args.to)
    translate_test(args.start, args.to, args.test_text)

if __name__ == "__main__":
    main()
