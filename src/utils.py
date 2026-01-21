"""
ユーティリティ関数
"""
import json
import os
from datetime import datetime
from pathlib import Path


def get_project_root():
    """プロジェクトのルートディレクトリを取得"""
    return Path(__file__).parent.parent


def load_json(file_path):
    """JSONファイルを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Noneの場合は空リストを返す（問題データ用）
            if data is None:
                return []
            # そのまま返す（設定ファイルなどは辞書のまま）
            return data
    except FileNotFoundError:
        # 問題データの場合は空リスト、それ以外はNone
        return []
    except json.JSONDecodeError as e:
        import streamlit as st
        try:
            st.error(f"⚠️ JSON解析エラー ({file_path}): {str(e)}")
        except:
            print(f"JSON解析エラー ({file_path}): {str(e)}")
        return []
    except Exception as e:
        import streamlit as st
        try:
            st.error(f"⚠️ ファイル読み込みエラー ({file_path}): {str(e)}")
        except:
            print(f"ファイル読み込みエラー ({file_path}): {str(e)}")
        return []


def save_json(data, file_path):
    """JSONファイルに保存"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_timestamp():
    """現在のタイムスタンプを取得"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def format_time(seconds):
    """秒数を時:分:秒形式に変換"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"
