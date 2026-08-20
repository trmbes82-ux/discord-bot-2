import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------------------------------
# ตั้งค่า ID ผู้ใช้ที่อนุญาตให้รันคำสั่ง (เปลี่ยนเป็น ID ของคุณ)
# ----------------------------------------------------
ALLOWED_USER_ID = 123456789012345678 

# ----------------------------------------------------
# 1. ยศใหม่ (Roles)
# ----------------------------------------------------
ROLES_DATA = [
    {"name": "👑 ทีมดูแล", "color": discord.Color.gold()},
    {"name": "👑 เจ้าของเซิร์ฟ", "color": discord.Color.red()},
    {"name": "🛡️ ผู้ดูแล", "color": discord.Color.blue()},
    {"name": "🔨 แอดมิน", "color": discord.Color.dark_blue()},
    {"name": "🔧 ม็อด", "color": discord.Color.green()},
    {"name": "🎫 ทีมซัพพอร์ต", "color": discord.Color.teal()},
    {"name": "⭐ สมาชิกพิเศษ", "color": discord.Color.gold()},
    {"name": "💎 VIP", "color": discord.Color.blue()},
    {"name": "🌟 Premium", "color": discord.Color.purple()},
    {"name": "🎨 Creator", "color": discord.Color.magenta()},
    {"name": "🎮 Gamer", "color": discord.Color.orange()},
    {"name": "🧑 สมาชิก", "color": discord.Color.light_gray()},
    {"name": "🌸 สมาชิก", "color": discord.Color.lighter_gray()},
    {"name": "🌱 สมาชิกใหม่", "color": discord.Color.green()},
    {"name": "🤖 บอท", "color": discord.Color.dark_grey()},
    {"name": "🎭 บทบาทเล่นๆ", "color": discord.Color.default()},
    {"name": "🌙 สายดึก", "color": discord.Color.dark_purple()},
    {"name": "☀️ สายเช้า", "color": discord.Color.yellow()},
    {"name": "🎮 สายเกม", "color": discord.Color.blue()},
    {"name": "🎵 สายเพลง", "color": discord.Color.red()},
    {"name": "🤣 สายฮา", "color": discord.Color.orange()},
    {"name": "💬 นักคุย", "color": discord.Color.blue()},
    {"name": "💤 AFK", "color": discord.Color.dark_grey()},
]

# ----------------------------------------------------
# 2. หมวดหมู่และช่อง (Categories & Channels)
# ----------------------------------------------------
STRUCTURE = {
    "🌟 หมวดหลัก": {
        "text": ["💬｜ห้องคุยเล่น", "🎮｜คุยเกม", "🤣｜มีม-ฮาๆ", "📸｜แชร์รูป", "🎵｜เพลง", "🤖｜คุยกับบอท"],
        "voice": []
    },
    "🔊 ห้องเสียง": {
        "text": [],
        "voice": ["🔊｜ห้องคุยเล่น 1", "🔊｜ห้องคุยเล่น 2", "🎮｜เล่นเกม", "🎵｜ฟังเพลง", "💤｜ห้อง AFK"]
    },
    "🎫 ห้องช่วยเหลือ": {
        "text": ["🎫｜เปิดตั๋ว", "📢｜ประกาศ", "📜｜กฎเซิร์ฟเวอร์"],
        "voice": []
    }
}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # คำสั่งลับสำหรับเริ่มสร้าง (พิมพ์ในดิสคอร์ด)
    if message.content.strip() == "เริ่มสร้างเซิร์ฟ":
        if message.author.id != ALLOWED_USER_ID:
            await message.channel.send("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!")
            return

        guild = message.guild
        await message.channel.send("⚠️ **กำลังเริ่มจัดระเบียบเซิร์ฟเวอร์ตามโครงสร้างใหม่...**")

        # 1. ลบช่องและหมวดหมู่เก่า (ระวัง: ข้อมูลหายทั้งหมด)
        for channel in guild.channels:
            try:
                await channel.delete()
            except: pass

        # 2. สร้างยศใหม่
        for role_info in ROLES_DATA:
            try:
                await guild.create_role(name=role_info["name"], color=role_info["color"], hoist=True)
            except: pass
            await asyncio.sleep(0.2)

        # 3. สร้างหมวดหมู่และช่องใหม่
        for cat_name, data in STRUCTURE.items():
            category = await guild.create_category(cat_name)
            await asyncio.sleep(0.3)
            
            for txt_name in data["text"]:
                await guild.create_text_channel(txt_name, category=category)
            
            for vc_name in data["voice"]:
                await guild.create_voice_channel(vc_name, category=category)

        await message.channel.send("✅ **จัดระเบียบเซิร์ฟเวอร์สำเร็จแล้ว!**")

    await bot.process_commands(message)

# รันบอท
TOKEN = os.getenv("DISCORD_TOKEN") or "YOUR_BOT_TOKEN_HERE"
bot.run(TOKEN)
