# AlvinMusicRobot (Telegram bot project)
# Copyright (C) 2021  Inukaasith
# Copyright (C) 2021  TheHamkerCat (Python_ARQ)
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


import json
from os import path
from typing import Callable

import aiofiles
import aiohttp
import ffmpeg
import requests
import wget
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from pyrogram import Client 
from pyrogram import filters
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import Voice
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Python_ARQ import ARQ
from youtube_search import YoutubeSearch
from AlvinMusicRobot.modules.play import generate_cover
from AlvinMusicRobot.modules.play import arq
from AlvinMusicRobot.modules.play import cb_admin_check
from AlvinMusicRobot.modules.play import transcode
from AlvinMusicRobot.modules.play import convert_seconds
from AlvinMusicRobot.modules.play import time_to_seconds
from AlvinMusicRobot.modules.play import changeImageSize
from AlvinMusicRobot.config import BOT_NAME as bn
from AlvinMusicRobot.config import DURATION_LIMIT
from AlvinMusicRobot.config import UPDATES_CHANNEL as updateschannel
from AlvinMusicRobot.config import que
from AlvinMusicRobot.function.admins import admins as a
from AlvinMusicRobot.helpers.errors import DurationLimitError
from AlvinMusicRobot.helpers.decorators import errors
from AlvinMusicRobot.helpers.admins import get_administrators
from AlvinMusicRobot.helpers.channelmusic import get_chat_id
from AlvinMusicRobot.helpers.decorators import authorized_users_only
from AlvinMusicRobot.helpers.filters import command
from AlvinMusicRobot.helpers.filters import other_filters
from AlvinMusicRobot.helpers.gets import get_file_name
from AlvinMusicRobot.services.callsmusic import callsmusic
from AlvinMusicRobot.services.callsmusic import client as USER
from AlvinMusicRobot.services.converter.converter import convert
from AlvinMusicRobot.services.downloaders import youtube
from AlvinMusicRobot.services.queues import queues

chat_id = None


@Client.on_message(filters.command(["channelplaylist","cplaylist"]) & filters.group & ~filters.edited)
async def playlist(client, message):
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
    except:
      message.reply("apakah obrolan tertautkan?")
      return
    global que
    queue = que.get(lol)
    if not queue:
        await message.reply_text("Player is idle")
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style="md")
    msg = "<b>Now Playing</b> in {}".format(lel.linked_chat.title)
    msg += "\n- " + now_playing
    msg += "\n- Req by " + by
    temp.pop(0)
    if temp:
        msg += "\n\n"
        msg += "<b>Queue</b>"
        for song in temp:
            name = song[0]
            usr = song[1].mention(style="md")
            msg += f"\n- {name}"
            msg += f"\n- Req by {usr}\n"
    await message.reply_text(msg)


# ============================= Settings =========================================


def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.active_chats:
        # if chat.id in active_chats:
        stats = "Settings of **{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "Volume : {}%\n".format(vol)
            stats += "Songs in queue : `{}`\n".format(len(que))
            stats += "Now Playing : **{}**\n".format(queue[0][0])
            stats += "Requested by : {}".format(queue[0][1].mention)
    else:
        stats = None
    return stats


def r_ply(type_):
    if type_ == "play":
        pass
    else:
        pass
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏹", "cleave"),
                InlineKeyboardButton("⏸", "cpuse"),
                InlineKeyboardButton("▶️", "cresume"),
                InlineKeyboardButton("⏭", "cskip"),
            ],
            [
                InlineKeyboardButton("Playlist 📖", "cplaylist"),
            ],
            [InlineKeyboardButton("❌ Close", "ccls")],
        ]
    )
    return mar


@Client.on_message(filters.command(["channelcurrent","ccurrent"]) & filters.group & ~filters.edited)
async def ee(client, message):
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      await message.reply("apakah obrolan tertautkan")
      return
    queue = que.get(lol)
    stats = updated_stats(conv, queue)
    if stats:
        await message.reply(stats)
    else:
        await message.reply("tidak ada VC yang berjalan saat ini")


@Client.on_message(filters.command(["channelplayer","cplayer"]) & filters.group & ~filters.edited)
@authorized_users_only
async def settings(client, message):
    playing = None
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      await message.reply("apakah obrolan tertautkan")
      return
    queue = que.get(lol)
    stats = updated_stats(conv, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("pause"))

        else:
            await message.reply(stats, reply_markup=r_ply("play"))
    else:
        await message.reply("tidak ada VC yang berjalan saat ini")


