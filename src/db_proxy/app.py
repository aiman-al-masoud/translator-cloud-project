import json
import os
from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)  # init app

# database connection credentials
DB_CONFIG = os.path.join(app.root_path,'..', 'config', 'db.json')
DB_DEFAULT_CONFIG = os.path.join(app.root_path, '..', 'config', 'db-default.json')

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
OFFSET = 2

def check_json(request):
    if request.json is None:
        return 'error: must include json in request', 400

    for k in ['from', 'to', 'from_text', 'id']:
        if k not in request.json:
            return f'error: missing {k} in json', 400

    if not request.json['from_text'].strip():
        return 'error: empty requested translation', 400

    return 1

@app.route('/insert-bad-translation', methods=['POST', 'GET'])
def insert_bad_translation():
    '''query to the mysql db for storing the bad translation'''

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

@app.route('/insert-possible-better-translation', methods=['POST', 'GET'])
def insert_possible_better_translation():

    '''query to the mysql db for storing the new possible better translations'''

    if request.method == 'POST':
        from_text = request.json['from_text']
        to_text = request.json['to_text']
        second_id = request.json['secondid']
        fid = request.json['fid']
        if(not from_text.strip() or not to_text.strip()):
            return "Empty from_text or to_text", 400

        # avoiding to send the response with error 500 (since there is already an equal request saved in the database)
        # users will see "Thank you for your feedback" regardless
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO possibleBetterTranslations VALUES(%s,%s,%s,%s,0,NOW())''',
                           (from_text, to_text, second_id, fid))
            mysql.connection.commit()
        except Exception as e:
            cursor = mysql.connection.cursor()
            cursor.execute(''' UPDATE possibleBetterTranslations SET votes=votes+1 WHERE secondid = (%s)''',
                           (second_id,))  # do not remove "," which is needed to create a tuple
            mysql.connection.commit()
        finally:
            cursor.close()
            return ""

@app.route('/read-bad-translations', methods=['POST', 'GET'])
def read_bad_translations():

    '''query to the mysql db to read the bad translations'''

    if request.method == 'POST':
        page =  request.json['page']

        try:
            cursor = mysql.connection.cursor()
            cursor.execute(''' SELECT * FROM badTranslations ORDER BY complaints DESC LIMIT %s OFFSET %s''', (OFFSET, OFFSET*page,)) # multipled by 2
            data = cursor.fetchall()
        except Exception as e:
            print("ERROR: Query exception:", e)
        finally:
            cursor.close()

    return json.dumps(data)

@app.route('/read-possible-better-translation-by-id', methods=['POST', 'GET'])
def read_possible_better_translation_by_id():

    '''return all the "possibleBetterTranslation" given the id of the specific text-translation'''

    if request.method == 'POST':
        id_prop =  request.json['id_prop']
        page =  request.json['page']

        try:
            cursor = mysql.connection.cursor()
            cursor.execute(''' SELECT from_text, to_text, secondid, fid, votes FROM possibleBetterTranslations WHERE fid = (%s) 
            ORDER BY votes DESC, timestamp LIMIT %s OFFSET %s''', (id_prop, OFFSET, OFFSET*page,))
            data = cursor.fetchall()
        except Exception as e:
            print("ERROR: Query exception:", e)
        finally:
            cursor.close()

    return json.dumps(data)

@app.route('/vote-possible-better-translation', methods=['POST', 'GET'])
def vote_possible_better_translation():

    '''query to the mysql db to vote a possible better translation'''

    if request.method == 'POST':
        second_id = request.json['secondid']
        operation = request.json["operation"]
        try:
            cursor = mysql.connection.cursor()

            cursor.execute(''' UPDATE possibleBetterTranslations SET votes=votes+(%s) WHERE secondid = (%s)''',
                           (operation,second_id,))  # do not remove "," which is needed to create a tuple
            mysql.connection.commit()
        except Exception as e:
            print("ERROR: Query votes exception:", e)
        finally:
            cursor.close()
            return ""

# added for running the server directly with the run button
app.run(host='localhost', port=8080)