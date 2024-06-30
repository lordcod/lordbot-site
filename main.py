from nextcord.ext import ipc
from flask import Flask

from .api import get_bot_command_data, get_bot_guilds_count, get_command_from_lang

app = Flask(__name__)
ipc_client = ipc.Client(host="localhost", secret_key="my_secret_key")


@app.route('/guilds-count')
async def handle_guilds_count():
    gc = await get_bot_guilds_count()
    return str(gc)


@app.route('/command_data')
async def handle_command_data():
    commands = await get_bot_command_data()
    return commands


@app.route('/command_data/<lang>')
async def handle_command_data_lang(lang):
    commands = await get_command_from_lang(lang)
    return commands


if __name__ == "__main__":
    app.run(debug=True)
