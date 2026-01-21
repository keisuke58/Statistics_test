"""
問題生成・多様化機能
計算問題の自動生成、パラメータ変更、実データ問題など
"""
import json
import random
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
from .utils import get_project_root


class ProblemGenerator:
    """問題の自動生成と多様化を行うクラス"""
    
    def __init__(self):
        self.root = get_project_root()
    
    def generate_calculation_problem(self, problem_template: Dict, 
                                     param_variations: Optional[Dict] = None) -> Dict:
        """計算問題をパラメータ変更して生成"""
        new_problem = problem_template.copy()
        
        if param_variations:
            # パラメータを変更
            for key, value_range in param_variations.items():
                if isinstance(value_range, tuple):
                    new_value = random.uniform(value_range[0], value_range[1])
                elif isinstance(value_range, list):
                    new_value = random.choice(value_range)
                else:
                    new_value = value_range
                
                # 問題文と選択肢を更新
                if key in new_problem.get("question", ""):
                    new_problem["question"] = new_problem["question"].replace(
                        str(problem_template.get(key, "")), str(new_value)
                    )
        
        return new_problem
    
    def generate_variation_problems(self, base_problem: Dict, num_variations: int = 5) -> List[Dict]:
        """基本問題からバリエーション問題を生成"""
        variations = []
        
        for i in range(num_variations):
            variation = base_problem.copy()
            variation["problem_id"] = f"{base_problem.get('problem_id', 'PROB')}_var_{i+1:03d}"
            
            # 数値をランダムに変更
            if "data_values" in variation:
                # データ値を変更
                variation["data_values"] = [
                    random.randint(10, 100) for _ in range(len(variation["data_values"]))
                ]
                # 再計算
                mean = sum(variation["data_values"]) / len(variation["data_values"])
                variation["correct_answer"] = mean
            
            variations.append(variation)
        
        return variations
    
    def create_chart_problem(self, grade: str, category: str, 
                            chart_type: str = "histogram") -> Dict:
        """図表を使った問題を生成"""
        problem = {
            "problem_id": f"{grade}_{category}_chart_{random.randint(1000, 9999)}",
            "grade": grade,
            "category": category,
            "difficulty": random.choice(["medium", "hard"]),
            "question_type": "multiple_choice",
            "has_chart": True,
            "chart_type": chart_type,
            "question": f"以下の{chart_type}を見て、次の問いに答えよ。",
            "options": ["選択肢1", "選択肢2", "選択肢3", "選択肢4"],
            "correct_answer": 0,
            "explanation": "図表から読み取れる情報を基に解答する。",
            "tags": ["図表", "データ可視化"]
        }
        
        return problem
    
    def create_real_data_problem(self, grade: str, category: str) -> Dict:
        """実データを使った問題を生成"""
        # 実データの例（実際のデータセットから生成）
        if category == "data_description":
            data = [random.gauss(50, 15) for _ in range(100)]
            mean = np.mean(data)
            std = np.std(data)
            
            problem = {
                "problem_id": f"{grade}_{category}_real_{random.randint(1000, 9999)}",
                "grade": grade,
                "category": category,
                "difficulty": "medium",
                "question_type": "multiple_choice",
                "has_real_data": True,
                "data": data[:20],  # 最初の20個を表示
                "question": f"以下の実データの平均値に最も近い値は？\n{data[:10]}",
                "options": [
                    f"{mean:.1f}",
                    f"{mean+5:.1f}",
                    f"{mean-5:.1f}",
                    f"{mean*1.1:.1f}"
                ],
                "correct_answer": 0,
                "explanation": f"実データの平均値は{mean:.2f}です。",
                "tags": ["実データ", "基本統計量"]
            }
        else:
            problem = self._create_default_real_data_problem(grade, category)
        
        return problem
    
    def _create_default_real_data_problem(self, grade: str, category: str) -> Dict:
        """デフォルトの実データ問題"""
        return {
            "problem_id": f"{grade}_{category}_real_{random.randint(1000, 9999)}",
            "grade": grade,
            "category": category,
            "difficulty": "medium",
            "question_type": "multiple_choice",
            "has_real_data": True,
            "question": "実データを用いた問題です。",
            "options": ["選択肢1", "選択肢2", "選択肢3", "選択肢4"],
            "correct_answer": 0,
            "explanation": "実データに基づく解答です。",
            "tags": ["実データ"]
        }
    
    def adjust_difficulty(self, problem: Dict, target_difficulty: str) -> Dict:
        """問題の難易度を調整"""
        adjusted = problem.copy()
        adjusted["difficulty"] = target_difficulty
        
        # 難易度に応じて問題文や選択肢を調整
        if target_difficulty == "easy":
            # 簡単にする: より明確な問題文、シンプルな計算
            pass
        elif target_difficulty == "hard":
            # 難しくする: 複合的な問題、複雑な計算
            if "question" in adjusted:
                adjusted["question"] += "\n（複数の概念を組み合わせて考えよ）"
        
        return adjusted
    
    def create_past_exam_style_problem(self, grade: str, category: str) -> Dict:
        """過去問スタイルの問題を生成"""
        # 過去問の特徴を模倣
        problem = {
            "problem_id": f"{grade}_{category}_past_{random.randint(1000, 9999)}",
            "grade": grade,
            "category": category,
            "difficulty": random.choice(["medium", "hard"]),
            "question_type": "multiple_choice",
            "is_past_exam_style": True,
            "question": self._generate_past_exam_question(grade, category),
            "options": self._generate_past_exam_options(grade, category),
            "correct_answer": random.randint(0, 3),
            "explanation": "過去問スタイルの問題です。本番試験に近い形式で出題されます。",
            "tags": ["過去問スタイル", category]
        }
        
        return problem
    
    def _generate_past_exam_question(self, grade: str, category: str) -> str:
        """過去問スタイルの質問文を生成"""
        templates = {
            "data_description": [
                "次のデータについて、適切な記述を選べ。",
                "以下の統計量のうち、正しいものを選べ。",
                "データの分布に関する記述として正しいものを選べ。"
            ],
            "probability": [
                "確率に関する次の記述のうち、正しいものを選べ。",
                "以下の確率計算において、正しい値を選べ。",
                "確率分布に関する記述として適切なものを選べ。"
            ],
            "inference": [
                "統計的推測に関する次の記述のうち、正しいものを選べ。",
                "信頼区間の計算において、正しい値を選べ。",
                "検定に関する記述として適切なものを選べ。"
            ]
        }
        
        category_templates = templates.get(category, ["次の問いに答えよ。"])
        return random.choice(category_templates)
    
    def _generate_past_exam_options(self, grade: str, category: str) -> List[str]:
        """過去問スタイルの選択肢を生成"""
        if grade == "2":
            return ["選択肢1", "選択肢2", "選択肢3", "選択肢4"]
        elif grade == "pre1":
            return ["選択肢1", "選択肢2", "選択肢3", "選択肢4", "選択肢5"]
        else:
            return ["選択肢1", "選択肢2", "選択肢3", "選択肢4"]


