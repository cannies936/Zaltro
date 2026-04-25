import discord
import discord from app_commands
from discord.ext import commands
import asyncio
from datetime import timedelta

bot = commands.Bot(command_prefix="/", intents=intents) 
tree = bot.tree

class TimeoutCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="timeout",description="ユーザーをサーバーからバンします")
    @app_commands.describe(user="タイムアウトするユーザー", duration="タイムアウトする期間(指定しない場合は30秒です)", reason="タイムアウトする理由")
    async def timeout(self, interaction: discord.Interaction, user: discord.Member, duration: int = 30, reason: str = "理由が入力されてません"):
        td = timedelta(seconds=duration)
