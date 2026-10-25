import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import timedelta

class TimeoutCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="timeout",description="ユーザーをタイムアウトします")
    @app_commands.describe(user="タイムアウトするユーザー", duration="タイムアウトする期間(指定しない場合は30秒です)", reason="タイムアウトする理由")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.checks.bot_has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, user: discord.Member, duration: int = 30, reason: str = "理由が入力されてません"):
        duration = timedelta(seconds=duration)
        audit_reason = f"実行者: {interaction.user} | 理由: {reason}"
        await user.timeout(duration, reason=audit_reason)
        embed = discord.Embed(title="Timeout Result:", color=0x2AC11C)
        embed.add_field(name="Target", value=f"{user.display_name}({user.id})", inline=False)
        embed.add_field(name="Duration", value=str(duration), inline=False)
        embed.add_field(name="Modertor", value=f"{interaction.user}", inline=False)
        embed.add_field(name="Reason", value=f"{reason}", inline=False)
        await interaction.response.send_message(embed=embed)
     
    @timeout.error
    async def timeout_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(title="実行に失敗しました", description="あなたには以下の権限が不足しています:メンバーをタイムアウト", color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, app_commands.BotMissingPermissions):
            embed = discord.Embed(title="実行に失敗しました", description="Botには以下の権限が不足しています:メンバーをタイムアウト", color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            embed = discord.Embed(title="実行に失敗しました", description=f"Error Code:{error.code}\nError Message:{error.text}", color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="実行に失敗しました", description=f"コマンド実行中にエラーが発生しました:{error.original}", color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(TimeoutCog(bot))
