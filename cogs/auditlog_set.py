CONFIG_FILE = "auditlog_config.json"

# 監査ログ送信チャンネルを管理
config = {}
check_audit_logs.start()

# 設定読み込み
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

# 保存関数
def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
  
class auditlog_set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# -----------------------------
# /auditlog_set コマンド
# -----------------------------
@tree.command(name="auditlog_set", description="Setting")
@app_commands.describe(channel="channel to send auditlog")
async def auditlog_set(interaction: discord.Interaction, channel: discord.TextChannel):
    # 権限チェック
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("⚠️ You don't have permission", ephemeral=True)
        return

    config[str(interaction.guild.id)] = channel.id
    save_config()
    await interaction.response.send_message(f"✅ Log chennel has set to{channel.mention} ", ephemeral=True)

# -----------------------------
# 監査ログチェック
# -----------------------------
last_checked = {}

@tasks.loop(seconds=10)
async def check_audit_logs():
    for guild_id, channel_id in config.items():
        guild = bot.get_guild(int(guild_id))
        if guild is None:
            continue

        log_channel = guild.get_channel(int(channel_id))
        if log_channel is None:
            continue

        # 最終確認時間
        lc = last_checked.get(guild_id, datetime.utcnow())

        async for entry in guild.audit_logs(limit=20, after=lc):
            embed = discord.Embed(
                title="📜 Audit log",
                color=discord.Color.green(),
                timestamp=entry.created_at
            )
            embed.add_field(name="Action", value=str(entry.action), inline=True)
            embed.add_field(name="Target", value=str(entry.target), inline=True)
            embed.add_field(name="repposible moderator", value=str(entry.user), inline=True)
            embed.add_field(name="Reason", value=entry.reason or "No reason", inline=False)
            embed.set_footer(text=f"ID: {entry.id}")

            await log_channel.send(embed=embed)

        last_checked[guild_id] = datetime.utcnow()

async def setup(bot):
    await bot.add_cog(auditlog_set(bot))

