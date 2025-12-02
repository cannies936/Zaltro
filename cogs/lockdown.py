# サーバーごとのロックダウン状態保存
lockdown_mode = {}  # { guild_id: "ban" | "kick" | "none" }

class lockdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.tree.command(name="lockdown", description="Action ban / kick / none")
@app_commands.describe(mode="coice ban / kick / none ")
async def lockdown(interaction: discord.Interaction, mode: str):

    mode = mode.lower()

    if mode not in ["ban", "kick", "none"]:
        await interaction.response.send_message("❌ You can choose `ban` `kick` `none` ", ephemeral=True)
        return

    # 状態を保存
    lockdown_mode[interaction.guild_id] = mode

    txt = {
        "ban": "🚫 Lockdown mode：**BAN**",
        "kick": "⚠️ Lockdown mode：**KICK**",
        "none": "✅ Lockdown set off"
    }

    await interaction.response.send_message(txt[mode])


# --- 新規メンバー参加時イベント ---
@bot.event
async def on_member_join(member: discord.Member):
    mode = lockdown_mode.get(member.guild.id, "none")

    try:
        if mode == "ban":
            await member.ban(reason="Join Auto ban")
            print(f"🔨 自動BAN: {member} ({member.id})")

        elif mode == "kick":
            await member.kick(reason="Join Auto kick")
            print(f"👢 自動Kick: {member} ({member.id})")

        # mode が none の時は何もしない

    except discord.Forbidden:
        print("⚠️ 権限不足でBAN/KICKできませんでした")
    except Exception as e:
        print(f"❌ エラー: {e}")

async def setup(bot):
    await bot.add_cog(lockdown(bot))
