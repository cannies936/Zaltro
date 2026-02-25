import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class GeneralCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

@app_commands.command(
    name="disable_apps",description="特定のロールから外部アプリの使用権限を取り除きます"
)
@app_commands.describe(target_role="対象のロール")
async def disable_apps(self, interaction: discord.Interaction, target_role: discord.Role):

    await interaction.response.send_message(
        embed=discord.Embed(
            description="実行中…",
            color=discord.Color.green()
        ),
        ephemeral=True
    )

    changed = 0
    skipped = 0

    for channel in interaction.guild.channels:
        current = channel.overwrites_for(target_role)

        if current.use_external_apps is False:
            skipped += 1
            continue

        current.use_external_apps = False

        try:
            await channel.set_permissions(target_role, overwrite=current)
            changed += 1
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"失敗: {channel.name} -> {e}")

    await interaction.edit_original_response(
        embed=discord.Embed(
            description=(
                "完了しました\n\n"
                f"✅ 変更: {changed} チャンネル\n"
                f"⏭️ スキップ: {skipped} チャンネル"
            ),
            color=discord.Color.green()
        )
    )