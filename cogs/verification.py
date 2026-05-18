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