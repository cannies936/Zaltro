import discord
import discord from app_commands
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix="/", intents=intents) 
tree = bot.tree

class KickCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.checks.bot_has_permissions(kick_members=True)
    @app_commands.command(name="kick",description="ユーザーをサーバーからキックします")
    @app_commands.describe(user="キックするユーザー", reason="キックする理由")
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "理由が入力されてません"):
        audit_reason = f"実行者: {interaction.user} | 理由: {reason}"     
        try:    
            await interaction.guild.kick(user, reason=audit_reason)
            embed=discord.Embed(title="Kick Result:", color=0x2AC11C)
            embed.add_field(name="Target", value=f"{user.display_name}({user.id})", inline=False)
            embed.add_field(name="Modertor", value="{interaction.user}", inline=False)
            embed.add_field(name="Reason", value="{audit_reason}", inline=False)
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

async def setup(bot):
    await bot.add_cog(KickCog(bot))
