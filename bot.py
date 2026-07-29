import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True  # สำคัญมาก: ต้องเปิดเพื่ออ่านข้อความ "เบลอ้วน" ได้

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------------------------------
# 📌 กำหนด Discord User ID ที่อนุญาตให้ใช้คำสั่งได้คนเดียว
# (นำ ID ของคุณมาวางแทนที่ตัวเลขด้านล่างนี้ได้เลยครับ)
# ----------------------------------------------------
ALLOWED_USER_ID =  933529869487321161

# ----------------------------------------------------
# 1. ข้อมูลยศ (Roles Data)
# ----------------------------------------------------
ROLES_DATA = [
    # Staff / Admin
    {"name": "👑 OWNER", "color": discord.Color.from_rgb(255, 215, 0)},
    {"name": "💠 CO-OWNER", "color": discord.Color.from_rgb(0, 255, 255)},
    {"name": "⚜️ MANAGER", "color": discord.Color.from_rgb(186, 85, 211)},
    {"name": "🛡️ ADMIN", "color": discord.Color.from_rgb(220, 20, 60)},
    {"name": "🔨 MODERATOR", "color": discord.Color.from_rgb(255, 140, 0)},
    {"name": "⭐ STAFF", "color": discord.Color.from_rgb(255, 215, 0)},
    {"name": "🎫 SUPPORT", "color": discord.Color.from_rgb(30, 144, 255)},
    {"name": "🎉 EVENT", "color": discord.Color.from_rgb(255, 105, 180)},
    {"name": "🎨 DESIGNER", "color": discord.Color.from_rgb(147, 112, 219)},
    {"name": "🤖 BOT", "color": discord.Color.from_rgb(112, 128, 144)},
    
    # VIP / Special
    {"name": "💜 BOOSTER", "color": discord.Color.from_rgb(244, 127, 255)},
    {"name": "💎 VIP+", "color": discord.Color.from_rgb(0, 191, 255)},
    {"name": "✨ VIP", "color": discord.Color.from_rgb(255, 223, 0)},
    {"name": "🌟 MEMBER+", "color": discord.Color.from_rgb(50, 205, 50)},
    
    # Member / Community Roles
    {"name": "👤 MEMBER", "color": discord.Color.from_rgb(169, 169, 169)},
    {"name": "🌱 NEW MEMBER", "color": discord.Color.from_rgb(144, 238, 144)},
    {"name": "🎮 GAMER", "color": discord.Color.from_rgb(138, 43, 226)},
    {"name": "🎨 CREATOR", "color": discord.Color.from_rgb(255, 160, 122)},
    {"name": "💬 CHATTY", "color": discord.Color.from_rgb(255, 182, 193)},
    {"name": "🌙 NIGHT OWL", "color": discord.Color.from_rgb(72, 61, 139)},
    {"name": "🐱 CAT LOVER", "color": discord.Color.from_rgb(255, 228, 196)},
]

# ----------------------------------------------------
# 2. ข้อมูลหมวดหมู่และช่อง (Categories & Channels)
# ----------------------------------------------------
CATEGORIES_DATA = {
    "📌｜INFORMATION": {
        "text": ["📜│กฎ", "📢│ประกาศ", "🎭│รับยศ", "👋│ยินดีต้อนรับ", "🚪│คนเข้า-ออก"],
        "voice": []
    },
    "💬｜COMMUNITY": {
        "text": ["💬│แชททั่วไป", "🌙│คุยกลางคืน", "😂│มีม", "📸│อวดรูป", "🎨│ผลงาน", "🎮│เกม", "🎵│เพลง", "🤝│หาเพื่อน", "💭│ระบาย", "☕│คุยเรื่อยเปื่อย"],
        "voice": []
    },
    "🎉｜EVENT": {
        "text": ["🎁│แจกของ", "🏆│กิจกรรม", "📅│อีเวนต์"],
        "voice": []
    },
    "🔊｜VOICE": {
        "text": [],
        "voice": ["🎙️│General 1", "🎙️│General 2", "🎮│Gaming", "🎵│Music", "😴│AFK"]
    },
    "🛡️｜SUPPORT": {
        "text": ["🎫│Ticket", "❓│ช่วยเหลือ", "🐞│แจ้งบั๊ก", "💡│เสนอแนะ"],
        "voice": []
    },
    "👑｜STAFF": {
        "text": ["📋│Staff Chat", "📢│Staff Notice", "📝│Logs"],
        "voice": []
    }
}

# ----------------------------------------------------
# 3. ระบบตรวจจับข้อความ "เบลอ้วน"
# ----------------------------------------------------
@bot.event
async def on_message(message):
    # ป้องกันไม่ให้บอทอ่านข้อความตัวเอง
    if message.author.bot:
        return

    # เช็กว่าพิมพ์คำว่า "เบลอ้วน" หรือไม่
    if message.content.strip() == "เบลอ้วน":
        # เช็ก ID ผู้ใช้ว่าตรงกับที่อนุญาตหรือไม่
        if message.author.id != ALLOWED_USER_ID:
            await message.channel.send("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!")
            return

        guild = message.guild
        await message.channel.send("⚠️ **ได้รับคำสั่งแล้ว! กำลังเริ่มจัดโครงสร้างเซิร์ฟเวอร์ใหม่...**")

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

# ดึง Token จาก Variable ใน Railway
TOKEN = os.getenv("DISCORD_TOKEN") or "YOUR_BOT_TOKEN_HERE"
bot.run(TOKEN)
