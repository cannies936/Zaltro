class leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.tree.command(name="leave", description="Making bot left ")
@app_commands.describe(server_id="Server ID")
async def leave(interaction: discord.Interaction, server_id: str):

    # ✅ 開発者チェック
    if interaction.user.id != DEVELOPER_ID:
        return await interaction.response.send_message(
            "❌ This command can be used by developer",
            ephemeral=True
        )

    guild = bot.get_guild(int(server_id))
    if guild is None:
        return await interaction.response.send_message(
            f"⚠️ Not found",
            ephemeral=True
        )

    await guild.leave()

    await interaction.response.send_message(
        f"👋 Bot left from server **{guild.name}**（ID: `{guild.id}`） ",
        ephemeral=True
    )

async def setup(bot):
    await bot.add_cog(leave(bot))
