from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ChatType
import asyncio
import logging

# 🔐 Token va admin ID
BOT_TOKEN = "7560330694:AAGjC_g33E5pCrhPvwtF2K8meY1hM__D9T8"
ADMIN_ID = 6589444343  # bu yerga o'z Telegram ID'ingizni yozing

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 📌 Taksi zakazlarini aniqlovchi kalit so'zlar
KEYWORDS = [
    "taksi", "taxi", "zakaz", "manzil", "yetkazib", "pochta", "dastavka" "buyurtma", "buyurtma berish", "yetkazish", "tashish", "tashish xizmati",
    "boraman", "kelaman", "yuboring", "jo'nat", "yo'nalish", "gaplashamiz", "aloqa", "aloqa uchun", "aloqa raqami", "telefon", "telefon raqami", "aloqaga", "Andijon", "Buxoro", "Farg‘ona", "Jizzax", "Xorazm", "Namangan", "Navoiy", "Qashqadaryo", "Samarqand", "Sirdaryo", "Surxondaryo", "Toshkent", "viloyati", "dan", "ga", "kerak", "bugunga", "ertaga", "ertalab" "kechga"
]

# 🔍 Zakaz ekanligini tekshiruvchi funksiya
def is_order_message(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in KEYWORDS)

@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def group_order_handler(message: Message):
    if message.text and is_order_message(message.text):
        try:
            user = message.from_user
            chat = message.chat

            # 🔹 Profil havola
            profile_link = f'<a href="tg://user?id={user.id}">{user.full_name}</a>'
            
            # 🔹 Xabar havola (guruh public emas bo‘lsa ishlamasligi mumkin)
            try:
                msg_link = f"https://t.me/c/{str(chat.id)[4:]}/{message.message_id}"
            except:
                msg_link = "Link mavjud emas"

            # 🧾 Formatlangan ma’lumot
            info = f"""
📥 <b>Yangi zakaz aniqlandi!</b>

📍 <b>Guruh:</b> {chat.title}
🔗 <b>Xabar havolasi:</b> <a href="{msg_link}">Ko‘rish</a>

👤 <b>Ism:</b> {user.full_name}
🆔 <b>Telegram ID:</b> <code>{user.id}</code>
🏷 <b>Username:</b> @{user.username if user.username else "Mavjud emas"}
🔗 <b>Profil havolasi:</b> {profile_link}

💬 <b>Xabar matni:</b>
<code>{message.text}</code>
"""

            # 👮‍♂️ Adminga yuborish
            await bot.send_message(chat_id=ADMIN_ID, text=info, parse_mode="HTML", disable_web_page_preview=True)

            # 📩 Asl xabarni forward qilish
            await bot.forward_message(chat_id=ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)

            # 🗑️ Guruhdan o‘chirish (admin bo‘lsa)
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            except:
                pass  # admin emas bo‘lsa, xatolik chiqmasin

        except Exception as e:
            await bot.send_message(chat_id=ADMIN_ID, text=f"❗Xatolik: {e}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
