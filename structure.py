import os
import telebot
from telebot import types
import random
import time
from dotenv import load_dotenv

# ─── 1. بـروتـوكـول الـتـشـغـيـل والأمـان ───
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# ─── 2. مـصـفـوفة الـهـوية الـبـصـريـة (𝐑𝐚𝐰   𝐔𝐑𝐋𝐬) ───
# تم دمج رابط القيادة العليا الجديد IMG_4780
SECTION_LOGOS = {
    "MAIN":      "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4782.jpeg",
    "RECEPTION": "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4793.jpeg",
    "LOGIC":     "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4794.jpeg",
    "SECURITY":  "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4791.jpeg",
    "ARCHIVE":   "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4792.jpeg",
    "CORE":      "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4794.jpeg",
    "STRATEGY":  "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4782.jpeg",
    "VISUAL":    "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4782.jpeg",
    "COMMAND":   "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4780.jpeg" # رابط القيادة المحقون
}

# ─── 3. الـثـوابـت والـأزرار ───
BTN_RECEPTION = '🤝 لـوحـة الـمـهـام ╎ 𝐐𝐔𝐄𝐒𝐓   𝐁𝐎𝐀𝐑𝐃'
BTN_LOGIC     = '🧠 مُـخـتـبـر الـمـنـطـق ╎ 𝐋𝐎𝐆𝐈𝐂   𝐋𝐀𝐁'
BTN_SEC       = '🛡️ أمـن الـبـيـانـات ╎ 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘   𝐂𝐄𝐍𝐓𝐄𝐑'
BTN_ARCHIVE   = '📂 الأرشــيــف ╎ 𝐓𝐇𝐄   𝐀𝐑𝐂𝐇𝐈𝐕𝐄'
BTN_CORE      = '⚙️ نـواة الـتـطويـر ╎ 𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐌𝐄𝐍𝐓   𝐂𝐎𝐑𝐄'
BTN_VISUAL    = '🎨 واجـهة الـنـظام ╎ 𝐕𝐈𝐒𝐔𝐀𝐋   𝐀𝐑𝐂𝐀𝐍𝐄'
BTN_STRATEGY  = '🧠 غـرفـة الاسـتـشـارة ╎ 𝐒𝐓𝐑𝐀𝐓𝐄𝐆𝐘   𝐑𝐎𝐎𝐌'
BTN_DEV       = '👤 الـتواصل مـع الـقـيادة ╎ 𝐇𝐈𝐆𝐇   𝐂𝐎𝐌𝐌𝐀𝐍𝐃'

# ─── 4. مـحـرك الإرسـال الـتـقـني ───
def send_interface(chat_id, text, reply_markup=None, logo_key="MAIN"):
    photo_url = SECTION_LOGOS.get(logo_key, SECTION_LOGOS["MAIN"])
    try:
        bot.send_photo(chat_id, photo_url, caption=text, reply_markup=reply_markup, parse_mode='Markdown')
    except:
        bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode='Markdown')

# ─── 5. بـروتـوكـول الـتـرحـيـب (/start) ───
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(BTN_RECEPTION, BTN_LOGIC)
    markup.add(BTN_SEC, BTN_ARCHIVE)
    markup.add(BTN_CORE, BTN_VISUAL)
    markup.add(BTN_STRATEGY, BTN_DEV)

    text = (
        f"*//ـ الـتـعـرف عـلى الـهـوية ╎ 𝐒𝐓𝐑𝐔𝐂𝐓𝐔𝐑𝐄   𝟎𝟏*\n\n"
        f"◈ الـمـستخـدم: `{message.from_user.first_name}`\n"
        "\"المنطق هو الحقيقة الوحيدة هنا.\""
    )
    send_interface(message.chat.id, text, markup, logo_key="MAIN")

# ─── 6. مـعـالـج الـأوامـر والـأقـسـام ───
@bot.message_handler(content_types=['text'])
def handle_requests(message):
    cid = message.chat.id
    txt = message.text

    if txt == BTN_RECEPTION:
        send_interface(cid, "*//ـ لـوحـة الـمـهـام ╎ 𝐐𝐔𝐄𝐒𝐓   𝐁𝐎𝐀𝐑𝐃*", logo_key="RECEPTION")
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
        tips = ["\"المنطق سلاح.\"", "\"تخلص من الثغرات العاطفية.\"", "\"السيادة لمن يملك البيانات.\""]
        send_interface(cid, f"*//ـ غـرفـة الاسـتـشـارة ╎ 𝐒𝐓𝐑𝐀𝐓𝐄𝐆𝐘   𝐑𝐎𝐎𝐌*\n\n{random.choice(tips)}", logo_key="STRATEGY")
    elif txt == BTN_DEV:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("𝑺𝒐𝒏𝒈 𝑱𝒊𝒏 𝑾𝒐𝒐", url="https://wa.me/96597805334"))
        markup.add(types.InlineKeyboardButton("𝙺𝚒𝚢𝚘𝚝𝚊𝚔𝚊 𝙰𝚢𝚊𝚗𝚘𝚔𝚘𝚞𝚓𝚒", url="https://wa.me/201055719273"))
        send_interface(cid, "*//ـ قـناة الاتـصال الـعـلـيا ╎ 𝐇𝐈𝐆𝐇   𝐂𝐎𝐌𝐌𝐀𝐍𝐃*", markup, logo_key="COMMAND")

if __name__ == "__main__":
    print("STRUCTURE 01 IS SECURE AND ONLINE...")
    bot.polling(none_stop=True)
