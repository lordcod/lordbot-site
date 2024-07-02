import orjson
from utils import set_cooldown
import aiohttp

api_url = ''
password = ''

async def post_api(endpoint: str, data: dict = {}):
    payload = {
        'endpoint': endpoint,
        'data': data
    }
    headers = {
        'Authorization': password
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json=payload, headers=headers) as responce:
            text = await responce.read()
            try:
                return orjson.loads(text)
            except orjson.JSONDecodeError:
                return text

@set_cooldown(10, {})
def get_bot_command_data():
    return post_api('get_command_data')


@set_cooldown(10, 0)
def get_bot_guilds_count():
    return post_api('get_guilds_count')


async def get_command_from_lang(lang):
    commands = await get_bot_command_data()

    new_cmds_data = []

    for cmd in commands:
        arguments = []
        old_arguments = cmd['arguments']
        for arg in old_arguments:
            if isinstance(arg, dict):
                arguments.append(arg.get(lang))
            else:
                arguments.append(arg)

        examples = []
        for exp in cmd.get('examples', []):
            examples.append([exp[0], exp[1].get(lang)])

        new_cmds_data.append({
            "name": cmd['name'],
            "category": cmd['category'],
            "aliases": cmd['aliases'],
            "arguments": arguments,
            "examples": examples,
            "descriptrion": cmd['descriptrion'].get(lang),
            "brief_descriptrion": cmd['brief_descriptrion'].get(lang),
            "allowed_disabled": cmd['allowed_disabled']
        })

    return new_cmds_data
