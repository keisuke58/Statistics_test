# クイックスタートガイド

## セットアップ（初回のみ）

### Conda環境を使用する場合（推奨）

```bash
# プロジェクトディレクトリに移動
cd C:\Users\nishi\Life\statics_test

# Conda環境の作成
conda env create -f environment.yml

# 環境の有効化
conda activate statics_test
```

### pipを使用する場合

```bash
# プロジェクトディレクトリに移動
cd C:\Users\nishi\Life\statics_test

# 依存パッケージのインストール
pip install -r requirements.txt
```

## 起動

```bash
# Conda環境を有効化（conda環境を使用する場合）
conda activate statics_test

# アプリケーションの起動
streamlit run main.py
```

ブラウザが自動的に開き、`http://localhost:8501` にアクセスされます。

## 主な機能

### 📝 問題練習
- 級・分野・難易度を選択して問題を練習
- 即座に正誤判定と解説を表示

### 📋 模擬試験
- 本番形式の模擬試験（タイマー付き）
- 自動採点と結果保存

### 📈 進捗確認
- 学習履歴の確認
- 正答率の推移グラフ

### 🔢 統計計算
- 基本統計量、検定統計量の計算
- 回帰分析ツール

### 📚 知識ベース
- 公式集（各級別）
- 用語集と検索機能

## サンプル問題

システムには以下のサンプル問題が含まれています：

- **2級**: データ記述、確率の問題（5問）
- **準1級**: 重回帰分析、分散分析の問題（3問）
- **1級**: 統計数理の問題（1問）

## 問題データの追加

問題データは `data/problems/` ディレクトリ内のJSONファイルに追加できます。
詳細は `USAGE.md` を参照してください。

## トラブルシューティング

### Condaがインストールされていない場合

[Anaconda](https://www.anaconda.com/products/distribution) または [Miniconda](https://docs.conda.io/en/latest/miniconda.html) をインストールしてください。

### 環境の再作成

環境に問題がある場合：

```bash
conda env remove -n statics_test
conda env create -f environment.yml
```

### NumPy/SciPyの互換性エラー（pip使用時のみ）

Conda環境を使用することで、この問題を回避できます。
pipを使用している場合のみ、以下のコマンドで再インストールしてください：

```bash
pip uninstall numpy scipy
pip install numpy==1.26.4 scipy==1.11.4
```

### その他のエラー

- Python 3.8以上を使用しているか確認
- Conda環境が有効化されているか確認（`conda activate statics_test`）
- すべての依存パッケージがインストールされているか確認
- 詳細は `SETUP.md` を参照してください
