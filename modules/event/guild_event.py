import discord
import requests
import json
from ..env import base_url
from ..func.exception_func import exception_process

async def create_server(guild:discord.Guild):
    createServerRequest = requests.post(
        f'{base_url}/server',
        data = json.dumps({
            "id": f'{guild.id}',
            "name": f'{guild.name}',
            "icon": f'{guild.icon.key if guild.icon else None}'
            })
        );

    await exception_process(
        createServerRequest,
        "create server process succeed.",
        "create server process failed."
        )