@Client.on_callback_query(filters.regex(pattern=r"^(cplaylist)$"))
async def p_cb(b, cb):
    global que
    try:
      lel = await client.get_chat(cb.message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      return    
    que.get(lol)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    cb.message.chat
    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "playlist":
        queue = que.get(lol)
        if not queue:
            await cb.message.edit("Player is idle")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**Now Playing** in {}".format(conv.title)
        msg += "\n- " + now_playing
        msg += "\n- Req by " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Queue**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n- {name}"
                msg += f"\n- Req by {usr}\n"
        await cb.message.edit(msg)


@Client.on_callback_query(
    filters.regex(pattern=r"^(cplay|cpause|cskip|cleave|cpuse|cresume|cmenu|ccls)$")
)
@cb_admin_check
async def m_cb(b, cb):
    global que
    if (
        cb.message.chat.title.startswith("Channel Music: ")
        and chat.title[14:].isnumeric()
    ):
        chet_id = int(chat.title[13:])
    else:
      try:
        lel = await b.get_chat(cb.message.chat.id)
        lol = lel.linked_chat.id
        conv = lel.linked_chat
        chet_id = lol
      except:
        return
    qeue = que.get(chet_id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    m_chat = cb.message.chat
    

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "cpause":
        if (chet_id not in callsmusic.active_chats) or (
            callsmusic.active_chats[chet_id] == "paused"
        ):
            await cb.answer("obrolan tidak terhubung!", show_alert=True)
        else:
            callsmusic.pause(chet_id)
            await cb.answer("Musik dijeda!")
            await cb.message.edit(
                updated_stats(conv, qeue), reply_markup=r_ply("play")
            )

    elif type_ == "cplay":
        if (chet_id not in callsmusic.active_chats) or (
            callsmusic.active_chats[chet_id] == "playing"
        ):
            await cb.answer("obrolan tidak terhubung!", show_alert=True)
        else:
            callsmusic.resume(chet_id)
            await cb.answer("Musik diputar!")
            await cb.message.edit(
                updated_stats(conv, qeue), reply_markup=r_ply("pause")
            )

    elif type_ == "cplaylist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("Player is idle")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**Now Playing** in {}".format(cb.message.chat.title)
        msg += "\n- " + now_playing
        msg += "\n- Req by " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Queue**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n- {name}"
                msg += f"\n- Req by {usr}\n"
        await cb.message.edit(msg)

    elif type_ == "cresume":
        if (chet_id not in callsmusic.active_chats) or (
            callsmusic.active_chats[chet_id] == "playing"
        ):
            await cb.answer("obrolan tidak terhubung atau sedang memutar", show_alert=True)
        else:
            callsmusic.resume(chet_id)
            await cb.answer("Musik diputar!")
    elif type_ == "cpuse":
        if (chet_id not in callsmusic.active_chats) or (
            callsmusic.active_chats[chet_id] == "paused"
        ):
            await cb.answer("obrolan tidak terhubung atau sedang dijeda", show_alert=True)
        else:
            callsmusic.pause(chet_id)
            await cb.answer("Musik dijeda!")
    elif type_ == "ccls":
        await cb.answer("menutup menu")
        await cb.message.delete()

    elif type_ == "cmenu":
        stats = updated_stats(conv, qeue)
        await cb.answer("membuka menu")
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏹", "cleave"),
                    InlineKeyboardButton("⏸", "cpuse"),
                    InlineKeyboardButton("▶️", "cresume"),
                    InlineKeyboardButton("⏭", "cskip"),
                ],
                [
                    InlineKeyboardButton("Playlist 📖", "cplaylist"),
                ],
                [InlineKeyboardButton("❌ Close", "ccls")],
            ]
        )
        await cb.message.edit(stats, reply_markup=marr)
    elif type_ == "cskip":
        if qeue:
            qeue.pop(0)
        if chet_id not in callsmusic.active_chats:
            await cb.answer("obrolan tidak terhubung!", show_alert=True)
        else:
            queues.task_done(chet_id)

            if queues.is_empty(chet_id):
                callsmusic.stop(chet_id)
                await cb.message.edit("- tidak ada daftar putar..\n- Leaving VC!")
            else:
                await callsmusic.set_stream(
                    chet_id, queues.get(chet_id)["file"]
                )
                await cb.answer.reply_text("✅ <b>Skipped</b>")
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(
                    f"- Skipped track\n- Now Playing **{qeue[0][0]}**"
                )

    else:
        if chet_id in callsmusic.active_chats:
            try:
               queues.clear(chet_id)
            except QueueEmpty:
                pass

            callsmusic.stop(chet_id)
            await cb.message.edit("berhasil keluar obrolan!")
        else:
            await cb.answer("obrolan tidak terhubung!", show_alert=True)


