import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class PurgeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name="purge",description="メッセージを一括削除します")
    @app_commands.describe(amount="一括削除するメッセージ数", user="対象のユーザー", reason="一括削除した理由", ephemeral="表示するかどうか")
    @app_commands.checks.has_permissions(manage_messages=True, read_message_history=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True, read_message_history=True)
    async def purge(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100], user: discord.Member = None, reason: str = "理由が入力されてません", ephemeral: bool = True):
        try:
            await interaction.response.defer()
            audit_reason = f"実行者: {interaction.user} | 理由: {reason}"     
            await interaction.channel.purge(limit=amount, check=lambda message: message.author.id == user.id, reason=audit_reason)
            embed = discord.Embed(title="Purge Result:", color=0x2AC11C)
            embed.add_field(name="Channel", value=f"{interaction.channel}", inline=False)
            embed.add_field(name="Amount", value=f"{amount}", inline=False)
            embed.add_field(name="Modertor", value=f"{interaction.user}", inline=False)
            embed.add_field(name="Reason", value=f"{reason}", inline=False)
            await interaction.response.followup.send(embed=embed, ephemeral=ephemeral)
        except app_commands.MissingPermissions:
            embed = discord.Embed(title="実行に失敗しました", description="あなたには以下の権限が不足しています:メッセージの管理、メッセージ履歴を読む", color=discord.Colour.red())
            await interaction.response.followup.send(embed=embed, ephemeral=True)
        except app_commands.BotMissingPermissions:
            embed = discord.Embed(title="実行に失敗しました", description="Botには以下の権限が不足しています:メッセージの管理、メッセージ履歴を読む", color=discord.Colour.red())
            await interaction.response.followup.send(embed=embed, ephemeral=True)
        except discord.HTTPException as e:
            embed = discord.Embed(title="実行に失敗しました", description=f"Error Code:{e.code}\nError Message:{e.text}", color=discord.Colour.red())
            await interaction.response.followup.send(embed=embed, ephemeral=True)
        except app_commands.CommandInvokeError as e:
            embed = embed=discord.Embed(title="実行に失敗しました", description=f"コマンド実行中にエラーが発生しました:{e}", color=discord.Colour.red())
            await interaction.response.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(PurgeCog(bot))
