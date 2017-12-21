# coding=utf-8
import json
import time
import traceback
from datetime import datetime
from threading import Thread
from typing import Optional, Dict

from websocket import WebSocketApp

from .utils import Utils


class ZaifStream:
    def __init__(self, pair: str):
        self.url: str = f"wss://ws.zaif.jp/stream?currency_pair={pair}"

        self.__last: Dict = None
        self.__lastUpdate: datetime = None
        self.__stop: bool = False

    def start(self) -> None:
        Thread(target=self._start).start()

    def _start(self) -> None:
        while not self.__stop:
            try:
                WebSocketApp(self.url, on_open=self.__onOpen, on_error=self.__onError, on_message=self.__onMessage).run_forever()
            except Exception:
                self.__onError(None, traceback.format_exc())
            finally:
                Utils.printError("WebSocket APIから切断されました. 3秒後に再接続します.")
                time.sleep(3)

    def get(self) -> Optional[Dict]:
        t = self.__last
        if t:
            self.__last = None
        return t

    def isDead(self) -> bool:
        return isinstance(self.__lastUpdate, datetime) and (datetime.now() - self.__lastUpdate).total_seconds() > 60

    def kill(self) -> None:
        self.__stop = True

    def __onOpen(self, _) -> None:
        Utils.printInfo(f"Zaif WebSocket APIに接続しました: {self.url}")

    def __onError(self, _, error: str):
        Utils.printError(f"WebSocketに接続中にエラーが発生しました: {error}")

    def __onMessage(self, _, message: str) -> None:
        self.__last = json.loads(message)
        self.__lastUpdate = datetime.now()
