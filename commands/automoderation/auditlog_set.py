guild_log_channels = {} 

@bot.tree.command(name="auditlog_set", description="send auditlog to channel")
@app_commands.describe(channel="channel to send auditlog")

async def auditlog_set(interaction: discord.Interaction, channel: discord.TextChannel):
        guild_id = interaction.guild.id
        guild_log_channels[guild_id] = channel.id
        await interaction.response.send_message(f"✅ Log channel set to {channel.mention} ", ephemeral=True)

@bot.event
async def on_member_unban(guild, user):
    channel_id = guild_log_channels.get(guild.id)
    if channel_id is None:
        return  # ログチャンネル未設定

    channel = guild.get_channel(LOG_CHANNEL_ID)
    if channel is None:
        return

    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
        executor = entry.user
        reason = entry.reason or "No reason was given"

        embed = discord.Embed(
            title="♻️ Unban add",
            description=f"👤 User: {user}\n🛡 Repposible moderator: {executor}\n📝 Reason: {reason}",
            color=0x44ff44
        )
        await channel.send(embed=embed)



