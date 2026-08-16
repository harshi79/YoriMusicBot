# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of YoriMusic (rebranded from AnonXMusic)


from pyrogram import filters, types

from yori import yori, app, db, lang
from yori.helpers import can_manage_vc


@app.on_message(filters.command(["skip", "next"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _skip(_, m: types.Message):
    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang["not_playing"])

    await yori.play_next(m.chat.id)
    await m.reply_text(m.lang["play_skipped"].format(m.from_user.mention))
