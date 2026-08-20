import discord
from discord.ext import commands
import asyncio
from discord import app_commands
from typing import Literal
from module.verify import nomal, calc, image

class VerifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="verify",description="認証パネルを作成し、認証形式を設定します")
    @app_commands.describe(type="認証形式", role="認証ロール")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    async def verify(self, interaction: discord.Interaction, type: Literal["通常", "計算", "画像"], role: discord.Role):
        try:
            if type == "通常":
                result_embed = discord.Embed(title="✅", description="パネルが送信されました")
                embed = discord.Embed(title="認証パネル", description=f"<@&{role.id}>を貰うにはボタンを押して認証してください")
                view = nomal.NomalView(role)
                await interaction.response.send_message(embed=result_embed, ephemeral=True)
                await interaction.channel.send(embed=embed, view=view)
            elif type == "計算":
                result_embed = discord.Embed(title="✅", description="パネルが送信されました")
                embed = discord.Embed(title="認証パネル", description=f"<@&{role.id}>を貰うにはボタンを押して認証してください")
                view = calc.CalcView(role)
                await interaction.response.send_message(embed=result_embed, ephemeral=True)
                await interaction.channel.send(embed=embed, view=view)
            else:
                result_embed = discord.Embed(title="✅", description="パネルが送信されました")
                embed = discord.Embed(title="認証パネル", description=f"<@&{role.id}>を貰うにはボタンを押して認証してください")
                view = image.ImageView(role)
                await interaction.response.send_message(embed=result_embed, ephemeral=True)
                await interaction.channel.send(embed=embed, view=view)
        except Forbidden:
            embed = discord.Embed(title="❌エラー", description="権限が不足しています")
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(VerifyCog(bot))
    await bot.tree.sync()
            
        
