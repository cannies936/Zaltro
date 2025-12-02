class MusicPlayer:
    def __init__(self):
        self.queue = []         # 曲のキュー
        self.current = None     # 現在再生中
        self.loop_mode = "off"  # off / one / all
        self.playing = False

    def add(self, info):
        self.queue.append(info)

    def next_song(self):
        if self.loop_mode == "one" and self.current:
            return self.current  # 同じ曲を再生

        if self.loop_mode == "all" and self.current:
            self.queue.append(self.current)  # 最後尾に戻す

        if self.queue:
            self.current = self.queue.pop(0)
            return self.current

        self.current = None
        return None


players = {}  # guild.id → MusicPlayer


def get_player(guild_id):
    if guild_id not in players:
        players[guild_id] = MusicPlayer()
    return players[guild_id]


# ─────────────────────────────
# ▼ /play — YouTube再生
# ─────────────────────────────

class play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@tree.command(name="play", description="Play music")
@app_commands.describe(url="Link of music")
async def play(interaction: discord.Interaction, url: str):
    await interaction.response.defer()

    player = get_player(interaction.guild_id)

    if not interaction.user.voice:
        return await interaction.followup.send("❌ join voice channel before playing")

    channel = interaction.user.voice.channel
    vc = interaction.guild.voice_client

    if vc is None:
        vc = await channel.connect()
    elif vc.channel != channel:
        await vc.move_to(channel)

    # YouTube情報取得
    ydl_opts = {"format": "bestaudio/best", "quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        stream_url = info["url"]
        title = info["title"]

    # キューに追加
    player.add({"url": stream_url, "title": title})

    await interaction.followup.send(f"⏳ queue add: **{title}**")

    # 再生していないなら再生開始
    if not player.playing:
        await start_playing(interaction.guild, vc)


async def start_playing(guild, vc):
    player = get_player(guild.id)

    while True:
        song = player.next_song()
        if not song:
            player.playing = False
            await vc.disconnect()
            return

        player.playing = True

        source = discord.FFmpegOpusAudio(song["url"], options="-vn")
        vc.play(source)

        # 再生終了を待つ
        while vc.is_playing():
            await asyncio.sleep(1)

async def setup(bot):
    await bot.add_cog(play(bot))

# ─────────────────────────────
# ▼ /skip — 次の曲へ
# ─────────────────────────────

class skip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@tree.command(name="skip", description="skip the sound")
async def skip(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if not vc:
        return await interaction.response.send_message("❌ this sound isn't played")

    vc.stop()
    await interaction.response.send_message("⏭ skipped")

async def setup(bot):
    await bot.add_cog(skip(bot))

# ─────────────────────────────
# ▼ /stop — 全停止
# ─────────────────────────────

class stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@tree.command(name="stop", description="stop sound")
async def stop(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if not vc:
        return await interaction.response.send_message("❌ This bot unconnects")

    player = get_player(interaction.guild_id)
    player.queue.clear()
    player.current = None
    player.playing = False

    vc.stop()
    await vc.disconnect()
    await interaction.response.send_message("⏹ This bot left")

async def setup(bot):
    await bot.add_cog(stop(bot))

# ─────────────────────────────
# ▼ /queue — キューを表示
# ─────────────────────────────

class queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@tree.command(name="queue", description="Show queue")
async def queue(interaction: discord.Interaction):
    player = get_player(interaction.guild_id)

    if not player.queue and not player.current:
        return await interaction.response.send_message("📭 キューは空です")

    txt = ""

    if player.current:
        txt += f"🎵 **Playing:** {player.current['title']}\n\n"

    if player.queue:
        txt += "📜 **queue:**\n"
        for i, s in enumerate(player.queue):
            txt += f"{i+1}. {s['title']}\n"

    await interaction.response.send_message(txt)

async def setup(bot):
    await bot.add_cog(queue(bot))

# ─────────────────────────────
# ▼ /loop — ループ設定
# ─────────────────────────────

class loop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@tree.command(name="loop", description="Change loop setting")
@app_commands.describe(mode="off / one / all")
async def loop(interaction: discord.Interaction, mode: str):
    mode = mode.lower()
    if mode not in ["off", "one", "all"]:
        return await interaction.response.send_message("❌ Able to use only off / one / all ")

    player = get_player(interaction.guild_id)
    player.loop_mode = mode

    await interaction.response.send_message(f"🔁 Loop mode: **{mode}** ")

async def loop(bot):
    await bot.add_cog(Ping(bot))
