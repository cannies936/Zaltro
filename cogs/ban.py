import discord
import discord from app_commands
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix="/", intents=intents) 
tree = bot.tree

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        @app_commands.command(name="ban",description="ユーザーをサーバーからバンします")
        @app_commands.describe(user="バンするユーザー", reason="バンする理由")
        async def kick(self, interaction: discord.Interaction, user: discord.User, reason: str = "理由が入力されてません")
            audit_reason = f"実行者: {interaction.user} | 理由: {reason}"     
            if isinstance(user, Member):
               await interaction.guild.ban(user, reason=audit_reason)
            else:
              user = get_user(user)
              await interaction.guild.ban(user, reason=audit_reason)
            embed=discord.Embed(title="Kick Result:", color=2AC11C)
            embed.add_field(name="Kick user", value="{user.display_name}({user.id})", inline=False)
            embed.add_field(name="Modertor", value="", inline=False)
            embed.add_field(name="Reason", value="{audit_reason}", inline=False)
            await interaction.response.send_message(embed=embed)
async def setup(bot):
    await bot.add_cog(BanCog(bot))
