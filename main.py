import os 
import discord

for cog in os.listdir("app_package"):
    if cog.endswith(".py"):
        await bot.load_extension(f"app_package.{cog[:-3]}")

# もしくはasyncioのgather(体感速度は同じ)
asyncio.gather(*[bot.load_extension(f"app _package.{cog[:-3]}") for cog in os.listdir("app_package") if cog.endswith(".py")])

