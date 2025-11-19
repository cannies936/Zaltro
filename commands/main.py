import discord
import aiohttp
import asyncio

GAS_URL = "https://script.google.com/macros/s/xxxxxx/exec"  # ← ここにGASのURL

intents = discord.Intents.default()
intents.guilds = True

class MyBot(discord.Client):
    async def on_guild_join(self, guild):
        async with aiohttp.ClientSession() as session:
            payload = {
                "server_id": guild.id,
                "server_name": guild.name
            }
            await session.post(GAS_URL, json=payload)
        print(f"Sent guild info to GAS: {guild.name} ({guild.id})")

bot = MyBot(intents=intents)
bot.run("YOUR_BOT_TOKEN")