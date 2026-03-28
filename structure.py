import os
import telebot
from telebot import types
import random
import time
from dotenv import load_dotenv

# ─── 1. بـروتـوكـول الـتـشـغـيـل والأمـان ───
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("⚠️ خـطأ: لـم يتم الـعثور على BOT_TOKEN")
    exit()

bot = telebot.TeleBot(TOKEN)

# ─── 2. مـصـفـوفة الـهـوية الـبـصـريـة (𝐑𝐚𝐰   𝐔𝐑𝐋𝐬) ───
# تم تحويل الروابط لتعمل مباشرة داخل التلجرام
SECTION_LOGOS = {
    "MAIN":      "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4782.jpeg",
    "RECEPTION": "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4793.jpeg",
    "LOGIC":     "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4794.jpeg",
    "AI":        "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4794.jpeg",
    "SECURITY":  "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4791.jpeg",
    "ARCHIVE":   "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4792.jpeg",
    "ENGINE":    "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4794.jpeg",
    "STRATEGY":  "https://raw.githubusercontent.com/SongJinwoo1/Structure-01/main/IMG_4782.jpeg" # مؤقت لـ أيانوكوجي
}

# ─── 3. الـثـوابـت والـأزرار ───
BTN_LOGIC     = '🐍 مُـخـتـبـر الـمـنـطـق ╎ 𝐋𝐎𝐆𝐈𝐂   𝐋𝐀𝐁'
BTN_RECEPTION = '🤝 قـسـم الاسـتـقـبال ╎ 𝐑𝐄𝐂𝐄𝐏𝐓𝐈𝐎𝐍'
BTN_AI        = '🤖 وكـلاء الـذكاء ╎ 𝐀𝐈   𝐀𝐠𝐞𝐧𝐭𝐬'
BTN_SEC       = '🛡️ أمن الـبيانات ╎ 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲'
BTN_DB        = '📂 الأرشـفة ╎ 𝐃𝐚تا𝐛𝐚𝐬𝐞'
BTN_ENGINE    = '⚙️ مـحرك 𝐀𝐑𝐈𝐒𝐄 ╎ 𝐄𝐧𝐠𝐢𝐧𝐞'
BTN_TIPS      = '🧠 اسـتـشارة الـنـظام'
BTN_DEV       = '👤 الـتواصل مـع الـقـيادة'
BTN_BACK      = '↩️ الـعودة لـلقائمة'

# تبريد الصور لضمان سلاسة الواجهة (كل 4.8 ساعة)
COOLDOWN_SECONDS = (24 / 5) * 3600 
user_last_photo_time = {}

# ─── 4. مـحـرك الإرسـال الـتـقـني ───
def send_interface(chat_id, text, reply_markup=None, logo_key="MAIN", force_photo=False):
    current_time = time.time()
    last_time = user_last_photo_time.get(chat_id, 0)
    photo_url = SECTION_LOGOS.get(logo_key, SECTION_LOGOS["MAIN"])
    
    # إرسال صورة في حالة البداية أو انتهاء وقت التبريد
    if force_photo or (current_time - last_time >= COOLDOWN_SECONDS):
        try:
            bot.send_photo(chat_id, photo_url, caption=text, reply_markup=reply_markup, parse_mode='Markdown')
            if not force_photo: user_last_photo_time[chat_id] = current_time
        except Exception as e:
            bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode='Markdown')

# ─── 5. بـروتـوكـول الـتـرحـيـب (/start) ───
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(BTN_LOGIC, BTN_RECEPTION)
    markup.add(BTN_AI, BTN_SEC, BTN_DB, BTN_ENGINE)
    markup.add(BTN_TIPS, BTN_DEV)
    
    welcome_text = (
        f"*//ـ الـتـعـرف عـلى الـهـوية ╎ 𝐒𝐓𝐑𝐔𝐂𝐓𝐔𝐑𝐄   𝟎𝟏*\n\n"
        f"◈ الـمـستخـدم: `{message.from_user.first_name}`\n"
        f"◈ الـرتبـة: `[C-Class Cadet]`\n\n"
        "\"المنطق هو الحقيقة الوحيدة هنا. اختر مسار التطوير.\""
    )
    send_interface(message.chat.id, welcome_text, markup, logo_key="MAIN", force_photo=True)

