import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class AdminGroup(app_commands.Group, name="admin"):
    @app_commands.command(name="leave", description="Botを脱退させます")
    @app_commands.describe(guild_id="脱退させるサーバーのID")
    async def leave(self, interaction: discord.Interaction, guild_id: str):
        load_dotenv()
        developer_id = int(os.getenv('DEVELOPER_ID'))
        guild = self.interaction.client.get_guild(int(guild_id))
        if interaction.user.id != developer_id:
            embed = discord.Embed(title="❌エラー", description="このコマンドは開発者専用です")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:   
            await guild.leave()
            embed = discord.Embed(title="", description="{guild.name}({guild_id})から脱退しました")
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="servers", description="サーバー一覧を書いたファイルを更新します")
    async def servers(self, interaction: discord.Interaction):
        load_dotenv()
        developer_id = int(os.getenv('DEVELOPER_ID'))
        if interaction.user.id != developer_id:
            embed = discord.Embed(title="❌エラー", description="このコマンドは開発者専用です")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else: 
            await interaction.response.defer(ephemeral=True)
            with open("servers.txt", "w", encoding="utf-8") as f:
                for guild in interaction.client.guilds:
                    f.write(f"サーバー名: {guild.name} (ID: {guild.id})\n")
            embed = discord.Embed(title="", description="更新しました")
            await interaction.followup.send(embed=embed)
    @app_commands.command(name="sync", description="コマンドを同期させます")
    async def sync(self, interaction: discord.Interaction):
        await interaction.client.tree.sync()
        embed = discord.Embed(title="", description="コマンドを同期しました")
        await interaction.response.send_message(embed=embed, ephemeral=True)

# 2. 通常通りCogを作成し、グループインスタンスを保持またはclass内で宣言する
class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # グループをCogに紐付ける場合
        self.group = AdminGroup()

async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))
    bot.tree.add_command(cog.group)
