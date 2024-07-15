from re import A
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

from modules.event.command_event import send_help, update_server_order, create_server_invite
from modules.event.vc_event import on_vc_join, on_vc_leave, on_vc_change

# env読み込み
load_dotenv()

# intent作成
intents:discord.Intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True
client:discord.Client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print('on_ready')
    await tree.sync()
    
@client.event
async def on_connect():
    print('on_connect.......')

@tree.command(name="help", description="サーバー表示順を更新します")
@app_commands.default_permissions(administrator=True)
async def up(inter:discord.Interaction):
    await send_help(inter)    

@tree.command(name="up", description="サーバー表示順を更新します")
@app_commands.default_permissions(administrator=True)
async def up(inter:discord.Interaction):
    await update_server_order(inter)

@tree.command(name="invite", description="招待リンクを指定のチャンネルに設定します")
@app_commands.default_permissions(administrator=True)
async def invite(inter:discord.Interaction):
    await create_server_invite(inter)
    
@client.event
async def on_voice_state_update(member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
    if before.channel == after.channel:
        return
    if before.channel == None and after.channel != None:
        await on_vc_join(member, before, after)
    if before.channel != None and after.channel == None:
        await on_vc_leave(member, before, after)
    if before.channel != None and after.channel != None:
        await on_vc_change(member, before, after)    

# botを接続
client.run(os.getenv("DISCORD_TOKEN"))