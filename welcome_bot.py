import os
import json
import logging
import telebot
import google.generativeai as genai
from telebot import types
from datetime import datetime
from dotenv import load_dotenv

# ─── تحميل المتغيرات البيئية ───────────────────────────────────────────
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
AI_KEY = os.getenv("GEMINI_API_KEY")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "529456789").split(",")))

# ─── إعداد التسجيل ─────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ─── التحقق من صحة المتغيرات ───────────────────────────────────────────
if not BOT_TOKEN or not AI_KEY:
    raise ValueError("❌ BOT_TOKEN و GEMINI_API_KEY مطلوبان في ملف .env")

# ─── إعداد الذكاء الاصطناعي ───────────────────────────────────────────
genai.configure(api_key=AI_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

# ─── ملف قاعدة البيانات ───────────────────────────────────────────────
DB_FILE = "authorized_chats.json"

def load_authorized_chats():
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_authorized_chats(chats):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(chats, f, indent=4, ensure_ascii=False)

AUTHORIZED_CHATS = load_authorized_chats()

# ─── نظام الكاش للصور ─────────────────────────────────────────────────
cached_file_ids = {}
DEFAULT_LOGO_URL = "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4793.jpeg"

# ─── دالة توليد الترحيب بالذكاء الاصطناعي ─────────────────────────────
def generate_ai_welcome(name):
    prompt = f"اكتب ترحيباً قصيراً (سطر واحد) بأسلوب غامض وذكي لعضو جديد اسمه {name} انضم لمنظمة Arise Tech."
    try:
        response = ai_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"AI generation failed: {e}")
        return "المنطق هو الحقيقة الوحيدة. مرحباً بك في النظام."

# ─── دالة إرسال الترحيب ───────────────────────────────────────────────
def send_welcome(chat_id, name, uid, username):
    image = cached_file_ids.get("LOGO", DEFAULT_LOGO_URL)
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
        sent = bot.send_photo(chat_id, image, caption=caption, parse_mode='Markdown')
        if "LOGO" not in cached_file_ids:
            cached_file_ids["LOGO"] = sent.photo[-1].file_id
    except Exception as e:
        logger.error(f"Failed to send photo: {e}")
        bot.send_message(chat_id, caption, parse_mode='Markdown')

# ─── أوامر الإدارة (للمديرين فقط) ─────────────────────────────────────
def is_admin(user_id):
    return user_id in ADMIN_IDS

@bot.message_handler(commands=['start'])
def start_command(message):
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
            "/panel – لوحة تحكم سريعة"
        )
    else:
        bot.reply_to(message, "مرحباً بك في نظام Arise. البوت يعمل بشكل آمن.")

