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
ALLOWED_USER_ID = 123456789012345678  # เปลี่ยนเป็น Discord User ID ของคุณ

# ----------------------------------------------------
# 1. ข้อมูลยศใหม่ (Roles Data)
# ----------------------------------------------------
ROLES_DATA = [
    {"name": "👑 Owner", "color": discord.Color.from_rgb(255, 215, 0)},
    {"name": "🌙 Co-Owner", "color": discord.Color.from_rgb(100, 149, 237)},
    {"name": "🛡️ Admin", "color": discord.Color.from_rgb(220, 20, 60)},
    {"name": "⚔️ Moderator", "color": discord.Color.from_rgb(255, 140, 0)},
    {"name": "⭐ Staff", "color": discord.Color.from_rgb(255, 215, 0)},
    {"name": "🎉 Event Team", "color": discord.Color.from_rgb(255, 105, 180)},
    {"name": "🤖 Bot", "color": discord.Color.from_rgb(112, 128, 144)},
    {"name": "💎 Booster", "color": discord.Color.from_rgb(244, 127, 255)},
    {"name": "🌸 VIP", "color": discord.Color.from_rgb(255, 182, 193)},
    {"name": "🎮 Gamer", "color": discord.Color.from_rgb(138, 43, 226)},
    {"name": "👤 Member", "color": discord.Color.from_rgb(169, 169, 169)},
]

# ----------------------------------------------------
# 2. ข้อมูลหมวดหมู่และช่อง (Categories & Channels)
# ----------------------------------------------------
CATEGORIES_DATA = {
    "🌌WELCOME": {
        "text": [
            "👋│ยินดีต้อนรับ", "📜│กฎเซิร์ฟเวอร์", "📢│ประกาศ", 
            "📖│แนะนำตัว", "🎭│รับยศ", "🎨│เลือกสีชื่อ", "📌│ข้อมูลเซิร์ฟเวอร์"
        ],
        "voice": []
    },
    "💬COMMUNITY": {
        "text": [
            "💬│แชททั่วไป", "☕│นั่งคุยชิล", "😂│มีม", "📷│รูปภาพ", 
            "🎬│คลิป", "🎵│แชร์เพลง", "🍜│ของกิน", "🐶│สัตว์เลี้ยง", "🎨│ผลงาน"
        ],
        "voice": []
    },
    "🎮GAMING": {
        "text": [
            "🎮│หาเพื่อนเล่นเกม", "🕹️│Minecraft", "🔫│Valorant", 
            "🚗│Roblox", "⚔️│League of Legends", "🎲│เกมอื่นๆ", "📺│ไลฟ์สตรีมเกม"
        ],
        "voice": []
    },
    "🎙️VOICE • CHILL": {
        "text": [],
        "voice": ["☕│ชิล 1", "☕│ชิล 2", "☕│ชิล 3", "☕│ชิล 4"]
    },
    "🎮VOICE • GAMING": {
        "text": [],
        "voice": [
            "🎮│เล่นเกม 1", "🎮│เล่นเกม 2", "🎮│เล่นเกม 3", 
            "🎮│เล่นเกม 4", "🎮│เล่นเกม 5"
        ]
    },
    "🎵VOICE • MUSIC": {
        "text": [],
        "voice": ["🎵│ฟังเพลง 1", "🎵│ฟังเพลง 2", "🎵│ฟังเพลง 3", "🎵│คาราโอเกะ"]
    },
    "📺VOICE • MOVIE": {
        "text": [],
        "voice": ["📺│ดูหนัง 1", "📺│ดูหนัง 2", "📺│ดูซีรีส์", "🍿│อนิเมะ"]
    },
    "😴VOICE • SLEEP": {
        "text": [],
        "voice": ["😴│ห้องนอน 1", "😴│ห้องนอน 2", "😴│ห้องนอน 3", "🌙│หลับยาว", "💤│งีบพัก"]
    },
    "🤝FIND FRIENDS": {
        "text": [
            "💞│หาเพื่อน", "💕│หาเพื่อนคุย", "👥│หาทีม", 
            "🎮│นัดเล่นเกม", "🎤│หาเพื่อนเข้าไมค์"
        ],
        "voice": []
    },
    "🎉EVENT": {
        "text": [
            "🎁│กิจกรรม", "🏆│การแข่งขัน", "🎂│อวยพรวันเกิด", 
            "📸│รูปกิจกรรม", "🎊│แจกของรางวัล"
        ],
        "voice": []
    },
    "🛠️SUPPORT": {
        "text": ["❓│ช่วยเหลือ", "📩│แจ้งปัญหา", "💡│เสนอแนะ", "🎫│เปิด Ticket"],
        "voice": []
    },
    "👑STAFF": {
        "text": ["📋│สตาฟแชท", "📝│บันทึก", "🚨│รายงาน", "📢│ประกาศทีมงาน"],
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
        await message.channel.send("⚠️ **กำลังเริ่มรีเซ็ตเซิร์ฟเวอร์และสร้างโครงสร้างใหม่ทั้งหมด...**")

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

        print("ตั้งค่าเซิร์ฟเวอร์เรียบร้อยแล้ว!")

    await bot.process_commands(message)

# ดึง Token จาก Variable บน Railway
TOKEN = os.getenv("DISCORD_TOKEN") or "YOUR_BOT_TOKEN_HERE"
bot.run(TOKEN)
