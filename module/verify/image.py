import discord
import asyncio
from captcha.image import ImageCaptcha
import random
import string

captcha_image = ImageCaptcha(width=280, height=90)

def code_generate():
    code_source = string.ascii_letters + string.digits
    return "".join(random.choice(code_source) for _ in range(7))



