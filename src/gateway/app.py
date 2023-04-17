# import json
# import os
# from flask import Flask, request, render_template
# import requests
# from flask_socketio import SocketIO
# from ..config.config import get_config

# app = Flask(__name__)  # init app
# LANGS = os.path.join(app.root_path, '..', 'config', 'langs.json')
# socketio = SocketIO(app,  cors_allowed_origins='*')
# langs = json.loads(open(LANGS, 'r').read())
# config = get_config(app.root_path)


# @app.route('/')
# def index():
#     return render_template('index.html', langs=langs.items())

# @app.route('/community', methods=['GET'])
# def display_records():
#     return render_template('community.html')

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/translate-api', methods=['GET', 'POST'])
# def translate():

#     res = requests.post(f'http://{config.IP_translate}:{config.translate_port}//translate-api', json=request.json) #TODO: extract IP
#     return json.dumps(res.json())

# @app.route('/query-db-api', methods=['POST', 'GET'])
# def send_query():

#     '''
#     Query the db for storing the bad translation
#     '''

#     res = requests.post(f'http://{config.IP_db_proxy}:{config.db_proxy_port}//insert-bad-translation', json=request.json) #TODO: extract IP
#     return json.dumps(res.json())

# @app.route('/query-db-api2', methods=['POST', 'GET'])
# def send_query2():

#     '''
#     Query the db for storing the new possible better translations
#     '''

#     res = requests.post(f'http://{config.IP_db_proxy}:{config.db_proxy_port}//insert-possible-better-translation', json=request.json) #TODO: extract IP
#     return json.dumps(res.json())

# @app.route('/query-db-api3', methods=['POST', 'GET'])
# def send_query3():

#     '''
#     Query the db for read the bad translations
#     '''

#     res = requests.post(f'http://{config.IP_db_proxy}:{config.db_proxy_port}//read-bad-translations', json=request.json) #TODO: extract IP
#     return json.dumps(res.json())

# @app.route('/query-db-api4', methods=['POST', 'GET'])
# def send_query4():

#     '''
#     Return all the "possibleBetterTranslation" given the id of the specific text-translation
#     '''

#     res = requests.post(f'http://{config.IP_db_proxy}:{config.db_proxy_port}//read-possible-better-translation-by-id', json=request.json) #TODO: extract IP
#     return json.dumps(res.json())

# @app.route('/query-db-api5', methods=['POST', 'GET'])
# def send_query5():

#     '''
#     Query the db to vote a possible better translation
#     '''

#     res = requests.post(f'http://{config.IP_db_proxy}:{config.db_proxy_port}//vote-possible-better-translation', json={**request.json, "ip":request.remote_addr}) 
#     json_string = json.dumps(res.json())
#     socketio.emit('votes-update', json_string, brodcast=True)
#     return json_string

# # run the server
# socketio.run(app, host=config.host, port=config.gateway_port)