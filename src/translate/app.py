import json
import os
from flask import Flask, jsonify, request
import argostranslate.package
import argostranslate.translate
import argostranslate
from ..config.config import get_config
from flask_cors import CORS

app = Flask(__name__)  # init app
CORS(app)

LANGS = os.path.join(app.root_path, '..', 'config', 'langs.json')
langs = json.loads(open(LANGS).read())
config = get_config(app.root_path)

@app.route('/get-available-langs', methods=['GET', 'POST'])
def get_available_langs():
    return json.dumps(langs)


@app.route('/translate-api', methods=['GET', 'POST'])
def translate():

    _from = request.json['from']
    to = request.json['to']

    installed_languages = argostranslate.translate.get_installed_languages()
    installed_lang_codes = {l.code for l in installed_languages}

    if _from not in installed_lang_codes:
        # TODO: language not found, try requesting it from bucket
        return f'language "{_from}" not available :\'-(', 400

    if to not in installed_lang_codes:
        # TODO: language not found, try requesting it from bucket
        return f'language "{to}" not available :\'-(', 400

    from_lang = list(filter(lambda x: x.code == _from, installed_languages))[0]
    to_lang = list(filter(lambda x: x.code == to, installed_languages))[0]

    translation = from_lang.get_translation(to_lang)

    return json.dumps({
        'to_text': translation.translate(request.json['from_text']),
        'id': int(request.json['id'])
    })


health_status = True

@app.route('/health-check')
def health():
    if health_status:
        resp = jsonify(health="healthy")
        resp.status_code = 200
    else:
        resp = jsonify(health="unhealthy")
        resp.status_code = 500

    return resp

app.run(host=config.host, port=config.translate_port)  # run with config