@Client.on_message(filters.command(["channelplay","cplay"])  & filters.group & ~filters.edited)
@authorized_users_only
async def play(_, message: Message):
    global que
    lel = await message.reply("🔄 <b>Processing</b>")

    try:
      conchat = await _.get_chat(message.chat.id)
      conv = conchat.linked_chat
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("apakah obrolan tertautkan")
      return
    try:
      administrators = await get_administrators(conv)
    except:
      await message.reply("apakah saya admin di channel")
    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        "<b>ingat untuk menambah helper di channel</b>",
                    )
                    pass

                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>tambahkan saya sebagai admin terlebih dahulu</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await lel.edit(
                        "<b>helper userbot bergabung di channel</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🔴 Flood Wait Error 🔴 \npengguna {user.first_name}  tidak dapat bergabung dengan grup Anda karena permintaan yang banyak untuk bot pengguna! Pastikan pengguna tidak dibanned dalam grup."
                        "\n\nAtau tambahkan @Alvin_junior secara manual ke Grup Anda dan coba lagi</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i> {user.first_name} Userbot tidak ada dalam obrolan ini, Minta admin untuk mengirim / memutar perintah untuk pertama kalinya atau menambahkan asisten secara manual</i>"
        )
        return
    message.from_user.id
    text_links = None
    message.from_user.first_name
    await lel.edit("🔎 <b>Finding</b>")
    message.from_user.id
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    if message.reply_to_message:
        if message.reply_to_message.audio:
            pass
        entities = []
        toxt = message.reply_to_message.text \
              or message.reply_to_message.caption
        if message.reply_to_message.entities:
            entities = message.reply_to_message.entities + entities
        elif message.reply_to_message.caption_entities:
            entities = message.reply_to_message.entities + entities
        urls = [entity for entity in entities if entity.type == 'url']
        text_links = [
            entity for entity in entities if entity.type == 'text_link'
        ]
    else:
        urls=None
    if text_links:
        urls = True    
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            await lel.edit(
                f"❌ Video lebih lama {DURATION_LIMIT} menit tidak diizinkan untuk bermain!"
            )
            return
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📖 Playlist", callback_data="cplaylist"),
                    InlineKeyboardButton("Menu ⏯ ", callback_data="cmenu"),
                ],
                [InlineKeyboardButton(text="❌ Close", callback_data="ccls")],
            ]
        )
        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/d19b68d228e2dc46eb8f5.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif urls:
        query = toxt
        await lel.edit("🎵 **memuat**")
        ydl_opts = {"format": "bestaudio/best"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "Song tidak ditemukan.Coba lagu lain atau mungkin mengejanya dengan benar."
            )
            print(str(e))
            return
        try:    
            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
            if (dur / 60) > DURATION_LIMIT:
                 await lel.edit(f"❌ Video lebih lama {DURATION_LIMIT} menit tidak diizinkan untuk bermain!")
                 return
        except:
            pass        
        dlurl = url
        dlurl=dlurl.replace("youtube","youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📖 Playlist", callback_data="cplaylist"),
                    InlineKeyboardButton("Menu ⏯ ", callback_data="cmenu"),
                ],
                [
                    InlineKeyboardButton(text="🎬 YouTube", url=f"{url}"),
                    InlineKeyboardButton(text="Download 📥", url=f"{dlurl}"),
                ],
                [InlineKeyboardButton(text="❌ Close", callback_data="ccls")],
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(youtube.download(url))        
    else:
        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        await lel.edit("🎵 **Processing**")
        ydl_opts = {"format": "bestaudio/best"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "Song tidak ditemukan.Coba lagu lain atau mungkin mengejanya dengan benar."
            )
            print(str(e))
            return
        try:    
            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
            if (dur / 60) > DURATION_LIMIT:
                 await lel.edit(f"❌ Video lebih lama {DURATION_LIMIT} menit tidak diizinkan untuk bermain!")
                 return
        except:
            pass
        dlurl = url
        dlurl=dlurl.replace("youtube","youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📖 Playlist", callback_data="cplaylist"),
                    InlineKeyboardButton("Menu ⏯ ", callback_data="cmenu"),
                ],
                [
                    InlineKeyboardButton(text="🎬 YouTube", url=f"{url}"),
                    InlineKeyboardButton(text="Download 📥", url=f"{dlurl}"),
                ],
                [InlineKeyboardButton(text="❌ Close", callback_data="ccls")],
            ]
        )
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await convert(youtube.download(url))
    chat_id = chid
    if chat_id in callsmusic.active_chats:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption=f"#⃣ lagu yang anda request <b>queued</b> di posisi {position}!",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        chat_id = chid
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await callsmusic.set_stream(chat_id, file_path)
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="▶️ <b>Playing</b> lagu yang anda request {} via Youtube Music 😎 di Linked Channel".format(
                message.from_user.mention()
            ),
        )
        os.remove("final.png")
        return await lel.delete()


