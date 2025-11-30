# --- Data ---
whitelist_roles = defaultdict(set)   # guild_id -> set(role_ids)
whitelist_channels = defaultdict(set) # guild_id -> set(channel_ids)
user_warns = defaultdict(lambda: defaultdict(int))  # guild_id -> user_id -> warns
anti_spam_enabled = defaultdict(bool)  # guild_id -> bool
message_cache = defaultdict(lambda: defaultdict(list))  # guild_id -> user_id -> [timestamps]

# --- Anti-Spam Settings ---
SPAM_THRESHOLD = 5  # messages
SPAM_INTERVAL = 10  # seconds

# ------------------------------
# Whitelist Commands
# ------------------------------

whitelist_group = app_commands.Group(name="whitelist", description="Manage whitelist for roles/channels")

@whitelist_group.command(name="add_role", description="Add a role to the whitelist")
@app_commands.describe(role="The role to whitelist")
async def whitelist_add_role(interaction: discord.Interaction, role: discord.Role):
    whitelist_roles[interaction.guild_id].add(role.id)
    await interaction.response.send_message(f"✅ Role {role.mention} added to whitelist.", ephemeral=True)

@whitelist_group.command(name="remove_role", description="Remove a role from the whitelist")
@app_commands.describe(role="The role to remove from whitelist")
async def whitelist_remove_role(interaction: discord.Interaction, role: discord.Role):
    whitelist_roles[interaction.guild_id].discard(role.id)
    await interaction.response.send_message(f"✅ Role {role.mention} removed from whitelist.", ephemeral=True)

@whitelist_group.command(name="add_channel", description="Add a channel to the whitelist")
@app_commands.describe(channel="The channel to whitelist")
async def whitelist_add_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    whitelist_channels[interaction.guild_id].add(channel.id)
    await interaction.response.send_message(f"✅ Channel {channel.mention} added to whitelist.", ephemeral=True)

@whitelist_group.command(name="remove_channel", description="Remove a channel from the whitelist")
@app_commands.describe(channel="The channel to remove from whitelist")
async def whitelist_remove_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    whitelist_channels[interaction.guild_id].discard(channel.id)
    await interaction.response.send_message(f"✅ Channel {channel.mention} removed from whitelist.", ephemeral=True)

bot.tree.add_command(whitelist_group)

# ------------------------------
# Anti-Spam Toggle
# ------------------------------

@bot.tree.command(name="antispam", description="Enable or disable anti-spam")
@app_commands.describe(state="True to enable, False to disable")
async def antispam_toggle(interaction: discord.Interaction, state: bool):
    anti_spam_enabled[interaction.guild_id] = state
    text = "✅ Anti-spam enabled." if state else "❌ Anti-spam disabled."
    await interaction.response.send_message(text, ephemeral=True)

# ------------------------------
# Message Listener for Anti-Spam
# ------------------------------

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    gid = message.guild.id
    uid = message.author.id

    # Skip whitelisted roles/channels
    if any(role.id in whitelist_roles[gid] for role in message.author.roles):
        return
    if message.channel.id in whitelist_channels[gid]:
        return

    if anti_spam_enabled[gid]:
        now = message.created_at.timestamp()
        message_cache[gid][uid].append(now)
        
        # Remove old timestamps
        message_cache[gid][uid] = [t for t in message_cache[gid][uid] if now - t <= SPAM_INTERVAL]
        
        if len(message_cache[gid][uid]) >= SPAM_THRESHOLD:
            user_warns[gid][uid] += 1
            message_cache[gid][uid].clear()
            await message.channel.send(f"⚠️ {message.author.mention}, please stop spamming! Warnings: {user_warns[gid][uid]}")
            
            # Optional: auto timeout / block at 3 warnings
            if user_warns[gid][uid] >= 3:
                timeout_duration = 300  # 5 minutes
                try:
                    await message.author.timeout(duration=discord.utils.utcnow()+discord.timedelta(seconds=timeout_duration),
                                                 reason="Reached 3 anti-spam warnings")
                    await message.channel.send(f"🔇 {message.author.mention} has been timed out for 5 minutes due to spam.")
                except:
                    await message.channel.send("❌ Could not timeout user (missing permissions).")

    await bot.process_commands(message)