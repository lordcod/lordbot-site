from .utils import set_cooldown


@set_cooldown(10, {})
async def get_bot_command_data(ipc_client):
    return await ipc_client.request("get_command_data")


@set_cooldown(10, 0)
async def get_bot_guilds_count(ipc_client):
    return await ipc_client.request("get_guilds_count")


async def get_command_from_lang(ipc_client, lang):
    commands = await get_bot_command_data(ipc_client)

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
