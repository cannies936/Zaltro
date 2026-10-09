import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class AppCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="disable_apps",description="外部アプリ対策をします")
    @app_commands.checks.has_permissions(administrator=True)
    async def disable_apps(self, interaction: discord.Interaction):
        excuted = bypass = 0
        everyone = interaction.guild.default_role
        try:
            embed = discord.Embed(title="実行中…", description="この操作は数分程度かかる場合があります...", color=0x2AC11C)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            for channel in interaction.guild.channels:
                overwrite = channel.overwrites_for(everyone)
                if overwrite.use_external_apps is not False:
                    overwrite.use_external_apps = False
                    await channel.set_permissions(everyone, overwrite=overwrite)
                    excuted = excuted + 1
                    await asyncio.sleep(2)
                else:
                    bypass = bypass + 1
                    pass
            embed = discord.Embed(title="✅ 実行中…", description=f"実行完了:{excuted}\nスキップ:{bypass}", color=0x2AC11C)
            await interaction.edit_original_response(embed=embed)
        except app_commands.MissingPermissions:
            embed = discord.Embed(title="実行に失敗しました", description="あなたには以下の権限が不足しています:管理者", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)
        except app_commands.BotMissingPermissions:
            embed = discord.Embed(title="実行に失敗しました", description="Botには以下の権限が不足しています:管理者", color=discord.Colour.red())
            await interaction.send_message(embed=embed, ephemeral=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.HTTPException as e:
            embed = discord.Embed(title="実行に失敗しました", description=f"Error Code:{e.code}\nError Message:{e.text}", color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except app_commands.CommandInvokeError as e:
            embed = embed=discord.Embed(title="実行に失敗しました", description=f"コマンド実行中にエラーが発生しました:{e}", color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AppCog(bot))
