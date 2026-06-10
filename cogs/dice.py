import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents) 
tree = bot.tree

class DiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
    
    @app_commands.command(name="dice",description="サイコロを振ります")
    @app_commands.check.cooldown(2, 60)
    async def dice(self, interaction: discord.Interaction):
      try:
          dice_notation = random.radint(1, 6)
          await interaction.response(f"🎲 サイコロの結果: **{dice_notation}**")
      except app_commands.CommandInvokeError as e:
          embed = discord.Embed(title="実行に失敗しました", description="コマンド実行中にエラーが発生しました:{e}", color=discord.Colour.red())
          await interaction.send_message(embed=embed, ephemeral=True)
      except app_commands.CommandOnCooldown as e:
          embed = discord.Embed(title="実行に失敗しました", description="実行してから1分間程度は使えません", color=discord.Colour.red())

async def setup(bot):
    await bot.add_cog(DiceCog(bot))
