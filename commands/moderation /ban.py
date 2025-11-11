@bot.tree.command(name="ban", description="Ban user from server")
@app_commands.describe(user="User to ban", reason="reason")
async def ban(interaction: discord.Interaction, user: discord.User, reason: str = "No reason was given."):

    if not interaction.user.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ You don't have permission to ban user.", ephemeral=True)

    if not interaction.guild.me.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ Bot doesn't have permission to ban user !", ephemeral=True)

    # 自分自身をバンしようとしているか
    if user.id == interaction.user.id:
        return await interaction.response.send_message("❌ You can't ban yourself !", ephemeral=True)

    # Botをバンしようとしているか
    if user.id == bot.user.id:
        return await interaction.response.send_message("❌ You can't ban bot !", ephemeral=True)

    # 権限階層チェック
    if user.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id and member is not None:
        return await interaction.response.send_message("❌ You can't ban user who has a higher or equal role.", ephemeral=True)

try:
        # ユーザーID からユーザー情報を取得
        user = await bot.fetch_user(int(user_id))

    except discord.NotFound:
        # ユーザーが Discord に存在しない
        await interaction.response.send_message("❌ This user_id doesn't exsit.", ephemeral=True)
        return 

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

    except discord.Forbidden:
        await interaction.response.send_message("❌ You failed to ban because of lack of permission.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error happened.: `{e}`", ephemeral=True)