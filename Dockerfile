FROM python:3.13-slim

WORKDIR /app

# ffmpeg is required for streaming; deno is used by yt-dlp for some extractors.
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends ffmpeg curl unzip ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL https://deno.land/install.sh | sh

ENV DENO_INSTALL="/root/.deno"
ENV PATH="${DENO_INSTALL}/bin:${PATH}"

RUN curl -Ls https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Install dependencies first so this layer caches across code changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

# Unbuffered logs so Render's log stream is live.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Render injects $PORT and expects the service to bind it. The default keeps
# `docker run -p 8080:8080` working locally.
ENV PORT=8080
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=45s --retries=3 \
    CMD python3 -c "import os,urllib.request;urllib.request.urlopen(f\"http://127.0.0.1:{os.getenv('PORT','8080')}/health\").read()" || exit 1

CMD ["uv", "run", "python3", "-m", "yori"]
