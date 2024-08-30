from typing import Dict
import aiohttp


api_url = ''
password = ''
cache: Dict[str, dict | list] = {}


async def post_api(endpoint: str, data: dict = {}):
    if not api_url:
        return {
            'message': 'authorization failed',
            'code': 401
        }

    payload = {
        'endpoint': endpoint,
        'data': data
    }
    headers = {
        'Authorization': password
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json=payload, headers=headers) as response:

            if response.status == 401:
                return {
                    'code': 401,
                    'message': 'authorization failed'
                }

            if response.status == 429:
                if endpoint not in cache:
                    data = {
                        'code': 429,
                        'message': 'There are too many requests. The caching state could not be saved.'
                    }
                else:
                    data = cache[endpoint]
                return data

            try:
                data = await response.json()
            except aiohttp.ContentTypeError:
                data = await response.read()

            cache[endpoint] = data
            return data


def get_bot_guilds_count():
    return post_api('get_guilds_count')


def get_bot_command_data():
    return post_api('get_command_data')


async def get_command_from_lang(lang):
    commands = await get_bot_command_data()

    if 'code' in commands:
        return commands

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


async def get_command_from_cmd(cmd_name):
    commands = await get_bot_command_data()

    if 'code' in commands:
        return commands

    for cmd in commands:
        if cmd['name'] == cmd_name:
            return cmd
    else:
        return {'code': 404, 'message': 'the command was not found'}


async def get_command_from_cmd_land(lang, cmd_name):
    commands = await get_command_from_lang(lang)

    if 'code' in commands:
        return commands

    for cmd in commands:
        if cmd['name'] == cmd_name:
            return cmd
    else:
        return {'code': 404, 'message': 'the command was not found'}
