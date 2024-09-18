import contextlib
import os
from dotenv import load_dotenv
from typing import Dict, Optional
import aiohttp

load_dotenv()

api_url = ''
password = ''
cache: Dict[str, dict | list] = {}
NGROK_API_KEY = os.getenv('NGROK_API_KEY')


async def get_endpoint_url(session: aiohttp.ClientSession) -> Optional[str]:
    url = "https://api.ngrok.com/endpoints"
    headers = {
        "Authorization": f"Bearer {NGROK_API_KEY}",
        "Ngrok-Version": '2'
    }

    async with session.get(url, headers=headers) as response:
        response.raise_for_status()
        json = await response.json()
        with contextlib.suppress(KeyError, IndexError):
            return json['endpoints'][0]['public_url']


async def update_config(session: aiohttp.ClientSession) -> bool:
    url = await get_endpoint_url(session)

    print('Get endpoint url:', url)

    if url is None:
        return False

    async with session.post(url+'/update') as response:
        print(f'Get update status from {response.url}: {response.status}')
        if response.status == 204:
            return True
        else:
            return False


async def try_update_config(session: aiohttp.ClientSession) -> Optional[dict]:
    result = await update_config(session)
    if not result:
        return {
            'code': 401,
            'message': 'Authorization failed'
        }


async def send_request(session: aiohttp.ClientSession,  payload: dict, headers: dict) -> dict | bytes:
    endpoint = payload['endpoint']

    if not api_url or not password:
        error = await try_update_config(session)
        if error is not None:
            return error

    async with session.post(api_url, json=payload, headers=headers) as response:
        if response.status == 401 or response.status == 404:
            error = await try_update_config(session)
            if error is not None:
                return error

        if response.status == 429:
            if endpoint not in cache:
                data = {
                    'code': 429,
                    'message': 'There are too many requests. The caching state could not be saved.'
                }
            else:
                data = cache[endpoint]
            return data
        
        if not response.ok:
            return {
                'code': 500,
                'message': 'Authorization failed'
            }

        try:
            data = await response.json()
        except aiohttp.ContentTypeError:
            data = await response.read()

        print(data)
        print(response.status)
        cache[endpoint] = data
        return data


async def post_api(endpoint: str, data: dict = {}):
    session = aiohttp.ClientSession()

    payload = {
        'endpoint': endpoint,
        'data': data
    }
    headers = {
        'Authorization': password
    }
    data = await send_request(session, payload, headers)

    await session.close()

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
            "description": cmd['description'].get(lang),
            "brief_description": cmd['brief_description'].get(lang),
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
