import discord
from discord.ext import commands

TOKEN = "MTQyODAwMjI2OTM5OTQ4MjQ4MA.G05dOo.aDdwR21B4yQrUc37HRHrnut5tbTmgeLedtCylI"
AUDIT_CHANNEL_ID = 1428018103303802970  

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():

@bot.event
async def on_audit_log_entry_create(entry: discord.AuditLogEntry):
    channel = bot.get_channel(AUDIT_CHANNEL_ID)
    if not channel:
        print("⚠️ ID НЕ НАЙДЕН ЕБАНЫЙ РОМАН НАХУЙ")
        return

    embed = discord.Embed(
        title="📜 Новая запись в журнале аудита",
        color=discord.Color.blurple()
    )
    embed.add_field(name="Действие", value=str(entry.action).replace("AuditLogAction.", ""), inline=False)
    embed.add_field(name="Модератор", value=f"{entry.user} (ID: {entry.user.id})", inline=False)
    if entry.target:
        embed.add_field(name="Цель", value=f"{entry.target}", inline=False)
    if entry.reason:
        embed.add_field(name="Причина", value=entry.reason, inline=False)

    embed.timestamp = entry.created_at

    await channel.send(embed=embed)

bot.run(TOKEN)
