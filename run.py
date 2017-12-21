# encoding: utf-8
from zaifbot import App, Config

bots = [
    Config(
        name="MONA",
        url="https://zaif.jp/trade_mona_jpy",
        token="<Botのトークンを入力してください>",
        channelIds=[""],
        currencyPair="mona_jpy",
        width=100
    ),
    Config(
        name="CMS (ERC20)",
        url="https://zaif.jp/trade/erc20.cms_jpy",
        token="<Botのトークンを入力してください>",
        channelIds=["393333723052900352"],
        currencyPair="erc20.cms_jpy",
        width=50
    )
]

if __name__ == "__main__":
    App(configs=bots).start()
