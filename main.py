import discord
from discord.ext import commands
import os
import asyncio

bot = commands.Bot(command_prefix='/', intents=intents)

class MyBot(commands.Bot):
    async def setup_hook(self):
        for cog in os.listdir("app_package"):
            if cog.endswith(".py"):
                await self.load_extension(f"app_package.{cog[:-3]}")

if __name__ == '__main__':
    # 環境変数からトークンを取得
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ DISCORD_BOT_TOKENが設定されていません")
        print("環境変数にDiscordボットのトークンを設定してください")
