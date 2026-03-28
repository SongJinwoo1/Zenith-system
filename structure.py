import os
import telebot
from telebot import types
import random
# تأكد من تثبيت المكتبة: pip install python-dotenv
from dotenv import load_dotenv 

# ─── 1. بـروتـوكـول الأمـان (إخفاء التوكن) ───
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("⚠️ خـطأ حـرج: لـم يتم الـعثور على مـفتاح BOT_TOKEN فـي مـلف .env")
    exit()

bot = telebot.TeleBot(TOKEN)

# ─── 2. الـثـوابـت الـنـصـيـة (لـمنع أخطاء الـتطابق) ───
LOGO_URL = "https://via.placeholder.com/800x400.png?text=STRUCTURE+01+ARISE+TECH"

BTN_LOGIC  = '🐍 مُـخـتـبـر الـمـنـطـق ╎ 𝐋𝐎𝐆𝐈𝐂   𝐋𝐀𝐁'
BTN_AI     = '🤖 وكـلاء الـذكاء ╎ 𝐀𝐈   𝐀𝐠𝐞𝐧𝐭𝐬'
BTN_SEC    = '🛡️ أمن الـبيانات ╎ 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲'
BTN_DB     = '📂 الأرشـفة ╎ 𝐃𝐚𝐭𝐚𝐛𝐚𝐬𝐞'
BTN_ENGINE = '⚙️ مـحرك 𝐀𝐑𝐈𝐒𝐄 ╎ 𝐄𝐧𝐠𝐢𝐧𝐞'
BTN_WEB    = '🌐 مـنطق الـويب ╎ 𝐖𝐞𝐛   𝐋𝐨𝐠𝐢𝐜'
BTN_UI     = '🎨 واجـهة الـنظام ╎ 𝐔𝐈/𝐔𝐗'
BTN_TIPS   = '🧠 اسـتـشارة الـنـظام'
BTN_DEV    = '👤 الـتواصل مـع الـقـيادة'
BTN_BACK   = '↩️ الـعودة لـلقائمة'
BTN_EXAM   = '🏁 الإخـتـبار 𝟏𝟎𝟎'

DAY_01 = '◈ الـيوم 𝟎𝟏'
DAY_02 = '◈ الـيوم 𝟎𝟐'
DAY_03 = '◈ الـيوم 𝟎𝟑'
DAY_50 = '◈ الـيوم 𝟓𝟎'
DAY_99 = '◈ الـيوم 𝟗𝟗'

# قـائمة الأقـسام الـتي قـيد الـتطوير
UNDER_DEVELOPMENT = [BTN_AI, BTN_SEC, BTN_DB, BTN_ENGINE, BTN_WEB, BTN_UI]

# ─── 3. الـمـحـرك الـرئـيـسـي لـلإرسـال ───
def send_with_logo(chat_id, text, reply_markup=None):
    """بـروتـوكول إرسـال الـهوية الـبصرية مـع صـائد الأخـطاء"""
    try:
        bot.send_photo(chat_id, LOGO_URL, caption=text, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        print(f"⚠️ [System Log] Error in send_with_logo: {e}")
        bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode='Markdown')

# ─── 4. بـروتـوكـول الـتـرحـيـب ───
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    markup.add(BTN_LOGIC)
    markup.add(BTN_AI, BTN_SEC, BTN_DB, BTN_ENGINE, BTN_WEB, BTN_UI)
    markup.add(BTN_TIPS, BTN_DEV)
    
    # تنظيف اسم المستخدم لتجنب أخطاء الـ Markdown
    safe_name = str(message.from_user.first_name).replace('_', '\\_').replace('*', '\\*').replace('[', '\\[')
    
    welcome_text = (
        f"*//ـ الـتـعـرف عـلى الـهـوية ╎ 𝐒𝐓𝐑𝐔𝐂𝐓𝐔𝐑𝐄   𝟎𝟏*\n\n"
        f"◈ الـمـستخـدم: `{safe_name}`\n"
        f"◈ الـرتبـة: `[C-Class Cadet]`\n"
        f"◈ الـتـسلـسل: `ID-{message.from_user.id}`\n\n"
        "\"المنطق هو الحقيقة الوحيدة هنا. اختر مسارك بعناية.\""
    )
    send_with_logo(message.chat.id, welcome_text, markup)

