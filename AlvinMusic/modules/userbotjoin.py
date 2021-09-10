# AlvinMusic (Telegram bot project )
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
from pyrogram import filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from AlvinMusic.helpers.decorators import authorized_users_only
from AlvinMusic.helpers.decorators import errors
from AlvinMusic.services.callsmusic import client as USER
from AlvinMusic.config import SUDO_USERS

@Client.on_message(filters.command(["userbotjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Add me as admin of yor group first</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "AlvinMusic"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "Saya bergabung di sini seperti yang Anda minta")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>Helper sudah bergabung di obrolan</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n pengguna {user.first_name} tidak dapat bergabung dengan grup Anda karena permintaan yang banyak untuk bot pengguna! Pastikan pengguna tidak dilarang dalam grup."
            "\n\nAtau tambahkan @Alvin_junior secara manual ke Grup Anda dan coba lagi</b>",
        )
        return
    await message.reply_text(
        "<b>Helper userbot bergabung obrolan</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>Pengguna tidak dapat meninggalkan grup Anda! Mungkin floodwaits."
            "\n\nAtau secara manual kick saya dari ke Grup Anda</b>",
        )
        return
    
@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("Assistant meninggalkan semua obrolan")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"Assistant meninggalkan... keluar: {left} obrolan. gagal: {failed} obrolan.")
            except:
                failed=failed+1
                await lol.edit(f"Assistant meninggalkan... keluar: {left} obrolan. gagal: {failed} obrolan.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Keluar {left} obrolan. gagal {failed} obrolan.")
    
    
@Client.on_message(filters.command(["userbotjoinchannel","ubjoinc"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("Apakah obrolan tertautkan")
      return    
    chat_id = chid
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Tambahkan saya sebagai admin terlebih dahulu</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "AlvinMusic"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "Saya bergabung di sini seperti yang Anda minta")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>Helper sudah bergabung obrolan</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n pengguna {user.first_name} tidak dapat bergabung dengan grup Anda karena permintaan yang banyak untuk bot pengguna! Pastikan pengguna tidak dibanned dalam channel."
            "\n\nAtau tambahkan @Alvin_junior secara manual ke Grup Anda dan coba lagi</b>",
        )
        return
    await message.reply_text(
        "<b>Helper userbot bergabung ke obrolan</b>",
    )
    
