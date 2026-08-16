# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of YoriMusic (rebranded from AnonXMusic)


"""Lightweight aiohttp web server.

Serves two things:

* ``/health`` (and ``/healthz``, ``/ping``) — a plain ``200 OK`` for uptime
  monitors such as UptimeRobot. Kept dependency-free and instant: it never
  touches Telegram or MongoDB, so a slow database can't make the monitor
  flap.
* ``/`` — the public landing page in ``web/``, so the same Render service
  doubles as the project's website.

Render's free *Web Service* tier requires the process to bind ``$PORT`` or the
deploy is marked failed, and it idles the instance without external traffic —
which is exactly what the uptime monitor prevents.
"""

import time
from pathlib import Path

from aiohttp import web

from yori import boot, config, logger

WEB_DIR = Path(__file__).resolve().parent.parent.parent / "web"


class WebServer:
    def __init__(self):
        self.runner: web.AppRunner | None = None
        self.app = web.Application()
        self._add_routes()

    def _add_routes(self) -> None:
        self.app.router.add_get("/health", self.health)
        self.app.router.add_get("/healthz", self.health)
        self.app.router.add_get("/ping", self.health)
        self.app.router.add_get("/", self.index)

        if WEB_DIR.is_dir():
            # Static assets for the landing page.
            self.app.router.add_static("/static/", WEB_DIR / "static", name="static")
            self.app.router.add_static("/assets/", WEB_DIR.parent / "assets", name="assets")

    async def health(self, request: web.Request) -> web.Response:
        """Always-200 endpoint for UptimeRobot / Render health checks."""
        return web.json_response(
            {
                "status": "ok",
                "uptime": int(time.time() - boot),
            }
        )

    async def index(self, request: web.Request) -> web.Response:
        index_file = WEB_DIR / "index.html"
        if index_file.is_file():
            return web.FileResponse(index_file)
        return web.Response(text="OK", content_type="text/plain")

    async def start(self) -> None:
        if not config.WEB_ENABLE:
            logger.info("Web server disabled.")
            return

        self.runner = web.AppRunner(self.app, access_log=None)
        await self.runner.setup()
        site = web.TCPSite(self.runner, "0.0.0.0", config.PORT)
        await site.start()
        logger.info(f"Web server listening on 0.0.0.0:{config.PORT}")

    async def close(self) -> None:
        if self.runner:
            await self.runner.cleanup()
            logger.info("Web server stopped.")
