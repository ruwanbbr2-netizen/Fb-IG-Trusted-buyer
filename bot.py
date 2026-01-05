import telebot
from telebot import types
import json
import os
from datetime import datetime, time

# ===== BOT CONFIG =====
BOT_TOKEN = "8358293320:AAExmqmr6TN8Q9gCrAfdOy309mspjqM77mw"
ADMIN_ID = 7517279474

bot = telebot.TeleBot(BOT_TOKEN)

# ===== FILES =====
USERS_FILE = "users.json"
SUB_FILE = "submissions.json"
REJECT_FILE = "reject_count.json"

# ===== UTIL =====
def load(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ===== SUBMISSION TIME (7:00am – 5:30pm) =====
def submission_open():
    now = datetime.now().time()
    start = time(7, 0)
    end = time(17, 30)
    return start <= now <= end

# ===== STATES =====
user_work_states = {}
work_type_states = {}
fb_subtype_states = {}

# ===== MAIN MENU =====
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📤 Submit Work", "👥 Joining Groups")
    kb.row("📞 Support")
    return kb

# ===== START =====
@bot.message_handler(commands=["start"])
def start(msg):
    users = load(USERS_FILE)
    users[str(msg.chat.id)] = {"name": msg.from_user.first_name}
    save(USERS_FILE, users)

    text = (
        "👋 *Welcome to Submit Work Bot*\n\n"
        "⏰ *Submission Time*\n"
        "• 7:00am – 5:30pm\n"
        "• Report: 9:00am (Next Day)\n"
        "• Payment: 3:30pm (Next Day)\n\n"
        "Zaɓi daga menu a ƙasa 👇"
    )
    bot.send_message(msg.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

# ===== JOINING GROUPS =====
@bot.message_handler(func=lambda m: m.text == "👥 Joining Groups")
def joining_groups(m):
    text = (
        "*HAUSA 🇳🇬*\n"
        "Kayi Joining din groups da channel dinmu na Whatsapp/Telegram domin:\n"
        "• Ganin price din kullum\n"
        "• Ganin report din aikinka kafin 9:00am\n\n"
        "*Whatsapp Group:*\n"
        "https://chat.whatsapp.com/JgSfsd2BrgwDcUXPj5BsTO\n\n"
        "*Telegram Channel:*\n"
        "https://t.me/mobileskillnetwork\n\n"
        "Idan kana da matsala ko tura bayanan payment ka tuntubi support.\n\n"
        "----------------------------------\n\n"
        "*ENGLISH 🇬🇧*\n"
        "Please join our Whatsapp group and Telegram channel to:\n"
        "• See daily prices\n"
        "• Check your work report before 9:00am\n\n"
        "*Whatsapp Group:*\n"
        "https://chat.whatsapp.com/JgSfsd2BrgwDcUXPj5BsTO\n\n"
        "*Telegram Channel:*\n"
        "https://t.me/mobileskillnetwork\n\n"
        "If you have any issue or want to submit payment details, contact support."
    )
    bot.send_message(m.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

# ===== SUPPORT =====
@bot.message_handler(func=lambda m: m.text == "📞 Support")
def support(m):
    text = (
        "*HAUSA 🇳🇬*\n"
        "Idan kana bukatar tambaya ko wani abu da baka saniba,\n"
        "ko ana rejected idan ka tura aiki,\n"
        "ko idan kana son ka tura bank details dinka,\n"
        "ka tuntubemu anan 👇\n\n"
        "https://t.me/Trustedonlinebuyer\n\n"
        "----------------------------------\n\n"
        "*ENGLISH 🇬🇧*\n"
        "If you have any questions,\n"
        "if your work was rejected,\n"
        "or if you want to submit your bank/payment details,\n"
        "please contact us here 👇\n\n"
        "https://t.me/Trustedonlinebuyer"
    )
    bot.send_message(m.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

# ===== SUBMIT WORK =====
@bot.message_handler(func=lambda m: m.text == "📤 Submit Work")
def submit_work(m):
    if not submission_open():
        bot.send_message(
            m.chat.id,
            "⛔ *Submission Closed*\n\n"
            "Lokacin submit aiki:\n"
            "• 7:00am – 5:30pm",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        return

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🔵 Facebook Work", "🟠 Instagram Work")
    kb.row("🔙 Back")

    user_work_states[m.chat.id] = True
    bot.send_message(m.chat.id, "Choose work type:", reply_markup=kb)

# ===== FACEBOOK =====
@bot.message_handler(func=lambda m: m.text == "🔵 Facebook Work")
def fb_work(m):
    work_type_states[m.chat.id] = "Facebook"
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    options = [
        "🆔 Webmail 00frnd 2FA",
        "🆔 Hotmail 30frnd 2FA",
        "🆔 Any Mail 00frnd 2FA",
        "🆔 Number 00frnd 2FA",
        "🆔 Facebook Switch Account",
        "🔙 Back"
    ]
    for o in options:
        kb.add(o)
    bot.send_message(m.chat.id, "Choose Facebook type:", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text.startswith("🆔"))
def fb_subtype(m):
    fb_subtype_states[m.chat.id] = m.text
    bot.send_message(m.chat.id, "📤 Upload proof now (Photo / Document)")

# ===== INSTAGRAM =====
@bot.message_handler(func=lambda m: m.text == "🟠 Instagram Work")
def insta(m):
    work_type_states[m.chat.id] = "Instagram"
    fb_subtype_states[m.chat.id] = ""
    bot.send_message(m.chat.id, "📤 Upload Instagram proof now")

# ===== RECEIVE WORK =====
@bot.message_handler(content_types=["photo", "document"])
def receive_work(m):
    if not submission_open():
        bot.send_message(m.chat.id, "⛔ Submission closed.", reply_markup=main_menu())
        return

    if m.chat.id not in user_work_states:
        return

    subs = load(SUB_FILE)
    sub_id = str(m.message_id)

    sub = {
        "user_id": m.chat.id,
        "status": "pending",
        "work_type": work_type_states.get(m.chat.id),
        "sub_type": fb_subtype_states.get(m.chat.id)
    }

    if m.content_type == "photo":
        sub["file_id"] = m.photo[-1].file_id
        sub["file_type"] = "photo"
    else:
        sub["file_id"] = m.document.file_id
        sub["file_type"] = "document"

    subs[sub_id] = sub
    save(SUB_FILE, subs)

    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✅ Approve", callback_data=f"approve_{sub_id}"),
        types.InlineKeyboardButton("❌ Reject", callback_data=f"reject_{sub_id}")
    )

    caption = (
        f"📥 New Work\n\n"
        f"User: {m.chat.id}\n"
        f"Work: {sub['work_type']}\n"
        f"Type: {sub['sub_type']}"
    )

    if sub["file_type"] == "photo":
        bot.send_photo(ADMIN_ID, sub["file_id"], caption=caption, reply_markup=kb)
    else:
        bot.send_document(ADMIN_ID, sub["file_id"], caption=caption, reply_markup=kb)

    bot.send_message(
        m.chat.id,
        "⏳ *Waiting for approval*",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

    user_work_states.pop(m.chat.id, None)
    work_type_states.pop(m.chat.id, None)
    fb_subtype_states.pop(m.chat.id, None)

# ===== ADMIN DECISION =====
@bot.callback_query_handler(func=lambda c: c.data.startswith(("approve_", "reject_")))
def decision(call):
    subs = load(SUB_FILE)
    reject = load(REJECT_FILE)

    action, sub_id = call.data.split("_")
    sub = subs.get(sub_id)
    if not sub:
        return

    uid = str(sub["user_id"])

    if action == "approve":
        reject[uid] = 0
        bot.send_message(sub["user_id"], "✅ Work Approved")
    else:
        reject[uid] = reject.get(uid, 0) + 1
        bot.send_message(sub["user_id"], f"❌ Work Rejected ({reject[uid]}/3)")

    save(REJECT_FILE, reject)
    save(SUB_FILE, subs)
    bot.answer_callback_query(call.id)

# ===== RUN =====
bot.infinity_polling(skip_pending=True)