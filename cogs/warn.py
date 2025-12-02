permission# 元ロール保存用: {guild_id: {user_id: [role_ids]}}
blocked_roles_backup = defaultdict(lambda: defaultdict(list))

# 自動解除スケジュール用: {guild_id: {user_id:解除時刻}}
blocked_timers = defaultdict(lambda: defaultdict(datetime))

class warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# --- /warn コマンド ---
@bot.tree.command(
    name="warn",
    description="warn user"
)
@app_commands.describe(user="User to warn", reason="reason", action="action: block / timeout")
async def warn(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason was given", action: str = "block"):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ This command can be used by admistor", ephemeral=True)

    guild_id = interaction.guild.id
    user_id = user.id

    warn_data[guild_id][user_id] += 1
    count = warn_data[guild_id][user_id]

    msg = f"⚠️ {user} was set warned Reason: `{reason}`\nWarn points: {count}/3"

    if count >= 3:
        warn_data[guild_id][user_id] = 0  # リセット

        if action.lower() == "block":
            role = discord.utils.get(interaction.guild.roles, name="blocked")
            if role:
                # 元ロールを保存（@everyone以外）
                blocked_roles_backup[guild_id][user_id] = [r.id for r in user.roles if r != interaction.guild.default_role]

                # 元ロールを全て削除
                try:
                    await user.remove_roles(*user.roles, reason="Warn 3 points ：一時block")
                except discord.Forbidden:
                    msg += "\n❌ ロール削除に失敗しました（権限不足）"

                # blockedロールを付与
                await user.add_roles(role, reason="warn reached 3")
                msg += f"\n🚫 {role.name} was given"

                # 自動解除タイマー（5分後に解除）
                unblock_time = datetime.utcnow() + timedelta(minutes=5)
                blocked_timers[guild_id][user_id] = unblock_time
                asyncio.create_task(auto_unblock(interaction.guild, user, unblock_time))

            else:
                msg += "\n❌ `blocked` ロールが存在しません。先に作成してください。"

        elif action.lower() == "timeout":
            try:
                await user.timeout(timedelta(minutes=5), reason="警告3回到達：タイムアウト")
                msg += "\n⏳ 5 minutes timed out"
            except discord.Forbidden:
                msg += "\n❌ lack of timed out permission"

    await interaction.response.send_message(msg)

# --- 自動解除タスク ---
async def auto_unblock(guild: discord.Guild, user: discord.Member, unblock_time: datetime):
    now = datetime.utcnow()
    delay = (unblock_time - now).total_seconds()
    if delay > 0:
        await asyncio.sleep(delay)

    guild_id = guild.id
    user_id = user.id

    # 元ロールを復元
    role_ids = blocked_roles_backup[guild_id].get(user_id, [])
    roles = [guild.get_role(rid) for rid in role_ids if guild.get_role(rid)]
    if roles:
        try:
            await user.add_roles(*roles, reason="block期間終了：元ロール復元")
        except discord.Forbidden:
            print(f"❌ {user} のロール復元に失敗しました")

    # blockedロール削除
    blocked_role = discord.utils.get(guild.roles, name="blocked")
    if blocked_role:
        try:
            await user.remove_roles(blocked_role, reason="block期間終了")
        except discord.Forbidden:
            print(f"❌ {user} の blocked ロール削除に失敗しました")

    # データ削除
    blocked_roles_backup[guild_id].pop(user_id, None)
    blocked_timers[guild_id].pop(user_id, None)

# --- /unblock コマンド ---
@bot.tree.command(
    name="unblock",
    description="unblocked user"
)
@app_commands.describe(user="user to unblock")
async def unblock(interaction: discord.Interaction, user: discord.Member):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ This command can be used by admistor", ephemeral=True)

    guild_id = interaction.guild.id
    user_id = user.id

    role_ids = blocked_roles_backup[guild_id].get(user_id, [])
    if not role_ids:
        return await interaction.response.send_message("❌ This user doesn't set blocked", ephemeral=True)

    roles = [interaction.guild.get_role(rid) for rid in role_ids if interaction.guild.get_role(rid)]
    if roles:
        await user.add_roles(*roles, reason="unblock by admistor")
    blocked_role = discord.utils.get(interaction.guild.roles, name="blocked")
    if blocked_role:
        await user.remove_roles(blocked_role, reason="管理者による手動 unblock")

    # データ削除
    blocked_roles_backup[guild_id].pop(user_id, None)
    blocked_timers[guild_id].pop(user_id, None)

    await interaction.response.send_message(f"✅ {user} was restored")

async def setup(bot):
    await bot.add_cog(warn(bot))
