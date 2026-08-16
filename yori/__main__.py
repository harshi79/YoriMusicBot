# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of YoriMusic (rebranded from AnonXMusic)


import asyncio
import signal
import importlib
from contextlib import suppress

from yori import (yori, app, config, db, logger,
                   stop, thumb, userbot, web, yt)
from yori.plugins import all_modules


async def idle():
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGABRT):
        with suppress(NotImplementedError):
            loop.add_signal_handler(sig, stop_event.set)
    await stop_event.wait()

async def main():
    # Bind $PORT first: Render fails a Web Service deploy if nothing is
    # listening shortly after boot, and Telegram/Mongo startup can be slow.
    await web.start()

    await db.connect()
    await app.boot()
    await userbot.boot()
    await yori.boot()
    await thumb.start()

    for module in all_modules:
        importlib.import_module(f"yori.plugins.{module}")
    logger.info(f"Loaded {len(all_modules)} modules.")

    if config.COOKIES_URL:
        await yt.save_cookies(config.COOKIES_URL)

    sudoers = await db.get_sudoers()
    app.sudoers.update(sudoers)
    app.bl_users.update(await db.get_blacklisted())
    logger.info(f"Loaded {len(app.sudoers)} sudo users.")

    await idle()
    asyncio.create_task(stop())


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
