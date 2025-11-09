@bot.tree.command(name="kick", description="ユーザーをサーバーからキックします")
@app_commands.describe(user="キックするユーザー", reason="理由")
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = "理由はありません"):

    if not interaction.user.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ あなたにはユーザーをタイムアウトする権限がありません", ephemeral=True)

    if not interaction.guild.me.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ Bot にタイムアウト権限がありません", ephemeral=True)

    # 自分自身をタイムアウトしようとしているか
    if user.id == interaction.user.id:
        return await interaction.response.send_message("❌ 自分自身をタイムアウトすることはできません。", ephemeral=True)

    # Botをタイムアウトしようとしているか
    if user.id == bot.user.id:
        return await interaction.response.send_message("❌ Bot をタイムアウトすることはできません", ephemeral=True)

    # 権限階層チェック
    if user.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
        return await interaction.response.send_message("権限不足でタイムアウトできませんでした", ephemeral=True)

   # 理由の長さ制限（Discord API制限対応）
    audit_reason = f"実行者: {interaction.user} | 理由: {reason}"     

    await interaction.guild.kick(user, reason=audit_reason)

    embed = discord.Embed(
        title=f"Kick result",
        description=f"{user.display_name} をサーバーからkickしました。\n理由: {reason} \n実行者: {interaction.user}",
        color=discord.Color.yellow(),
        timestamp=discord.utils.utcnow()
    )

    await interaction.response.send_message(embed=embed)

    except discord.Forbidden:
        await interaction.response.send_message("❌ 権限不足でタイムアウトできませんでした", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ エラーが発生しました: `{e}`", ephemeral=True)