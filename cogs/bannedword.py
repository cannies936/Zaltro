# --- Banned words storage ---
banned_words = {}  # {guild_id: set(["word1", "word2"])}

# --- User warnings storage ---
user_warns = {}  # {guild_id: {user_id: count}}

WARN_LIMIT = 3  # Number of warnings before punishment
TIMEOUT_DURATION = 300  # Timeout duration in seconds (5 minutes)

class BannedWord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bannedword = app_commands.Group(
        name="bannedword",
        description="Manage banned words"
    )

    @bannedword.command(name="add", description="Add a new banned word")
    async def add(self, interaction: discord.Interaction, word: str):
        gid = interaction.guild_id
        banned_words.setdefault(gid, set()).add(word.lower())
        await interaction.response.send_message(
            f"🔒 Banned word **'{word}'** has been added.",
            ephemeral=True
        )

    @bannedword.command(name="remove", description="Remove a banned word")
    async def remove(self, interaction: discord.Interaction, word: str):
        gid = interaction.guild_id
        banned_words.setdefault(gid, set()).discard(word.lower())
        await interaction.response.send_message(
            f"🗑 Banned word **'{word}'** has been removed.",
            ephemeral=True
        )

    @bannedword.command(name="list", description="Show all banned words")
    async def list(self, interaction: discord.Interaction):
        gid = interaction.guild_id
        words = banned_words.get(gid, set())
        msg = "(No banned words)" if not words else "\n".join([f"• `{w}`" for w in words])
        embed = discord.Embed(title="🚫 Banned Words List", description=msg, color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)


# ==============================
# Check messages for banned words and auto-warn
# ==============================
async def check_banned_words(message: discord.Message):
    if message.author.bot:
        return

    gid = message.guild.id
    uid = message.author.id

    words = banned_words.get(gid, set())
    content = message.content.lower()

    for w in words:
        if w in content:
            await message.delete()

            # Notify user
            try:
                await message.channel.send(
                    f"⚠️ {message.author.mention} Your message contained the banned word **'{w}'** and was deleted.",
                    delete_after=5
                )
            except:
                pass

            # Increase warn count
            user_warns.setdefault(gid, {})
            user_warns[gid][uid] = user_warns[gid].get(uid, 0) + 1
            warn_count = user_warns[gid][uid]

            if warn_count >= WARN_LIMIT:
                # Apply punishment: timeout
                try:
                    member = message.author
                    await member.timeout(discord.utils.utcnow() + discord.timedelta(seconds=TIMEOUT_DURATION))
                    await message.channel.send(
                        f"⛔ {member.mention} has reached {WARN_LIMIT} warnings and has been **timed out**.",
                        delete_after=10
                    )
                    user_warns[gid][uid] = 0  # Reset warn count
                except:
                    pass
            else:
                # Show warning count
                await message.channel.send(
                    f"⚠️ {message.author.mention} Warning {warn_count}/{WARN_LIMIT}",
                    delete_after=5
                )
            return


# Register bot events
def setup_events(bot: commands.Bot):
    @bot.event
    async def on_message(message):
        await check_banned_words(message)
        await bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(BannedWord(bot))
    setup_events(bot)
