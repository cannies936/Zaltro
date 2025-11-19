@bot.tree.command(name="delete_invite", description="Delete a invite from this server")
@app_commands.describe(invite_code="Invite code to delete (example: abc123)")
async def delete_invite(interaction: discord.Interaction, invite_code: str):

    # 権限チェック（招待管理）
    if not interaction.user.guild_permissions.manage_guild:
        return await interaction.response.send_message(
            "❌ You don't have permission to delete invites (Manage Server).",
            ephemeral=True
        )

    if not interaction.guild.me.guild_permissions.manage_guild:
        return await interaction.response.send_message(
            "❌ Bot does not have permission to delete invites (Manage Server).",
            ephemeral=True
        )

    # 招待一覧を取得
    invites = await interaction.guild.invites()

    # 指定されたコードに一致する招待を探す
    target_invite = None
    for inv in invites:
        if inv.code == invite_code:
            target_invite = inv
            break

    # 見つからなかった場合
    if target_invite is None:
        return await interaction.response.send_message(
            "❌ That invite code does not exist on this server.",
            ephemeral=True
        )

    # 招待削除
    try:
        await target_invite.delete(reason=f"Deleted by {interaction.user}")
        await interaction.response.send_message(
            f"✅ Invite `{invite_code}` has been deleted.",
            ephemeral=True
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Failed to delete invite due to insufficient bot permission.",
            ephemeral=True
        )

    except Exception as e:
        await interaction.response.send_message(
            f"❌ Error occurred: `{e}`",
            ephemeral=True
        )