import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

class SyncCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
    @app_commands.command(name="sync", description="サーバーのコマンドを同期させます")
    async def servers(self, interaction: discord.Interaction):
        load_dotenv()
        developer_id = int(os.getenv('DEVELOPER_ID'))
        if interaction.user.id != developer_id:
            embed = discord.Embed(title="❌エラー", description="このコマンドは開発者専用です")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else: 
            await interaction.response.defer()
            await self.bot.tree.sync()
            embed = discord.Embed(title="同期完了", description="同期したコマンド数:{len(synced)}個")
            await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(SyncCog(bot))
