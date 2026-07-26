import discord
from discord.ext import commands
from typing import Literal
from module.auth import nomal, calc, image

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name="ban",description="ユーザーをサーバーからバンします")
    @app_commands.describe(user="バンするユーザー", reason="バンする理由", days="削除する日数")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.User, days: int = 0, reason: str = "理由が入力されてません"):
