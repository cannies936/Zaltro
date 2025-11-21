@bot.tree.command(name="say", description="しゃべります")
@app_commands.describe(word="しゃべるワード")
async def say(interaction: discord.Interaction, word: str):
    await interaction.response.send_message(word)