import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
INITIAL_EXTENSIONS = [
    'cogs.ban',
    'cogs.kick',
    'cogs.unban',
    'cogs.timeout',
    'cogs.untimeout',
    'cogs.dice',
    'cogs.modlog_set',
    'cogs.supurite'
]

intents = discord.Intents.default()

class Zaltro(commands.Bot):
    async def setup_hook(self):
        for cog in INITIAL_EXTENSIONS:
            await self.load_extension(cog)

bot = Zaltro(command_prefix='/', intents=intents)
load_dotenv()
if __name__ == '__main__':
    # 環境変数からトークンを取得
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        asyncio.run(setup_hook())
        bot.run(token)
    else:
        print("❌ DISCORD_BOT_TOKENが設定されていません")
        print("環境変数にDiscordボットのトークンを設定してください")
