import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_USER_ID = 933529869487321161  # เปลี่ยนเป็น Discord User ID ของคุณ

# ยศคงเดิม
ROLES_DATA = [
    {"name": "👑 ผู้อำนวยการโรงเรียน", "color": discord.Color.from_rgb(255, 215, 0)},
    {"name": "🔱 รองผู้อำนวยการ", "color": discord.Color.from_rgb(238, 130, 238)},
    {"name": "📜 อาจารย์ใหญ่", "color": discord.Color.from_rgb(186, 85, 211)},
    {"name": "🧑‍🏫 อาจารย์", "color": discord.Color.from_rgb(100, 149, 237)},
    {"name": "🪽 อาจารย์ฝ่ายเทพ", "color": discord.Color.from_rgb(255, 255, 224)},
    {"name": "😈 อาจารย์ฝ่ายปีศาจ", "color": discord.Color.from_rgb(139, 0, 0)},
    {"name": "⚔️ ผู้ฝึกสอนการต่อสู้", "color": discord.Color.from_rgb(220, 20, 60)},
    {"name": "✨ ผู้สอนเวทมนตร์", "color": discord.Color.from_rgb(147, 112, 219)},
    {"name": "🩺 แพทย์ประจำโรงเรียน", "color": discord.Color.from_rgb(60, 179, 113)},
    {"name": "👑 ประธานนักเรียน", "color": discord.Color.from_rgb(255, 140, 0)},
    {"name": "🥇 รองประธานนักเรียน", "color": discord.Color.from_rgb(255, 165, 0)},
    {"name": "📋 เลขาประธานนักเรียน", "color": discord.Color.from_rgb(255, 215, 0)},
    {"name": "🎓 นักเรียนปี 3", "color": discord.Color.from_rgb(70, 130, 180)},
    {"name": "🎓 นักเรียนปี 2", "color": discord.Color.from_rgb(100, 149, 237)},
    {"name": "🎓 นักเรียนปี 1", "color": discord.Color.from_rgb(173, 216, 230)},
    {"name": "🪽 สายเทพ", "color": discord.Color.from_rgb(240, 248, 255)},
    {"name": "☀️ เทพฝึกหัด", "color": discord.Color.from_rgb(255, 250, 205)},
    {"name": "✨ เทพ", "color": discord.Color.from_rgb(255, 223, 0)},
    {"name": "😈 ปีศาจ", "color": discord.Color.from_rgb(75, 0, 130)},
    {"name": "💚จ่ายเซิฟ", "color": discord.Color.from_rgb(50, 205, 50)},
    {"name": "✅️ผ่านสัม", "color": discord.Color.from_rgb(46, 204, 113)},
    {"name": "🔄รอสัม", "color": discord.Color.from_rgb(241, 196, 15)},
]

# หมวดหมู่และช่องที่ปรับปรุงแล้ว
CATEGORIES_DATA = {
    "✦━━🏫 โรงเรียนเทพปีศาจ ━━✦": {
        "text": ["📜กฎโรงเรียน", "📢ประกาศโรงเรียน", "📖ประวัติโรงเรียน", "🗺️แผนที่โรงเรียน", "🎓ระบบการเรียน", "🏆ระบบคะแนน"],
        "voice": []
    },
    "✦━━🌸 ต้อนรับนักเรียน ━━✦": {
        "text": ["🐰welcome", "🎖️รับยศ", "✅ยืนยันตัวตน", "🌸แนะนำตัว", "👋goodbye"],
        "voice": []
    },
    "✦━━📚 การเรียน ━━✦": {
        "text": ["📖ตารางเรียน", "🏫ห้องเรียน", "📝การบ้าน", "⚔️ฝึกต่อสู้", "✨ฝึกเวทมนตร์", "🧪ปรุงยา", "📜การสอบ"],
        "voice": []
    },
    "✦━━🪽 เทพ ━━✦": {
        "text": ["☀️หอเทพ", "🪽พูดคุยเทพ", "✨พลังศักดิ์สิทธิ์", "👑สายเลือดเทพ"],
        "voice": []
    },
    "✦━━😈 ปีศาจ ━━✦": {
        "text": ["🔥หอปีศาจ", "😈พูดคุยปีศาจ", "🌑พลังปีศาจ", "👑สายเลือดปีศาจ"],
        "voice": []
    },
    "✦━━🐉 เผ่าพันธุ์ ━━✦": {
        "text": ["🐉เผ่ามังกร", "🦊เผ่าจิ้งจอก", "🐺เผ่าสัตว์อสูร", "🧚เผ่านางฟ้า", "🌙เผ่าพิเศษ"],
        "voice": []
    },
    "✦━━🎭 ตัวละคร ━━✦": {
        "text": ["🌸แนะนำตัวละคร", "📋แบบฟอร์มตัวละคร", "📨ส่งแบบฟอร์ม", "✅ตัวละครผ่าน", "📚ทะเบียนนักเรียน"],
        "voice": []
    },
    "✦━━🎬 โรลเพลย์ ━━✦": { # ปรับตรงนี้ให้เป็นช่องเสียงทั้งหมด
        "text": [],
        "voice": ["🏫 โรงเรียน", "🌳 สวนโรงเรียน", "📚 ห้องสมุด", "⚔️ สนามประลอง", "🌲 ป่าต้องห้าม", "🏰 ปราสาท", "🌌 พื้นที่ลับ"]
    },
    "✦━━💬 ชุมชน ━━✦": {
        "text": ["💬พูดคุย", "📸ส่งรูป-วิดีโอ", "🎨fanart", "🎵เพลง", "😂มีม"],
        "voice": []
    }
}

@bot.event
async def on_message(message):
    if message.author.bot: return

    if message.content.strip() == "เบลอ้วน":
        if message.author.id != ALLOWED_USER_ID:
            await message.channel.send("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!")
            return

        guild = message.guild
        await message.channel.send("⚠️ **กำลังเริ่มสร้างเซิร์ฟเวอร์โรงเรียนเทพปีศาจ (โหมดโรลเพลย์ช่องเสียง)...**")

        # ลบห้องเก่า
        for channel in guild.channels:
            try: await channel.delete()
            except: pass

        # สร้างยศ
        for role_info in ROLES_DATA:
            try: await guild.create_role(name=role_info["name"], color=role_info["color"], hoist=True)
            except: pass
            await asyncio.sleep(0.2)

        # สร้างช่อง
        for cat_name, data in CATEGORIES_DATA.items():
            category = await guild.create_category(cat_name)
            for txt_name in data["text"]: await guild.create_text_channel(txt_name, category=category)
            for vc_name in data["voice"]: await guild.create_voice_channel(vc_name, category=category)
            await asyncio.sleep(0.3)

        await message.channel.send("✅ **ตั้งค่าเสร็จสิ้น!**")

    await bot.process_commands(message)

TOKEN = os.getenv("DISCORD_TOKEN") or "YOUR_BOT_TOKEN_HERE"
bot.run(TOKEN)
