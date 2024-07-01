from nextcord.ext import ipc
from flask import Flask

from .api import get_bot_command_data, get_bot_guilds_count, get_command_from_lang


app = Flask(__name__)
ipc_client = ipc.Client(host="localhost", secret_key="my_secret_key")

global_token = 'HyZB2UIvZwejO7XRY9n7GZ9YISzw6qMNEz386dKbdY0'


@app.route('/.well-known/acme-challenge/<local_token>')
def handle_token(local_token):
    return local_token + '.' + global_token


@app.route('/guilds-count')
async def handle_guilds_count():
    gc = await get_bot_guilds_count(ipc_client)
    return str(gc)


@app.route('/command_data')
def handle_command_data():
    return get_bot_command_data(ipc_client)


@app.route('/command_data/<lang>')
def handle_command_data_lang(lang):
    return get_command_from_lang(ipc_client, lang)


if __name__ == "__main__":
    app.run(debug=True)
