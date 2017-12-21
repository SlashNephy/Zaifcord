# Zaifcord
Zaifの最終価格を通知するDiscord Botです. 対日本円レートの通貨ペアにのみ対応しています.

# 動作環境
Python 3.6 以降

# 機能
- 5円刻みで現在の価格をプレイ中として表示します.  
<img src="https://raw.githubusercontent.com/SlashNephy/Zaifcord/master/img/playing.png">  
5円刻みとしているのは Discord APIに負荷を掛けすぎないためです.
- 大きな価格変動があった際に メッセージを送信します.  
<img src="https://raw.githubusercontent.com/SlashNephy/Zaifcord/master/img/price_change.png">  
例えば 50円間隔で価格変動を監視したいときは `width=50` とします.

# 導入方法
##### 1. pipで必要なライブラリをインストール.
```bash
pip install discord.py colorama
```

##### 2. run.py 内にBotの情報を記述.
Botのトークンは https://discordapp.com/developers/applications/me で取得できます.
```python
bots = [
    Config(
        name="MONA",  # Bot名 (ニックネーム)
        url="https://zaif.jp/trade_mona_jpy",  # 取引ページ
        token="xxxxxxxxxxxxx",  # Botのトークン
        channelIds=["0000000000000"],  # 価格変動を通知するテキストチャンネルID
        currencyPair="mona_jpy",  # 通貨ペアID
        width=100  # 価格変動を通知する幅
    ),
    # 複数のBotを動かすことも可能です
    Config(
        name="CMS (ERC20)",
        url="https://zaif.jp/trade/erc20.cms_jpy",
        token="yyyyyyyyyyyyy",
        channelIds=["11111111111111"],
        currencyPair="erc20.cms_jpy",
        width=50
    )
]
```

##### 3. run.py スクリプトを実行.
```bash
python3 run.py
```
