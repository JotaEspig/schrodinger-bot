import json


with open('config.json', 'r') as file:
    config = json.load(file)
    TOKEN, PREFIX, DB_USER, DB_PASSWD = config['token'], config['prefix'], config['dbuser'], config['dbpassword']
