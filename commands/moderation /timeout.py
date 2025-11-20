@bot.tree.command(name="timeout", description="Timed out for user ")
@app_commands.describe(
    user="user to be timed out",
    seconds="second to be timed out",
    reason="Reason of timed out"
)
async def timeout(interaction: discord.Interaction, user: discord.Member, seconds: int, reason: str = "No reason was given."):
    # 権限チェック
    if not interaction.user.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ You don't have permission that can be timed out user.", ephemeral=True)

    if not interaction.guild.me.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ Bot doesn't have permission that can be timed out user !", ephemeral=True)

    # 自分自身をタイムアウトしようとしているか
    if user.id == interaction.user.id:
        return await interaction.response.send_message("❌ You can't be timed out yourself !", ephemeral=True)

    # Botをタイムアウトしようとしているか
    if user.id == bot.user.id:
        return await interaction.response.send_message("❌ You can't be timed out bot", ephemeral=True)

    # 権限階層チェック
    if user.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
        return await interaction.response.send_message("❌ You can't be timed out user who has a higher or same role.", ephemeral=True)

    # タイムアウト開始
    try:
        await user.timeout(timedelta(seconds=seconds), reason=reason)

        embed = discord.Embed(
            title="⏳ Timed out result",
            description=f"{user.mention} was timed out for **{seconds} seconds.** ",
            color=discord.Color.orange()
        )

        await interaction.response.send_message(embed=embed)

    except discord.Forbidden:
        await interaction.response.send_message("❌ You failed to be timed out because of lack of permission.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error happened: `{e}`", ephemeral=True)