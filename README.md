# fastapi-open-telemetry-example

## 概要

Open Telemetry を FastAPI に導入するサンプル。

Trace のために、以下を用いてデータ通信を実装している。

- データベース: SQL Alchemy
- API クライアント: HTTPX

## 起動手順

1. (初回のみ) Python 3.11.9 をインストール (バージョン管理に `asdf` を使用)
2. (初回のみ) pipenv をインストール
   - `pip install pipenv`
3. (初回のみ) pipenv 開発環境を作成
   - `pipenv sync`
4. FastAPI を起動
   - `fastapi dev src/main.py`
