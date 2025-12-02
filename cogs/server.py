DEVELOPER_ID = 1362035197255749884  

class server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.tree.command(name="servers", description=("check server bot joins")
async def servers(interaction: discord.Interaction):

    if interaction.user.id != DEVELOPER_ID:
        return await interaction.response.send_message(
            "❌ This command can be used by developer",
            ephemeral=True)

    guilds = bot.guilds
    description = ""

    for guild in guilds:
        description += (
            f"📌 **{guild.name}**\n"
            f"　🆔 Server ID: `{guild.id}`\n"
            f"　👥 Membercount: {guild.member_count}\n\n"
        )

    embed = discord.Embed(
        title="🤖 Server joined bot",
        description=description if description else "This bot doesn't join",
        color=0x00aaff
    )

    await interaction.response.send_message(embed=embed)

    await guild.leave()

    await interaction.response.send_message(
        f"👋 Bot left from server **{guild.name}**（ID: `{guild.id}`） ",
        ephemeral=True

async def setup(bot):
    await bot.add_cog(server(bot))    
