import discord
from discord.ui import Button, View

class NomalView(discord.ui.View):
    def __init__(self, role):
        super().__init__(timeout=0)  # タイムアウト時間（秒）
        self.role = role
    @discord.ui.button(label="認証する", style=discord.ButtonStyle.green)
    async def my_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
      　    interaction.user.add_roles(role)
            embed = discord.Embed(title="", description="✅認証しました", color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Forbidden:
            embed = discord.Embed(title="❌エラー", description="認証に失敗しました: BOTに適切な権限がないかロールがBOTよりも上にあります", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
