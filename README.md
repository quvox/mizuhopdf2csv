pdfからcsvへの変換ツール
====

みずほeビジネスサイトの入出金明細のPDFから数値を抜き出して、収入、支出を仕分けしたcsvを作成するツールです。


## インストール

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Javaランタイムも必要
```bash
brew install openjdk
```


## 利用方法

1. 入出金明細のPDFをe-ビジネスサイトから取ってくる


2. expenditure_item_map.json に振込元と費目の対応関係を書く


3. ツールを実行する
```bash

```


