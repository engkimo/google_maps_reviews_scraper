# Google Maps Reviews Scraper

このプロジェクトは、Google Maps からレビューをスクレイピングするためのツールです。SerpAPI を使用して Google Maps のレビューデータを取得します。

## 事前準備 Prerequisites

SerpAPI の API キーが必要です。SerpAPI の公式サイト で取得してください。
poetry がインストールされていることを確認してください。
This project provides a tool for scraping reviews from Google Maps. It uses SerpAPI to retrieve review data from Google Maps.

## インストール Installation

```
poetry install
```

## 使用方法 Usage

URL ファイルからのレビューの取得 Fetching reviews from a file of URLs:

```
poetry run python [ファイル名] --file [URL リストを含むファイルのパス] --api_key [SerpAPI の API キー]
```

クエリからのレビューの取得 Fetching reviews using a query::

```
poetry run python [ファイル名] --query [検索クエリ] --latitude [緯度] --longitude [経度] --api_key [SerpAPI の API キー]
```

## オプション Options

`--cnt` : 取得するページネーションの最大数 (デフォルトはすべて)

## 注意事項 Caution

使用する前に、Google Maps のデータ利用ポリシーを確認してください。
大量のリクエストは、IP のブロックや API キーの制限を引き起こす可能性がありますので、注意してください。

Before usage, please check Google Maps' data usage policies.
Excessive requests may lead to IP blocks or restrictions on your API key, so use with caution.