# 統計検定学習支援システム

統計検定1級・準1級・2級の合格を支援するための包括的な学習システムです。

## 機能

- **問題練習**: 各級の問題を練習できます
- **模擬試験**: 本番形式の模擬試験を受験できます
- **進捗確認**: 学習の進捗を可視化できます
- **統計計算**: 統計計算ツールを使用できます
- **知識ベース**: 公式集や用語集を参照できます

## インストール

### Conda環境を使用する場合（推奨）

```bash
# Conda環境の作成
conda env create -f environment.yml

# 環境の有効化
conda activate statics_test

# アプリケーションの起動
streamlit run main.py
```

### pipを使用する場合

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
# Conda環境を有効化（conda環境を使用する場合）
conda activate statics_test

# アプリケーションの起動
streamlit run main.py
```

ブラウザで `http://localhost:8501` にアクセスしてください。

## プロジェクト構造

```
statics_test/
├── main.py                 # メインアプリケーション
├── requirements.txt        # 依存パッケージ（pip用）
├── environment.yml         # Conda環境設定ファイル
├── config/                 # 設定ファイル
├── data/                   # データファイル
│   ├── problems/          # 問題データ
│   ├── history/           # 学習履歴
│   └── formulas/          # 公式データ
└── src/                    # ソースコード
    ├── problem_manager.py # 問題管理
    ├── exam_simulator.py  # 模擬試験
    ├── progress_tracker.py # 進捗管理
    ├── calculator.py      # 統計計算ツール
    └── knowledge_base.py  # 知識ベース
```

詳細なセットアップ手順は `SETUP.md` を参照してください。

## 統計検定について

- **2級**: 大学教養課程レベル、35問、90分、合格ライン70点
- **準1級**: 2級を含む応用レベル、25-30問、90分、合格ライン60点
- **1級**: 大学専門課程・大学院レベル、論述式、各90分
