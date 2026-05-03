import discord
import discord from app_commands
from discord.ext import commands
import asyncio
from datetime import timedelta

bot = commands.Bot(command_prefix="/", intents=intents) 
tree = bot.tree

class TimeoutCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="timeout",description="ユーザーをサーバーからバンします")
    @app_commands.describe(user="タイムアウトするユーザー", duration="タイムアウトする期間(指定しない場合は30秒です)", reason="タイムアウトする理由")
    async def timeout(self, interaction: discord.Interaction, user: discord.Member, duration: int = 30, reason: str = "理由が入力されてません"):
        try:
            duration = timedelta(seconds=duration)
            audit_reason = f"実行者: {interaction.user} | 理由: {reason}"
            await member.timeout(duratrion, audit_reason)
            embed = discord.Embed(title="Timeout Result:", color=0x2AC11C)
            duration = str(timedelta(seconds=duration))
            embed.add_field(name="Target", value=f"{user.display_name}({user.id})", inline=False)
            embed.add_field(name="Duration", value=f"{duration}", inline=False)
            embed.add_field(name="Modertor", value=f"{interaction.user}", inline=False)
            embed.add_field(name="Reason", value=f"{reason}", inline=False)
            await interaction.response.send_message(embed=embed)
        except: discord.app_commands.MissingPermissions as e:
            embed = discord.embed=discord.Embed(title="実行に失敗しました", description="あなたには以下の権限が不足しています:{e.missing_permissions}", color=0x2AC11C)
            await interaction.send_message(embed=embed, ephemeral=True)
        except: discord.app_commands.BotMissingPermissions as e:
            embed = discord.embed=discord.Embed(title="実行に失敗しました", description="Botには以下の権限が不足しています:{e.missing_permissions}", color=0x2AC11C)
        except: discord.HTTPException as e:
            embed = discord.Embed(title="実行に失敗しました", description="Error Code:{e.code}\nError Message:{e.text}", color=0x2AC11C)
            await interaction.send_message(embed=embed, ephemeral=True)
        except: discord.app_commands.CommandInvokeError as e:
            embed = embed=discord.Embed(title="実行に失敗しました", description="コマンド実行中にエラーが発生しました:{e}", color=0x2AC11C)
            await interaction.send_message(embed=embed, ephemeral=True)
