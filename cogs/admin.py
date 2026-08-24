import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

class LeaveCog(commands.Cog):
    def _init_(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
    @app_commands.command(name="leave", description="Botを脱退させます")
    @app_commands.describe(guild_id="脱退させるサーバーのID")
    async def leave(self, interaction: discord.Interaction, guild_id: int):
        load_dotenv()
        developer_id = os.getenv('DEVELOPER_ID')
        guild = bot.get_guild(guild_id)
        if interaction.user.id == developer_id:
            embed = discord.Embed(title="❌エラー", description="このコマンドは開発者専用です")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:   
            await guild.leave()
            embed = discord.Embed(title="", description="{guild.name}({guild_id})から脱退しました")
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(LeaveCog(bot))
    await bot.tree.sync()
