FROM mcr.microsoft.com/playwright/python:v1.64.1-noble
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ffmpeg xclip x11-utils \
    && rm -rf /var/lib/apt/lists/* \
    && (id -u pwuser >/dev/null 2>&1 || useradd --create-home --shell /bin/bash pwuser) \
    && mkdir -p /home/pwuser/.cache /home/pwuser/.config \
    && chown -R pwuser:pwuser /home/pwuser
