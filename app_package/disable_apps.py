from discord import app_commands
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.guilds = True
tree = bot.tree

@bot.tree.command(name="disable_apps", description="特定のロールから外部アプリの使用権限を取り除きます")
@app_commands.describe(target_role="対象のロール")
async def disable_apps(interaction: discord.Interaction, target_role: discord.Role):
    before_embed = discord.Embed(
        title="",
        description="実行中…",
        color=discord.Color.green() # 色の設定
    )
    await interaction.response.send_message(embed=before_embed, ephemeral=True)
    overwrite = discord.PermissionOverwrite()
    overwrite.use_external_apps = False
    for channel in interaction.guild.channels:
      await interaction.channel.set_permissions(target_role, overwrite=overwrite)
      await asyncio.sleep(2)
      if overwrite.use_external_apps == False:
          return
      after_embed = discord.Embed(
        title="",
        description="完了しました",
        color=discord.Color.green() # 色の設定
    )
    await interaction.edit_original_response(embed=after_embed, ephemeral=True)
