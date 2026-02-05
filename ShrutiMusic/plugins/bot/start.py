import time
import random
from typing import Final, List, Optional

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from py_yt import VideosSearch

import config
from ShrutiMusic import app
from ShrutiMusic.misc import _boot_
from ShrutiMusic.plugins.sudo.sudoers import sudoers_list
from ShrutiMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
)
from ShrutiMusic.utils import bot_sys_stats
from ShrutiMusic.utils.decorators.language import LanguageStart
from ShrutiMusic.utils.formatters import get_readable_time
from ShrutiMusic.utils.inline import (
    help_pannel_page1,
    private_panel,
    start_panel,
)
from strings import get_string
from config import BANNED_USERS


# =====================================================
#                    CONSTANTS
# =====================================================

RANDOM_STICKERS: Final[List[str]] = [
    "CAACAgUAAxkBAAEEnzFor872a_gYPHu-FxIwv-nxmZ5U8QACyBUAAt5hEFVBanMxRZCc7h4E",
    "CAACAgUAAxkBAAEEnzJor88q_xRO1ljlwh_I6fRF7lDR-AACnBsAAlckCFWNCpez-HzWHB4E",
    "CAACAgUAAxkBAAEEnzNor88uPuVTSyRImyVXsu1pqrpRLgACKRMAAvOEEFUpvggmgDu6bx4E",
    "CAACAgUAAxkBAAEEnzRor880z_spEYEnEfyFXN55tNwydQACIxUAAosKEVUB8iqZMVYroR4E",
]


# =====================================================
#          INLINE BUTTONS – AUTO SANITIZER
# =====================================================

def sanitize_buttons(
    markup: Optional[InlineKeyboardMarkup],
) -> Optional[InlineKeyboardMarkup]:
    """
    Removes all InlineKeyboardButtons that contain user_id
    Prevents PEER_ID_INVALID crashes completely
    """
    if not markup:
        return None

    safe_keyboard = []

    for row in markup.inline_keyboard:
        safe_row = []
        for btn in row:
            # ❌ user_id buttons are dangerous
            if getattr(btn, "user_id", None):
                continue
            safe_row.append(btn)
        if safe_row:
            safe_keyboard.append(safe_row)

    return InlineKeyboardMarkup(safe_keyboard) if safe_keyboard else None


# =====================================================
#             SAFE MEDIA SENDER (HARDENED)
# =====================================================

async def safe_reply_video(
    message: Message,
    video: str,
    caption: str,
    reply_markup: Optional[InlineKeyboardMarkup] = None,
):
    reply_markup = sanitize_buttons(reply_markup)

    try:
        return await message.reply_video(
            video=video,
            caption=caption,
            reply_markup=reply_markup,
            has_spoiler=True,
        )
    except Exception:
        return await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=caption,
            reply_markup=reply_markup,
            has_spoiler=True,
        )


async def send_random_sticker(message: Message):
    if getattr(config, "START_STICKER_ENABLED", True):
        await message.reply_sticker(random.choice(RANDOM_STICKERS))


# =====================================================
#                   PRIVATE /start
# =====================================================

@app.on_message(filters.command("start") & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_private(_, message: Message, lang):

    await send_random_sticker(message)
    await add_served_user(message.from_user.id)

    args = message.text.split(maxsplit=1)

    if len(args) > 1:
        cmd = args[1]

        if cmd.startswith("help"):
            return await safe_reply_video(
                message,
                config.START_VID_URL,
                lang["help_1"].format(config.SUPPORT_GROUP),
                InlineKeyboardMarkup(help_pannel_page1(lang)),
            )

        if cmd.startswith("sud"):
            return await sudoers_list(app, message, lang)

        if cmd.startswith("inf"):
            return await send_video_info(message, lang, cmd)

    UP, CPU, RAM, DISK = await bot_sys_stats()

    await safe_reply_video(
        message,
        config.START_VID_URL,
        lang["start_2"].format(
            message.from_user.mention,
            app.mention,
            UP,
            DISK,
            CPU,
            RAM,
        ),
        InlineKeyboardMarkup(private_panel(lang)),
    )


# =====================================================
#                   GROUP /start
# =====================================================

@app.on_message(filters.command("start") & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_group(_, message: Message, lang):

    await send_random_sticker(message)

    uptime = get_readable_time(int(time.time() - _boot_))

    await safe_reply_video(
        message,
        config.START_VID_URL,
        lang["start_1"].format(app.mention, uptime),
        InlineKeyboardMarkup(start_panel(lang)),
    )

    await add_served_chat(message.chat.id)


# =====================================================
#                VIDEO INFO HANDLER
# =====================================================

async def send_video_info(message: Message, lang, cmd: str):

    wait = await message.reply_text("🔍 Searching...")
    video_id = cmd.replace("info_", "")
    query = f"https://www.youtube.com/watch?v={video_id}"

    search = VideosSearch(query, limit=1)
    results = (await search.next()).get("result")

    if not results:
        return await wait.edit("❌ No results found.")

    r = results[0]

    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(lang["S_B_8"], url=r["link"]),
            InlineKeyboardButton(lang["S_B_9"], url=config.SUPPORT_GROUP),
        ]]
    )

    await wait.delete()

    await app.send_photo(
        message.chat.id,
        photo=r["thumbnails"][0]["url"].split("?")[0],
        caption=lang["start_6"].format(
            r["title"],
            r["duration"],
            r["viewCount"]["short"],
            r["publishedTime"],
            r["channel"]["link"],
            r["channel"]["name"],
            app.mention,
        ),
        reply_markup=sanitize_buttons(buttons),
    )


# =====================================================
#                   WELCOME HANDLER
# =====================================================

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(_, message: Message):

    for member in message.new_chat_members:
        try:
            lang_code = await get_lang(message.chat.id)
            lang = get_string(lang_code)

            if await is_banned_user(member.id):
                return await message.chat.ban_member(member.id)

            if member.id == app.id:

                if message.chat.type != ChatType.SUPERGROUP:
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    return await app.leave_chat(message.chat.id)

                await send_random_sticker(message)

                await safe_reply_video(
                    message,
                    config.START_VID_URL,
                    lang["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    InlineKeyboardMarkup(start_panel(lang)),
                )

                await add_served_chat(message.chat.id)
                return await message.stop_propagation()

        except Exception as e:
            print(f"[WELCOME ERROR]: {e}")
