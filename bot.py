from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
import qrcode
import os

from config import BOT_TOKEN, CONFIG_PATH_RU, CONFIG_PATH_US, DOMAIN_RU, DOMAIN_US, XRAY_RESTART_CMD
from vpn_utils import add_user

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_cmd(msg: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🇷🇺 Россия", "🇺🇸 США")
    await msg.reply("Привет! Выбери сервер:", reply_markup=kb)

from ssh_utils import add_user_ssh
from config import SSH_SERVERS

@dp.message_handler(lambda msg: msg.text in ["🇷🇺 Россия", "🇺🇸 США"])
async def region_selected(msg: types.Message):
    await msg.reply("⚙️ Подготавливаем доступ...")

    user_id = msg.from_user.id
    region = "ru" if msg.text == "🇷🇺 Россия" else "us"
    ssh_config = SSH_SERVERS[region]

    try:
        new_uuid, out, err = add_user_ssh(
            host=ssh_config["host"],
            port=ssh_config["port"],
            username=ssh_config["username"],
            password=ssh_config["password"],
            config_path=ssh_config["config_path"],
            user_id=user_id
        )
    except Exception as e:
        await msg.reply(f"❌ Ошибка при подключении к серверу: {e}")
        return

    # Сборка VLESS-ссылки
    domain = ssh_config["domain"]
    link = f"vless://{new_uuid}@{domain}:443?encryption=none&security=tls&type=ws&host={domain}&path=%2Fvpn#VPN-{region.upper()}"

    # QR
    qr = qrcode.make(link)
    qr_path = f"{user_id}_vpn_qr.png"
    qr.save(qr_path)

    await bot.send_message(msg.chat.id, f"✅ Готово!\nВот твоя VLESS-ссылка:\n`{link}`", parse_mode="Markdown")
    await bot.send_photo(msg.chat.id, photo=InputFile(qr_path))
    os.remove(qr_path)


if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