@Client.on_message(filters.command(["channelsplay","csplay"]) & filters.group & ~filters.edited)
@authorized_users_only
async def jiosaavn(client: Client, message_: Message):
    global que
    lel = await message_.reply("🔄 **memuat**")
    try:
      conchat = await client.get_chat(message_.chat.id)
      conid = conchat.linked_chat.id
      conv = conchat.linked_chat
      chid = conid
    except:
      await message_.reply("apakah obrolan tertautkan")
      return
    try:
      administrators = await get_administrators(conv)
    except:
      await message.reply("apakah saya admin di channel?")
    try:
        user = await USER.get_me()
    except:
        user.first_name = "AlvinMusicRobot"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await client.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message_.from_user.id:
                if message_.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        "<b>ingat untuk tambahkan helper di channel</b>",
                    )
                    pass
                try:
                    invitelink = await client.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>tambahkan saya sebagai admin terlebih dahulu</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await lel.edit(
                        "<b>helper userbot bergabung ke channel</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🔴 Flood Wait Error 🔴 \npengguna {user.first_name}  tidak dapat bergabung dengan grup Anda karena permintaan yang banyak untuk bot pengguna! Pastikan pengguna tidak dibanned dalam grupp."
                        "\n\nAtau tambahkan @Alvin_junior secara manual ke Grup Anda dan coba lagi</b>",
                    )
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            "<i> helper Userbot tidak ada dalam obrolan ini, Minta admin untuk mengirim / memutar perintah untuk pertama kalinya atau menambahkan asisten secara manual</i>"
        )
        return
    requested_by = message_.from_user.first_name
    chat_id = message_.chat.id
    text = message_.text.split(" ", 1)
    query = text[1]
    res = lel
    await res.edit(f"mencari 🔎 untuk `{query}` di jio saavn")
    try:
        songs = await arq.saavn(query)
        if not songs.ok:
            await message_.reply_text(songs.result)
            return
        sname = songs.result[0].song
        slink = songs.result[0].media_url
        ssingers = songs.result[0].singers
        sthumb = "https://telegra.ph/file/d19b68d228e2dc46eb8f5.jpg"
        sduration = int(songs.result[0].duration)
    except Exception as e:
        await res.edit("Tidak Menemukan Apa-apa!, Anda Harus Mengerjakan Bahasa Inggris Anda.")
        print(str(e))
        return
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📖 Playlist", callback_data="cplaylist"),
                InlineKeyboardButton("Menu ⏯ ", callback_data="cmenu"),
            ],
            [
                InlineKeyboardButton(
                    text="Join Updates Channel", url=f"https://t.me/{updateschannel}"
                )
            ],
            [InlineKeyboardButton(text="❌ Close", callback_data="ccls")],
        ]
    )
    file_path = await convert(wget.download(slink))
    chat_id = chid
    if chat_id in callsmusic.active_chats:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = sname
        r_by = message_.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await res.delete()
        m = await client.send_photo(
            chat_id=message_.chat.id,
            reply_markup=keyboard,
            photo="final.png",
            caption=f"✯{bn}✯=#️⃣ Queued di posisi {position}",
        )

    else:
        await res.edit_text(f"{bn}=▶️ memutar.....")
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = sname
        r_by = message_.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
    await callsmusic.set_stream(chat_id, file_path)
    await res.edit("membuat Thumbnail.")
    await generate_cover(requested_by, sname, ssingers, sduration, sthumb)
    await res.delete()
    m = await client.send_photo(
        chat_id=message_.chat.id,
        reply_markup=keyboard,
        photo="final.png",
        caption=f"memutar {sname} Via Jiosaavn di linked channel",
    )
    os.remove("final.png")
