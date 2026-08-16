# 🎵 YoriMusic

An advanced Telegram **music bot** that streams high-quality audio and video into group voice chats, with a full **moderation** toolkit built in.

Built with **Python**, **Pyrogram**, **Py-TgCalls / ntgcalls**, **FFmpeg** and **MongoDB**.

## ✨ Features

### 🎧 Playback
- Stream **audio** (`/play`) and **video** (`/vplay`) into group voice/video chats
- Sources: **YouTube**, **Spotify**, **Apple Music**, **SoundCloud**, **Resso**, **M3U8 live streams** and Telegram audio/video files
- Queue management with auto-play, **loop**, **shuffle**, **seek**, skip-to-specific, replay
- Inline player controls (pause / resume / skip / stop)
- Auto-generated song thumbnails, lyrics & global stats
- Multi-assistant support (up to 3) for large deployments

### 🛡️ Moderation
- **AuthUsers** — restrict playback controls to chat admins / authorized users / sudo
- **Sudo users** (`/addsudo`, `/delsudo`) with full remote control
- **Blacklist** — `/blacklistchat` blocks chats, global **gban** for users
- **Owner / sudo / admin** permission tiers
- **Admin-only playback mode** and **clean-mode** (auto-delete executed commands)
- Broadcast, stats, maintenance & restart controls for the owner

### 🌐 More
- 13 built-in languages (Arabic, German, English, Spanish, French, Hindi, Japanese, Burmese, Punjabi, Portuguese, Russian, Turkish, Chinese)
- Private-bot mode, auto-leave on inactive voice chats, song download duration limits
- Docker & VPS deploy scripts

## 🚀 Quick start

### Requirements
- Python **3.10+**, **FFmpeg**, **MongoDB** (Atlas or self-hosted), and optionally **uv** / **Deno**

### 1. Clone
```bash
git clone https://t.me/yorichiiprime
cd YoriMusicBot
```

### 2. Configure
```bash
cp sample.env .env
```
Fill in the values (see [sample.env](sample.env)):

| Variable | Description |
| --- | --- |
| `API_ID` / `API_HASH` | From https://my.telegram.org/apps |
| `BOT_TOKEN` | From @BotFather |
| `MONGO_URL` | MongoDB connection string |
| `LOGGER_ID` | Log group ID (bot must be admin there) |
| `OWNER_ID` | Your Telegram user ID |
| `SESSION` | Pyrogram string session for the assistant account (@StringFatherBot) |
| `SUPPORT_CHAT` / `SUPPORT_CHANNEL` | Links shown in the bot menus (default to the YoriMusic group/channel; set empty to hide) |
| `JOIN_CHANNEL` | Channel the assistant joins on startup |
| `PORT` / `WEB_ENABLE` | Web server port and on/off switch (Render sets `PORT` for you) |
| `DEFAULT_THUMB` / `PING_IMG` / `START_IMG` | Artwork (local paths or URLs) |

> Branded artwork lives in [`assets/`](assets). Use `assets/avatar.png` as the bot's
> profile picture in @BotFather. Source art and the regeneration script are in
> [`art/`](art/README.md).

### 3. Run
```bash
bash setup     # installs dependencies (VPS)
bash start     # starts the bot
```

### Docker
```bash
docker build -t yorimusic .
docker run -d --env-file .env -p 8080:8080 --restart unless-stopped yorimusic
```

### Deploy free on Render

The bot ships a small web server, so it can run as a **free Render Web Service**
(the free tier has no Worker plan) and doubles as the project's website.

1. Push this repo to GitHub and create a **New → Blueprint** on
   [Render](https://render.com), pointing at [`render.yaml`](render.yaml) —
   or create a Web Service with **Runtime: Docker** manually.
2. Add the required secrets (`API_ID`, `API_HASH`, `BOT_TOKEN`, `MONGO_URL`,
   `LOGGER_ID`, `OWNER_ID`, `SESSION`) in the dashboard.
3. Deploy. Your site is live at `https://<your-app>.onrender.com`.

> **Keep it awake:** free instances sleep after ~15 minutes of no traffic.
> Point [UptimeRobot](https://uptimerobot.com) at
> `https://<your-app>.onrender.com/health` with a 5-minute interval.

| Endpoint | Purpose |
| --- | --- |
| `/` | Landing page (source in [`web/`](web)) |
| `/health` | Returns `200 OK` with JSON `{"status":"ok","uptime":N}` — for uptime monitors |
| `/healthz`, `/ping` | Aliases of `/health` |

`/health` never touches Telegram or MongoDB, so a slow database can't make your
monitor flap. Set `WEB_ENABLE=False` to turn the server off.

## 📖 Commands

| Command | Description |
| --- | --- |
| `/play` `/vplay` | Play audio / video from a query, URL or reply to media |
| `/pause` `/resume` `/skip` `/stop` | Playback controls |
| `/seek` `/loop` `/shuffle` | Seek, loop and shuffle the queue |
| `/queue` `/playing` | View the queue / current track |
| `/settings` | Toggle admin-only mode, clean-mode and language |
| `/blacklistchat` | Block a chat from using the bot |
| `/auth` | Manage authorized users |
| `/addsudo` `/delsudo` | Manage sudo users (owner only) |
| `/broadcast` `/stats` `/restart` `/maintenance` | Owner tools |

Use `/help` inside the bot for the full, language-localised menu.

## 💬 Community

- Channel — [@yorifederation](https://t.me/yorifederation)
- Support group — [join here](https://t.me/+nzIAZDVK_61lZDQ9)

## 📄 License

MIT License. This project is rebranded from [AnonXMusic](https://github.com/AnonymousX1025/AnonXMusic) — original
copyright retained as required by the MIT license (see [LICENSE](LICENSE)).

## 🙏 Credits
- Original project: [AnonymousX1025/AnonXMusic](https://github.com/AnonymousX1025/AnonXMusic)
- [Pyrogram](https://github.com/pyrogram/pyrogram) · [Py-TgCalls](https://github.com/pytgcalls/pytgcalls)
