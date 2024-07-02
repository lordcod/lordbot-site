import logging
from flask import Flask, Response, request
import orjson


from . import api
from .api import get_bot_command_data, get_bot_guilds_count, get_command_from_lang

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
global_token = 'HyZB2UIvZwejO7XRY9n7GZ9YISzw6qMNEz386dKbdY0'
secret_token = 'DE05EbFbe596F5ce3E6e707ec'


@app.post('/post-api-config/<password>')
async def handle_api_token(password: str):
    if password != secret_token:
        return Response(status=401)
    try:
        json = request.json
        api.api_url = json['url']
        api.password = json['password']
    except Exception as exp:
        print(exp)
        return Response(status=400)
    return Response(status=204)


@app.get('/.well-known/acme-challenge/<local_token>')
async def handle_token(local_token: str):
    return local_token + '.' + global_token


@app.get('/guilds-count')
async def handle_guilds_count():
    gc = await get_bot_guilds_count()
    return gc


@app.get('/command_data')
async def handle_command_data():
    result = await get_bot_command_data()
    return result


@app.get('/command_data/<lang>')
async def handle_command_data_lang(lang: str):
    result = await get_command_from_lang(lang)
    return result

