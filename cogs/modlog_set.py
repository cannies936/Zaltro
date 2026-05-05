import discord
import discord from app_commands
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix="/", intents=intents) 
tree = bot.tree

class ModlogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name="modlog_set",description="モデレーションログをセットします")
    @app_commands.describe(channel="モデレーションログを送信するチャンネル")
    async def modlog_set(self, interaction: discord.Interaction, channel: discord.Channel):
        interaction.responce.send_message(f"<#{channel.id}>にログを送信するようにしました")

async def setup(bot):
    await bot.add_cog(ModlogCog(bot))
