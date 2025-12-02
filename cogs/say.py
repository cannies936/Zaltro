class say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.tree.command(name="say", description="say something")
@app_commands.describe(word="word to say")
async def say(interaction: discord.Interaction, word: str):
    await interaction.response.send_message(word)

async def setup(bot):
    await bot.add_cog(say(bot))