# ─── 6. مـعـالـج الـأوامـر والـأقـسـام ───
@bot.message_handler(content_types=['text'])
def handle_requests(message):
    cid = message.chat.id
    txt = message.text

    # --- 🤝 قـسـم الاسـتـقـبـال (الجديد) ---
    if txt == BTN_RECEPTION:
        reception_msg = (
            "//ـ ســيـسـتـم أريــس تــك ╎ 𝐀𝐑𝐈𝐒𝐄 𝐓𝐄𝐂𝐇 ⚖️\n"
            "— 𝐒𝐭𝐫𝐚𝐭𝐞𝐠𝐢𝐜 𝐈𝐧𝐭𝐞𝐥𝐥𝐢𝐠𝐞𝐧𝐜𝐞 ⚔️ 𝐓𝐞𝐜𝐡𝐧𝐢𝐜𝐚𝐥 𝐒𝐮𝐩𝐞𝐫𝐢𝐨𝐫𝐢𝐭𝐲 —\n\n"
            "\"الجميع مجرد أدوات، والمبرمج الحق هو من يملك الكود الذي يتحكم في تلك الأدوات.\"\n\n"
            "🌑 ━━━━━━━━━━━━━━ 🌑\n\n"
            "✦ روابـط الـسـيـادة (𝐒𝐭𝐫𝐚𝐭𝐞𝐠𝐢𝐜   𝐋𝐢𝐧𝐤𝐬):\n"
            "• 💠 [𝐖𝐞𝐥𝐜𝐨𝐦𝐞   𝐆𝐚𝐭𝐞](https://songjinwoo1.github.io/Bot-Song-Jin-Woo/)\n"
            "• 🐙 𝐆𝐢𝐭𝐇𝐮𝐛 𝐇𝐮𝐛 ↠ `[🔒 Restricted Access]`\n\n"
            "🏆 𝐒𝐲𝐬𝐭𝐞𝐦   𝐇𝐢𝐞𝐫𝐚𝐫𝐜𝐡𝐲:\n"
            "• 𝐒𝐭𝐫𝐚𝐭𝐞𝐠𝐢𝐜 𝐋𝐞𝐚𝐝 ♜ ↠ 𝑺𝒐𝒏𝒈 𝑱𝒊𝒏 𝑾𝒐𝒐\n"
            "• 𝐒𝐨𝐯𝐞𝐫𝐞𝐢𝐠𝐧 𝐄𝐱𝐞𝐜𝐮𝐭𝐨𝐫 👑 ↠ ⟨𝙺𝚒𝚢𝚘𝚝𝚊𝚔𝚊 𖦹 𝙰𝚢𝚊𝚗𝚘𝚔𝚘𝚞𝚓𝚒⟩"
        )
        send_interface(cid, reception_msg, logo_key="RECEPTION")

    # --- 🧠 مُـخـتـبـر الـمـنـطـق ---
    elif txt == BTN_LOGIC:
        logic_msg = (
            "*//ـ مُـخـتـبـر الـمـنـطـق ╎ 𝐋𝐎𝐆𝐈𝐂   𝐋𝐀𝐁*\n"
            "\"هنا يتم بناء عقل النظام. النتائج هي المعيار الوحيد.\""
        )
        send_interface(cid, logic_msg, logo_key="LOGIC")

    # --- 🛡️ أمـن الـبـيـانـات ---
    elif txt == BTN_SEC:
        send_interface(cid, "*//ـ مـركـز الـحـمـاية ╎ 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘   𝐂𝐄𝐍𝐓𝐄𝐑*", logo_key="SECURITY")

    # --- 📂 الأرشفة ---
    elif txt == BTN_DB:
        send_interface(cid, "*//ـ الأرشـيـف الـتـقـني ╎ 𝐓𝐇𝐄   𝐀𝐑𝐂𝐇𝐈𝐕𝐄*", logo_key="ARCHIVE")

    # --- ⚙️ المحرك ---
    elif txt == BTN_ENGINE:
        send_interface(cid, "*//ـ نـواة الـتـطويـر ╎ 𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐌𝐄𝐍𝐓   𝐂𝐎𝐑𝐄*", logo_key="ENGINE")

    # --- 🧠 الاستشارة الاستراتيجية ---
    elif txt == BTN_TIPS:
        tips = [
            "\"أن تكون الأقوى لا يعني أن تصرخ، بل أن تصمت بذكاء.\"",
            "\"العاطفة ثغرة في الكود.. تخلص منها.\"",
            "\"المنطق هو السلاح الذي لا يخطئ.\""
        ]
        send_interface(cid, f"*//ـ غـرفة الاسـتـشـارة 🧠*\n\n{random.choice(tips)}", logo_key="STRATEGY")

    # --- 👤 التواصل ---
    elif txt == BTN_DEV:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("𝑺𝒐𝒏𝒈 𝑱𝒊𝒏 𝑾𝒐𝒐", url="https://wa.me/96597805334"))
        markup.add(types.InlineKeyboardButton("𝙺𝚒𝚢𝚘𝚝𝚊𝚔𝚊 𝙰𝚢𝚊𝚗𝚘𝚔𝚘𝚞𝚓𝚒", url="https://wa.me/201055719273"))
        send_interface(cid, "*//ـ قـناة الاتـصال الـعـلـيا ╎ 𝐇𝐢𝐠𝐡   𝐂𝐨𝐦𝐦𝐚𝐧𝐝*", markup)

    # --- الـعودة ---
    elif txt == BTN_BACK:
        welcome(message)

if __name__ == "__main__":
    print("STRUCTURE 01 IS SECURE AND ONLINE...")
    bot.polling(none_stop=True)
