import discord
from discord.ext import commands
from discord import app_commands
import random
import string
from captcha.image import ImageCaptcha
import asyncio
import pillow
from discord import ui

class AuthView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @ui.button(label="認証", style=discord.ButtonStyle.success)
    async def success_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("ボタンが押されました！", ephemeral=True)
