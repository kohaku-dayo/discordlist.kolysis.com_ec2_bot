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
    
async def update_server_icon(guild:discord.Guild):
    requests.patch(
        f'{base_url}/server/{guild.id}',
        data = json.dumps({
            "icon": f'{guild.icon.key if guild.icon else None}'
            })
        );

async def update_server_name(guild:discord.Guild):
    requests.patch(
        f'{base_url}/server/{guild.id}',
        data = json.dumps({
            "name": f'{guild.name}',
            })
        );

