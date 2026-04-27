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
    async def timeout(self, interaction: discord.Interaction, user: discord.Member, duration: datatime.timedelta = 30, reason: str = "理由が入力されてません"):
        duration = timedelta(seconds=duration)
        audit_reason = f"実行者: {interaction.user} | 理由: {reason}"
        await member.timeout(duratrion audit_reason)
        embed = discord.Embed(title="Timeout Result:", color=0x2AC11C)
        embed.add_field(name="Target", value=f"{user.display_name}({user.id})", inline=False)
        embed.add_field(name="Modertor", value=f"{interaction.user}", inline=False)
        embed.add_field(name="Reason", value=f"{reason}", inline=False)
                await interaction.response.send_message(embed=embed)
