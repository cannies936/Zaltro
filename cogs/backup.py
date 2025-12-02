class backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.tree.command(name="backup", description="creating backup file and use it to restore")
@app_commands.describe(action="create = crate backup / restore = restore", file = if restoreing send backup file")
async def backup(interaction: discord.Interaction, action: str, file: discord.Attachment = None):
    guild = interaction.guild

    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ **You need admistor permission**", ephemeral=True)

    # ==========================
    # バックアップ作成
    # ==========================
    if action.lower() == "create":
        await interaction.response.defer()

        data = {
            "roles": [],
            "channels": []
        }

        # ロール
        for role in guild.roles:
            data["roles"].append({
                "name": role.name,
                "permissions": role.permissions.value,
                "color": role.color.value,
                "position": role.position
            })

        # チャンネル
        for channel in guild.channels:
            data["channels"].append({
                "name": channel.name,
                "type": str(channel.type),
                "category": channel.category.name if channel.category else None,
                "position": channel.position
            })

        filename = f"backup_{guild.id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        await interaction.followup.send(
            "✅ **Backup process has completed !**\n Please store it.",
            file=discord.File(filename)
        )
        return

    # ==========================
    # バックアップ復元
    # ==========================
    elif action.lower() == "restore":
        if file is None:
            return await interaction.response.send_message("❌ **restore source needs backup file
**", ephemeral=True)

        await interaction.response.defer()

        data = json.loads(await file.read())

        # === ロール復元（既存はスキップ） ===
        existing_role_names = [r.name for r in guild.roles]
        for role in data["roles"]:
            if role["name"] not in existing_role_names:
                await guild.create_role(
                    name=role["name"],
                    permissions=discord.Permissions(role["permissions"]),
                    color=discord.Color(role["color"]),
                    reason="Restoreing"
                )

        # カテゴリ生成
        existing_categories = {c.name: c for c in guild.categories}
        for ch in data["channels"]:
            if ch["category"] and ch["category"] not in existing_categories:
                existing_categories[ch["category"]] = await guild.create_category(ch["category"])

        # チャンネル復元
        existing_channels = [c.name for c in guild.channels]
        for ch in data["channels"]:
            if ch["name"] in existing_channels:
                continue  

            category = existing_categories.get(ch["category"])
            if ch["type"] == "text":
                await guild.create_text_channel(ch["name"], category=category)
            elif ch["type"] == "voice":
                await guild.create_voice_channel(ch["name"], category=category)

        await interaction.followup.send("✅ **restore completed !**（things exsit is skiped.）")
        return

    else:
        await interaction.response.send_message("❌ Please enter `create` or `restore` in `action`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(backup(bot))
