from pyrogram.types import InlineKeyboardButton

async def start_cmd(Legend):
    x = await Legend.get_me()
    START_OP = [
        [
            InlineKeyboardButton(
                text="🥀 Developer 🥀", url=f"https://t.me/LegendSpamBot_Owner"
            ),
            InlineKeyboardButton(
                text="✨ Support ✨", url=f"https://t.me/LegendBotSpam"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🧸 Add me in your group 🧸",
                url=f"https://t.me/{x.username}?startgroup=true",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❄️ Source Code ❄️", url=f"https://github.com/LEGEND-AI/BOTSPAM"
            ),
            InlineKeyboardButton(
                text="☁️ Updates ☁️", url=f"https://t.me/LegendBot_AI"
            ),
        ],
    ]
    return START_OP
