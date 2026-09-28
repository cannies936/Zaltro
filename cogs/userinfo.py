import discord
from datetime import datetime
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
        join_identitifier = interaction.guild.get_member(user.id)
        embed = discord.Embed(title=f"👤 {user.global_name}のユーザー情報", color=0x2AC11C)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="📛 ユーザー名", value=f"{user.name}", inline=True)
        embed.add_field(name="🆔 ユーザーID", value=f"{user.id}", inline=True)
        embed.add_field(name="📝 ニックネーム", value=f"{user.display_name}", inline=True)
        if user.bot:
            type = "ボット"
        else:
            type = "ユーザー"
        embed.add_field(name="👥 アカウントの種類", value=f"{type}")
        embed.add_field(name="📅 アカウント作成日", value=user.created_at.strftime("%Y年%m月%d日 %H:%M"), inline=False)
        if not join_identitifier is None:
            embed.add_field(name="🚪 サーバー参加日", value=user.joined_at.strftime("%Y年%m月%d日 %H:%M"), inline=False)
            if join_identitifier.status == discord.Status.online:
                user_status = "🟢 オンライン"
            elif join_identitifier.status == discord.Status.idle:
                user_status = "🌙 退席中"
            elif join_identitifier.status == discord.Status.idle:
                user_status = "⛔️ 取り込み中"
            elif join_identitifier.status == discord.Status.offline:
                user_status = "🔘 オフライン"

            if join_identitifier.is_on_mobile:
                user_device = "📱 モバイル"
            elif not join_identitifier.is_on_mobile:
                user_device = "🌐・💻 Web/デスクトップ"
            else:
                user_device = "❓ 不明"
            status_set = f"{user_status}({user_device})"
            embed.add_field(name="📶 ステータス", value=f"{status_set}", inline=True)
            roles = [role for role in join_identitifier.roles]
            if roles:
                roles.sort(key=lambda x: x.position, reverse=True)
                role_total = [role.mention for role in roles]
            
            role_text = ", ".join(role_total)
            embed.add_field(name="🎭 所持ロール", value=f"{role_text}", inline=False)
        else:
            pass
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(UserinfoCog(bot))
