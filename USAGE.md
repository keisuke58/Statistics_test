# 使用方法ガイド

## 起動方法

### Conda環境を使用する場合（推奨）

```bash
# Conda環境の作成（初回のみ）
conda env create -f environment.yml

# 環境の有効化
conda activate statics_test

# アプリケーションの起動
streamlit run main.py
```

### pipを使用する場合

```bash
# 依存パッケージのインストール
pip install -r requirements.txt

# アプリケーションの起動
streamlit run main.py
```

ブラウザで `http://localhost:8501` にアクセスしてください。

## 機能の使い方

### 1. 問題練習

1. サイドバーから「問題練習」を選択
2. 級（2級/準1級/1級）を選択
3. 分野を選択（全分野または特定分野）
4. 問題数を設定（1-50問）
5. 難易度を選択（全て/easy/medium/hard）
6. 「練習開始」ボタンをクリック
7. 問題に解答し、「正誤を確認」で答え合わせ
8. 「結果を保存」で学習履歴に記録

### 2. 模擬試験

1. サイドバーから「模擬試験」を選択
2. 級を選択
3. 「模擬試験を開始」ボタンをクリック
4. 問題に解答（前の問題/次の問題で移動可能）
5. 「試験を終了して採点」で結果を確認
6. 結果は自動的に保存されます

### 3. 進捗確認

1. サイドバーから「進捗確認」を選択
2. 級を選択（全て/2級/準1級/1級）
3. 統計情報とセッション履歴を確認
4. 正答率の推移グラフを確認

### 4. 統計計算

1. サイドバーから「統計計算」を選択
2. 計算タイプを選択
3. データをカンマ区切りで入力
4. 結果を確認

### 5. 知識ベース

1. サイドバーから「知識ベース」を選択
2. 「公式集」タブで級を選択して公式を確認
3. 「用語集」タブでキーワードを検索

## 問題データの追加

問題データは `data/problems/` ディレクトリ内のJSONファイルに保存されています。

### 問題データの形式

#### 多肢選択問題（2級、準1級）

```json
{
  "problem_id": "G2_001",
  "grade": "2",
  "category": "data_description",
  "difficulty": "easy",
  "question_type": "multiple_choice",
  "question": "問題文",
  "options": ["選択肢1", "選択肢2", "選択肢3", "選択肢4"],
  "correct_answer": 1,
  "explanation": "解説",
  "formulas_used": ["mean"],
  "tags": ["平均", "基本統計量"]
}
```

#### 数値入力問題（準1級）

```json
{
  "problem_id": "GP1_002",
  "grade": "pre1",
  "category": "regression_advanced",
  "difficulty": "hard",
  "question_type": "numeric_input",
  "question": "問題文",
  "correct_answer": 22.5,
  "tolerance": 0.1,
  "explanation": "解説",
  "formulas_used": ["linear_regression"],
  "tags": ["単回帰", "予測"]
}
```

#### 論述式問題（1級）

```json
{
  "problem_id": "G1_001",
  "grade": "1",
  "category": "statistics_math",
  "difficulty": "hard",
  "question_type": "essay",
  "question": "問題文",
  "correct_answer": "",
  "explanation": "解説",
  "formulas_used": ["maximum_likelihood"],
  "tags": ["最尤推定", "統計数理"]
}
```

## トラブルシューティング

### 問題が表示されない

- `data/problems/` ディレクトリに問題データが存在するか確認
- JSONファイルの形式が正しいか確認

### エラーが発生する

- 依存パッケージが正しくインストールされているか確認
- Pythonのバージョンが3.8以上であることを確認

### 結果が保存されない

- `data/history/` ディレクトリの書き込み権限を確認
