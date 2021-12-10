FROM python:3.10.0-slim-bullseye
LABEL org.opencontainers.image.source https://github.com/qolplus/discord-current-price-bot.py
WORKDIR /usr/src/app
ENV SHORT_CODE=""
ENV DISCORD_BOT_TOKEN=""

COPY install-poetry.py pyproject.toml poetry.lock /usr/src/app/
RUN python install-poetry.py &&\
    $HOME/.local/bin/poetry install

COPY . /usr/src/app/

ENTRYPOINT [ "./entrypoint.sh" ]
