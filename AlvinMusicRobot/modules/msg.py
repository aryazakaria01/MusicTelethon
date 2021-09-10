# AlvinMusicRobot (Telegram bot project )
# Copyright (C) 2021  Inukaasith

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

import os
from AlvinMusicRobot.config import SOURCE_CODE
from AlvinMusicRobot.config import ASSISTANT_NAME
from AlvinMusicRobot.config import PROJECT_NAME
from AlvinMusicRobot.config import SUPPORT_GROUP
from AlvinMusicRobot.config import UPDATES_CHANNEL
class Messages():
      START_MSG = "**🎶Halo🎶 [{}](tg://user?id={})!**\n\n Saya Adalah Bot Canggih Yang Dibuat Untuk Memutar Musik Di Voice Chat Grup & Channel.\n\n kirim /help Untuk Info Lebih Lanjut.\n\n jika ada yang ingin ditanyakan bisa PM @alvin_junior tapi mohon untuk tidak melakukan spam."
      HELP_MSG = [
        ".",
f"""
**🎶Hey🎶 Selamat Datang Kembali di {PROJECT_NAME}

⚪️ {PROJECT_NAME} Dapat Memutar Musik Di Voice Chat Grup Anda Serta Voice Chat Channel

⚪️ Nama Assistant >> @{ASSISTANT_NAME}\n\nKlik Next Untuk Petunjuk Berikutnya**
""",

f"""
**Setting**

1) Jadikan Bot Admin (Group Dan Di Channel Jika Menggunakan cplay)
2) Mulai voice chat
3) Coba /play [nama Lagu] Untuk Pertama Kali Oleh Admin
*) Jika userbot bergabung nikmati musik, Jika tidak tambahkan @{ASSISTANT_NAME} ke grup Anda dan coba lagi
**Untuk Voice Chat Channel**
1) Jadikan Saya Admin Di Channel Anda
2) Ketik /userbotjoinchannel Di Dalam Group Yang Tertautkan
3) Sekarang Kirim Perintah Di Grup Yang Tertautkan
""",
f"""
**Perintah**

**=>> Song Playing 🎧**

- /play: Putar Lagu Yang Di Request
- /play [yt url] : Mainkan url yt yang diberikan
- /play [reply to audio]: Putar audio yang dibalas
- /splay: Putar Lagu Melalui jio saavn
- /ytplay: Langsung memutar lagu melalui Youtube Music

**=>> Playback ⏯**

- /player: Buka Menu Setting Pemain
- /skip: Melewati Trek Saat Ini
- /pause: Jeda Lagu
- /resume: Memulai Lagu Yang Di Jeda
- /end: Menghentikan Pemutaran Media
- /current: Menunjukkan Trek Putar Saat Ini
- /playlist: Tampilkan Daftar Putar

*Player cmd dan semua cmd lainnya kecuali /play, /current dan /playlist hanya untuk admin grup.
""",

f"""
**=>> Channel Music Play 🛠**

⚪️ Hanya Untuk Admin Di Grup Yang Tertautkan:

- /cplay [song name] - Putar Lagu Yang Di Request
- /csplay [song name] - Putar Lagu Melalui jio saavn
- /cplaylist - Tampilkan Daftar Putar Sekarang
- /cccurrent - Tampilkan Daftar Putar 
- /cplayer - Buka Panel Pengaturan Pemutar Musik
- /cpause - Jeda Lagu
- /cresume - Mmemuali Lagu Yang Di Jeda
- /cskip - Melewati Trek
- /cend - Menghentikan Music
- /userbotjoinchannel - undang asisten ke obrolan Anda

channel juga dapat digunakan sebagai pengganti c ( /cplay = /channelplay )

⚪️ Jika Anda tidak suka play di grup tertaut:

1) Dapatkan ID saluran Anda.
2) Buat grup dengan judul: Channel Music: your_channel_id
3) Tambahkan bot sebagai admin Saluran dengan izin penuh
4) Tambahkan @{ASSISTANT_NAME} ke saluran sebagai admin.
5) Cukup kirim perintah di grup Anda. (ingat untuk menggunakan /ytplay sebagai gantinya /play)
""",

f"""
**=>> More tools 🧑‍🔧**

- /musicplayer [on/off]: Aktifkan/Nonaktifkan Pemutar musik
- /admincache: Memperbarui info admin grup Anda. Coba jika bot tidak mengenali admin
- /userbotjoin: undang @{ASSISTANT_NAME} ke obrolan Anda
""",
f"""
**=>> Song Download 🎸**

- /video [song mame]: Download video dari youtube
- /song [song name]: Download audio dari youtube
- /saavn [song name]: Download lagu dari saavn
- /deezer [song name]: Download lagu dari deezer

**=>> Search Tools 📄**

- /search [song name]: Cari di youtube untuk lagu
- /lyrics [song name]: Lirik lagu
""",

f"""
**=>> Commands for Sudo Users ⚔️**

 - /userbotleaveall - keluarkan asisten dari semua obrolan
 - /broadcast <reply to message> - brodcast global membalas pesan ke semua obrolan
 - /pmpermit [on/off] - Aktif/Nonaktif pesan pmpermit
*Sudo Users dapat menjalankan perintah apa pun di grup mana pun

"""
      ]
