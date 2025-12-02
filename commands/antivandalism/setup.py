async def restrict_channel_permissions(channel: discord.abc.GuildChannel, role: discord.Role):
    try:
        overwrites = channel.overwrites
        current = overwrites.get(role, discord.PermissionOverwrite())

        # 閲覧権限削除 & 外部アプリ使用不可
        current.view_channel = False
        current.use_external_apps = False

        overwrites[role] = current
        await channel.edit(overwrites=overwrites)
        print(f"[OK] {channel.name} 権限を更新しました")
    except Exception as e:
        print(f"[Error] {channel.name}: {e}")

class settingup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# ---------- 統合コマンド ----------
@bot.tree.command(
    name="settingup",
    description="set up for antivandarism"
)
async def settingup(interaction: discord.Interaction):
    # 管理者チェック
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ This command can be used by admistor", ephemeral=True)

    guild = interaction.guild
    if guild is None:
        return await interaction.response.send_message("❌ This command can be used here", ephemeral=True)

    role_name = "blocked"

    # 既にロールがある場合
    existing = discord.utils.get(guild.roles, name=role_name)
    if existing:
        return await interaction.response.send_message(f"❌ `{role_name}` exsits", ephemeral=True)

    # ロール作成（赤色）
    role = await guild.create_role(name=role_name, colour=discord.Colour.red())
    await interaction.response.send_message(f"✅ `{role_name}` was created setting up now...")

    # 既存チャンネル全てに権限適用
    for channel in guild.channels:
        await restrict_channel_permissions(channel, role)

    await interaction.followup.send("✅ Comleted")

# ---------- 新規チャンネル作成イベント ----------
@bot.event
async def on_guild_channel_create(channel):
    guild = channel.guild
    role = discord.utils.get(guild.roles, name="blocked")
    if role:
        await restrict_channel_permissions(channel, role)

async def setup(bot):
    await bot.add_cog(settingup(bot))