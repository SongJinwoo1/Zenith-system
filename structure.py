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

# ─── 2. مـصـفـوفة الـهـوية الـبـصـريـة (المحدثة بـروابـطك الـجديدة) ───
# تم تصحيح الروابط لتعمل مباشرة (Raw) داخل التلجرام
SECTION_LOGOS = {
    "MAIN":      "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4782.jpeg",
    "RECEPTION": "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4789.jpeg",
    "LOGIC":     "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4790.jpeg",
    "SECURITY":  "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4791.jpeg",
    "ARCHIVE":   "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4792.jpeg",
    "CORE":      "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4794.jpeg",
    "STRATEGY":  "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4788.jpeg",
    "VISUAL":    "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4787.jpeg",
    "COMMAND":   "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4780.jpeg"
}

# ─── 3. الـثـوابـت والـأزرار ───
BTN_RECEPTION = '🤝 قـسـم الاسـتـقـبال ╎ 𝐑𝐄𝐂𝐄𝐏𝐓𝐈𝐎𝐍'
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
    except Exception as e:
        print(f"Error sending photo: {e}")
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
        msg = (
            "*//ـ قـسـم الاسـتـقـبال ╎ 𝐑𝐄𝐂𝐄𝐏𝐓𝐈𝐎𝐍*\n\n"
            "\"مرحباً بك في بوابـة أريـس تـك. السيادة تبدأ من هنا.\"\n\n"
            "• [Welcome Gate](https://songjinwoo1.github.io/Bot-Song-Jin-Woo/)"
        )
        send_interface(cid, msg, logo_key="RECEPTION")
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
        tips = ["\"المنطق سلاح.\"", "\"السيادة لمن يملك البيانات.\"", "\"الهدوء هو قمة القوة.\""]
        send_interface(cid, f"*//ـ غـرفـة الاسـتـشـارة ╎ 𝐒𝐓𝐑𝐀𝐓𝐄𝐆𝐘   𝐑𝐎𝐎𝐌*\n\n{random.choice(tips)}", logo_key="STRATEGY")
    elif txt == BTN_DEV:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("𝑺𝒐𝒏𝒈 𝑱𝒊𝒏 𝑾𝒐𝒐", url="https://wa.me/96597805334"))
        markup.add(types.InlineKeyboardButton("𝙺𝚒𝚢𝚘𝚝𝚊𝚔𝚊 𝙰𝚢𝚊𝒏𝚘𝚔𝒐𝒖𝒋𝚒", url="https://wa.me/201055719273"))
        send_interface(cid, "*//ـ قـناة الاتـصال الـعـلـيا ╎ 𝐇𝐈𝐆𝐇   𝐂𝐎𝐌𝐌𝐀𝐍𝐃*", markup, logo_key="COMMAND")

if __name__ == "__main__":
    print("STRUCTURE 01 IS SECURE AND ONLINE...")
    bot.polling(none_stop=True)
