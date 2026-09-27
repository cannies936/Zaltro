import discord
from datetime import datetime
from discord.ext import commands
import asyncio
from discord import app_commands

class ServerinfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="serverinfo",description="サーバー情報を取得します")
    async def serverinfo(self, interaction: discord.Interaction):
        await interaction.response.defer()
        text_channels = len([c for c in guild.channels if isinstance(c, discord.TextChannel)])
        voice_channels = len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)])
        categories = len([c for c in guild.channels if isinstance(c, discord.CategoryChannel)])
        total_channels = len(guild.channels)
        role_count = len(guild.roles) - 1
        humans = len([m for m in guild.members if not m.bot])
        bots = len([m for m in guild.members if m.bot])
        online_members = len([m for m in guild.members if m.status == discord.Status.online])
        idle_members = len([m for m in guild.members if m.status == discord.Status.idle])
        dnd_members = len([m for m in guild.members if m.status == discord.Status.dnd])
        offline_members = len([m for m in guild.members if m.status == discord.Status.offline])
        embed = discord.Embed(title=f"📊 {interaction.guild.name}のサーバー情報", color=0x2AC11C)
        embed.set_thumbnail(url=interaction.guild.icon.url)
        embed.add_field(name="🆔 サーバーID", value=f"{interaction.guild.id}", inline=True)
        embed.add_field(name="👑 所有者", value=f"{interaction.guild.owner.mention}{interaction.guild.owner.name}(ID: {interaction.guild.owner.id})", inline=True)
        embed.add_field(name="📅 作成日", value=f"{interaction.guild.created_at.strftime("%Y年%m月%d日 %H:%M")}", inline=True)
        embed.add_field(name="👥 メンバー数", value=f"**総数**: {member_count}\n👤 人間: {humans}\n🤖 ボット: {bots}", inline=True)
        embed.add_field(name="📈 オンライン状況", value=f"🟢 オンライン: {online_members}\n🌙 退席中: {idle_members}\n⛔️ 取り込み中: {dnd_members}\n🔘️ オフライン: {dnd_members}", inline=True)
        embed.add_field(name="📺 チャンネル数", value=f"**総数**: {total_channels}\n💬 テキストチャンネル: {text_channels}\n🔊 ボイスチャンネル: {voice_channels}\n📂 カテゴリー: {categories}")
        embed.add_field(name="💎 ブースト",  value=f"{guild.premium_subscription_count or 0}ブースト(レベル{guild.premium_tier})")
        embed.add_field(name="🎭 ロール数", value=f"{role_count}", inline=True)
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(ServerinfoCog(bot))
