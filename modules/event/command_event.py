from venv import logger
import discord
import requests
import json
import time
from ..func.exception_func import exception_process
from ..env import base_url

async def send_help(inter:discord.Interaction):
    print("[send_help] detected...")
    await inter.response.send_message("this feature is currently on development")
    pass

async def update_server_order(inter:discord.Interaction):
    await inter.response.defer()
    updateServerOrderResponse = requests.patch(
        f'{base_url}/server/{inter.guild.id}/updated_log',
        data = json.dumps({"updated_epoch": f'{int(time.time())}'})
        )

    try:
        updateServerOrderResponse.raise_for_status()
    except Exception as e:
        remainSecResult = int(e.response.text)
        remainHour = remainSecResult // 60 // 60
        remainMin = remainSecResult // 60 % 60
        remainSec = remainSecResult % 60
        remainSecText = ""
        if remainHour > 0:
            remainSecText += f'{remainHour}h '
        else:
            remainSecText += '0h '

        if remainMin > 0:
            remainSecText += f'{remainMin}m '
        else:
            remainSecText += '0m '
            
        if remainSec > 0:
            remainSecText += f'{remainSec}s'
        else:
            remainSecText += f'0s'

        await inter.followup.send(remainSecText)
        return

    vcMemberCounts = 0
    for member in inter.guild.members:
        if member.voice is not None:
            vcMemberCounts += 1

    updateServerCurrentActiveUsersResponse = requests.patch(
        f'{base_url}/server/{inter.guild.id}/current_active_users',
        data = json.dumps({"user_num": f'{vcMemberCounts}'})
        )

    await inter.followup.send("表示順の更新完了！")
    
async def create_server_invite(inter:discord.Interaction):
    await inter.response.defer()
    if inter.guild_id is None:
        await inter.response.send_message("this command is not allowed to use in DM")
        return

    vcMemberCounts = 0
    for member in inter.guild.members:
        if member.voice is not None:
            vcMemberCounts += 1

    updateServerCurrentActiveUsersResponse = requests.patch(
        f'{base_url}/server/{inter.guild.id}/current_active_users',
        data = json.dumps({"user_num": f'{vcMemberCounts}'})
        )

    await exception_process(
        updateServerCurrentActiveUsersResponse,
        "update server current active users number process successed.",
        "update server current active users number failed."
        )

    invite:discord.Invite = await inter.channel.create_invite(
        reason="dislist invitation created."
        )

    inviteURLUpdateResponse = requests.patch(
        f'{base_url}/server/{inter.guild.id}',
        data = json.dumps({"invite_url": f'{invite.url}'})
        )
    
    
    await exception_process(
        inviteURLUpdateResponse,
        "update server process successed.",
        "update server process failed."
        )
    
    await inter.followup.send("招待リンクの作成に成功しました！")