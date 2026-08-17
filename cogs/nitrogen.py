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
    async def on_timeout(self):
        self.nitro.disabled = True
        embed = discord.Embed(title="あなたにNitroが贈呈されています！", description="どうやら期限が切れたようです...", color=discord.Colour.fuchsia())
        self.message.edit(embed=embed, view=self)
 
class NitroCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
    
    @app_commands.command(name="nitrogen",description="ニトロギフトを送ります")
    @app_commands.checks.cooldown(2, 60, type=discord.BucketType.user)
    async def nitrogen(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="あなたにNitroが贈呈されています！", description=f"{interaction.user}があなたたちにNitroを送りました！", color=discord.Colour.fuchsia())
            await interaction.response.send_message(embed=embed, view=NitroView())
        except app_commands.CommandOnCooldown:
          embed = discord.Embed(title="実行に失敗しました", description="実行してから1分間程度は使えません", color=discord.Colour.red())
          await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(NitroCog(bot))
