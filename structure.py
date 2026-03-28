"""
================================================================================
STRUCTURE 01 – Technical Notes for the Developer
================================================================================
1. API:        pyTelegramBotAPI (telebot)
2. Fast Send:  The dictionary `cached_file_ids` stores Telegram file_ids after
               the first send. Subsequent sends use the ID, making images load
               instantly.
3. Security:   Token is read from .env using python-dotenv. NEVER hardcode it,
               and make sure .env is added to .gitignore.
4. Polling:    timeout=90 ensures stability even in Termux environments.
5. Markdown:   All captions use parse_mode='Markdown' for the cyber look.
6. Visual IDs: All image links are stored in `SECTION_LOGOS` for easy updates.
================================================================================
"""

import os
import telebot
from telebot import types
from dotenv import load_dotenv

# ─── Environment & Security ───────────────────────────────────────────────────
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables. Please create a .env file.")
bot = telebot.TeleBot(TOKEN)

# ─── Fast Send Cache (stores Telegram file_ids after first use) ──────────────
cached_file_ids = {}

# ─── Visual Identity – all section logos (easily replaceable) ────────────────
SECTION_LOGOS = {
    "MAIN":      "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4782.jpeg",
    "RECEPTION": "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4793.jpeg",
    "LOGIC":     "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4790.jpeg",
    "SECURITY":  "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4791.jpeg",
    "ARCHIVE":   "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4792.jpeg",
    "CORE":      "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4794.jpeg",
    "STRATEGY":  "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4788.jpeg",
    "VISUAL":    "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4787.jpeg",
    "COMMAND":   "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4780.jpeg"
}

# ─── Button Texts (Constants) ────────────────────────────────────────────────
BTN_RECEPTION = '🤝 قـسـم الاسـتـقـبال ╎ 𝐑𝐄𝐂𝐄𝐏𝐓𝐈𝐎𝐍'
BTN_LOGIC     = '🧠 مُـخـتـبـر الـمـنـطـق ╎ 𝐋𝐎𝐆𝐈𝐂   𝐋𝐀𝐁'
BTN_SEC       = '🛡️ أمـن الـبـيـانـات ╎ 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘   𝐂𝐄𝐍𝐓𝐄𝐑'
BTN_ARCHIVE   = '📂 الأرشــيــف ╎ 𝐓𝐇𝐄   𝐀𝐑𝐂𝐇𝐈𝐕𝐄'
BTN_CORE      = '⚙️ نـواة الـتـطويـر ╎ 𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐌𝐄𝐍𝐓   𝐂𝐎𝐑𝐄'
BTN_VISUAL    = '🎨 واجـهة الـنظام ╎ 𝐕𝐈𝐒𝐔𝐀𝐋   𝐀𝐑𝐂𝐀𝐍𝐄'
BTN_STRATEGY  = '🧠 غـرفـة الاسـتـشـارة ╎ 𝐒𝐓𝐑𝐀𝐓𝐄𝐆𝐘   𝐑𝐎𝐎𝐌'
BTN_DEV       = '👤 الـتواصل مـع الـقـيادة ╎ 𝐇𝐈𝐆𝐇   𝐂𝐎𝐌𝐌𝐀𝐍𝐃'

# ─── Fast Send Engine (caches and sends images) ──────────────────────────────
def send_interface(chat_id, text, reply_markup=None, logo_key="MAIN"):
    """
    Sends a message with an image. On first use, the image is downloaded
    from the URL; later calls use the cached Telegram file_id for speed.
    If sending the image fails, falls back to text-only message.
    """
    image = cached_file_ids.get(logo_key, SECTION_LOGOS.get(logo_key))
    try:
        sent = bot.send_photo(chat_id, image,
                              caption=text,
                              reply_markup=reply_markup,
                              parse_mode='Markdown')
        # Cache the file_id after the first successful send
        if logo_key not in cached_file_ids:
            cached_file_ids[logo_key] = sent.photo[-1].file_id
    except Exception:
        # Fallback: send only text if image fails
        bot.send_message(chat_id, text,
                         reply_markup=reply_markup,
                         parse_mode='Markdown')

