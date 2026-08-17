import discord
import asyncio
from discord import app_commands
from discord.ext import commands

class NitroView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
    @discord.ui.button(label="受け取る", style=discord.ButtonStyle.green, custom_id=nitro)
    async def nitro(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("https://klipy.com/gifs/never-gonna-give-you-up-4", ephemeral=True)

class NitroCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
    
    @app_commands.command(name="nitrogen",description="ニトロギフトを送ります")
    @app_commands.checks.cooldown(2, 60, type=discord.BucketType.user)
    async def nitrogen(self, interaction: discord.Interaction):
        embed = discord.Embed(title="あなたにNitroが贈呈されています！", description=f"{interaction.user}があなたたちにNitroを送りました！", color=discord.Colour.fuchsia())
        await interaction.response.send_message(embed=embed, view=NitroView())

async def setup(bot):
    await bot.add_cog(NitroCog(bot))
