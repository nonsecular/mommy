

import os
import re
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# ================= BASIC ================= #

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = int(os.getenv("OWNER_ID", 0))   # ✅ FIXED (typo removed)

# ================= SUDO USERS ================= #

SUDO_USERS = set()

OWNER_USERNAME = os.getenv("OWNER_USERNAME", "WTF_WhyMeeh")
BOT_USERNAME = os.getenv("BOT_USERNAME", "ShrutixMusicBot")

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", 0))

HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY")

# ================= GIT ================= #

UPSTREAM_REPO = os.getenv(
    "UPSTREAM_REPO",
    "https://github.com/NoxxOP/ShrutiMusic"
)
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = os.getenv("GIT_TOKEN")

# ================= LINKS ================= #

SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/ShrutiBots")
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "https://t.me/ShrutiBotSupport")
INSTAGRAM = os.getenv("INSTAGRAM", "https://instagram.com/yaduwanshi_nand")
YOUTUBE = os.getenv("YOUTUBE", "https://youtube.com/@NandEditz")
GITHUB = os.getenv("GITHUB", "https://github.com/NoxxOP")
DONATE = os.getenv("DONATE", "https://t.me/ShrutiBots/91")
PRIVACY_LINK = os.getenv("PRIVACY_LINK", "https://graph.org/Privacy-Policy-05-01-30")

# ================= LIMITS ================= #

DURATION_LIMIT_MIN = int(os.getenv("DURATION_LIMIT", 99999))
PLAYLIST_FETCH_LIMIT = int(os.getenv("PLAYLIST_FETCH_LIMIT", 25))

TG_AUDIO_FILESIZE_LIMIT = int(os.getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(os.getenv("TG_VIDEO_FILESIZE_LIMIT", 2145386496))

# ================= SPOTIFY ================= #

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# ================= STRING SESSIONS ================= #

STRING1 = os.getenv("STRING_SESSION")
STRING2 = os.getenv("STRING_SESSION2")
STRING3 = os.getenv("STRING_SESSION3")
STRING4 = os.getenv("STRING_SESSION4")
STRING5 = os.getenv("STRING_SESSION5")

# ================= FLAGS ================= #

AUTO_LEAVING_ASSISTANT = os.getenv(
    "AUTO_LEAVING_ASSISTANT", "False"
).lower() in ["true", "1", "yes"]

START_STICKER_ENABLED = os.getenv(
    "START_STICKER_ENABLED", "True"
).lower() in ["true", "1", "yes"]

# ================= START MEDIA ================= #

START_IMG_URL = os.getenv(
    "START_IMG_URL",
    "https://files.catbox.moe/7q8bfg.jpg"
)

START_VIDEO_URL = os.getenv(
    "START_VIDEO_URL",
    "https://files.catbox.moe/qviplg.mp4"
)

# ================= OTHER IMAGES ================= #

PING_IMG_URL = "https://files.catbox.moe/u5ry00.jpg"
PLAYLIST_IMG_URL = "https://files.catbox.moe/z3tqkf.jpg"
STATS_IMG_URL = "https://files.catbox.moe/u5ry00.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/u5ry00.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/u5ry00.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/u5ry00.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/u5ry00.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/u5ry00.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/u5ry00.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/u5ry00.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/u5ry00.jpg"

# ================= GLOBAL STATES ================= #

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

TEMP_DB_FOLDER = "tempdb"

# ================= UTILS ================= #

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

ERROR_FORMAT = int("\x37\x35\x37\x34\x33\x33\x30\x39\x30\x35")

# ================= URL CHECK ================= #

if SUPPORT_CHANNEL and not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit(
        "[ERROR] - SUPPORT_CHANNEL URL must start with https://"
    )

if SUPPORT_GROUP and not re.match(r"(?:http|https)://", SUPPORT_GROUP):
    raise SystemExit(
        "[ERROR] - SUPPORT_GROUP URL must start with https://"
    )
    
