import discord
import discord from app_commands
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix="/", intents=intents) 
tree = bot.tree

class UnbanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="ban",description="ユーザーのバンを解除します")
    @app_commands.describe(user="バンを解除するユーザー", reason="バンする理由")
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason: str = "理由が入力されてません", days: int):
        try:
            audit_reason = f"実行者: {interaction.user} | 理由: {reason}"     
            if isinstance(user, Member):
                await interaction.guild.ban(user, reason=audit_reason, delete_message_days=days)
                embed = discord.Embed(title="Unban Result:", color=0x2AC11C)
            　　 embed.add_field(name="Target", value=f"{user.display_name}({user.id})", inline=False)
                embed.add_field(name="Modertor", value=f"{interaction.user}", inline=False)
                embed.add_field(name="Reason", value="{audit_reason}", inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                user = get_user(user)
                await interaction.guild.unban(user, reason=audit_reason)
            embed = discord.Embed(title="Kick Result:", color=0x2AC11C)
            embed.add_field(name="Target", value=f"{user.display_name}({user.id})", inline=False)
            embed.add_field(name="Modertor", value=f"{interaction.user}", inline=False)
            embed.add_field(name="Reason", value="{audit_reason}", inline=False)
            await interaction.response.send_message(embed=embed)
        except: discord.MissingPermissions as e:
            embed = discord.embed=discord.Embed(title="実行に失敗しました", description="Botの権限もしくは自身の権限を確認してください:{e}", color=0x2AC11C)
            await interaction.send_message(embed=embed, ephemeral=True)
        except: discord.HTTPException as e:
            embed = discord.Embed(title="実行に失敗しました", description="Error Code:{e.code}\nError Message:{e.text}", color=0x2AC11C)
            await interaction.send_message(embed=embed, ephemeral=True)
        except: discord.app_commands.CommandInvokeError as e:
            embed = embed=discord.Embed(title="実行に失敗しました", description="コマンド実行中にエラーが発生しました:{e}", color=0x2AC11C)
            await interaction.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(UnbanCog(bot))
