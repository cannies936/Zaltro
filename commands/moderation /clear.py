@bot.tree.command(name="clear", description="Delete message")
@app_commands.describe(
    amount="message to delete（1〜500）",
    member="User to delete message"
)
async def clear(
    interaction: discord.Interaction,
    amount: int,
    member: discord.Member | None = None
):
    # サーバー内のみ
    if not interaction.guild:
        return await interaction.response.send_message("❌ Use it at server.", ephemeral=True)

    # 権限チェック
    if not interaction.user.guild_permissions.manage_messages:
        return await interaction.response.send_message("❌ You have permission to message.", ephemeral=True)

    # 限度
    if amount < 1 or amount > 500:
        return await interaction.response.send_message("❌ You can delete message more than 1 and less than 500", ephemeral=True)

    await interaction.response.defer(ephemeral=True)

    # ユーザー指定がある場合 → その人だけ削除
    if member:
        def check(msg):
            return msg.author.id == member.id
        deleted = await interaction.channel.purge(limit=amount, check=check)

        return await interaction.followup.send(
            f"🧹 **{member.mention}** 's **{len(deleted)} ** messages were deleted.",
            ephemeral=True
        )

    # 指定無し → 全メッセージ削除
    deleted = await interaction.channel.purge(limit=amount)

    await interaction.followup.send(
        f"🧼  **{len(deleted)}** messeges were deleted.",
        ephemeral=True
    )