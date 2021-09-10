# Calls Music 1 - Telegram bot for streaming audio in group calls
# Copyright (C) 2021  Roj Serbest

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

from os import path

from youtube_dl import YoutubeDL

from AlvinMusicRobot.config import DURATION_LIMIT
from AlvinMusicRobot.helpers.errors import DurationLimitError

ydl_opts = {
    "format": "bestaudio/best",
    "verbose": True,
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}

ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"🛑 Video lebih dari {DURATION_LIMIT} menit tidak diizinkan, "
            f"video yang disediakan adalah {duration} menit",
        )
    try:
        ydl.download([url])
    except:
        raise DurationLimitError(
            f"🛑 Video lebih dari {DURATION_LIMIT} menit tidak diizinkan, "
            f"video yang disediakan adalah {duration} menit",
        )
    return path.join("downloads", f"{info['id']}.{info['ext']}")
