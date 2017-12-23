# coding=utf-8
from typing import List, Optional


class Config:
    name: str
    url: str
    token: str
    textChannelIds: List[str]
    currencyPair: str
    width: int
    debug: bool
    coinmarketcapId: Optional[str]

    def __init__(self, name: str, url: str, token: str, channelIds: List[str], currencyPair: str, width: int, debug: bool=False, coinmarketcapId: Optional[str]=None) -> None:
        self.name = name
        self.url = url
        self.token = token
        self.textChannelIds = channelIds
        self.currencyPair = currencyPair
        self.width = width
        self.debug = debug
        self.coinmarketcapId = coinmarketcapId
