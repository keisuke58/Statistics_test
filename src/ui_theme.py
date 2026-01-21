"""
UI/UXテーマ管理
ダークモード、カスタムテーマ、スタイル設定
"""
import streamlit as st
from typing import Dict, Optional


class UITheme:
    """UIテーマを管理するクラス"""
    
    THEMES = {
        "light": {
            "name": "ライトモード",
            "background": "#ffffff",
            "text": "#262730",
            "primary": "#ff4b4b",
            "secondary": "#f0f2f6",
            "success": "#21c354",
            "warning": "#ffc107",
            "error": "#ff4b4b"
        },
        "dark": {
            "name": "ダークモード",
            "background": "#0e1117",
            "text": "#fafafa",
            "primary": "#ff4b4b",
            "secondary": "#262730",
            "success": "#21c354",
            "warning": "#ffc107",
            "error": "#ff4b4b"
        },
        "blue": {
            "name": "ブルーテーマ",
            "background": "#f0f8ff",
            "text": "#1e3a8a",
            "primary": "#3b82f6",
            "secondary": "#dbeafe",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444"
        },
        "green": {
            "name": "グリーンテーマ",
            "background": "#f0fdf4",
            "text": "#14532d",
            "primary": "#22c55e",
            "secondary": "#dcfce7",
            "success": "#16a34a",
            "warning": "#eab308",
            "error": "#dc2626"
        }
    }
    
    @staticmethod
    def apply_theme(theme_name: str = "light"):
        """テーマを適用"""
        theme = UITheme.THEMES.get(theme_name, UITheme.THEMES["light"])
        
        css = f"""
        <style>
        /* メイン背景 */
        .stApp {{
            background-color: {theme['background']};
        }}
        
        /* テキスト色 */
        .stMarkdown, .stText, h1, h2, h3, h4, h5, h6, p {{
            color: {theme['text']};
        }}
        
        /* サイドバー */
        .css-1d391kg {{
            background-color: {theme['secondary']};
        }}
        
        /* ボタン */
        .stButton > button {{
            background-color: {theme['primary']};
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            background-color: {theme['primary']};
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        /* メトリック */
        .metric-card {{
            background-color: {theme['secondary']};
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: scale(1.05);
        }}
        
        /* カード */
        .card {{
            background-color: {theme['secondary']};
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .card:hover {{
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transform: translateY(-2px);
        }}
        
        /* アニメーション */
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.5s ease-in;
        }}
        
        /* スムーズスクロール */
        html {{
            scroll-behavior: smooth;
        }}
        
        /* 選択ボックス */
        .stSelectbox > div > div {{
            background-color: {theme['background']};
            border-radius: 8px;
        }}
        
        /* 入力フィールド */
        .stTextInput > div > div > input {{
            background-color: {theme['background']};
            border-radius: 8px;
        }}
        
        /* 成功メッセージ */
        .stSuccess {{
            background-color: {theme['success']};
            color: white;
            padding: 1rem;
            border-radius: 8px;
        }}
        
        /* エラーメッセージ */
        .stError {{
            background-color: {theme['error']};
            color: white;
            padding: 1rem;
            border-radius: 8px;
        }}
        
        /* レスポンシブデザイン */
        @media (max-width: 768px) {{
            .stApp {{
                padding: 0.5rem;
            }}
            
            .card {{
                padding: 1rem;
            }}
        }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)
    
    @staticmethod
    def get_theme_selector():
        """テーマ選択UI"""
        theme_options = {name: key for key, name in 
                        [(k, v["name"]) for k, v in UITheme.THEMES.items()]}
        
        if "current_theme" not in st.session_state:
            st.session_state.current_theme = "light"
        
        selected_theme = st.sidebar.selectbox(
            "🎨 テーマ",
            options=list(theme_options.keys()),
            index=list(theme_options.keys()).index(
                UITheme.THEMES[st.session_state.current_theme]["name"]
            ),
            key="theme_selector"
        )
        
        # テーマ名からキーを取得
        theme_key = [k for k, v in UITheme.THEMES.items() 
                    if v["name"] == selected_theme][0]
        
        if theme_key != st.session_state.current_theme:
            st.session_state.current_theme = theme_key
            UITheme.apply_theme(theme_key)
            st.rerun()
        
        return theme_key
    
    @staticmethod
    def create_animated_card(content: str, delay: float = 0.0):
        """アニメーション付きカードを作成"""
        return f"""
        <div class="card fade-in" style="animation-delay: {delay}s;">
            {content}
        </div>
        """
    
    @staticmethod
    def create_metric_card(title: str, value: str, icon: str = "📊"):
        """メトリックカードを作成"""
        return f"""
        <div class="metric-card fade-in">
            <h3>{icon} {title}</h3>
            <h2>{value}</h2>
        </div>
        """