# ─── 5. مـعـالـج الـنـصـوص (مـؤمـن لـلنـصوص فـقط) ───
@bot.message_handler(content_types=['text'])
def handle_requests(message):
    text = message.text
    
    # --- قـسـم مُـخـتـبـر الـمـنـطـق ---
    if text == BTN_LOGIC:
        day_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        btns = [
            types.KeyboardButton(DAY_01), types.KeyboardButton(DAY_02), 
            types.KeyboardButton(DAY_03), types.KeyboardButton(DAY_50), 
            types.KeyboardButton(DAY_99), types.KeyboardButton(BTN_EXAM)
        ]
        day_markup.add(*btns)
        day_markup.add(types.KeyboardButton(BTN_BACK))
        
        lab_description = (
            "*//ـ مُـخـتـبـر الـمـنـطـق ╎ 𝐋𝐎𝐆𝐈𝐂   𝐋𝐀𝐁 🧠*\n"
            "— 𝐏𝐲𝐭𝐡𝐨𝐧   𝐌𝐚𝐬𝐭𝐞𝐫𝐲 ⚔️ 𝐀.𝐈   𝐄𝐧𝐠𝐢𝐧𝐞𝐞𝐫𝐢𝐧𝐠 —\n\n"
            "\"هنا يتم تطوير عقل النظام وبناء المحركات الذكية.\"\n\n"
            "✦ *نـطـاق الـعـمـل (𝐓𝐞𝐜𝐡   𝐒𝐭𝐚𝐜𝐤):*\n"
            "   ◈ لغة المنطق (Python Scripts).\n"
            "   ◈ بناء المحركات (Engine Architecture).\n"
            "   ◈ وكلاء الذكاء (AI Agents).\n\n"
            "📊 *𝐒𝐲𝐬𝐭𝐞𝐦   𝐒𝐭𝐚𝐭𝐮𝐬   𝐑𝐞𝐩𝐨𝐫𝐭:*\n"
            "• 🟢 𝐄𝐧𝐠𝐢𝐧𝐞   𝐒𝐭𝐚𝐭𝐮𝐬: 𝐎𝐩𝐞𝐫𝐚𝐭𝐢𝐨𝐧𝐚𝐥\n\n"
            "⚠️ \"المنطق هو السلاح الأقوى.. ابدأ بالبرمجة.\""
        )
        send_with_logo(message.chat.id, lab_description, day_markup)

    # --- مـحتوى الـيوم الأول ---
    elif text == DAY_01:
        day1_text = (
            "*//ـ الـمـهـمة 𝟎𝟏 ╎ 𝐈𝐍𝐈𝐓𝐈𝐀𝐋𝐈𝐙𝐀𝐓𝐈𝐎𝐍*\n\n"
            "✦ الـمـهمـة ↞ [تحليل الأساسيات](https://www.youtube.com/watch?v=MWbucf-IgSI)\n"
            "✦ الـمـسار ↞ [بـروتوكول الـبايثون](https://bit.ly/3S2S1qT)\n\n"
            "⏰ *مـهـلـة الـتـنـفـيـذ:* 𝟒𝟖 سـاعـة."
        )
        send_with_logo(message.chat.id, day1_text)

    # --- الأقـسام قـيد الـتطوير والـأيام الـمغـلـقة ---
    elif text in UNDER_DEVELOPMENT or text in [DAY_02, DAY_03, DAY_50, DAY_99]:
        locked_tips = [
            "\"الاستعجال هو ثغرة في منطق الضعفاء.. الزم مكانك.\"",
            "\"نحن لا نمنح المعرفة لمن لا يستحقها.. أتمم ما قبله أولاً.\"",
            "\"الصبر هو معالجة هادئة لبيانات الواقع.\""
        ]
        response = (
            "*//ـ حـالة الـوصـول ╎ 𝐔𝐍𝐃𝐄𝐑   𝐂𝐎𝐍𝐒𝐓𝐑𝐔𝐂𝐓𝐈𝐎𝐍*\n\n"
            f"\"{random.choice(locked_tips)}\"\n\n"
            "⚠️ هذا القطاع قيد التشفير البرمجي حالياً وسيتم فتحه قريباً."
        )
        send_with_logo(message.chat.id, response)

    # --- الإخـتبـار الـنهائي 100 ---
    elif text == BTN_EXAM:
        send_with_logo(message.chat.id, "*//ـ بـوابـة الـنـخـبة ╎ 𝐄𝐗𝐀𝐌   𝟏𝟎𝟎*\n\n🔒 **الـحـالة:** مـحـظـور.\nيـتـطلب الوصول نـسبة تـوافق 100% مع الـمختبر.")

    # --- الـتواصل مـع الـقيادة ---
    elif text == BTN_DEV:
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_jin = types.InlineKeyboardButton("𝑺𝒐𝒏𝒈 𝑱𝒊𝒏 𝑾𝒐𝒐 ╎ Strategic Overseer", url="https://wa.me/96597805334")
        btn_kyo = types.InlineKeyboardButton("𝙺𝚒𝚢𝚘𝚝𝚊𝚔𝚊 𝙰𝚢𝚊𝚗𝚘𝚔𝚘𝚞𝚓𝚒 ╎ Executor", url="https://wa.me/201055719273")
        markup.add(btn_jin, btn_kyo)
        send_with_logo(message.chat.id, "*//ـ قـناة الاتـصال الـعـلـيا ╎ 𝐇𝐢𝐠𝐡   𝐂𝐨𝐦𝐦𝐚𝐧𝐝*", markup)

    # --- اسـتـشارات عشوائية ---
    elif text == BTN_TIPS:
        tips = ["\"المنطق هو السلاح الأقوى.\"", "\"العاطفة لا تبني كوداً.\"", "\"ابحث بنفسك أولاً.\""]
        send_with_logo(message.chat.id, f"\" {random.choice(tips)} \"")

    # --- الـعودة ---
    elif text == BTN_BACK:
        welcome(message)

    # --- 6. صـائد الأوامـر الـمـجـهـولـة (Fallback) ---
    else:
        fallback_text = (
            "*//ـ إدخـال غـيـر مـعـروف ╎ 𝐔𝐍𝐊𝐍𝐎𝐖𝐍   𝐂𝐎𝐌𝐌𝐀𝐍𝐃*\n\n"
            "\"البيانات العشوائية تسبب خللاً في النظام.\"\n"
            "الرجاء استخدام لوحة التحكم بالأسفل للتنقل."
        )
        send_with_logo(message.chat.id, fallback_text)

if __name__ == "__main__":
    print("STRUCTURE 01 IS SECURE AND ONLINE...")
    bot.polling(none_stop=True)
