import discord
from discord.ext import commands
import asyncio
from discord import app_commands

class UserinfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="userinfo",description="ユーザー情報を取得します")
    @app_commands.describe(user="調べたいユーザー(値がない場合は自分自身)")
    async def userinfo(self, interaction: discord.Interaction, user: discord.User = None):
        await interaction.response.defer()
        if user is None:
            user = interaction.user

        embed = discord.Embed(title=f"👤 {user.global_name}のユーザー情報", color=0x2AC11C)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="📛 ユーザー名", value=f"{user.name}", inline=True)
        embed.add_field(name="🆔 ユーザーID", value=f"{user.id}", inline=True)
        embed.add_field(name="📝 ニックネーム", value=f"{user.display_name}", inline=True)
        embed.add_field(name="📅 アカウント作成日", value=f"{user.created_at.strftime("%Y年%m月%d日 %H:%M")}", inline=True)
        if isinstance(user, discord.Member) == True:
            if user.status == discord.Status.online:
                user_status = "🟢 オンライン"
                if user.is_on_mobile == True:
                    user_device = "📱 モバイル"
                else:
                    user_device = "🌐・💻 Web/デスクトップ"
            elif user.status == discord.Status.idle:
                user_status = "🌙 退席中"
                if user.is_on_mobile == True:
                    user_device = "📱 モバイル"
                else:
                    user_device = "🌐・💻 Web/デスクトップ"
            elif user.status == discord.Status.idle:
                user_status = "⛔️ 取り込み中"
                if user.is_on_mobile == True:
                    user_device = "📱 モバイル"
                else:
                    user_device = "🌐・💻 Web/デスクトップ"
            elif user.status == discord.Status.offline:
                user_status = "🔘 オフライン"
                user_device = "❓ 不明"
        else:
            pass

        embed.add_field(name="📶 ステータス", value=f"{status_set}", inline=True)
