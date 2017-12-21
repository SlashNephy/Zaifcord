# coding=utf-8
import asyncio
import time
from datetime import datetime
from threading import Thread
from typing import Dict

import discord
from colorama import Back
from discord import Game, Embed, Colour, Client, Channel

from .config import Config
from .stream import ZaifStream
from .utils import Utils


class ZaifBot:
    def __init__(self, config: Config) -> None:
        self.config: Config = config

        self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self.client: Client = Client(loop=self.loop)
        self.textChannels: Dict[str, Channel] = {}

        self.zaifStream: ZaifStream = ZaifStream(self.config.currencyPair)
        self.priceHistory: Dict = {}

    async def sendMessage(self, phase: int, up: bool, price: float):
        key: str = f"{'u' if up else 'd'}_{phase}"
        lastTime = self.priceHistory.get(key)
        self.priceHistory[key] = datetime.now()
        if lastTime and (datetime.now() - lastTime).total_seconds() < 180:
            return

        embedObject = Embed(
                title="上昇中:arrow_heading_up:" if up else "下落中:arrow_heading_down:",
                color=Colour(int("88B04B" if up else "FF4444", 16)),
                description=f"{phase}円台に突入しました！現在 {price}JPY",
                timestamp=datetime.utcnow(),
        )
        embedObject.set_author(
                name=f"{self.config.name} (Zaif)",
                url=self.config.url
        )

        for channel in self.textChannels.values():
            await self.client.purge_from(channel, check=lambda x: x.author == self.client.user)
            await self.client.send_message(channel, embed=embedObject)
        Utils.printInfo(f"{self.config.name} が {Back.LIGHTRED_EX + '上昇中' if up else Back.LIGHTBLUE_EX + '下落中'}{Back.RESET}です. {phase}円台に突入しました. 現在の価格は {price}JPYです.")

    async def stream(self) -> None:
        self.zaifStream.start()

        phase: int = None
        while True:
            try:
                t = self.zaifStream.get()
                if t:
                    price, action = t["last_price"]["price"], "買い" if t["last_price"]["action"] == "ask" else "売り"
                    latestPhase = int(price // self.config.width) * self.config.width
                    preciseLatestPhase = int(price // 10) * 10
                    if phase and phase != latestPhase:
                        await self.sendMessage(preciseLatestPhase, latestPhase > phase, price)

                    phase = latestPhase

                    await self.client.change_presence(
                        game=Game(
                            name=f"{preciseLatestPhase}円台{'前半' if price - preciseLatestPhase <= 5 else '後半'} (Zaif)"
                        )
                    )

                    if self.config.debug:
                        Utils.printDebug(f"{self.config.name}: {action} {price}JPY")

                if self.zaifStream.isDead():
                    self.zaifStream.kill()
                    self.zaifStream = ZaifStream(self.config.currencyPair)
                    self.zaifStream.start()
                    await asyncio.sleep(10)
                    continue

                await asyncio.sleep(0.5)
            except Exception as e:
                print(e)

    def start(self) -> None:
        Thread(target=self._start).start()

    def _start(self) -> None:
        @self.client.event
        async def on_ready() -> None:
            if len(self.client.servers) == 0:
                Utils.printError("サーバに参加していません. https://discordapi.com/permissions.html などを利用してサーバにBotを追加してください.", critical=True)

            for server in self.client.servers:
                try:
                    await self.client.change_nickname(server.me, self.config.name)
                except discord.errors.Forbidden:
                    pass
            for channelId in self.config.textChannelIds:
                self.textChannels[channelId] = self.client.get_channel(channelId)
                await self.client.purge_from(self.textChannels[channelId], check=lambda x: x.author == self.client.user)

            Utils.printInfo(f"Discordに接続しました: Bot \"{self.config.name}\"")
            await self.stream()

        @self.client.event
        async def on_error(event, *args, **kwargs) -> None:
            Utils.printError(f"{event} -> {args} + {kwargs}")

        while True:
            try:
                self.client.run(self.config.token)
            except Exception as e:
                Utils.printError(f"Discordとの接続が失われました ({e}). 3秒後に再接続します.")
                time.sleep(3)
