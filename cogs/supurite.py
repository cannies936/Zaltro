import discord
import discord from app_commands
from discord.ext import commands
import asyncio
import random

bot = commands.Bot(command_prefix="/", intents=intents) 
tree = bot.tree

class SupuriteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
    
    @app_commands.command(name="supurite",description="ランダムなスプライト画像を送信します")
    @app_commands.Cooldown(2, 60)
    async def supurite(self, interaction: discord.Interaction):
      try:
          files = [discord.File("images/sprite_bottle_1.png", filename="sprite_bottle_1.png"), discord.File("images/sprite_can_1.png", filename="sprite_can_1.png"), discord.File("images/sprite_image_3.jpg", filename="sprite_image_3.jpg")]
          sprite_file = random.choice(files)
          embed = discord.Embed(title="🥤 Sprite Random!", description="ランダムに選ばれたSprite画像です！")
          embed.set_image(url=f"attachment://{sprite_file.filename}")
          embed.set_footer(text=f"要求者: {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
          await interaction.response.send_message(embed=embed, file=sprite_file)
      except app_commands.CommandInvokeError as e:
          embed = embed=discord.Embed(title="実行に失敗しました", description="コマンド実行中にエラーが発生しました:{e}", color=discord.Colour.red())
          await interaction.responce.send_message(embed=embed, ephemeral=True)
      except app_commands.CommandOnCooldown as e:
          embed = discord.Embed(title="実行に失敗しました", description="実行してから1分間程度は使えません", color=discord.Colour.red())

async def setup(bot):
    await bot.add_cog(SupuriteCog(bot))
