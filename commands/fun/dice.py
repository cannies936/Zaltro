class dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.tree.command(name="dice", description="roll the dice")
@app_commands.describe(sides="dice_notations")
async def dice(interaction: discord.Interaction, sides: int = 6):
    if sides < 2:
        await interaction.response.send_message("⚠️ You have to enter number more than 2", ephemeral=True)
        return

    result = random.randint(1, sides)
    await interaction.response.send_message(f"🎲 **{sides}dice_notations result:{result}**")

async def setup(bot):
    await bot.add_cog(dice(bot))