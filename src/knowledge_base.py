"""
知識ベース（公式集、用語集）
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from .utils import get_project_root, load_json


class KnowledgeBase:
    """知識ベースを管理するクラス"""
    
    def __init__(self):
        self.root = get_project_root()
        self.formulas_dir = self.root / "data" / "formulas"
        self.formulas_dir.mkdir(parents=True, exist_ok=True)
        
        # 初期データを作成
        self._initialize_formulas()
    
    def get_formulas(self, grade: Optional[str] = None) -> Dict:
        """公式を取得"""
        formulas = {}
        
        if grade:
            file_path = self.formulas_dir / f"grade{grade}.json"
            if file_path.exists():
                formulas = load_json(file_path)
        else:
            # 全級の公式を取得
            for file_path in self.formulas_dir.glob("grade*.json"):
                grade_name = file_path.stem.replace("grade", "")
                formulas[grade_name] = load_json(file_path)
        
        return formulas
    
    def search_term(self, keyword: str) -> List[Dict]:
        """用語を検索"""
        # 簡易実装（後で拡張可能）
        terms = self._get_terms()
        results = []
        
        keyword_lower = keyword.lower()
        for term in terms:
            if keyword_lower in term.get("term", "").lower() or \
               keyword_lower in term.get("description", "").lower():
                results.append(term)
        
        return results
    
    def _initialize_formulas(self):
        """公式データを初期化"""
        # 2級の公式
        grade2_formulas = {
            "基本統計量": {
                "平均": "x̄ = (1/n) Σxᵢ",
                "分散（母分散）": "σ² = (1/n) Σ(xᵢ - μ)²",
                "分散（標本分散）": "s² = (1/(n-1)) Σ(xᵢ - x̄)²",
                "標準偏差": "σ = √σ²",
                "中央値": "データを小さい順に並べたときの中央の値"
            },
            "確率": {
                "確率の定義": "P(A) = n(A) / n(S)",
                "条件付き確率": "P(A|B) = P(A∩B) / P(B)",
                "ベイズの定理": "P(A|B) = P(B|A)P(A) / P(B)"
            },
            "検定": {
                "t統計量": "t = (x̄ - μ₀) / (s/√n)",
                "カイ二乗統計量": "χ² = Σ((Oᵢ - Eᵢ)² / Eᵢ)",
                "F統計量": "F = s₁² / s₂²"
            },
            "回帰分析": {
                "回帰直線": "y = ax + b",
                "回帰係数": "a = Σ(xᵢ - x̄)(yᵢ - ȳ) / Σ(xᵢ - x̄)²",
                "決定係数": "R² = 1 - (SS_res / SS_tot)"
            }
        }
        
        # 準1級の公式
        grade_pre1_formulas = {
            **grade2_formulas,
            "重回帰分析": {
                "回帰式": "y = β₀ + β₁x₁ + β₂x₂ + ... + βₖxₖ",
                "調整済み決定係数": "R²_adj = 1 - (1-R²)(n-1)/(n-k-1)"
            },
            "分散分析": {
                "F統計量": "F = MSB / MSW",
                "群間平均平方": "MSB = SSB / (k-1)",
                "群内平均平方": "MSW = SSW / (n-k)"
            },
            "多変量解析": {
                "主成分": "Z = a₁X₁ + a₂X₂ + ... + aₚXₚ"
            }
        }
        
        # 1級の公式
        grade1_formulas = {
            **grade_pre1_formulas,
            "最尤推定": {
                "尤度関数": "L(θ) = Π f(xᵢ|θ)",
                "対数尤度": "l(θ) = log L(θ) = Σ log f(xᵢ|θ)"
            },
            "情報量規準": {
                "AIC": "AIC = -2log L + 2k",
                "BIC": "BIC = -2log L + k log n"
            }
        }
        
        # 保存
        for grade, formulas in [("2", grade2_formulas), ("pre1", grade_pre1_formulas), ("1", grade1_formulas)]:
            file_path = self.formulas_dir / f"grade{grade}.json"
            if not file_path.exists():
                from .utils import save_json
                save_json(formulas, file_path)
    
    def _get_terms(self) -> List[Dict]:
        """用語集を取得"""
        return [
            {
                "term": "平均",
                "description": "データの合計をデータ数で割った値",
                "category": "基本統計量"
            },
            {
                "term": "分散",
                "description": "データの散らばり具合を表す指標",
                "category": "基本統計量"
            },
            {
                "term": "標準偏差",
                "description": "分散の平方根",
                "category": "基本統計量"
            },
            {
                "term": "t検定",
                "description": "平均値の差を検定する方法",
                "category": "検定"
            },
            {
                "term": "カイ二乗検定",
                "description": "独立性や適合度を検定する方法",
                "category": "検定"
            },
            {
                "term": "回帰分析",
                "description": "変数間の関係を分析する方法",
                "category": "回帰分析"
            },
            {
                "term": "決定係数",
                "description": "回帰モデルの当てはまりの良さを表す指標",
                "category": "回帰分析"
            }
        ]
