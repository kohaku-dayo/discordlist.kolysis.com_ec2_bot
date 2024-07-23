import discord
import requests
import json
from ..env import base_url
from ..func.exception_func import exception_process
async def on_guild_join(guild:discord.Guild):
    createServerRequest = requests.post(
        f'{base_url}/server',
        data = json.dumps({
            "id": f'{guild.id}',
            "name": f'{guild.name}'
            })
        );

    await exception_process(
        createServerRequest,
        "create server process succeed.",
        "create server process failed."
        )