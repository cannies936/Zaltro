import discord
import random

class CalcModal(discord.ui.Modal):
   def _init_(self, num1: int, num2: int, answer: int, role: discord.Role,  question_calc: str):
       self.answer = answer
       self.role = role
       super().__init__(title="以下の指示にしたがってください")
       self.question = discord.ui.TextInput(label="{question_calc}の答えを入力してください", placeholder="例: 15", required=True, max_length=3)
       self.add_item(self.question)
  
   async def on_submit(self, interaction: discord.interact.Interaction):
        try:
            if role in interaction.user.role:
                embed = discord.Embed(title="❌認証に失敗しました", description="既に認証済みです", color=discord.Color.red()) 
            elif self.answer != self.test.value:
                embed = discord.Embed(title="❌認証に失敗しました", description="計算の答えが違います", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            elif str(self.answer) == self.question.value:
                await interaction.user.add_roles(self.role, reason="Zaltro計算認証")
                embed = discord.Embed(title="", description="✅認証しました", color=discord.Color.green())
                await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(title="❌エラー", description="認証に失敗しました: BOTに適切な権限がないかロールがBOTよりも上にあります", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
       
class CalcView(discord.ui.View):
    def __init__(self, role: discord.Roles):
        self.role = role
        super().__init__(timeout=0)  # タイムアウト時間（秒）
    @discord.ui.button(label="認証する", style=discord.ButtonStyle.green, custom_id="calc")
    async def calc(self, interaction: discord.Interaction, button: discord.ui.Button):
       calc_prefix = random.randint(1, 3)
       if calc_prefix == 1:
          num1 = random.randint(0, 20)
          num2 = random.randint(0, 20)
          question_calc = f"{num1}+{num2}"
          answer = num1 + num2
       elif calc_prefix == 2:
          num1 = random.randint(0, 20)
          num2 = random.randint(0, 20)
          question_calc = f"{num1}-{num2}"
          answer = num1 - num2
       else:
          num1 = random.randint(0, 20)
          num2 = random.randint(0, 20)
          question_calc = f"{num1}×{num2}"
          answer = num1 * num2
       await interaction.response.send_modal(CalcModal(num1, num2, answer, self.role, question_calc))
