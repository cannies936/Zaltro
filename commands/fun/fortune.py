fortune_list = [
    "✴️The luckiest ! You will happen something happy.",
    "✨Lucky, That's daily～.",
    "🟣Unlucky, I hope your luck will get better",
    "🥹Bad...  You will happen something bad..."
    ]

@bot.tree.command(name="fortune", description="Tell your fortune")
async def fortune(interaction: discord.Interaction):
    fortune_result = random.choice(fortune_list)
    await interaction.response.send_message(f"{interaction.user}'s fortune is {fortune_result}")