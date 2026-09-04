import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

class ServersCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
    @app_commands.command(name="servers", description="サーバー一覧を書いたファイルを更新します")
    async def servers(self, interaction: discord.Interaction):
        load_dotenv()
        developer_id = int(os.getenv('DEVELOPER_ID'))
        if interaction.user.id != developer_id:
            embed = discord.Embed(title="❌エラー", description="このコマンドは開発者専用です")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else: 
            await interaction.response.defer()
            with open("servers.txt", "w", encoding="utf-8") as f:
                for guild in self.bot.guilds:
                    f.write(f"サーバー名: {guild.name} (ID: {guild.id})\n")
            embed = discord.Embed(title="", description="更新しました")
            await interaction.response.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ServersCog(bot))
    await bot.tree.sync()
