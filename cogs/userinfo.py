import discord
from discord.ext import commands
import asyncio
from discord import app_commands

class UserinfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="userinfo",description="ユーザー情報を取得します")
    @app_commands.describe(user="調べたいユーザー(値がない場合は自分自身)")
    async def userinfo(self, interaction: discord.Interaction, user: discord.User = None):
      
