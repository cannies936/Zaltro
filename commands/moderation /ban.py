@bot.tree.command(name="ban", description="Ban user from server")
@app_commands.describe(user="User to ban", reason="reason")
async def ban(interaction: discord.Interaction, user: discord.User, reason: str = "No reason was given."):

 # 理由の長さ制限（Discord API制限対応）
    audit_reason = f"Ban performer: {interaction.user} | Reason: {reason}"        

    await interaction.guild.ban(user, reason=audit_reason)

    embed = discord.Embed(
        title=f"Ban result",
        description=f"{user.display_name} was banned from server.,
        color=discord.Color.red(),
        timestamp=discord.utils.utcnow()
    )

    await interaction.response.send_message(embed=embed)