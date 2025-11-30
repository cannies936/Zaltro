import discord
import random
import re
import os
import asyncio
import glob
from discord.ext import commands
from discord import app_commands
from typing import Optional
from collections import defaultdict, deque
import time
import aiohttp
import commands

# ========================
# Google Apps Script URL
# ========================
GAS_URL = "https://script.google.com/macros/s/AKfycbwJ_NbRUEbmY43YYDQEUyX1uuJLXaiN00x23UMY7B3GKh6pzkRpEZMiV34FQEyJSf85/exec"  # ← 必ず自分のURLへ変更

# --- インテント設定（必須） ---
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True      # サーバー参加・退出イベント用
intents.members = True     # メンバー情報取得
intents.invites = True
intents.voice_sates = True

# Discordボット設定
bot = commands.Bot(command_prefix='/', intents=intents)

# コマンドツリー
tree = bot.tree


# ==============================================
# Google Apps Script へデータ送信する関数
# ==============================================
async def send_to_gas(payload: dict):
    async with aiohttp.ClientSession() as session:
        try:
            await session.post(GAS_URL, json=payload)
        except Exception as e:
            print(f"GAS送信エラー: {e}")


# ==============================================
# Bot がサーバーに参加した時
# ==============================================
@bot.event
async def on_guild_join(guild):
    payload = {
        "event": "join",
        "server_id": guild.id,
        "server_name": guild.name
    }
    await send_to_gas(payload)
    print(f"[JOIN] {guild.name} ({guild.id}) をGASへ送信")


# ==============================================
# Bot がサーバーから退出した時
# ==============================================
@bot.event
async def on_guild_remove(guild):
    payload = {
        "event": "leave",
        "server_id": guild.id,
        "server_name": guild.name
    }
    await send_to_gas(payload)
    print(f"[LEAVE] {guild.name} ({guild.id}) をGASへ送信")


# ==============================================
# Bot 準備完了イベント
# ==============================================
@bot.event
async def on_ready():
    await bot.tree.sync()
    if bot.user:
        print(f'{bot.user} としてログインしました！')
        print(f'Bot ID: {bot.user.id}')
        print('ボットが準備完了です！')

if __name__ == '__main__':
    # 環境変数からトークンを取得
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ DISCORD_BOT_TOKENが設定されていません")
        print("環境変数にDiscordボットのトークンを設定してください")
