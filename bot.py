import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# รายชื่อยศพร้อมสี (ปรับเปลี่ยนสีตามใจชอบได้ครับ)
ROLES_DATA = [
    {"name": "🌑 Owner", "color": discord.Color.from_rgb(30, 30, 30)},
    {"name": "🌙 Co-Owner", "color": discord.Color.from_rgb(100, 100, 150)},
    {"name": "🐈‍⬛ Admin", "color": discord.Color.from_rgb(50, 50, 50)},
    {"name": "⭐ Staff", "color": discord.Color.from_rgb(241, 196, 15)},
    {"name": "🎨 Designer", "color": discord.Color.from_rgb(155, 89, 182)},
    {"name": "🖌️ Artist", "color": discord.Color.from_rgb(230, 126, 34)},
    {"name": "💎 Premium", "color": discord.Color.from_rgb(52, 152, 219)},
    {"name": "🛍️ Customer", "color": discord.Color.from_rgb(46, 204, 113)},
    {"name": "🐾 Member", "color": discord.Color.from_rgb(149, 165, 166)},
]

# โครงสร้างหมวดหมู่และช่องทั้งหมด
CATEGORIES_DATA = {
    "🌙 Welcome & Goodbye": [
        "【🌙】︱ยินดีต้อนรับ",
        "【🐾】︱รับยศ",
        "【📜】︱เริ่มต้นที่นี่",
        "【🖤】︱ลาจาก"
    ],
    "🔔 Important": [
        "【📢】︱ประกาศ",
        "【✨】︱อัปเดตสินค้า",
        "【🌑】︱กฎร้าน",
        "【👑】︱ยศทั้งหมด",
        "【🎁】︱กิจกรรม",
        "【📌】︱คำถามที่พบบ่อย"
    ],
    "🐈‍⬛ Skin Shop": [
        "【🎨】︱สกินทั้งหมด",
        "【🔥】︱สกินใหม่",
        "【⭐】︱สกินแนะนำ",
        "【💎】︱สกินพรีเมียม",
        "【🛒】︱โปรโมชั่น",
        "【🖼️】︱ตัวอย่างงาน",
        "【📂】︱ผลงานที่ผ่านมา"
    ],
    "🌙 Rate & Order": [
        "【💰】︱เรทราคา",
        "【📝】︱วิธีสั่งงาน",
        "【📋】︱ฟอร์มสั่งงาน",
        "【💳】︱ช่องทางชำระเงิน",
        "【🧾】︱แจ้งโอน"
    ],
    "🎫 Ticket Support": [
        "【🎫】︱เปิดตั๋ว",
        "【❓】︱สอบถาม",
        "【⚒️】︱แจ้งปัญหา",
        "【💬】︱ติดต่อแอดมิน"
    ],
    "🌌 Community": [
        "【🌸】︱พูดคุย",
        "【📸】︱โชว์สกิน",
        "【😂】︱มีม",
        "【🎮】︱เกม",
        "【🐈】︱รูปแมว"
    ],
    "👑 Staff": [
        "【📢】︱ประกาศทีมงาน",
        "【📈】︱สถิติ",
        "【📝】︱งานสตาฟ",
        "【🔒】︱ห้องทีมงาน"
    ],
    "🎫 ระบบกดตั๋ว": [
        "🎨 สั่งซื้อสกิน",
        "❓ สอบถาม",
        "💸 แจ้งโอน",
        "⚠️ แจ้งปัญหา",
        "🤝 ติดต่อสตาฟ"
    ]
}

@bot.command()
@commands.is_owner() # เซฟความปลอดภัย: อนุญาตเฉพาะ "เจ้าของบอท" เท่านั้นที่สั่งได้
async def setup_server(ctx):
    guild = ctx.guild
    await ctx.send("⚠️ **กำลังเริ่มกระบวนการ Reset และรีเซ็ตโครงสร้างเซิร์ฟเวอร์...**")

    # ----------------------------------------------------
    # 1. ลบช่องเดิมทั้งหมด
    # ----------------------------------------------------
    print("กำลังลบห้องเก่าทั้งหมด...")
    for channel in guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(0.3) # หน่วงเวลาเล็กน้อยกัน Rate Limit
        except Exception as e:
            print(f"ไม่สามารถลบช่อง {channel.name} ได้: {e}")

    # ----------------------------------------------------
    # 2. สร้างยศ (Roles)
    # ----------------------------------------------------
    print("กำลังสร้างยศ...")
    for role_info in ROLES_DATA:
        # เช็คว่ามียศนี้อยู่แล้วหรือยัง ถ้ายังไม่มีค่อยสร้าง
        existing_role = discord.utils.get(guild.roles, name=role_info["name"])
        if not existing_role:
            try:
                await guild.create_role(
                    name=role_info["name"],
                    color=role_info["color"],
                    hoist=True # แสดงแยกกลุ่มในรายชื่อสมาชิกด้านขวา
                )
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"ไม่สามารถสร้างยศ {role_info['name']} ได้: {e}")

    # ----------------------------------------------------
    # 3. สร้างหมวดหมู่และห้องใหม่
    # ----------------------------------------------------
    print("กำลังสร้างหมวดหมู่และห้องใหม่...")
    for cat_name, channels in CATEGORIES_DATA.items():
        # สร้าง Category
        category = await guild.create_category(cat_name)
        await asyncio.sleep(0.5)

        # สร้าง Text Channel ด้านใน Category
        for channel_name in channels:
            await guild.create_text_channel(channel_name, category=category)
            await asyncio.sleep(0.4)

    print("เสร็จสิ้นการตั้งค่าเซิร์ฟเวอร์!")

bot.run("YOUR_BOT_TOKEN_HERE")
