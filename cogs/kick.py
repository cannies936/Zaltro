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
                    embed=discord.Embed(title="Kick Result:", color=2AC11C)
                    embed.add_field(name="Kick user", value="undefined", inline=False)
                    embed.add_field(name="Reason", value="undefined", inline=False)
                    await interaction.responce.send_message(embed=embed)
            
