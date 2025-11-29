@bot.tree.command(name="serverinfo", description="Show server infomation")
async def server_info(interaction: discord.Interaction):

    guild = interaction.guild

    if guild is None:
        await interaction.response.send_message("❌ This command can be used there", ephemeral=True)
        return

    owner = guild.owner
    created_at = guild.created_at
    member_count = guild.member_count

    text_channels = len([c for c in guild.channels if isinstance(c, discord.TextChannel)])
    voice_channels = len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)])
    categories = len([c for c in guild.channels if isinstance(c, discord.CategoryChannel)])
    total_channels = len(guild.channels)

    role_count = len(guild.roles) - 1

    humans = len([m for m in guild.members if not m.bot])
    bots = len([m for m in guild.members if m.bot])

    online_members = len([m for m in guild.members if m.status == discord.Status.online])
    idle_members = len([m for m in guild.members if m.status == discord.Status.idle])
    dnd_members = len([m for m in guild.members if m.status == discord.Status.dnd])
    offline_members = len([m for m in guild.members if m.status == discord.Status.offline])

    verification_level = str(guild.verification_level).replace('_', ' ').title()
    content_filter = str(guild.explicit_content_filter).replace('_', ' ').title()

    boost_level = guild.premium_tier
    boost_count = guild.premium_subscription_count or 0

    features = []
    if guild.features:
        feature_names = {
            'VERIFIED': '✅ Verified',
            'PARTNERED': '🤝 Partner',
            'COMMUNITY': '🏘️ Community',
            'NEWS': '📰 News',
            'DISCOVERABLE': '🔍 Discoverable',
            'VANITY_URL': '🔗 Costom url',
            'BANNER': '🎨 バナー',
            'ANIMATED_ICON': '✨ Animation icon',
            'BOOST_LEVEL_1': '🚀 Boost level1',
            'BOOST_LEVEL_2': '🚀 Boost level2',
            'BOOST_LEVEL_3': '🚀 Boostlevel3'
        }
        features = [feature_names.get(f, f) for f in guild.features[:10]]

    embed = discord.Embed(
        title=f"📊 {guild.name} Server infomation",
        description=f"Server ID: `{guild.id}`",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    embed.add_field(name="👑 Owner", value=f"{owner}\n(ID: {owner.id})", inline=True)
    embed.add_field(name="📅 Created", value=f"{created_at.strftime('%Y/%m/%d')}", inline=True)
    embed.add_field(name="🔒 Verification level", value=verification_level, inline=True)

    embed.add_field(name="👥 Membercount", value=f"Total: {member_count}\nhumans: {humans}\nBOT: {bots}", inline=True)
    embed.add_field(name="📈 Online", value=f"🟢 {online_members} / 🟡 {idle_members} / 🔴 {dnd_members} / ⚫ {offline_members}", inline=True)
    embed.add_field(name="📺 Channel", value=f"Total: {total_channels}\n💬 {text_channels} / 🔊 {voice_channels} / 📁 {categories}", inline=True)

    embed.add_field(name="🎭 Role count", value=str(role_count), inline=True)

    if boost_level > 0 or boost_count > 0:
        emoji = ["", "🥉", "🥈", "🥇"][boost_level] if boost_level < 4 else "💎"
        embed.add_field(name=f"{emoji} Boost", value=f"Level {boost_level}\n{boost_count} Boost", inline=True)
    else:
        embed.add_field(name="🚀 Boost", value="Unboost", inline=True)

    embed.add_field(name="🛡️ Content filter", value=content_filter, inline=True)

    if features:
        embed.add_field(name="⭐ type", value="\n".join(features), inline=False)

    embed.set_footer(text=f"intonation geter: {interaction.user}", icon_url=interaction.user.display_avatar.url)

    await interaction.response.send_message(embed=embed)