def generate_diverse_problems(num_problems: int = 50):
    """多様な問題を一括生成"""
    generator = ProblemGenerator()
    problems = []
    
    grades = ["2", "pre1", "1"]
    categories_2 = ["data_description", "probability", "inference", "regression"]
    categories_pre1 = ["regression_advanced", "anova", "multivariate", "time_series", "bayes"]
    categories_1 = ["statistics_math", "statistics_applied"]
    
    for _ in range(num_problems):
        grade = random.choice(grades)
        
        if grade == "2":
            category = random.choice(categories_2)
        elif grade == "pre1":
            category = random.choice(categories_pre1)
        else:
            category = random.choice(categories_1)
        
        # ランダムに問題タイプを選択
        problem_type = random.choice([
            "past_exam",
            "real_data",
            "chart",
            "calculation"
        ])
        
        if problem_type == "past_exam":
            problem = generator.create_past_exam_style_problem(grade, category)
        elif problem_type == "real_data":
            problem = generator.create_real_data_problem(grade, category)
        elif problem_type == "chart":
            problem = generator.create_chart_problem(grade, category)
        else:
            # 計算問題のテンプレート
            template = {
                "grade": grade,
                "category": category,
                "difficulty": random.choice(["easy", "medium", "hard"]),
                "question_type": "multiple_choice",
                "question": "計算問題です。",
                "options": ["選択肢1", "選択肢2", "選択肢3", "選択肢4"],
                "correct_answer": 0,
                "explanation": "計算過程を示す。"
            }
            problem = generator.generate_calculation_problem(template)
        
        problems.append(problem)
    
    return problems
