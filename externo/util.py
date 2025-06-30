import json

with open("config.json") as f:
    config = json.load(f)

senha = config["senha"]

EMAIL_USER = 'evellynfreitas@edu.unirio.br'
EMAIL_PASSWORD = senha