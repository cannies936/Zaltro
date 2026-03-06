import os 
import discord

for cog in os.listdir("app_package"):
    if cog.endswith(".py"):
        await bot.load_extension(f"app_package.{cog[:-3]}")

# もしくはasyncioのgather(体感速度は同じ)
asyncio.gather(*[bot.load_extension(f"app _package.{cog[:-3]}") for cog in os.listdir("app_package") if cog.endswith(".py")])

if __name__ == '__main__':
    # 環境変数からトークンを取得
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ DISCORD_BOT_TOKENが設定されていません")
        print("環境変数にDiscordボットのトークンを設定してください")
