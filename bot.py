import discord
from discord.ext import commands
import os
import asyncio
from aiohttp import web

TOKEN = os.getenv("DISCORD_TOKEN")
AUDIT_CHANNEL_ID = 1428018103303802970  # замени на свой канал

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------------------
# Discord-события
# -------------------------------
@bot.event
async def on_ready():
    print(f"✅ Бот запущен как {bot.user}")

@bot.event
async def on_audit_log_entry_create(entry: discord.AuditLogEntry):
    channel = bot.get_channel(AUDIT_CHANNEL_ID)
    if not channel:
        print("⚠️ Канал не найден. Проверь ID.")
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

# -------------------------------
# Мини HTTP-сервер для Render
# -------------------------------
async def handle(request):
    return web.Response(text="Bot is running ✅")

async def start_server():
    app = web.Application()
    app.add_routes([web.get("/", handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)  # порт 10000 для Render
    await site.start()
    print("🌐 Web server running on port 10000")

# -------------------------------
# Запуск бота и сервера
# -------------------------------
async def main():
    # Запуск HTTP-сервера
    bot.loop.create_task(start_server())
    # Запуск Discord-бота
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
