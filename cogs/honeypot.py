import discord
from discord import app_commands
from discord.ext import commands
import asyncio

honeypot_list = []

class HoneypotGroup(app_commands.Group, name="honeypot"):
    @app_commands.command(name="add", description="指定したチャンネルをハニーポッドチャンネルから追加します")
    @app_commands.describe(channel="指定のチャンネル")
    async def add(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not channel.id in honeypot_list:
            honeypot_list.append(channel.id)
            embed = discord.Embed(title="ハニーポッドチャンネルに指定しました", description=f"<#{channel.id}>にメッセージを送ったユーザーは自動的にバンされます", color=0x2AC11C)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="ハニーポッドチャンネルに指定に失敗しました", description="このチャンネルは既に登録されています", color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
    @app_commands.command(name="remove", description="指定したチャンネルをハニーポッドチャンネルから削除します")
    @app_commands.describe(channel="指定のチャンネル")
    async def remove(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if channel.id in honeypot_list: 
            honeypot_list.remove(channel.id)
            embed = discord.Embed(title="ハニーポッドチャンネルを削除しました", description=f"<#{channel.id}>にメッセージを送ったユーザーは自動的にバンされることはありません", color=0x2AC11C)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="ハニーポッドチャンネルに指定に失敗しました", description="このチャンネルは既に登録されています", color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
    @app_commands.command(name="list", description="ハニーポッドチャンネルとして指定されているチャンネルの一覧を表示します")
    async def list(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if len(honeypot_list) == 0:
            embed = discord.Embed(title="実行に失敗しました", description="")
            await interaction.followup.send(embed=embed)
        else:
            channels = "\n".join([f"<#{channel_id}>" for channel_id in honeypot_list])
            embed = discord.Embed(title="ハニーポッドチャンネルの一覧", description=channels, color=0x2AC11C)
            await interaction.followup.send(embed=embed)

class HoneypotCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.group = HoneypotGroup()
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id in honeypot_list:
   	        permission = message.author.guild_permissions
            if permission.ban_members or message.author.bot:
                return
            else:
                await message.guild.ban(message.author, reason="ハニーポッドチャンネルでの投稿", delete_message_seconds=3600)

async def setup(bot: commands.Bot):
        cog = HoneypotCog(bot)
        await bot.add_cog(cog)
        bot.tree.add_command(cog.group)
