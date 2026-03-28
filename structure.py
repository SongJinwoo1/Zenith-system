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

# ─── 2. مـصـفـوفة الـهـوية الـبـصـريـة (المحدثة) ───
SECTION_LOGOS = {
    "MAIN":      "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4782.jpeg",
    "RECEPTION": "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4793.jpeg", # الرابط الجديد
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
        reception_text = (
            "//ـ ســيـسـتـم أريــس تــك ╎ *𝐀𝐑𝐈𝐒𝐄 𝐓𝐄𝐂𝐇* ⚖️\n"
            "— *𝐒𝐭𝐫𝐚𝐭𝐞𝐠𝐢𝐜 𝐈𝐧𝐭𝐞𝐥𝐥𝐢𝐠𝐞𝐧𝐜𝐞* ⚔️ *𝐓𝐞𝐜𝐡 n𝐢𝐜𝐚𝐥 𝐒𝐮𝐩𝐞𝐫𝐢𝐨𝐫𝐢𝐭𝐲* —\n\n"
            "\"الجميع مجرد أدوات، والمبرمج الحق هو من يملك الكود الذي يتحكم في تلك الأدوات. نحن لا نُعلمك، نحن نُعيد برمجتك لتسود.\"\n\n"
            "🌑 ━━━━━━━━━━━━━━ 🌑\n\n"
            "✦ *روابـط الـسـيـادة (𝐒𝐭𝐫𝐚𝐭𝐞𝐠𝐢𝐜   𝐋𝐢𝐧𝐤𝐬):*\n"
            "• 💠 [𝐖𝐞𝐥𝐜𝐨𝐦𝐞   𝐆𝐚𝐭𝐞](https://songjinwoo1.github.io/Bot-Song-Jin-Woo/)\n"
            "• 🐙 𝐆𝐢𝐭𝐇𝐮𝐛 𝐇𝐮𝐛 ↠ `[🔒 Restricted Access]`\n"
            "*(المستودع متاح حالياً للنخبة فقط؛ سيتم فتحه تدريجياً مع اكتمال القوة).* \n\n"
            "🛠️ ━━━━━━━━━━━━━━ 🛠️\n\n"
            "✦ *الـمـسـارات الـمـدعـومـة:*\n"
            "◈ الـويب ◈ الـذكاء ◈ الأمـن ◈ الـتطبيقات\n\n"
            "🏆 ━━━━━━━━━━━━━━ 🏆\n\n"
            "✦ *الـقـيـادة (𝐒𝐲𝐬𝐭𝐞𝐦   𝐇𝐢𝐞𝐫𝐚𝐫𝐜𝐡𝐲):*\n"
            "• 𝐒𝐭𝐫𝐚𝐭𝐞𝐠𝐢𝐜 𝐋𝐞𝐚𝐝 ♜ ↠ *𝑺𝒐𝒏𝒈 𝑱𝒊𝒏 𝑾𝒐𝒐*\n"
            "• 𝐒𝐨𝐯𝐞𝐫𝐞𝐢𝐠𝐧 𝐄𝐱𝐞𝐜𝐮𝐭𝐨𝐫 👑 ↠ ⟨*𝙺𝚒𝚢𝚘𝚝𝚊𝚔𝚊 𖦹 𝙰𝚢𝚊𝚗𝚘𝚔𝚘𝚞𝚓𝚒*⟩\n\n"
            "🔗 ━━━━━━━━━━━━━━ 🔗\n"
            "𝐒𝐢𝐧𝐜𝐞 𝟐𝟎𝟐𝟔 ╎ 𝐀𝐑𝐈𝐒𝐄 𝐓𝐄𝐂𝐇 ╎ *𝐋𝐞𝐯𝐞𝐥 𝐔𝐩 𝐘𝐨𝐮𝐫 𝐑𝐞𝐚𝐥𝐢𝐭𝐲* 🌌"
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
        tips = ["\"المنطق سلاح.\"", "\"الهدوء هو قمة القوة.\""]
        send_interface(cid, f"*//ـ غـرفـة الاسـتـشـارة ╎ 𝐒𝐓𝐑𝐀𝐓𝐄𝐆𝐘   𝐑𝐎𝐎𝐌*\n\n{random.choice(tips)}", logo_key="STRATEGY")
    elif txt == BTN_DEV:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("𝑺𝒐𝒏𝒈 𝑱𝒊𝒏 𝑾𝒐𝒐", url="https://wa.me/96597805334"))
        markup.add(types.InlineKeyboardButton("𝙺𝚒𝚢𝚘𝚝𝚊𝚔𝚊 𝙰𝚢𝚊𝚗𝚘𝚔𝚘𝚞𝚓𝚒", url="https://wa.me/201055719273"))
        send_interface(cid, "*//ـ قـناة الاتـصال الـعـلـيا ╎ 𝐇𝐈𝐆𝐇   𝐂𝐎𝐌𝐌𝐀𝐍𝐃*", markup, logo_key="COMMAND")

if __name__ == "__main__":
    print("STRUCTURE 01 IS SECURE AND ONLINE...")
    bot.polling(none_stop=True)
