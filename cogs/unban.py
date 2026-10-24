import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class UnbanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="unban",description="ユーザーのバンを解除します")
    @app_commands.describe(user="バンを解除するユーザー", reason="バンを解除する理由")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    
    async def unban(self, interaction: discord.Interaction, user: discord.User, reason: str = "理由が入力されてません"):
        audit_reason = f"実行者: {interaction.user} | 理由: {reason}"     
        await interaction.guild.unban(user, reason=audit_reason)
        embed = discord.Embed(title="Unban Result:", color=0x2AC11C)
        embed.add_field(name="Target", value=f"{user.display_name}({user.id})", inline=False)
        embed.add_field(name="Modertor", value=f"{interaction.user}", inline=False)
        embed.add_field(name="Reason", value=f"{reason}", inline=False)
        await interaction.response.send_message(embed=embed)
      
    @unban.error
    async def unban_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            embed = discord.Embed(title="実行に失敗しました", description="あなたには以下の権限が不足しています:メンバーをバン", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, app_commands.BotMissingPermissions):
            embed = discord.Embed(title="実行に失敗しました", description="Botには以下の権限が不足しています:メンバーをバン", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            embed = discord.Embed(title="実行に失敗しました", description="Error Code:{error.code}\nError Message:{error.text}", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="実行に失敗しました", description="コマンド実行中にエラーが発生しました:{error.original}", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(UnbanCog(bot))
