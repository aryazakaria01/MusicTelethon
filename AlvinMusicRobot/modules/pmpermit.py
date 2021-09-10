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

from pyrogram import Client
import asyncio
from AlvinMusicRobot.config import SUDO_USERS
from AlvinMusicRobot.config import PMPERMIT
from pyrogram import filters
from pyrogram.types import Message
from AlvinMusicRobot.services.callsmusic import client as USER

PMSET =True
pchats = []

@USER.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: USER, message: Message):
    if PMPERMIT == "ENABLE":
        if PMSET:
            chat_id = message.chat.id
            if chat_id in pchats:
                return
            await USER.send_message(
                message.chat.id,
                "Halo, Ini adalah layanan asisten musik .\n\n ❗️ Rules:\n   - Tidak ada obrolan yang diizinkan\n   - tidak ada spam yang diizinkan \n\n 👉 **KIRIM LINK UNDANGAN GRUP ATAU USERNAME JIKA USERBOT TIDAK BISA JOIN GROUP ANDA.**\n\n ⚠️ Disclamer: Jika Anda mengirim pesan di sini, itu berarti admin akan melihat pesan Anda dan bergabung dengan obrolan\n    - jangan menambahkan pengguna ini ke group private.\n   - Jangan Bagikan info pribadi di sini\n\n",
            )
            return

    

@Client.on_message(filters.command(["/pmpermit"]))
async def bye(client: Client, message: Message):
    if message.from_user.id in SUDO_USERS:
        global PMSET
        text = message.text.split(" ", 1)
        queryy = text[1]
        if queryy == "on":
            PMSET = True
            await message.reply_text("Pmpermit diaktifkan")
            return
        if queryy == "off":
            PMSET = None
            await message.reply_text("Pmpermit dinonaktifkan")
            return

@USER.on_message(filters.text & filters.private & filters.me)        
async def autopmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if not chat_id in pchats:
        pchats.append(chat_id)
        await message.reply_text("Disetujui untuk PM karena pesan keluar")
        return
    message.continue_propagation()    
    
@USER.on_message(filters.command("a", [".", ""]) & filters.me & filters.private)
async def pmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if not chat_id in pchats:
        pchats.append(chat_id)
        await message.reply_text("disetujui untuk PM")
        return
    message.continue_propagation()    
    

@USER.on_message(filters.command("da", [".", ""]) & filters.me & filters.private)
async def rmpmPermiat(client: USER, message: Message):
    chat_id = message.chat.id
    if chat_id in pchats:
        pchats.remove(chat_id)
        await message.reply_text("tidak disetujui untuk PM")
        return
    message.continue_propagation()
