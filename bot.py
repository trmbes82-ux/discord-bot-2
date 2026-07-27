import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# Roles
# =========================
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

# =========================
# Categories
# =========================
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


@bot.event
async def on_ready():
    print(f"ล็อกอินเป็น {bot.user}")
    print("Bot Online!")


@bot.command()
@commands.is_owner()
async def setup_server(ctx):
    guild = ctx.guild

    await ctx.send("⚠️ กำลังรีเซ็ตและสร้างเซิร์ฟเวอร์...")

    # ลบทุกช่อง
    for channel in guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(0.3)
        except Exception as e:
            print(e)

    # สร้าง Roles
    for role in ROLES_DATA:
        if discord.utils.get(guild.roles, name=role["name"]) is None:
            try:
                await guild.create_role(
                    name=role["name"],
                    color=role["color"],
                    hoist=True
                )
                await asyncio.sleep(0.3)
            except Exception as e:
                print(e)

    # สร้าง Categories และ Channels
    for category_name, channels in CATEGORIES_DATA.items():
        category = await guild.create_category(category_name)
        await asyncio.sleep(0.5)

        for channel_name in channels:
            await guild.create_text_channel(
                channel_name,
                category=category
            )
            await asyncio.sleep(0.3)

    await ctx.send("✅ ตั้งค่าเซิร์ฟเวอร์เสร็จแล้ว!")


# =========================
# TOKEN จาก Environment Variable
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError(
        "ไม่พบ DISCORD_TOKEN กรุณาเพิ่ม Environment Variable ชื่อ DISCORD_TOKEN"
    )

bot.run(TOKEN)
