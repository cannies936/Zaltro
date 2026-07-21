import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name="ban",description="ユーザーをサーバーからバンします")
    @app_commands.describe(user="バンするユーザー", reason="バンする理由", days="削除する日数")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.User, days: int = 0, reason: str = "理由が入力されてません"):
        try:
            audit_reason = f"実行者: {interaction.user} | 理由: {reason}"     
            await interaction.guild.ban(user, reason=audit_reason, delete_message_days=days)
            embed = discord.Embed(title="Ban Result:", color=0x2AC11C)
            embed.add_field(name="Target", value=f"{user.display_name}({user.id})", inline=False)
            embed.add_field(name="Modertor", value=f"{interaction.user}", inline=False)
            embed.add_field(name="Reason", value=f"{audit_reason}", inline=False)
            await interaction.response.send_message(embed=embed)
        except app_commands.MissingPermissions:
            embed = discord.Embed(title="実行に失敗しました", description="あなたには以下の権限が不足しています:メンバーをバン", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)
        except app_commands.BotMissingPermissions:
            embed = discord.Embed(title="実行に失敗しました", description="Botには以下の権限が不足しています:メンバーをバン", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.HTTPException as e:
            embed = discord.Embed(title="実行に失敗しました", description=f"Error Code:{e.code}\nError Message:{e.text}", color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except app_commands.CommandInvokeError as e:
            embed = embed=discord.Embed(title="実行に失敗しました", description=f"コマンド実行中にエラーが発生しました:{e}", color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(BanCog(bot))
