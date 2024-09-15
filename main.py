import logging
import orjson
from flask import Flask, Response, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import api
from api import (get_bot_command_data, get_bot_guilds_count,
                 get_command_from_lang, get_command_from_cmd,
                 get_command_from_cmd_land)


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["3000 per day", "600 per hour", "30 per minute"]
)
global_token = 'HyZB2UIvZwejO7XRY9n7GZ9YISzw6qMNEz386dKbdY0'
secret_token = 'DE05EbFbe596F5ce3E6e707ec'

langs = ['en', 'ru', 'id', 'da', 'de', 'es', 'fr', 'pl', 'tr']


def handle_response(result: dict) -> Response:
    if 'code' in result:
        status = result['code']
    else:
        status = 200

    resp = Response(
        orjson.dumps(result),
        status=status,
        headers={
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        })
    return resp


@app.get('/api-config')
async def handle_get_api_token():
    if request.headers.get('Authorization') != secret_token:
        return Response(status=401)

    data = {
        'url': api.api_url,
        'password': api.password
    }
    return handle_response(data)


@app.post('/api-config')
async def handle_post_api_token():
    if request.headers.get('Authorization') != secret_token:
        return Response(status=401)

    try:
        json = request.json
        api.api_url = json['url']
        api.password = json['password']
    except Exception:
        return Response(status=400)
    return Response(status=204)


@app.get('/.well-known/acme-challenge/<local_token>')
async def handle_token(local_token: str):
    return local_token + '.' + global_token


@app.get('/guilds-count')
async def handle_guilds_count():
    result = await get_bot_guilds_count()
    return handle_response(result)


@app.get('/command_data')
async def handle_command_data():
    result = await get_bot_command_data()
    return handle_response(result)


@app.get('/command_data/<data>')
async def handle_comman_lang_or_cmd(data: str):
    if data in langs:
        result = await get_command_from_lang(data)
    else:
        result = await get_command_from_cmd(data)

    return handle_response(result)


@app.get('/command_data/<lang>/<cmd>')
async def handle_command_lang_cmd(lang: str, cmd: str):
    result = await get_command_from_cmd_land(lang, cmd)
    return handle_response(result)


@app.errorhandler(404)
def page_not_found(error):
    return handle_response({
        'code': 404,
        'message': 'the endpoint was not found'
    })


@app.errorhandler(429)
def page_client_error(error):
    return handle_response({
        'code': 429,
        'message': 'There are too many requests.'
    })


@app.errorhandler(500)
def page_server_error(error):
    return handle_response({
        'code': 500,
        'message': 'unexpected error'
    })


if __name__ == '__main__':
    app.run(port=5000)
