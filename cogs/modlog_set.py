import discord
import discord from app_commands
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix="/", intents=intents) 
tree = bot.tree

class ModlogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name="modlog_set",description="モデレーションログをセットします")
    @app_commands.describe(channel="モデレーションログを送信するチャンネル")
    async def modlog_set(self, interaction: discord.Interaction, channel: discord.Channel):
        interaction.responce.send_message(f"<#{channel.id}>にログを送信するようにしました")

        @commands.Cog.listener()
        async def on_kick(self, member):
            try:    
                audit_log = async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
                embed = discord.Embed(title="Member Kick", color=0x2AC11C)
                embed.add_field(name=f"Target", value=f"{member.mention}", inline=False)
                embed.add_field(name=f"Moderator", value=f"{entry.user.mention}", inline=False)
                embed.add_field(name=f"Reason", value=f"{entry.reason}", inline=False)
                await channel.send(embed=embed)
           expect: discord.DiscordExpection:
                pass
           expect: Expection:
                pass


async def setup(bot):
    await bot.add_cog(ModlogCog(bot))
