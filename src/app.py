import json
import os
from flask import Flask, request , render_template
import argostranslate.package, argostranslate.translate, argostranslate

app = Flask(__name__)

@app.route('/')  
def index():                        
    return render_template('index.html') 

@app.route('/translate-api', methods=['GET', 'POST'])
def translate(): 

    if request.json is None:
        return 'error: must include json in request', 400

    print('request jsoooon')
    print(request.json)
    
    for k in ['from', 'to', 'from_text', 'id']:
        if k not in request.json:
            print(k, 'not found in json')
            return f'error: missing {k} in json', 400

    _from = request.json['from']   
    to = request.json['to']
    
    installed_languages = argostranslate.translate.get_installed_languages()
    
    if not {_from, to} & {l.code for l in installed_languages}:
        return 'language not available :\'-( ', 400  # TODO: language not found, bucket request

    from_lang = list(filter(lambda x: x.code == _from, installed_languages))[0]
    to_lang = list(filter(lambda x: x.code == to, installed_languages))[0]

    translation = from_lang.get_translation(to_lang)
    
    return json.dumps({
        "to_text" : translation.translate(request.json['from_text']),
        "id" : int(request.json['id'])  
    })
