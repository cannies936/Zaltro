class userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.tree.command(name="userinfo", description="Show user infomation")
@app_commands.describe(user="User you want to check")
async def userinfo(interaction: discord.Interaction, user: discord.User | None = None):
    # ユーザーが指定されていない場合はコマンド実行者
    user = user or interaction.user

    embed = discord.Embed(
        title=f"👤 User infomation: {user}",
        color=discord.Color.blue()
    )

    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)

    embed.add_field(name="User name", value=f"`{user}`", inline=False)
    embed.add_field(name="User ID", value=f"`{user.id}`", inline=False)

    # guildに存在する場合はサーバー情報も付ける
    if isinstance(user, discord.Member):
        embed.add_field(name="Nick name", value=f"`{user.nick}`" if user.nick else "なし", inline=False)
        embed.add_field(
            name="Join date",
            value=f"<t:{int(user.joined_at.timestamp())}:F>",
            inline=False
        )
        embed.add_field(name="Role", value=", ".join([role.mention for role in user.roles if role.name != "@everyone"]), inline=False)

    embed.add_field(
        name="Account created",
        value=f"<t:{int(user.created_at.timestamp())}:F>",
        inline=False
    )

    await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(userinfo(bot))
