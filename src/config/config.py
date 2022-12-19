import os
import json
from dataclasses import dataclass

@dataclass
class Config:
    IP_gateway:str
    IP_translate:str
    IP_db_proxy:str
    IP_db:str
    neo4j_user:str
    neo4j_password:str
    neo4j_port:int
    db_proxy_port:int
    gateway_port:int
    translate_port:int

def getConfig(root:str)->Config:

    DB_CONFIG = os.path.join(root, '..', 'config', 'db.json')
    DB_DEFAULT_CONFIG = os.path.join(root, '..', 'config', 'db-default.json')

    if os.path.exists(DB_CONFIG):
        return Config(**json.loads(open(DB_CONFIG, 'r').read()))
    elif os.path.exists(DB_DEFAULT_CONFIG):
        return Config(**json.loads(open(DB_DEFAULT_CONFIG, 'r').read()))
    else:
        print('Please add a DB config file in /src/config/db.json !')
        exit(1)
