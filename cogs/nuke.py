class nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.tree.command(name="nuke", description="Nuke this sevrer")   
async def nuke(interaction: discord.Interaction):
    await interaction.response.send_message(f"# This server has nuked ! https://tenor.com/bPrDD.gif")

async def setup(bot):
    await bot.add_cog(nuke(bot))
