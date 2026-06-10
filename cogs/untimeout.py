import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import timedelta

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents) 
tree = bot.tree

class UntimeoutCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
    
    @app_commands.command(name="untimeout",description="ユーザーのタイムアウトを解除します")
    @app_commands.describe(user="タイムアウトを解除するユーザー", reason="タイムアウトを解除する理由")
    async def untimeout(self, interaction: discord.Interaction, user: discord.Member, reason: str = "理由が入力されてません"):
        try:    
            duration = timedelta(seconds=0)
            audit_reason = f"実行者: {interaction.user} | 理由: {reason}"
            await member.timeout(duratrion, audit_reason)
            embed = discord.Embed(title="Untimeout Result:", color=0x2AC11C)
            embed.add_field(name="Target", value=f"{user.display_name}({user.id})", inline=False)
            embed.add_field(name="Modertor", value=f"{interaction.user}", inline=False)
            embed.add_field(name="Reason", value=f"{reason}", inline=False)
            await interaction.response.send_message(embed=embed)
        except app_commands.MissingPermissions:
            embed = discord.Embed(title="実行に失敗しました", description="あなたには以下の権限が不足しています:メンバーの管理", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)
        except app_commands.BotMissingPermissions:
            embed = discord.Embed(title="実行に失敗しました", description="Botには以下の権限が不足しています:メンバーの管理", color=discord.Colour.red())
        except discord.HTTPException as e:
            embed = discord.Embed(title="実行に失敗しました", description="Error Code:{e.code}\nError Message:{e.text}", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)
        except app_commands.CommandInvokeError:
            embed = discord.Embed(title="実行に失敗しました", description="コマンド実行中にエラーが発生しました:{error}", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(UntimeoutCog(bot))
