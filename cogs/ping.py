class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.tree.command(name="ping", description="Botの応答時間を確認します")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")

async def setup(bot):
    await bot.add_cog(ping(bot))
