
from balethon import Client
from balethon.conditions import private, is_joined
from balethon.objects import InlineKeyboard, InlineKeyboardButton
from local_config import TOKEN
import os
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = Path(os.getenv("PDF_PATH", str(BASE_DIR / "rahnama_valed.pdf")))

bot = Client(TOKEN)

CHANNEL_ID = 6068445854
CHANNEL_URL = "https://ble.ir/kidiko1405"

JOIN_REQUIRED_TEXT = (
    "برای استفاده از امکانات ربات کیدیکو، ابتدا عضو کانال ما شوید. 🌱\n\n"
    "پس از عضویت، دوباره دستور موردنظر را اجرا کنید."
)


# Menus

def main_menu():
    return InlineKeyboard(
        [("📄 دریافت PDF", "pdf")],
        [("👤 پروفایل", "profile")],
        [("⚙️ تنظیمات", "settings"), ("❓ راهنما", "help")],
    )


def back_menu():
    return InlineKeyboard(
        [("🏠 منوی اصلی", "home")]
    )


def membership_menu():
    return InlineKeyboard(
        [
            InlineKeyboardButton(
                text="📢 عضویت در کانال",
                url=CHANNEL_URL,
            )
        ]
    )


# Page texts

HOME_TEXT = (
    "سلام! 👋\n"
    "به کیدیکو خوش اومدی🌱\n\n"
    "اینجا قراره بهترین و جذاب‌ترین چیزهایی که برای بچه‌ها پیدا می‌شه رو بهت معرفی کنیم؛\n"
    "از کتاب و محصولات کمک‌آموزشی گرفته تا لباس، کفش، اسباب‌بازی، لوازم مدرسه و کلی چیز جذاب دیگه.\n\n"
    "اما فقط معرفی محصول نیست!\n"
    "گاهی قراره یه انتخاب خوب بهت پیشنهاد بدیم،\n"
    "گاهی یه محصول خفن رو زودتر از بقیه ببینی،\n"
    "و گاهی هم یه هدیه کوچیک مهمون ما باشی. 🎁\n\n"
    "فقط کافیه عضو کانال کیدیکو بشی تا کتاب‌ها رو دریافت کنی.👇\n"
    "@kidiko1405\n"
    "بزن بریم 🚀"
)

HELP_TEXT = (
    "❓ راهنمای ربات کیدیکو\n"
    "از طریق منوی ربات می‌توانید به بخش‌های مختلف دسترسی داشته باشید.\n\n"
    "📄 دریافت PDF\n"
    "/pdf: برای دریافت فایل‌های PDF در دسترس.\n\n"
    "👤 پروفایل\n"
    "/profile: برای مشاهده اطلاعات حساب کاربری.\n\n"
    "⚙️ تنظیمات\n"
    "/settings: برای مشاهده تنظیمات ربات.\n\n"
    "/start: 🏠 منوی اصلی\n"
    "برای بازگشت به صفحه اصلی ربات."
)

PROFILE_TEXT = (
    "👤 پروفایل کاربری\n\n"
    "به بخش پروفایل کیدیکو خوش آمدید.\n"
    "برای مشاهده شناسه کاربری خود، دستور /profile را ارسال کنید."
)

SETTINGS_TEXT = (
    "⚙️ تنظیمات\n\n"
    "در حال حاضر، گزینه‌ای برای تغییر تنظیمات فعال نیست.\n"
    "امکانات جدید در نسخه‌های آینده اضافه خواهند شد."
)

PDF_TEXT = (
    "❗️برای دریافت PDF روی دستور زیر کلیک کن.❗️\n"
    "📘 کتاب راهنمای والدین برای پیش‌دبستانی "
    "(انتشارات بین‌المللی آبرنگ): \n"
    "/pdf_rahnama_valed\n\n"
    "⚠️ ارسال فایل ممکنه طول بکشه لطفا صبور باشید."
)

# Check membership for non-start messages

@bot.on_message(private & ~is_joined(CHANNEL_ID))
async def require_membership(*, message):
    text = (message.text or "").strip()

    command = text.split(maxsplit=1)[0] if text else ""
    command = command.split("@")[0]

    # Send the welcome message to non-members too
    if command == "/start":
        await message.reply(
            HOME_TEXT,
            reply_markup=main_menu(),
        )
        return

    # Ignore empty messages
    if not text:
        return

    await message.reply(
        JOIN_REQUIRED_TEXT,
        reply_markup=membership_menu(),
    )


