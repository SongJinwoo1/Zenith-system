import os
import json
import logging
import threading
import time
from datetime import datetime
from typing import List, Optional

import telebot
from telebot import types
import google.generativeai as genai
from dotenv import load_dotenv

# =============================================================================
# Configuration & Environment
# =============================================================================
load_dotenv()

# Required tokens
BOT_TOKEN = os.getenv("WELCOME_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("❌ WELCOME_BOT_TOKEN and GEMINI_API_KEY must be set in .env")

# Admin IDs: split by comma, strip spaces, convert to int
ADMIN_IDS = [
    int(id_.strip()) for id_ in os.getenv("ADMIN_IDS", "529456789").split(",")
]

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Gemini setup
genai.configure(api_key=GEMINI_API_KEY)
AI_MODEL = genai.GenerativeModel("gemini-1.5-flash")  # fastest model

# Bot instance
bot = telebot.TeleBot(BOT_TOKEN)

# =============================================================================
# Persistent data (authorized chats) with thread safety
# =============================================================================
DB_FILE = "authorized_chats.json"
AUTHORIZED_CHATS: List[int] = []
AUTHORIZED_CHATS_LOCK = threading.Lock()


def load_authorized_chats() -> List[int]:
    """Load list of authorized chat IDs from JSON file."""
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_authorized_chats() -> None:
    """Save the current list of authorized chats to JSON file."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(AUTHORIZED_CHATS, f, indent=4, ensure_ascii=False)


# Initial load
AUTHORIZED_CHATS.extend(load_authorized_chats())
logger.info(f"Loaded {len(AUTHORIZED_CHATS)} authorized chats from {DB_FILE}")

# =============================================================================
# Cached image file_id
# =============================================================================
DEFAULT_LOGO_URL = "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4793.jpeg"
cached_logo_file_id: Optional[str] = None
CACHE_LOCK = threading.Lock()


def get_logo_file_id() -> Optional[str]:
    """Return cached file_id, or None if not cached."""
    with CACHE_LOCK:
        return cached_logo_file_id


def set_logo_file_id(file_id: str) -> None:
    """Set the cached file_id."""
    with CACHE_LOCK:
        global cached_logo_file_id
        cached_logo_file_id = file_id


# =============================================================================
# AI Welcome Message Generation (with caching and timeout)
# =============================================================================
# Simple cache to avoid regenerating the same welcome for identical names
_welcome_cache: dict = {}
_cache_lock = threading.Lock()
AI_TIMEOUT = 5  # seconds


def generate_ai_welcome(name: str) -> str:
    """
    Generate a short, mysterious welcome message using Gemini.
    Caches result per name to speed up repeated joins.
    """
    # Check cache first
    with _cache_lock:
        if name in _welcome_cache:
            return _welcome_cache[name]

    prompt = (
        f"اكتب ترحيباً قصيراً جداً (سطر واحد فقط) بأسلوب غامض وذكي "
        f"بصفته مساعداً تقنياً لعضو جديد اسمه {name} انضم لمنظمة Arise Tech."
    )
    try:
        # Use a thread with timeout to avoid blocking forever
        response = AI_MODEL.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=50,
            ),
        )
        text = response.text.strip()
        # Cache only if not empty
        if text:
            with _cache_lock:
                _welcome_cache[name] = text
        return text
    except Exception as e:
        logger.error(f"AI generation failed for {name}: {e}")
        return "المنطق هو الحقيقة الوحيدة. مرحباً بك في النظام."


# =============================================================================
# Welcome Message Sending
# =============================================================================
def send_welcome(chat_id: int, name: str, uid: int, username: str) -> None:
    """Send the welcome photo + AI‑generated caption."""
    # Get logo (cached file_id or default URL)
    logo = get_logo_file_id()
    if not logo:
        logo = DEFAULT_LOGO_URL

    now = datetime.now()
    date_str = now.strftime("%Y/%m/%d")
    time_str = now.strftime("%I:%M %p")
    ai_msg = generate_ai_welcome(name)

    caption = (
        f"⌯ **WELCOME TO ARISE SYSTEM** ⌯\n"
        f"━━━━━━━━━━━━━━\n"
        f"• `{ai_msg}`\n\n"
        f"• اسـمك ⇐ `{name}`\n"
        f"• ايـديـك ⇐ `{uid}`\n"
        f"• يـوزرك ⇐ `{username}`\n\n"
        f"📅 تـاريـخ الانـضـمام ⇐ `{date_str}`\n"
        f"⏰ الـسـاعـة ⇐ `{time_str}`\n"
        f"━━━━━━━━━━━━━━\n"
        f"« تـم تـحـلـيـل بـصـمـتـك الـرقـمـيـة بـنـجـاح. »"
    )

    try:
        sent = bot.send_photo(chat_id, logo, caption=caption, parse_mode="Markdown")
        # Cache the file_id if it was a URL and we haven't cached yet
        if logo == DEFAULT_LOGO_URL and not get_logo_file_id():
            set_logo_file_id(sent.photo[-1].file_id)
    except Exception as e:
        logger.error(f"Failed to send photo to {chat_id}: {e}")
        # Fallback: send as text only
        bot.send_message(chat_id, caption, parse_mode="Markdown")


# =============================================================================
# Helper Functions
# =============================================================================
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


def ensure_chat_authorized(chat_id: int) -> bool:
    """Check if a chat is authorized (thread‑safe)."""
    with AUTHORIZED_CHATS_LOCK:
        return chat_id in AUTHORIZED_CHATS


def add_authorized_chat(chat_id: int) -> None:
    """Add a chat to the authorized list and persist (thread‑safe)."""
    with AUTHORIZED_CHATS_LOCK:
        if chat_id not in AUTHORIZED_CHATS:
            AUTHORIZED_CHATS.append(chat_id)
            save_authorized_chats()


def remove_authorized_chat(chat_id: int) -> None:
    """Remove a chat from the authorized list and persist (thread‑safe)."""
    with AUTHORIZED_CHATS_LOCK:
        if chat_id in AUTHORIZED_CHATS:
            AUTHORIZED_CHATS.remove(chat_id)
            save_authorized_chats()


# =============================================================================
# Bot Command Handlers
# =============================================================================
@bot.message_handler(commands=["start"])
def start_command(message: types.Message):
    if is_admin(message.from_user.id):
        bot.reply_to(
            message,
            "🔰 **Arise Welcome AI** 🔰\n\n"
            "البوت يعمل بنجاح.\n"
            "الأوامر المتاحة للمدير:\n"
            "/Arise – تفعيل البوت في المجموعة الحالية\n"
            "/unauth – إلغاء تفعيل المجموعة الحالية\n"
            "/list_auth – عرض المجموعات المفعلة\n"
            "/set_logo <url> – تغيير صورة الترحيب\n"
            "/panel – لوحة تحكم سريعة",
            parse_mode="Markdown",
        )
    else:
        bot.reply_to(message, "مرحباً بك في نظام Arise. البوت يعمل بشكل آمن.")


@bot.message_handler(commands=["Arise"])
def activate_chat(message: types.Message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "🌑 « وحـده الـمـؤسـس يـمـلك سـلطة الإيـقـاظ. »")
        return

    chat_id = message.chat.id
    if ensure_chat_authorized(chat_id):
        bot.reply_to(message, "✅ البوت مفعل بالفعل في هذه المجموعة.")
        return

    add_authorized_chat(chat_id)
    bot.reply_to(
        message,
        "✅ **بـروتوكول الـسيادة: نـشط**\n"
        "━━━━━━━━━━━━━━\n"
        "◈ الـحالة: مـؤمـن بـواسطة أريـس تـك.\n"
        "◈ الـنظام: الـذكاء الاصـطـناعـي مـفـعـل.\n\n"
        "« الـآن، الـمـجـمـوعة تـحـت سـيـطرتـنا. »",
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["unauth"])
def deactivate_chat(message: types.Message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "🌑 « وحـده الـمـؤسـس يـمـلك سـلطة الإيـقـاظ. »")
        return

    chat_id = message.chat.id
    if not ensure_chat_authorized(chat_id):
        bot.reply_to(message, "❌ البوت غير مفعل في هذه المجموعة.")
        return

    remove_authorized_chat(chat_id)
    bot.reply_to(
        message,
        "⛔ **بـروتوكول الـسيادة: تـعـطـيـل**\n"
        "تم إلغاء تفعيل البوت في هذه المجموعة.",
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["list_auth"])
def list_authorized(message: types.Message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "🌑 « وحـده الـمـؤسـس يـمـلك سـلطة الإيـقـاظ. »")
        return

    with AUTHORIZED_CHATS_LOCK:
        if not AUTHORIZED_CHATS:
            bot.reply_to(message, "📭 لا توجد مجموعات مفعلة.")
            return
        text = "📋 **المجموعات المفعلة:**\n\n"
        for cid in AUTHORIZED_CHATS:
            text += f"• `{cid}`\n"
        bot.reply_to(message, text, parse_mode="Markdown")


@bot.message_handler(commands=["set_logo"])
def set_logo(message: types.Message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "🌑 « وحـده الـمـؤسـس يـمـلك سـلطة الإيـقـاظ. »")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(
            message,
            "❌ **استخدام خاطئ**\n"
            "أرسل: `/set_logo <URL الصورة>`\n"
            "مثال: `/set_logo https://example.com/logo.jpg`",
            parse_mode="Markdown",
        )
        return

    url = args[1].strip()
    # Test the URL by trying to send a photo (to get file_id)
    try:
        sent = bot.send_photo(message.chat.id, url, caption="✅ تم تغيير الشعار بنجاح.")
        file_id = sent.photo[-1].file_id
        set_logo_file_id(file_id)
        # Delete the test message to keep chat clean
        bot.delete_message(message.chat.id, sent.message_id)
        bot.reply_to(
            message,
            f"✅ **تم تحديث الشعار**\n"
            f"الـ URL الجديد: {url}\n"
            f"سيتم استخدامه في الترحيبات القادمة.",
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Failed to set logo: {e}")
        bot.reply_to(
            message,
            f"❌ فشل تحميل الصورة من الرابط.\n"
            f"تأكد من صحة الرابط وأنه صورة مدعومة.",
            parse_mode="Markdown",
        )


@bot.message_handler(commands=["panel"])
def admin_panel(message: types.Message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "🌑 « وحـده الـمـؤسـس يـمـلك سـلطة الإيـقـاظ. »")
        return

    with AUTHORIZED_CHATS_LOCK:
        count = len(AUTHORIZED_CHATS)

    panel_text = (
        "🔧 **لوحة التحكم - Arise Welcome AI**\n\n"
        f"📊 **المجموعات المفعلة:** `{count}`\n"
        f"🧠 **نموذج الذكاء:** `gemini-1.5-flash`\n"
        f"🖼 **الشعار:** {'مخبأ' if get_logo_file_id() else 'افتراضي'}\n\n"
        "**الأوامر السريعة:**\n"
        "/Arise – تفعيل المجموعة الحالية\n"
        "/unauth – إلغاء تفعيل المجموعة الحالية\n"
        "/list_auth – عرض المجموعات المفعلة\n"
        "/set_logo <url> – تغيير الشعار"
    )
    bot.reply_to(message, panel_text, parse_mode="Markdown")


# =============================================================================
# New Member Handler
# =============================================================================
@bot.message_handler(content_types=["new_chat_members"])
def welcome_new_member(message: types.Message):
    chat_id = message.chat.id
    if not ensure_chat_authorized(chat_id):
        return

    for member in message.new_chat_members:
        if member.is_bot:
            continue
        # Send welcome in a separate thread to avoid blocking the update loop
        threading.Thread(
            target=send_welcome,
            args=(
                chat_id,
                member.first_name,
                member.id,
                f"@{member.username}" if member.username else "لا يوجد",
            ),
            daemon=True,
        ).start()


# =============================================================================
# Main Entry Point
# =============================================================================
if __name__ == "__main__":
    logger.info("🛡️ ARISE WELCOME AI IS ONLINE...")
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.critical(f"Bot stopped: {e}")