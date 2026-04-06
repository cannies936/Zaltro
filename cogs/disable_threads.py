import discord
from discord import app_commands
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="/", intents=intents) 
tree = bot.tree

class PermCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="disable_threads",description="特定のロールからスレッドの作成権限を取り除きます")
    @app_commands.describe(target_role="対象のロール")
    async def disable_threads(self, interaction: discord.Interaction, target_role: discord.Role):

        await interaction.response.send_message(
        embed=discord.Embed(description="実行中…",color=discord.Color.green()),ephemeral=True)

        changed = 0
        skipped = 0

        for channel in interaction.guild.channels:
            current = channel.overwrites_for(target_role)

            if current.create_private_threads is False and current.create_public_threads is False:
                skipped += 1
                continue

            current.create_public_threads = False
            current.create_private_threads = False

            try:
                await channel.set_permissions(target_role, overwrite=current)
                changed += 1
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"失敗: {channel.name} -> {e}")

        await interaction.edit_original_response(
            embed=discord.Embed(description=("完了しました\n\n"f"✅ 変更: {changed} チャンネル\n"f"⏭️ スキップ: {skipped} チャンネル"),
            color=discord.Color.green()))


async def setup(bot):
    await bot.add_cog(PermCog(bot))
