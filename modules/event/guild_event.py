import discord
import requests
import json
from ..env import base_url
from ..func.exception_func import exception_process

async def join_server(guild:discord.Guild):
    joinServerRequest = requests.patch(
        f'{base_url}/server/{guild.id}/join',
        data = json.dumps({
            "name": f'{guild.name}',
            "icon": f'{guild.icon.key if guild.icon else None}',
            })
        );

    await exception_process(
        joinServerRequest,
        "join server process succeed.",
        "join server process failed."
        )

async def leave_server(guild:discord.Guild):
    leaveServerRequest = requests.patch(f'{base_url}/server/{guild.id}/leave');

    await exception_process(
        leaveServerRequest,
        "join server process succeed.",
        "join server process failed."
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

