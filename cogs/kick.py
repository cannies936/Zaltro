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
        async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "理由が入力されてません")
            audit_reason = f"実行者: {interaction.user} | 理由: {reason}"     
            await interaction.guild.kick(user, reason=audit_reason)
            embed=discord.Embed(title="Kick Result:", color=2AC11C)
            embed.add_field(name="Kick user", value="{user.display_name}({user.id})", inline=False)
            embed.add_field(name="Modertor", value="", inline=False)
            embed.add_field(name="Reason", value="{audit_reason}", inline=False)
            await interaction.response.send_message(embed=embed)
            
async def setup(bot):
    await bot.add_cog(KickCog(bot))
