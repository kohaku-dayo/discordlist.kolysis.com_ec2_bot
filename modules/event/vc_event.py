import discord
import requests
import time
import json
from ..func.exception_func import exception_process
from ..env import base_url

memberVCLog:dict = {}

async def on_vc_join(member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
    create_tmp_vc_log(member)
    await incrementCurrentActiveUsers(member)

async def on_vc_change(member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
    await post_vc_log(member)
    create_tmp_vc_log(member)

async def on_vc_leave(member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
    await post_vc_log(member)
    await decrementCurrentActiveUsers(member)

def create_tmp_vc_log(member: discord.Member):
    global memberVCLog
    memberVCLog[member.id] = int(time.time())    

async def post_vc_log(member: discord.Member):
    global memberVCLog
    createVCLogRequest = requests.post(
        f'{base_url}/vc_log',
        data = json.dumps({
            "server_id": f'{member.guild.id}',
            "member_id": f'{member.id}',
            "start_epoch": f'{memberVCLog[member.id]}',
            "interval_sec": f'{int(time.time()) - memberVCLog[member.id]}'
            })
        )
    await exception_process(
        createVCLogRequest,
        "create vc log process succeed.",
        "create vc log process failed.",
        )
    del memberVCLog[member.id]
    
async def incrementCurrentActiveUsers(member: discord.Member):
    incrementCurrentActiveUsersResponse = requests.patch(f'{base_url}/server/{member.guild.id}/current_active_users/increment')
    #########作業予定#########
    #### exception_processを挟んで、decrementが実装できない理由を探す。
    await exception_process(
        incrementCurrentActiveUsersResponse,
        "increment current active users succeed",
        "increment current active users failed"
        )

async def decrementCurrentActiveUsers(member: discord.Member):
    decrementCurrentActiveUsersResponse = requests.patch(f'{base_url}/server/{member.guild.id}/current_active_users/decrement')
    
    await exception_process(
        decrementCurrentActiveUsersResponse,
        "decrement current active users succeed",
        "decrement current active users failed"
        )