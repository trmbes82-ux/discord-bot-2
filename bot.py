import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True  # ต้องเปิด Message Content Intent ใน Discord Developer Portal

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------------------------------
# 📌 ID ผู้ใช้ที่ได้รับอนุญาตให้ใช้คำสั่งได้คนเดียว
# ----------------------------------------------------
ALLOWED_USER_ID = 933529869487321161  # เปลี่ยนเป็น Discord User ID ของคุณ

# ----------------------------------------------------
# 1. ข้อมูลยศใหม่ (Roles Data - ธีมเรือนจำ)
# ----------------------------------------------------
ROLES_DATA = [
    {"name": "👑 เจ้าของเรือนจำ", "color": discord.Color.from_rgb(255, 215, 0)},
    {"name": "🛡️ ผู้ดูแล", "color": discord.Color.from_rgb(220, 20, 60)},
    {"name": "👮 ผู้คุม", "color": discord.Color.from_rgb(30, 144, 255)},
    {"name": "🧪 นักวิจัย", "color": discord.Color.from_rgb(186, 85, 211)},
    {"name": "⚔️ ผู้คุมสนามประลอง", "color": discord.Color.from_rgb(255, 140, 0)},
    {"name": "⛓️ นักโทษ", "color": discord.Color.from_rgb(112, 128, 144)},
    {"name": "🧬 ผู้ทดลอง", "color": discord.Color.from_rgb(0, 255, 127)},
    {"name": "🏆 นักประลอง", "color": discord.Color.from_rgb(255, 69, 0)},
    {"name": "👤 ผู้เล่น", "color": discord.Color.from_rgb(169, 169, 169)},
]

# ----------------------------------------------------
# 2. ข้อมูลหมวดหมู่และช่องธีมเรือนจำ (Categories & Channels)
# ----------------------------------------------------
CATEGORIES_DATA = {
    "🚪・PRISON GATE": {
        "text": ["📥・ผู้ต้องขังเข้าใหม่", "📤・ผู้ต้องขังออกจากเรือนจำ"],
        "voice": []
    },
    "🔒・PRISON INFORMATION": {
        "text": [
            "📜・กฎเรือนจำ", "📢・ประกาศจากผู้คุม", "📖・เนื้อเรื่อง", 
            "🗺️・แผนผังเรือนจำ", "🎮・วิธีเข้าเล่น", "📋・สมัครตัวละคร", "🎖️・รับยศ"
        ],
        "voice": []
    },
    "🎤・INTERVIEW ZONE": {
        "text": ["📋・ห้องสัมภาษณ์", "🎙️・สัมภาษณ์เข้าเซิร์ฟ", "📝・ผลสัมภาษณ์"],
        "voice": []
    },
    "🎤・โซนสัมภาษณ์": {
        "text": [],
        "voice": ["🔊・ห้องสัมภาษณ์・01", "🔊・ห้องสัมภาษณ์・02", "🔊・ห้องสัมภาษณ์・03"]
    },
    "🧪・LABORATORY": {
        "text": ["🧬・ห้องทดลอง", "🔬・ข้อมูลการทดลอง", "📁・แฟ้มผู้ทดลอง", "🩸・การทดลองพิเศษ", "⚠️・เหตุการณ์ผิดปกติ"],
        "voice": []
    },
    "⚔️・ARENA": {
        "text": ["🏟️・สนามประลอง", "📜・กติกาการประลอง", "⚔️・ประกาศคู่ต่อสู้", "🏆・อันดับนักโทษ", "💀・ประลองพิเศษ"],
        "voice": []
    },
    "🏠・PRISON COMMUNITY": {
        "text": ["💬・ห้องพูดคุย", "😂・มีมคุก", "📸・ภาพจากเซิร์ฟ", "🎵・ห้องเพลง", "🤖・บอท"],
        "voice": []
    },
    "🎭・ROLEPLAY START": {
        "text": ["📍・จุดเริ่มต้น", "📝・ลงทะเบียนนักโทษ", "🎫・รับหมายเลขนักโทษ", "🚪・ประตูเรือนจำ", "📢・เรียกเข้าโซน"],
        "voice": []
    },
    "🎙️・ROLEPLAY ZONE": {
        "text": [],
        "voice": [
            "🔊・VC・เริ่มต้น", "🔊・VC・01", "🔊・VC・02", "🔊・VC・03", "🔊・VC・04", 
            "🔊・VC・05", "🔊・VC・06", "🔊・VC・07", "🔊・VC・08", "🔊・VC・09", 
            "🔊・VC・10", "🔊・VC・11", "🔊・VC・12", "🔊・VC・13", "🔊・VC・14", 
            "🔊・VC・15", "🔊・VC・16", "🔊・VC・17", "🔊・VC・18", "🔊・VC・19", "🔊・VC・20"
        ]
    },
    "👮・PRISON STAFF": {
        "text": ["🔐・ห้องผู้คุม", "📋・รายงานนักโทษ", "🚨・แจ้งเหตุฉุกเฉิน", "🧪・ฝ่ายวิจัย", "⚔️・ฝ่ายสนามประลอง", "📂・แฟ้มคดี", "💬・Staff Chat"],
        "voice": []
    },
    "🛠️・SYSTEM": {
        "text": ["🤖・คำสั่งบอท", "📊・สถิติเซิร์ฟ", "📝・บันทึกระบบ", "🚨・Logs"],
        "voice": []
    }
}

# ----------------------------------------------------
# 3. ระบบตรวจจับข้อความ "เบลอ้วน"
# ----------------------------------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.strip() == "เบลอ้วน":
        if message.author.id != ALLOWED_USER_ID:
            await message.channel.send("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!")
            return

        guild = message.guild
        await message.channel.send("⚠️ **กำลังเริ่มรีเซ็ตเซิร์ฟเวอร์และสร้างอาณาจักรเรือนจำใหม่...**")

        # 1. ลบช่องเดิมทั้งหมด
        print("กำลังลบห้องเก่า...")
        for channel in guild.channels:
            try:
                await channel.delete()
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"ลบช่อง {channel.name} ไม่ได้: {e}")

        # 2. สร้างยศใหม่
        print("กำลังสร้างยศ...")
        for role_info in ROLES_DATA:
            existing_role = discord.utils.get(guild.roles, name=role_info["name"])
            if not existing_role:
                try:
                    await guild.create_role(
                        name=role_info["name"],
                        color=role_info["color"],
                        hoist=True
                    )
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"สร้างยศ {role_info['name']} ไม่ได้: {e}")

        # 3. สร้างหมวดหมู่ และช่อง (Text / Voice)
        print("กำลังสร้างหมวดหมู่และช่อง...")
        for cat_name, data in CATEGORIES_DATA.items():
            category = await guild.create_category(cat_name)
            await asyncio.sleep(0.5)

            # สร้าง Text Channels
            for txt_name in data["text"]:
                await guild.create_text_channel(txt_name, category=category)
                await asyncio.sleep(0.3)

            # สร้าง Voice Channels
            for vc_name in data["voice"]:
                await guild.create_voice_channel(vc_name, category=category)
                await asyncio.sleep(0.3)

        print("ตั้งค่าเซิร์ฟเวอร์ธีมเรือนจำเรียบร้อยแล้ว!")

    await bot.process_commands(message)

# ดึง Token จาก Variable บน Railway
TOKEN = os.getenv("DISCORD_TOKEN") or "YOUR_BOT_TOKEN_HERE"
bot.run(TOKEN)
