import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random

class DiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="dice",description="サイコロを振ります")
    @app_commands.checks.cooldown(2, 60, key=lambda interaction: interaction.user.id)
    async def dice(self, interaction: discord.Interaction):
        dice_notation = random.randint(1, 6)
        await interaction.response.send_message(f"🎲 サイコロの結果: **{dice_notation}**")
    @dice.error
    async def dice_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError)
        if isinstance(error, app_commands.CommandInvokeError):
            embed = discord.Embed(title="実行に失敗しました", description=f"コマンドの実行に失敗しました:{error.text}", color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(title="実行に失敗しました", description=f"{error.retry_after}秒待機してください", color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(DiceCog(bot))
