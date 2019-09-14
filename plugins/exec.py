"""Execute GNU/Linux commands inside Telegram
Syntax: .exec Code"""
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pyrogram import Client, Filters

import asyncio
import io
import subprocess
import time

# maximum message length in Telegram
MAX_MESSAGE_LENGTH = 4096


@Client.on_message(Filters.command("exec", "{")  & Filters.me)
async def execution(client, message):
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_id = message.message_id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id

    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    o = stdout.decode()
    if not o:
        o = "**Tip**: \n`If you want to see the results of your code, I suggest printing them to stdout.`"
    else:
        _o = o.split("\n")
        o = "`\n".join(_o)
    OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"

    if len(OUTPUT) > MAX_MESSAGE_LENGTH:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "exec.text"
            await client.send_document(
                chat_id=message.chat.id,
                document=out_file,
                caption=cmd,
                disable_notification=True,
                reply_to_message_id=reply_to_id
            )
            await event.delete()
    else:
        await message.edit(OUTPUT)
