import json
import os
from flask import Flask, request, render_template, abort
import argostranslate.package
import argostranslate.translate
import argostranslate
from flask_mysqldb import MySQL

app = Flask(__name__)  # init app

# database connection credentials
DB_CONFIG = os.path.join(app.root_path, 'config', 'db.json')
DB_DEFAULT_CONFIG = os.path.join(app.root_path, 'config', 'db-default.json')
LANGS = os.path.join(app.root_path, 'config', 'langs.json')
langs = json.loads(open(LANGS).read())

if os.path.exists(DB_CONFIG):
    config = json.loads(open(DB_CONFIG).read())
elif os.path.exists(DB_DEFAULT_CONFIG):
    config = json.loads(open(DB_DEFAULT_CONFIG).read())
else:
    print('Please add a DB config file in /src/config/db.json !')
    exit(1)

# connection with db
app.config.update(config)
mysql = MySQL(app)

def check_json(request):
    if request.json is None:
        return 'error: must include json in request', 400

    for k in ['from', 'to', 'from_text', 'id']:
        if k not in request.json:
            return f'error: missing {k} in json', 400

    if not request.json['from_text'].strip():
        return 'error: empty requested translation', 400

    return 1

@app.route('/')
def index():
    return render_template('index.html', langs=langs.items())

# display all records when the page "community" is loaded using the mysql's cursor for scrolling and fetching the records
@app.route('/community', methods=['GET', 'POST'])
def display_records():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute(
            ''' SELECT * FROM badTranslations ORDER BY complaints DESC LIMIT 2''')
        results = cursor.fetchall()
        return render_template('community.html', data=results)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/translate-api', methods=['GET', 'POST'])
def translate():

    if (check:=check_json(request)) != 1:
        return check

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


# query to the mysql db for storing the bad translation
@app.route('/query-db-api', methods=['POST', 'GET'])
def send_query():

    if (check:=check_json(request)) != 1:
        return check

    if request.method == 'POST':
        fromTag = request.json['from']
        toTag = request.json['to']
        from_text = request.json['from_text']
        to_text = request.json['to_text']
        _id = request.json['id']

        # avoiding to send the response with error 500 (since there is already an equal request saved in the database)
        # users will see "Thank you for your feedback" regardless
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO badTranslations VALUES(%s,%s,%s,%s,%s,1)''',
                           (fromTag, toTag, from_text, to_text, _id))
            mysql.connection.commit()
        except:
            cursor = mysql.connection.cursor()
            cursor.execute(''' UPDATE badTranslations SET complaints=complaints+1 WHERE id = (%s)''',
                           (_id,))  # do not remove "," which is needed to create a tuple
            mysql.connection.commit()
        finally:
            cursor.close()
            return ""

# query to the mysql db for storing the new possible better translations
@app.route('/query-db-api2', methods=['POST', 'GET'])
def send_query2():

    # if (check:=check_json(request)) != 1:
    #     return check

    if request.method == 'POST':
        from_text = request.json['from_text']
        to_text = request.json['to_text']
        second_id = request.json['secondid']
        fid = request.json['fid']

        # avoiding to send the response with error 500 (since there is already an equal request saved in the database)
        # users will see "Thank you for your feedback" regardless
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO possibleBetterTranslations VALUES(%s,%s,%s,%s,0)''',
                           (from_text, to_text, second_id, fid))
            mysql.connection.commit()
        except Exception as e:
            print(e)
            cursor = mysql.connection.cursor()
            cursor.execute(''' UPDATE possibleBetterTranslations SET votes=votes+1 WHERE secondid = (%s)''',
                           (second_id,))  # do not remove "," which is needed to create a tuple
            mysql.connection.commit()
        finally:
            cursor.close()
            return ""

# query to the mysql db for read the bad translations
@app.route('/query-db-api3', methods=['POST', 'GET'])
def send_query3():

    if request.method == 'POST':
        page =  request.json['page']

        try:
            cursor = mysql.connection.cursor()
            cursor.execute(''' SELECT * FROM badTranslations ORDER BY complaints DESC LIMIT 2 OFFSET %s''', (2*page,)) # multipled by 2
            data = cursor.fetchall()
        except Exception as e:
            print("ERROR: Query exception:", e)
        finally:
            cursor.close()
    
    return json.dumps(data)


# added for running the server directly with the run button
app.run(host='localhost', port=5000)
