class unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.tree.command(name="unban", description="Unban user from server")
@app_commands.describe(user="User to unban", reason="Reason for unban")
async def unban(interaction: discord.Interaction, user_id: str, reason: str = "No reason was given."):

    # ---- 権限チェック ----
    if not interaction.user.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ You don't have permission to unban user.", ephemeral=True)

    if not interaction.guild.me.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ Bot doesn't have permission to unban user.", ephemeral=True)

    # ---- ユーザーIDが数字以外の場合 ----
    try:
        user_id = int(user_id)
    except ValueError:
        return await interaction.response.send_message("⚠ Please enter a **valid User ID** (numbers only).", ephemeral=True)

    # ---- ユーザーがDiscordに存在するか ----
    try:
        user = await bot.fetch_user(user_id)
    except discord.NotFound:
        return await interaction.response.send_message("❌ This user_id doesn't exist.", ephemeral=True)

    # ---- サーバーの Ban リストから確認 ----
    try:
        bans = await interaction.guild.bans()
        banned_entry = discord.utils.get(bans, user=user)

        if banned_entry is None:
            return await interaction.response.send_message("ℹ That user is **not banned** from this server.", ephemeral=True)

        audit_reason = f"Unban performer: {interaction.user} | Reason: {reason}"

        await interaction.guild.unban(user, reason=audit_reason)

        embed = discord.Embed(
            title="Unban Result",
            description=f"✅ **{user.display_name}** was unbanned.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )

        return await interaction.response.send_message(embed=embed)

    except discord.Forbidden:
        return await interaction.response.send_message("❌ Unban failed because of luck of permissions.", ephemeral=True)

    except Exception as e:
        return await interaction.response.send_message(f"❌ Error happened: `{e}`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(unban(bot))