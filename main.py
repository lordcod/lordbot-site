import logging
from fastapi import FastAPI, Request, Response
import orjson
from uvicorn import Config, Server


from . import api
from .api import get_bot_command_data, get_bot_guilds_count, get_command_from_lang

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
global_token = 'HyZB2UIvZwejO7XRY9n7GZ9YISzw6qMNEz386dKbdY0'
secret_token = 'DE05EbFbe596F5ce3E6e707ec'


@app.post('/post-api-config/{password}')
async def handle_api_token(request: Request, password: str):
    if password != secret_token:
        return Response(status_code=401)
    try:
        json = await request.json()
        api.api_url = json['url']
        api.password = json['password']
    except Exception:
        return Response(status_code=400)
    return Response(status_code=204)


@app.get('/.well-known/acme-challenge/{local_token}')
async def handle_token(local_token: str):
    return local_token + '.' + global_token


@app.get('/guilds-count')
async def handle_guilds_count():
    gc = await get_bot_guilds_count()
    return str(gc)


@app.get('/command_data')
async def handle_command_data():
    result = await get_bot_command_data()
    return orjson.dumps(result).decode()


@app.get('/command_data/{lang}')
async def handle_command_data_lang(lang: str):
    result = await get_command_from_lang(lang)
    return orjson.dumps(result).decode()


if __name__ == "__main__":
    config = Config(app, "0.0.0.0", 8000, log_config=None,
                    log_level=logging.CRITICAL)
    server = Server(config)
    server.run()
