import discord
import asyncio
from captcha.image import ImageCaptcha
import random
import string
import io

captcha_image = ImageCaptcha(width=280, height=90)

def code_generate():
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(7))

class ImageView(discord.ui.View):
    def __init__(self, role: discord.Role):
        self.role = role
        super().__init__(timeout=0)
    @discord.ui.button(label="認証する", style=discord.ButtonStyle.green, custom_id="image")
    async def image(self, interaction: discord.Interaction, button: discord.ui.Button):
        captcha_source = [code_generate() for _ in range(5)]
        captcha_code = random.choice(captcha_source)
        random.shuffle(captcha_source)
        image = captcha_image.generate(captcha_code)
        image_bytes = io.BytesIO(image.read())
        file = discord.File(fp=image_bytes, filename="captcha.png")
        select_menu = discord.ui.Select(placeholder="画像に書かれた文字を選択してください", min_values=1, max_values=1, options=[discord.SelectOption(label=option, value=option) for option in captcha_source], custom_id="captcha_image")
        async def select_callback(select_interaction: discord.Interaction):
            choice = select_menu.values[0]
            if choice == captcha_code:
                try:
                    if self.role in select_interaction.user.roles:
                        embed = discord.Embed(title="❌エラー", description="認証に失敗しました: 既に認証済みです", color=discord.Color.red())
                        await select_interaction.response.send_message(embed=embed, ephemeral=True) 
                    else:
                        await select_interaction.user.add_roles(self.role, reason="Zaltro画像認証")
                        embed = discord.Embed(title="", description="✅認証しました", color=discord.Color.green())
                        await select_interaction.response.send_message(embed=embed, ephemeral=True)
                except discord.Forbidden:
                    embed = discord.Embed(title="❌エラー", description="認証に失敗しました: BOTに適切な権限がないかロールがBOTよりも上にあります", color=discord.Color.red())
                    await select_interaction.response.send_message(embed=embed, ephemeral=True)
        select_menu.callback = select_callback
        view = discord.ui.View(timeout=0)
        view.add_item(select_menu)
        embed = discord.Embed(title="", description="以下の指示に従ってください", color=discord.Color.green())
        embed.set_image(url="attachment://captcha.png")
        await interaction.response.send_message(embed=embed, file=file, view=view, ephemeral=True)
