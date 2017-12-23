# Zaifcord
[Zaif](https://zaif.jp)で取り扱っている仮想通貨の価格変化を通知するDiscord Botです.  
対日本円レートの通貨ペアにのみ対応しています. (MONA/JPY, BTC/JPYなど)  

Zaifはテックビューロ株式会社の登録商標です.

## 動作環境
Python 3.6 以降

## 機能
- 5円刻みで現在の価格をプレイ中として表示します.  
    ![](https://raw.githubusercontent.com/SlashNephy/Zaifcord/master/img/playing.png)
    
    5円刻みとしているのは Discord APIに負荷を掛けすぎないためです.

- 大きな価格変動があった際に メッセージを送信します.  
    ![](https://raw.githubusercontent.com/SlashNephy/Zaifcord/master/img/price_change.png)

- 見やすいログをコンソールに出力します.  
    ![](https://raw.githubusercontent.com/SlashNephy/Zaifcord/master/img/console.png)
    
    Pythonライブラリ "colorama" を利用しているので Windowsでも色付きのログが出力されます.

## 導入方法
1. pipで必要なライブラリをインストール.  
    ```bash
    pip3 install discord.py requests websocket-client colorama
    ```

2. `run.py` 内にBotの情報を記述.  
    ```python
    bots = [
        Config(
            name="MONA",  # Bot名 (ニックネーム)
            url="https://zaif.jp/trade_mona_jpy",  # 取引ページ
            token="xxxxxxxxxxxxx",  # Botのトークン
            channelIds=["0000000000000"],  # 価格変動を通知するテキストチャンネルID
            currencyPair="mona_jpy",  # 通貨ペア
            width=100  # 価格変動を通知する幅
                       # 例えば50円間隔で価格変動を監視したいときは width=50 とします.
        ),
        # 複数のBotを動かすことも可能です
        Config(
            name="CMS (ERC20)",
            url="https://zaif.jp/trade/erc20.cms_jpy",
            token="yyyyyyyyyyyyy",
            channelIds=["11111111111111"],
            currencyPair="erc20.cms_jpy",
            width=50,
            debug=True  # デバッグモードを有効にします, 価格更新時にログに出力されます
        )
    ]
    ```

3. `run.py` スクリプトを実行.  
    ```bash
    python3 run.py
    ```

## Q&A
- DiscordのBotのトークンの取得方法を知りたい  
    Discordの[My Apps](https://discordapp.com/developers/applications/me)でユーザごとに10個まで作成できます.

- 通貨ペアがわからない  
    Zaifの[API](http://techbureau-api-document.readthedocs.io/ja/latest/public/2_individual/2_currency_pairs.html)で取得できます.  
