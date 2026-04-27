import discord
from discord.ext import commands
import asyncio

INITIAL_EXTENSIONS = [
    'cogs.ban',
    'cogs.kick',
    'cogs.unban'
]

intents = discord.Intents.default()

class MyBot(commands.Bot):
    async def load_extension():
        for cog in INITIAL_EXTENSIONS:
            await self.load_extension(cog)

bot = MyBot(command_prefix='/', intents=intents)

if __name__ == '__main__':
    # 環境変数からトークンを取得
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        await load_extension()
        bot.run(token)
    else:
        print("❌ DISCORD_BOT_TOKENが設定されていません")
        print("環境変数にDiscordボットのトークンを設定してください")
