CONFIG_FILE = "verify_config.json"

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        verify_config = json.load(f)
else:
    verify_config = {}

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(verify_config, f, indent=4)

# ------------------- 認証ボタン -------------------
class VerifyButton(discord.ui.View):
    @discord.ui.button(label=　"Verify", style=discord.ButtonStyle.primary)
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_id = str(interaction.guild.id)

        if guild_id not in verify_config:
            return await interaction.response.send_message("❌ This server doesn't set up verification", ephemeral=True)

        method = verify_config[guild_id]["method"]

        await interaction.response.send_message("✅ Check your direct message !", ephemeral=True)

        try:
            dm = await interaction.user.create_dm()

            if method == "image":
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                await dm.send(f"🔑 **Code Verification**\nAnswers this:\n```\n{code}\n```")
            else:
                a, b = random.randint(1, 9), random.randint(1, 9)
                code = str(a + b)
                await dm.send(f"🧮 **Calc Verification**\nAnswer this:\n```\n{a} + {b} = ?\n```")

            def check(m):
                return m.author == interaction.user and m.channel == dm

            response = await bot.wait_for("message", check=check, timeout=60)

            if response.content.strip() == code:
                role = interaction.guild.get_role(verify_config[guild_id]["role_id"])
                await interaction.user.add_roles(role)
                await dm.send("✅ Verification sucessed !")
            else:
                await dm.send("❌ Verification failed.")

        except discord.Forbidden:
            await interaction.response.send_message("❌ DM is denied,", ephemeral=True)

# ------------------- verifysetup -------------------
@bot.tree.command(name="verifysetup", description="Set Verification and Verify button")
@app_commands.describe(role="Given role when verification sucseed", method="Verification method (code / calc)")
async def verifysetup(interaction: discord.Interaction, role: discord.Role, method: str):
    if method not in ["code", "calc"]:
        return await interaction.response.send_message("Verification method is chosen`code` or `calc` ", ephemeral=True)

    verify_config[str(interaction.guild.id)] = {
        "role_id": role.id,
        "method": method
    }
    save_config()

    embed = discord.Embed(
        title="🔐 Need verification",
        description="Press button and Verify",
        color=0x00bfff
    )
    embed.add_field(name="Given role", value=role.mention, inline=False)
    embed.add_field(name="verification method", value=" 🔑 Code Verification" if method == "code" else "🧮 Calc verification", inline=False)

    await interaction.response.send_message("✅ Setting completed !", ephemeral=True)
    await interaction.channel.send(embed=embed, view=VerifyButton())

# 