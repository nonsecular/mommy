import time
import random
from typing import Final

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
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
    is_on_off,
)
from ShrutiMusic.utils import bot_sys_stats
from ShrutiMusic.utils.decorators.language import LanguageStart
from ShrutiMusic.utils.formatters import get_readable_time
from ShrutiMusic.utils.inline import help_pannel_page1, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


# ================= SAFE VIDEO SENDER ================= #
async def safe_reply_video(message, video, caption, reply_markup=None):
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


# ================= DATA ================= #
NAND_YADUWANSHI_EFFECTS: Final[list[str]] = [
    "5104841245755180586",
    "5107584321108051014",
    "5159385139981059251",
    "5046509860389126442",
]

RANDOM_STICKERS = [
    "CAACAgUAAxkBAAEEnzFor872a_gYPHu-FxIwv-nxmZ5U8QACyBUAAt5hEFVBanMxRZCc7h4E",
    "CAACAgUAAxkBAAEEnzJor88q_xRO1ljlwh_I6fRF7lDR-AACnBsAAlckCFWNCpez-HzWHB4E",
    "CAACAgUAAxkBAAEEnzNor88uPuVTSyRImyVXsu1pqrpRLgACKRMAAvOEEFUpvggmgDu6bx4E",
    "CAACAgUAAxkBAAEEnzRor880z_spEYEnEfyFXN55tNwydQACIxUAAosKEVUB8iqZMVYroR4E"
]


# ================= PRIVATE START ================= #
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):

    if getattr(config, "START_STICKER_ENABLED", True):
        await message.reply_sticker(sticker=random.choice(RANDOM_STICKERS))

    await add_served_user(message.from_user.id)

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name.startswith("help"):
            keyboard = help_pannel_page1(_)
            return await safe_reply_video(
                message,
                video=config.START_VID_URL,
                caption=_["help_1"].format(config.SUPPORT_GROUP),
                reply_markup=keyboard,
            )

        if name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            return

        if name.startswith("inf"):
            m = await message.reply_text("🔎")
            query = f"https://www.youtube.com/watch?v={name.replace('info_', '')}"

            results = VideosSearch(query, limit=1)
            for r in (await results.next())["result"]:
                title = r["title"]
                duration = r["duration"]
                views = r["viewCount"]["short"]
                thumbnail = r["thumbnails"][0]["url"].split("?")[0]
                channellink = r["channel"]["link"]
                channel = r["channel"]["name"]
                link = r["link"]
                published = r["publishedTime"]

            key = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(text=_["S_B_8"], url=link),
                    InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_GROUP),
                ]]
            )

            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=_["start_6"].format(
                    title, duration, views, published, channellink, channel, app.mention
                ),
                reply_markup=key,
            )
            return

    out = private_panel(_)
    UP, CPU, RAM, DISK = await bot_sys_stats()

    await safe_reply_video(
        message,
        video=config.START_VID_URL,
        caption=_["start_2"].format(
            message.from_user.mention, app.mention, UP, DISK, CPU, RAM
        ),
        reply_markup=InlineKeyboardMarkup(out),
    )


# ================= GROUP START ================= #
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):

    if getattr(config, "START_STICKER_ENABLED", True):
        await message.reply_sticker(sticker=random.choice(RANDOM_STICKERS))

    out = start_panel(_)
    uptime = int(time.time() - _boot_)

    await safe_reply_video(
        message,
        video=config.START_VID_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )

    await add_served_chat(message.chat.id)


# ================= WELCOME ================= #
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):

    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                await message.chat.ban_member(member.id)

            if member.id == app.id:

                if message.chat.type != ChatType.SUPERGROUP:
                    await app.leave_chat(message.chat.id)
                    return

                if message.chat.id in await blacklisted_chats():
                    await app.leave_chat(message.chat.id)
                    return

                if getattr(config, "START_STICKER_ENABLED", True):
                    await message.reply_sticker(sticker=random.choice(RANDOM_STICKERS))

                out = start_panel(_)

                await safe_reply_video(
                    message,
                    video=config.START_VID_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )

                await add_served_chat(message.chat.id)
                await message.stop_propagation()

        except Exception as ex:
            print(ex)
