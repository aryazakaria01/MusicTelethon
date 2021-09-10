# AlvinMusic- Telegram bot project
# Copyright (C) 2021  Roj Serbest
# Copyright (C) 2021  Inuka Asith
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# Modified by alvin_junior

import os
from os import path
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

que = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "Alvin Music Bot")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "alvin_image_editor")
BG_IMAGE = getenv("BG_IMAGE", "https://telegra.ph/file/b623ab3cd8caef9efff2b.jpg")
admins = {}
API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH")
BOT_USERNAME = getenv("BOT_USERNAME", "AlvinMusicRobot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "alvin_junior")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "Alvin_image_editor_group")
PROJECT_NAME = getenv("PROJECT_NAME", "Alvin Junior Bot")
SOURCE_CODE = getenv("SOURCE_CODE", "github.com/aryazakaria01/MusicTelethon")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "15"))
ARQ_API_KEY = getenv("ARQ_API_KEY", None)
PMPERMIT = getenv("PMPERMIT", None)
LOG_GRP = getenv("LOG_GRP", None)
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ !").split())
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
CREATOR_NAME = getenv("CREATOR_NAME", "alvin_junior")
