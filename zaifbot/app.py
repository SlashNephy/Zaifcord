# coding=utf-8
from typing import List

from .bot import ZaifBot
from .config import Config


class App:
    def __init__(self, configs: List[Config]) -> None:
        self.configs = configs

    def start(self) -> None:
        for config in self.configs:
            bot = ZaifBot(config)
            bot.start()
