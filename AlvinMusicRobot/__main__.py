# AlvinMusicRobot (Telegram bot project)
# Copyright (C) 2021  Inuka Asith & Rojserbest

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


import requests
from pyrogram import Client as Bot

from AlvinMusicRobot.config import API_HASH
from AlvinMusicRobot.config import API_ID
from AlvinMusicRobot.config import BG_IMAGE
from AlvinMusicRobot.config import BOT_TOKEN
from AlvinMusicRobot.services.callsmusic import run

response = requests.get(BG_IMAGE)
file = open("./etc/foreground.png", "wb")
file.write(response.content)
file.close()

bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="AlvinMusicRobot.modules"),
)

bot.start()
run()
