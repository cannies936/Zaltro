import discord
from discord import app_commands
from discord.ext import commands

# 1. コマンドグループのクラスを作成
class AdminGroup(app_commands.Group, name="admin"):
    def _init_(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
    @app_commands.command(name="leave", description="Botを脱退させます")
    @app_commands.describe(guild_id="脱退させるサーバーのID")
    async def leave(self, interaction: discord.Interaction):
        guild = bot.get_guild(guild_id)
        if interaction.user.id == developer_id:
          embed = discord.Embed(title="❌エラー", description="このコマンドは開発者専用です")
          await interaction.response.send_message(embed=embed, ephemeral=True)
        else:   
          await guild.leave()
          embed = discord.Embed(title="", description="{guild.name}({guild_id})から脱退しました")
          await interaction.response.send_message(embed=embed, ephemeral=True)
    @app_commands.command(name="servers", description="サーバー一覧を書いたファイルを更新します")
    async def servers(interaction: discord.Interaction):
    if interaction.user.id == developer_id:
          embed = discord.Embed(title="❌エラー", description="このコマンドは開発者専用です")
          await interaction.response.send_message(embed=embed, ephemeral=True)
    else: 
          with open("servers.txt", "w", encoding="utf-8") as f:
          for guild in bot.guilds:
                f.write(f"サーバー名: {guild.name} (ID: {guild.id})\n")
          embed = discord.Embed(title="", description="更新しました")
          await interaction.response.send_message(embed=embed, ephemeral=True)

class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # 作成したグループをインスタンス化して追加
        self.group = AdminGroup()

    # cog_load でツリーに登録するパターン
    async def cog_load(self):
        self.bot.tree.add_command(self.group)

async def setup_hook(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))
