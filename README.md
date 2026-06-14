# Astrology Cusp Calculator (HANA) - 第1段階

このプロジェクトは、ユーザーが入力した生年月日、出生時間、および出生場所から、ハウスのカスプ（境界線）とアセンダント（ASC）、ミディアム・コエリ（MC）を高精度に計算して表示するWebアプリケーションです。

## ディレクトリ構成

```text
astrology_app/
├── venv/                 # Python仮想環境 (セットアップ済み)
├── geocoder.py          # 住所から緯度経度・タイムゾーンを取得するモジュール
├── horoscope.py         # Swiss Ephemerisを使用したハウス計算モジュール
├── main.py              # FastAPIサーバー（メインプログラム）
├── test_app.py          # 自動テストコード
└── templates/
    └── index.html       # フロントエンド画面 (HTML/CSS/JS)
```

## 起動方法

### 1. サーバーの起動
すでにバックグラウンドで起動していますが、手動で起動する場合は以下のコマンドを実行してください。
```bash
# astrology_app ディレクトリへ移動
cd /Users/chizukoasahi/.gemini/antigravity/scratch/astrology_app

# サーバーの起動
./venv/bin/python main.py
```

### 2. ブラウザでアクセス
以下のURLをブラウザ（SafariやChromeなど）で開きます。
* [http://localhost:8000](http://localhost:8000)

## テストの実行方法
バックエンドの動作検証用テストを実行するには、以下のコマンドを使用します。
```bash
./venv/bin/python test_app.py
```

## 技術スタック
- **Backend**: Python 3.9.6, FastAPI, Uvicorn
- **Calculation**: pyswisseph (Swiss Ephemeris Python wrapper)
- **Geocoding & Timezone**: Nominatim API (OpenStreetMap), timezonefinder, pytz
- **Frontend**: HTML5, Vanilla CSS (Glassmorphism), JavaScript (Fetch API)
