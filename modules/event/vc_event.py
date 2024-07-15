import discord
import requests
import time
import json
from ..func.exception_func import exception_process
from ..env import base_url

memberVCLog:dict = {}

async def on_vc_join(member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
    create_tmp_vc_log(member)
    incrementCurrentActiveUsers(member)

async def on_vc_change(member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
    await post_vc_log(member)
    create_tmp_vc_log(member)

async def on_vc_leave(member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
    await post_vc_log(member)
    decrementCurrentActiveUsers(member)

def create_tmp_vc_log(member):
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
    
def incrementCurrentActiveUsers(member: discord.Member):
    requests.patch(f'{base_url}/server/{member.guild.id}/current_active_users/increment')

def decrementCurrentActiveUsers(member: discord.Member):
    requests.patch(f'{base_url}/server/{member.guild.id}/current_active_users/decrement')
    