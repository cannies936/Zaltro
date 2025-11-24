@bot.tree.command(name="say", description="say something")
@app_commands.describe(word="word to say")
async def say(interaction: discord.Interaction, word: str):
    await interaction.response.send_message(word)