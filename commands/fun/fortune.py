fortune_list = [
    "✴️The luckiest ! You will happen something happy.",
    "✨Lucky, That's daily～.",
    "🟣Unlucky, I hope your luck will get better",
    "🥹Bad...  You will happen something bad..."
    ]

class fortune(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.tree.command(name="fortune", description="Tell your fortune")
async def fortune(interaction: discord.Interaction):
    fortune_result = random.choice(fortune_list)
    await interaction.response.send_message(f"{interaction.user}'s fortune is {fortune_result}")

async def setup(bot):
    await bot.add_cog(fortune(bot))