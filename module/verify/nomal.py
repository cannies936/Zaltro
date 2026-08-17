import discord
import asyncio

class NomalView(discord.ui.View):
    def __init__(self, role: discord.Role):
        self.role = role
        super().__init__(timeout=0)
    @discord.ui.button(label="認証する", style=discord.ButtonStyle.green, custom_id=nomal)
    async def nomal(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if role in interaction.user.roles:
                embed = discord.Embed(title="❌エラー", description="認証に失敗しました: 既に認証済みです", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
                interaction.user.add_roles(self.role, reason="Zaltro即時認証")
                embed = discord.Embed(title="", description="✅認証しました", color=discord.Color.green())
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except Forbidden:
            embed = discord.Embed(title="❌エラー", description="認証に失敗しました: BOTに適切な権限がないかロールがBOTよりも上にあります", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