# ─── Handlers ────────────────────────────────────────────────────────────────
@bot.message_handler(commands=['start'])
def welcome(message):
    """Start command – shows main menu with all buttons."""
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(BTN_RECEPTION, BTN_LOGIC, BTN_SEC,
               BTN_ARCHIVE, BTN_CORE, BTN_VISUAL,
               BTN_STRATEGY, BTN_DEV)
    text = (f"*//ـ الـتـعـرف عـلى الـهـوية ╎ 𝐒𝐓𝐑𝐔𝐂𝐓𝐔𝐑𝐄   𝟎𝟏*\n\n"
            f"◈ الـمـستخـدم: `{message.from_user.first_name}`\n"
            "\"المنطق هو الحقيقة الوحيدة هنا.\"")
    send_interface(message.chat.id, text, markup, logo_key="MAIN")

@bot.message_handler(func=lambda message: True)   # catches all text messages
def handle_requests(message):
    """Handles button presses and other text inputs."""
    cid = message.chat.id
    txt = message.text

    if txt == BTN_RECEPTION:
        reception_text = (
            "//ـ ســيـسـتـم أريــس تــك ╎ *𝐀𝐑𝐈𝐒𝐄 𝐓𝐄𝐂𝐇* ⚖️\n"
            "— *𝐒𝐭𝐫𝐚𝐭𝐞𝐠𝐢𝐜 𝐈𝐧𝐭𝐞𝐥𝐥𝐢𝐠𝐞𝐧𝐜𝐞* ⚔️ *𝐓𝐞𝐜𝐡 𝐧𝐢𝐜𝐚𝐥 𝐒𝐮𝐩𝐞𝐫𝐢𝐨𝐫𝐢𝐭𝐲* —\n\n"
            "\"الجميع مجرد أدوات، والمبرمج الحق هو من يملك الكود الذي يتحكم في تلك الأدوات.\"\n\n"
            "• 💠 [𝐖𝐞𝐥𝐜𝐨𝐦𝐞   𝐆𝐚𝐭𝐞](https://songjinwoo1.github.io/Bot-Song-Jin-Woo/)\n"
            "• 🐙 𝐆𝐢𝐭𝐇𝐮𝐛 𝐇𝐮𝐛 ↠ `[🔒 Restricted Access]`"
        )
        send_interface(cid, reception_text, logo_key="RECEPTION")
    elif txt == BTN_LOGIC:
        send_interface(cid, "*//ـ مُـخـتـبـر الـمـنـطـق ╎ 𝐋𝐎𝐆𝐈𝐂   𝐋𝐀𝐁*", logo_key="LOGIC")
    elif txt == BTN_SEC:
        send_interface(cid, "*//ـ أمـن الـبـيـانـات ╎ 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘   𝐂𝐄𝐍𝐓𝐄𝐑*", logo_key="SECURITY")
    elif txt == BTN_ARCHIVE:
        send_interface(cid, "*//ـ الأرشـيـف ╎ 𝐓𝐇𝐄   𝐀𝐑𝐂𝐇𝐈𝐕𝐄*", logo_key="ARCHIVE")
    elif txt == BTN_CORE:
        send_interface(cid, "*//ـ نـواة الـتـطويـر ╎ 𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐌𝐄𝐍𝐓   𝐂𝐎𝐑𝐄*", logo_key="CORE")
    elif txt == BTN_VISUAL:
        send_interface(cid, "*//ـ واجـهة الـنـظام ╎ 𝐕𝐈𝐒𝐔𝐀𝐋   𝐀𝐑𝐂𝐀𝐍𝐄*", logo_key="VISUAL")
    elif txt == BTN_STRATEGY:
        send_interface(cid, f"*//ـ غـرفـة الاسـتـشـارة*\n\n\"الهدوء هو قمة القوة.\"", logo_key="STRATEGY")
    elif txt == BTN_DEV:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("𝑺𝒐𝒏𝒈 𝑱𝒊𝒏 𝑾𝒐𝒐", url="https://wa.me/96597805334"))
        markup.add(types.InlineKeyboardButton("𝙺𝚒𝚢𝚘𝚝𝚊𝚔𝚊 𝙰𝚢𝚊𝒏𝚘𝚔𝚘𝚞𝒋𝚒", url="https://wa.me/201055719273"))
        send_interface(cid, "*//ـ قـناة الاتـصال الـعـلـيا ╎ 𝐇𝐈𝐆𝐇   𝐂𝐎𝐌𝐌𝐀𝐍𝐃*", markup, logo_key="COMMAND")

# ─── Main Execution ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("STRUCTURE 01 IS SECURE AND ONLINE...")
    bot.polling(none_stop=True, timeout=90, long_polling_timeout=10)