import discord
import discord from app_commands
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix="/", intents=intents) 
tree = bot.tree

class KickCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        @app_commands.command(name="kick",description="ユーザーをサーバーからキックします")
        @app_commands.describe(user="キックするユーザー", reason="キックする理由")
        async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str)
                    await interaction.response.send_message(
        embed=discord.Embed(title="Kick Result:", description=f"Kick user:{display_name}", reason:color=discord.Color.green())
            
