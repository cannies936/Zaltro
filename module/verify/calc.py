import discord
import random

class CalcModal(discord.ui.Modal, title="以下の指示にしたがってください"):
   def _init_(self, num1: int, num2: int, role: discord.Role):
       self.num1 = num1
       self.num2 = num2
       self.role = role
  
   async def on_submit(self, interaction: discord.interact.Interaction, role: discord.Role):
        try:
            if self.answer == self.test.value:
                await interaction.user.add_roles(role, reason="Zaltro計算認証")
                embed = discord.Embed(title="", description="✅認証しました", color=discord.Color.green())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            elif role in interaction.user.role:
                embed = discord.Embed(title="❌認証に失敗しました", description="既に認証済みです", color=discord.Color.red())
            elif self.answer != self.test.value:
                embed = discord.Embed(title="❌認証に失敗しました", description="計算の答えが違います", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
       
class CalcView(discord.ui.View):
    def __init__(self, role):
        super().__init__(timeout=0)  # タイムアウト時間（秒）
    @discord.ui.button(label="認証する", style=discord.ButtonStyle.green, custom_id=nomal)
    async def calc(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CalcModal())
