import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class KickCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.checks.bot_has_permissions(kick_members=True)
    @app_commands.command(name="kick",description="ユーザーをサーバーからキックします")
    @app_commands.describe(user="キックするユーザー", reason="キックする理由")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.bot_has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "理由が入力されてません"):
        audit_reason = f"実行者: {interaction.user} | 理由: {reason}"     
        await interaction.guild.kick(user, reason=audit_reason)
        embed = discord.Embed(title="Kick Result:", color=0x2AC11C)
        embed.add_field(name="Target", value=f"{user.display_name}({user.id})", inline=False)
        embed.add_field(name="Modertor", value="{interaction.user}", inline=False)
        embed.add_field(name="Reason", value="{reason}", inline=False)
        await interaction.response.send_message(embed=embed)
    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(app_commands.MissingPermissions):
            embed = discord.Embed(title="実行に失敗しました", description="あなたには以下の権限が不足しています:メンバーをキック", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, app_commands.BotMissingPermissions):
            embed = discord.Embed(title="実行に失敗しました", description="Botには以下の権限が不足しています:メンバーをキック", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            embed = discord.Embed(title="実行に失敗しました", description="Error Code:{error.code}\nError Message:{error.text}", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="実行に失敗しました", description="コマンド実行中にエラーが発生しました:{error.original}", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(KickCog(bot))
