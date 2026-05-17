import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random

bot = commands.Bot(command_prefix="/", intents=intents) 
tree = bot.tree

class DiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
    
    @app_commands.command(name="dice",description="サイコロを振ります")
    async def dice(self, interaction: discord.Interaction):
      try:
          dice_notation = random.radint(1, 6)
          await interaction.response(f"🎲 サイコロの結果: **{dice_notation}**")
      except app_commands.CommandInvokeError as e:
          embed = embed=discord.Embed(title="実行に失敗しました", description="コマンド実行中にエラーが発生しました:{e}", color=discord.Colour.red())
          await interaction.send_message(embed=embed, ephemeral=True)
      
async def setup(bot):
    await bot.add_cog(DiceCog(bot))
