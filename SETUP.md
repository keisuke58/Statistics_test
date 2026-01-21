# セットアップガイド

## Conda環境を使用する場合（推奨）

Conda環境を使用することで、パッケージの依存関係やバージョン管理が容易になります。

### 1. Conda環境の作成

```bash
# プロジェクトディレクトリに移動
cd C:\Users\nishi\Life\statics_test

# Conda環境の作成
conda env create -f environment.yml
```

これにより、`statics_test` という名前のConda環境が作成され、必要なパッケージがインストールされます。

### 2. 環境の有効化

```bash
conda activate statics_test
```

### 3. アプリケーションの起動

```bash
streamlit run main.py
```

### 4. 環境の無効化

作業が終わったら、環境を無効化できます：

```bash
conda deactivate
```

### 5. 環境の削除

環境を削除する場合：

```bash
conda env remove -n statics_test
```

## pipを使用する場合

Condaがインストールされていない場合や、pipを使用したい場合：

### 1. 依存パッケージのインストール

```bash
# プロジェクトディレクトリに移動
cd C:\Users\nishi\Life\statics_test

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 2. アプリケーションの起動

```bash
streamlit run main.py
```

## トラブルシューティング

### Condaがインストールされていない場合

1. [Anaconda](https://www.anaconda.com/products/distribution) または [Miniconda](https://docs.conda.io/en/latest/miniconda.html) をインストール
2. インストール後、ターミナルを再起動
3. 上記の手順に従って環境を作成

### 環境の再作成

環境に問題がある場合、再作成できます：

```bash
# 既存の環境を削除
conda env remove -n statics_test

# 環境を再作成
conda env create -f environment.yml
```

### パッケージの更新

環境内のパッケージを更新する場合：

```bash
conda activate statics_test
pip install --upgrade -r requirements.txt
```

### NumPy/SciPyの互換性エラー（pip使用時）

pipを使用していて互換性エラーが発生する場合：

```bash
pip uninstall numpy scipy
pip install numpy==1.26.4 scipy==1.11.4
```

## 推奨事項

- **Conda環境の使用を推奨**: パッケージの依存関係管理が容易で、互換性問題を回避できます
- **Python 3.10**: 環境はPython 3.10で設定されています。他のバージョンが必要な場合は `environment.yml` を編集してください