@bot.message_handler(commands=['Arise'])
def activate_chat(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if not is_admin(user_id):
        bot.reply_to(message, "🌑 « وحـده الـمـؤسـس يـمـلك سـلطة الإيـقـاظ. »")
        return

    if chat_id in AUTHORIZED_CHATS:
        bot.reply_to(message, "✅ البوت مفعل بالفعل في هذه المجموعة.")
        return

    AUTHORIZED_CHATS.append(chat_id)
    save_authorized_chats(AUTHORIZED_CHATS)
    bot.reply_to(
        message,
        "✅ **بـروتوكول الـسيادة: نـشط**\n"
        "━━━━━━━━━━━━━━\n"
        "◈ الـحالة: مـؤمـن بـواسطة أريـس تـك.\n"
        "◈ الـنظام: الـذكاء الاصـطـناعـي مـفـعـل.\n\n"
        "« الـآن، الـمـجـمـوعة تـحـت سـيـطرتـنا. »",
        parse_mode='Markdown'
    )
    logger.info(f"Admin {user_id} activated bot in chat {chat_id}")

@bot.message_handler(commands=['unauth'])
def deactivate_chat(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "⛔ غير مصرح لك باستخدام هذا الأمر.")
        return

    chat_id = message.chat.id
    if chat_id not in AUTHORIZED_CHATS:
        bot.reply_to(message, "⚠️ هذه المجموعة غير مفعلة أصلاً.")
        return

    AUTHORIZED_CHATS.remove(chat_id)
    save_authorized_chats(AUTHORIZED_CHATS)
    bot.reply_to(message, "✅ تم إلغاء تفعيل البوت في هذه المجموعة.")
    logger.info(f"Admin {message.from_user.id} deactivated chat {chat_id}")

@bot.message_handler(commands=['list_auth'])
def list_authorized(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "⛔ غير مصرح لك باستخدام هذا الأمر.")
        return

    if not AUTHORIZED_CHATS:
        bot.reply_to(message, "📭 لا توجد مجموعات مفعلة حالياً.")
        return

    lines = "\n".join([f"• `{chat}`" for chat in AUTHORIZED_CHATS])
    bot.reply_to(message, f"📋 **المجموعات المفعلة:**\n{lines}", parse_mode='Markdown')

@bot.message_handler(commands=['set_logo'])
def set_logo(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "⛔ غير مصرح لك باستخدام هذا الأمر.")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ الاستخدام: /set_logo <image_url>")
        return

    new_url = args[1]
    try:
        test_sent = bot.send_photo(message.chat.id, new_url, caption="اختبار الصورة الجديدة")
        cached_file_ids["LOGO"] = test_sent.photo[-1].file_id
        bot.reply_to(message, f"✅ تم تحديث صورة الترحيب بنجاح.\nالرابط: {new_url}")
        logger.info(f"Admin {message.from_user.id} changed logo to {new_url}")
    except Exception as e:
        bot.reply_to(message, f"❌ فشل تحميل الصورة. تأكد من صحة الرابط.\nخطأ: {e}")

@bot.message_handler(commands=['panel'])
def admin_panel(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "⛔ غير مصرح لك باستخدام هذا الأمر.")
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("➕ تفعيل هنا", callback_data="activate_here")
    btn2 = types.InlineKeyboardButton("❌ إلغاء تفعيل هنا", callback_data="deactivate_here")
    btn3 = types.InlineKeyboardButton("📋 عرض المفعلة", callback_data="list_auth")
    btn4 = types.InlineKeyboardButton("🖼️ تغيير الصورة", callback_data="change_logo")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "🔧 **لوحة التحكم**\nاختر الإجراء:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_panel_buttons(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك.")
        return

    chat_id = call.message.chat.id

    if call.data == "activate_here":
        if chat_id in AUTHORIZED_CHATS:
            bot.answer_callback_query(call.id, "المجموعة مفعلة بالفعل.")
        else:
            AUTHORIZED_CHATS.append(chat_id)
            save_authorized_chats(AUTHORIZED_CHATS)
            bot.answer_callback_query(call.id, "✅ تم التفعيل بنجاح.")
            bot.send_message(chat_id, "✅ تم تفعيل البوت في هذه المجموعة.")
    elif call.data == "deactivate_here":
        if chat_id not in AUTHORIZED_CHATS:
            bot.answer_callback_query(call.id, "المجموعة غير مفعلة.")
        else:
            AUTHORIZED_CHATS.remove(chat_id)
            save_authorized_chats(AUTHORIZED_CHATS)
            bot.answer_callback_query(call.id, "✅ تم إلغاء التفعيل.")
            bot.send_message(chat_id, "✅ تم إلغاء تفعيل البوت في هذه المجموعة.")
    elif call.data == "list_auth":
        list_authorized(call.message)
        bot.answer_callback_query(call.id)
    elif call.data == "change_logo":
        bot.send_message(chat_id, "أرسل الأمر `/set_logo <url>` لتغيير الصورة.")
        bot.answer_callback_query(call.id)

# ─── معالج دخول الأعضاء الجدد ─────────────────────────────────────────
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    chat_id = message.chat.id

    if chat_id not in AUTHORIZED_CHATS:
        return

    for member in message.new_chat_members:
        if member.is_bot:
            continue

        name = member.first_name
        uid = member.id
        username = f"@{member.username}" if member.username else "لا يـوجـد"
        send_welcome(chat_id, name, uid, username)

# ─── تشغيل البوت ─────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("🛡️ ARISE WELCOME AI IS ONLINE...")
    try:
        bot.polling(none_stop=True, timeout=90, long_polling_timeout=10)
    except Exception as e:
        logger.error(f"Bot stopped: {e}")