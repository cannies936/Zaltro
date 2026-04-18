import discord
from discord import app_commands
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="/", intents=intents) 
tree = bot.tree

class PermCogApp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="disable_apps", description="外部アプリの使用権限を取り除きます")
    async def disable_apps(self, interaction: discord.Interaction):
        
        await interaction.response.send_message()

        for role in interaction.guild.roles:
            await edit(permissions=discord.Permissions(use_external_apps=False))

async def setup(bot):
    await bot.add_cog(PermCogApp(bot))
