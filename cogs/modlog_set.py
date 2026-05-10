import discord
from app_commands import discord
from discord.ext import commands
import asyncio
from timedate import timedelta

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
    async def modlog_set(self, interaction: discord.Interaction, channel: discord.TextChannel):
        interaction.response.send_message(f"{channel.mention}にログを送信するようにしました")

        @commands.Cog.listener()
        async def on_member_remove(self, member: discord.Member):
            try:    
                audit_log = async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
                embed = discord.Embed(title="Member Kick", color=0x2AC11C)
                embed.add_field(name=f"Target", value=f"{member.mention}", inline=False)
                embed.add_field(name=f"Moderator", value=f"{entry.user.mention}", inline=False)
                embed.add_field(name=f"Reason", value=f"{entry.reason}", inline=False)
                await channel.send(embed=embed)
           except: discord.DiscordException:
                pass
           except: Exception:
                pass

        @commands.Cog.listener()
        async def on_member_ban(self, member: discord.User):
            try:    
                audit_log = async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                embed = discord.Embed(title="Member Ban", color=0x2AC11C)
                embed.add_field(name=f"Target", value=f"{member.mention}", inline=False)
                embed.add_field(name=f"Moderator", value=f"{entry.user.mention}", inline=False)
                embed.add_field(name=f"Reason", value=f"{entry.reason}", inline=False)
                await channel.send(embed=embed)
           except: discord.DiscordException:
                pass
           except: Exception:
                pass

        @commands.Cog.listener()
        async def on_member_update(before, after):
            try:    
                duration = after.timed_out_until - before.timed_out_until
                duration = datetime.timedelta(duration)
                audit_log = async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.):
                embed = discord.Embed(title="Member Ban", color=0x2AC11C)
                embed.add_field(name=f"Target", value=f"{after.name.mention}", inline=False)
                embed.add_field(name=f"Duration", value=f"{duration}", inline=False)
                embed.add_field(name=f"Moderator", value=f"{entry.user.mention}", inline=False)
                embed.add_field(name=f"Reason", value=f"{entry.reason}", inline=False)
                await channel.send(embed=embed)
           except: discord.DiscordException:
                pass
           except: Exception:
                pass

async def setup(bot):
    await bot.add_cog(ModlogCog(bot))
