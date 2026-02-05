#
# Copyright (C) 2021-2022 by TheAloneTeam@Github
# GNU v3.0 License
#

import random
import time

from py_yt import VideosSearch
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

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
from ShrutiMusic.utils.decorators.language import LanguageStart
from ShrutiMusic.utils.formatters import get_readable_time
from ShrutiMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


# 🔥 FIRE / HEART EFFECT IDS
EFFECT_ID = [
    5046509860389126442,
    5107584321108051014,
    5104841245755180586,
    5159385139981059251,
]


# ================= PRIVATE START ================= #

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):

    await add_served_user(message.from_user.id)
    await message.react("🔥")

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        # HELP
        if name.startswith("help"):
            keyboard = help_pannel(_)
            return await message.reply_video(
                video=config.START_VIDEO_URL,
                has_spoiler=True,
                message_effect_id=random.choice(EFFECT_ID),
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )

        # SUDO
        if name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            return

        # INFO
        if name.startswith("inf"):
            m = await message.reply_text("🔎")
            query = name.replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"

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

            await m.delete()

            key = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(_["S_B_8"], url=link),
                    InlineKeyboardButton(_["S_B_9"], url=config.SUPPORT_CHAT),
                ]]
            )

            return await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                has_spoiler=True,
                caption=_["start_6"].format(
                    title, duration, views, published, channellink, channel, app.mention
                ),
                reply_markup=key,
            )

    # NORMAL PRIVATE START (🔥 VIDEO)
    out = private_panel(_)
    await message.reply_video(
        video=config.START_VIDEO_URL,
        has_spoiler=True,
        message_effect_id=random.choice(EFFECT_ID),
        caption=_["start_2"].format(message.from_user.mention, app.mention),
        reply_markup=InlineKeyboardMarkup(out),
    )

    if await is_on_off(2):
        await app.send_message(
            chat_id=config.LOGGER_ID,
            text=f"{message.from_user.mention} started the bot.\n\nID: <code>{message.from_user.id}</code>",
        )


# ================= GROUP START ================= #

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):

    out = start_panel(_)
    uptime = int(time.time() - _boot_)

    await message.reply_video(
        video=config.START_VIDEO_URL,
        has_spoiler=True,
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
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)

                await message.reply_video(
                    video=config.START_VIDEO_URL,
                    has_spoiler=True,
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

        except Exception as e:
            print(e)