# Start command: available to everyone

@bot.on_command(private, name="start")
async def start(*, message):
    await message.reply(
        HOME_TEXT,
        reply_markup=main_menu(),
    )



# Text commands: members only

@bot.on_command(private & is_joined(CHANNEL_ID), name="help")
async def help_command(*, message):
    await message.reply(
        HELP_TEXT,
        reply_markup=back_menu(),
    )


@bot.on_command(private & is_joined(CHANNEL_ID), name="profile")
async def profile_command(*, message):
    user = message.author

    await message.reply(
        f"👤 پروفایل کاربری\n\n"
        f"شناسه کاربری: {user.id}",
        reply_markup=back_menu(),
    )


@bot.on_command(private & is_joined(CHANNEL_ID), name="settings")
async def settings_command(*, message):
    await message.reply(
        SETTINGS_TEXT,
        reply_markup=back_menu(),
    )


@bot.on_command(private & is_joined(CHANNEL_ID), name="pdf")
async def pdf_command(*, message):
    await message.reply(
        PDF_TEXT,
        reply_markup=back_menu(),
    )


# Send the parents' guide PDF: members only

@bot.on_command(
    private & is_joined(CHANNEL_ID),
    name="pdf_rahnama_valed",
)
async def pdf_rahnama_valed_command(*, message):
    print("PDF command received")
    print(f"PDF path: {PDF_PATH}")
    print(f"PDF exists: {PDF_PATH.is_file()}")

    if not PDF_PATH.is_file():
        await message.reply(
            "❌ فایل PDF پیدا نشد.\n"
            "لطفاً فایل rahnama_valed.pdf را در پوشه ربات قرار دهید."
        )
        return

    try:
        print("Sending PDF...")
        await message.reply_document(
            str(PDF_PATH),
            caption=(
                "📘 کتاب راهنمای والدین برای پیش‌دبستانی\n"
                "انتشارات بین‌المللی آبرنگ"
            ),
        )
        print("PDF sent successfully.")

    except Exception:
        logging.exception("Failed to send PDF")
        await message.reply(
            "❌ هنگام ارسال فایل مشکلی پیش آمد. لطفاً دوباره تلاش کنید."
        )


# Handle callback queries from menu buttons

@bot.on_callback_query()
async def button_handler(callback_query):
    data = callback_query.data

    # Check membership before allowing menu actions
    try:
        member = await is_joined(CHANNEL_ID)(
            bot,
            callback_query.message,
        )
    except Exception:
        logging.exception("Failed to check channel membership")
        await callback_query.answer(
            "بررسی عضویت ناموفق بود. لطفاً دوباره تلاش کنید."
        )
        return

    if not member:
        try:
            await callback_query.answer("ابتدا عضو کانال شوید.")
        except Exception:
            pass

        await callback_query.message.edit_text(
            JOIN_REQUIRED_TEXT,
            reply_markup=membership_menu(),
        )
        return

    if data == "home":
        text = HOME_TEXT
        keyboard = main_menu()

    elif data == "help":
        text = HELP_TEXT
        keyboard = back_menu()

    elif data == "profile":
        try:
            await callback_query.answer(" ")
        except Exception:
            pass

        user = getattr(callback_query, "author", None)

        if user is None:
            await callback_query.message.reply(
                "امکان شناسایی کاربر وجود ندارد."
            )
            return

        await callback_query.message.reply(
            f"👤 پروفایل کاربری\n\n"
            f"شناسه کاربری: {user.id}",
            reply_markup=back_menu(),
        )
        return

    elif data == "settings":
        text = SETTINGS_TEXT
        keyboard = back_menu()

    elif data == "pdf":
        text = PDF_TEXT
        keyboard = back_menu()

    elif data == "pdf_rahnama_valed":
        try:
            await callback_query.answer(" ")
        except Exception:
            pass

        await pdf_rahnama_valed_command(
            message=callback_query.message
        )
        return

    else:
        try:
            await callback_query.answer("Invalid option.")
        except Exception:
            pass
        return

    try:
        await callback_query.answer(" ")
    except Exception:
        pass

    await callback_query.message.edit_text(
        text,
        reply_markup=keyboard,
    )


bot.run()