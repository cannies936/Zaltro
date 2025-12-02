class kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.tree.command(name="kick", description="Kick the user from server")
@app_commands.describe(user="user to kick", reason="reason")
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason was given."):

    if not interaction.user.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ You don't have permission that can kick user.", ephemeral=True)

    if not interaction.guild.me.guild_permissions.moderate_members:
        return await interaction.response.send_message("❌ Bot doesn't have permission that can kick user !", ephemeral=True)

    # 自分自身をキックしようとしているか
    if user.id == interaction.user.id:
        return await interaction.response.send_message("❌ You can't kick yourself !", ephemeral=True)

    # Botをキックしようとしているか
    if user.id == bot.user.id:
        return await interaction.response.send_message("❌ You can't kick bot !", ephemeral=True)

    # 権限階層チェック
    if user.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
        return await interaction.response.send_message("❌ You can't kick user who has a higher or same role.", ephemeral=True)

   # 理由の長さ制限（Discord API制限対応）
    audit_reason = f"Kick Peformer: {interaction.user} | Reason: {reason}"     

    await interaction.guild.kick(user, reason=audit_reason)

    embed = discord.Embed(
        title=f"👢 Kick result",
        description=f"{user.display_name} was kicked from server.
        color=discord.Color.yellow(),
        timestamp=discord.utils.utcnow()
    )

    await interaction.response.send_message(embed=embed)

    except discord.Forbidden:
        await interaction.response.send_message("❌ You failed to kick because of lack of permission.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error happened.: `{e}`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(kick(bot))