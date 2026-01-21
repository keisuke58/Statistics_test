"""
準1級の問題を圧倒的に大量生成
"""
import json
import random
import numpy as np
from pathlib import Path

def generate_massive_pre1_problems():
    """準1級の問題を圧倒的に大量生成（各分野100問以上）"""
    
    base_path = Path(__file__).parent / "data" / "problems" / "grade_pre1"
    base_path.mkdir(parents=True, exist_ok=True)
    
    # regression_advanced分野 - 150問
    regression_advanced_problems = []
    for i in range(150):
        n = random.randint(30, 300)
        k = random.randint(2, 8)
        r_squared = random.uniform(0.3, 0.98)
        adj_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - k - 1)
        
        # 多様な問題タイプ
        problem_types = [
            {
                "question": f"重回帰分析において、サンプル数{n}、説明変数数{k}、決定係数R²={r_squared:.3f}のとき、調整済み決定係数は？",
                "options": [
                    f"{adj_r_squared:.4f}",
                    f"{r_squared:.4f}",
                    f"{r_squared*0.9:.4f}",
                    f"{r_squared*1.1:.4f}",
                    f"{(1-r_squared):.4f}"
                ],
                "correct_answer": 0
            },
            {
                "question": f"重回帰分析で、説明変数数{k}、サンプル数{n}の場合、自由度調整済み決定係数の計算に必要な値は？",
                "options": [
                    f"n={n}, k={k}",
                    f"n={n}, k={k+1}",
                    f"n={n-1}, k={k}",
                    f"n={n+1}, k={k}",
                    f"n={n}, k={k-1}"
                ],
                "correct_answer": 0
            }
        ]
        p = random.choice(problem_types)
        regression_advanced_problems.append({
            "problem_id": f"GP1_reg_{i+1:04d}",
            "grade": "pre1",
            "category": "regression_advanced",
            "difficulty": random.choice(["easy", "medium", "hard"]),
            "question_type": "multiple_choice",
            "question": p["question"],
            "options": p["options"],
            "correct_answer": p["correct_answer"],
            "explanation": f"調整済み決定係数 = 1 - (1-R²)(n-1)/(n-k-1)",
            "formulas_used": ["adjusted_r_squared"],
            "tags": ["重回帰分析", "決定係数"]
        })
    
    # anova分野 - 150問
    anova_problems = []
    for i in range(150):
        groups = random.randint(3, 6)
        n_per_group = random.randint(8, 40)
        total_n = groups * n_per_group
        
        problem_types = [
            {
                "question": f"一元配置分散分析において、群数{groups}、各群のサンプル数{n_per_group}のとき、群間の自由度は？",
                "options": [f"{groups-1}", f"{groups}", f"{total_n-1}", f"{total_n-groups}", f"{groups+1}"],
                "correct_answer": 0
            },
            {
                "question": f"一元配置分散分析において、群数{groups}、各群のサンプル数{n_per_group}のとき、群内の自由度は？",
                "options": [f"{total_n-groups}", f"{groups-1}", f"{total_n-1}", f"{groups}", f"{total_n-groups+1}"],
                "correct_answer": 0
            },
            {
                "question": f"一元配置分散分析において、群間平方和120、群内平方和80、群数{groups}、各群のサンプル数{n_per_group}のとき、F統計量は？",
                "options": [
                    f"{(120/(groups-1)) / (80/(total_n-groups)):.2f}",
                    f"{(120/(groups)) / (80/(total_n-groups)):.2f}",
                    f"{(80/(groups-1)) / (120/(total_n-groups)):.2f}",
                    f"{(120/(total_n-groups)) / (80/(groups-1)):.2f}",
                    f"{(120+80)/(total_n):.2f}"
                ],
                "correct_answer": 0
            }
        ]
        p = random.choice(problem_types)
        anova_problems.append({
            "problem_id": f"GP1_anova_{i+1:04d}",
            "grade": "pre1",
            "category": "anova",
            "difficulty": random.choice(["easy", "medium", "hard"]),
            "question_type": "multiple_choice",
            "question": p["question"],
            "options": p["options"],
            "correct_answer": p["correct_answer"],
            "explanation": f"F統計量 = (群間平均平方) / (群内平均平方)",
            "formulas_used": ["anova", "f_statistic"],
            "tags": ["分散分析", "ANOVA"]
        })
    
    # multivariate分野 - 120問
    multivariate_problems = []
    for i in range(120):
        n = random.randint(50, 300)
        p = random.randint(3, 15)
        
        problem_types = [
            {
                "question": f"主成分分析において、サンプル数{n}、変数数{p}のとき、最大主成分数は？",
                "options": [f"{p}", f"{n}", f"{min(n,p)}", f"{n+p}", f"{max(n,p)}"],
                "correct_answer": 2
            },
            {
                "question": f"主成分分析において、累積寄与率が80%を超える主成分数を求める問題。変数数{p}の場合、通常は何個程度か？",
                "options": [
                    f"{min(3, p)}個以下",
                    f"{p//2}個程度",
                    f"{p}個すべて",
                    f"{p+1}個",
                    "1個のみ"
                ],
                "correct_answer": 0
            },
            {
                "question": f"判別分析において、群数3、変数数{p}のとき、判別関数の最大数は？",
                "options": [f"{min(2, p)}", f"{min(3, p)}", f"{p}", f"{3}", f"{p+1}"],
                "correct_answer": 0
            }
        ]
        p_type = random.choice(problem_types)
        multivariate_problems.append({
            "problem_id": f"GP1_multi_{i+1:04d}",
            "grade": "pre1",
            "category": "multivariate",
            "difficulty": random.choice(["medium", "hard"]),
            "question_type": "multiple_choice",
            "question": p_type["question"],
            "options": p_type["options"],
            "correct_answer": p_type["correct_answer"],
            "explanation": "多変量解析の基礎的な概念に関する問題です。",
            "formulas_used": ["pca", "multivariate"],
            "tags": ["多変量解析", "主成分分析"]
        })
    
    # time_series分野 - 120問
    time_series_problems = []
    for i in range(120):
        problem_types = [
            {
                "question": "時系列データの自己相関関数（ACF）がラグ1で0.8、ラグ2で0.6のとき、この時系列の特徴は？",
                "options": [
                    "強い正の自己相関",
                    "弱い正の自己相関",
                    "負の自己相関",
                    "自己相関なし",
                    "周期性あり"
                ],
                "correct_answer": 0
            },
            {
                "question": "AR(1)モデル y_t = 0.7y_{t-1} + ε_t において、定常性の条件は？",
                "options": [
                    "|0.7| < 1 より定常",
                    "|0.7| > 1 より非定常",
                    "0.7 = 1 より単位根",
                    "常に定常",
                    "常に非定常"
                ],
                "correct_answer": 0
            },
            {
                "question": "移動平均MA(1)モデル y_t = ε_t + 0.5ε_{t-1} の分散は？",
                "options": [
                    "σ²(1 + 0.5²) = 1.25σ²",
                    "σ²",
                    "0.5σ²",
                    "1.5σ²",
                    "2σ²"
                ],
                "correct_answer": 0
            }
        ]
        p = random.choice(problem_types)
        time_series_problems.append({
            "problem_id": f"GP1_ts_{i+1:04d}",
            "grade": "pre1",
            "category": "time_series",
            "difficulty": random.choice(["medium", "hard"]),
            "question_type": "multiple_choice",
            "question": p["question"],
            "options": p["options"],
            "correct_answer": p["correct_answer"],
            "explanation": "時系列解析の基礎的な概念に関する問題です。",
            "formulas_used": ["acf", "time_series"],
            "tags": ["時系列解析", "自己相関"]
        })
    
    # bayes分野 - 100問
    bayes_problems = []
    for i in range(100):
        p_a = random.uniform(0.1, 0.9)
        p_b_given_a = random.uniform(0.3, 0.9)
        p_b = random.uniform(0.2, 0.8)
        p_a_given_b = (p_b_given_a * p_a) / p_b
        
        problem_types = [
            {
                "question": f"ベイズの定理において、事前確率P(A)={p_a:.2f}、尤度P(B|A)={p_b_given_a:.2f}、周辺確率P(B)={p_b:.2f}のとき、事後確率P(A|B)は？",
                "options": [
                    f"{p_a_given_b:.4f}",
                    f"{p_a:.4f}",
                    f"{p_b_given_a:.4f}",
                    f"{p_b:.4f}",
                    f"{(p_a + p_b)/2:.4f}"
                ],
                "correct_answer": 0
            },
            {
                "question": "ベイズ統計における事前分布と事後分布の関係について、正しい記述は？",
                "options": [
                    "事後分布は事前分布と尤度の積に比例する",
                    "事後分布は事前分布と独立",
                    "事後分布は尤度のみで決まる",
                    "事前分布は事後分布に影響しない",
                    "事後分布は常に正規分布"
                ],
                "correct_answer": 0
            }
        ]
        p = random.choice(problem_types)
        bayes_problems.append({
            "problem_id": f"GP1_bayes_{i+1:04d}",
            "grade": "pre1",
            "category": "bayes",
            "difficulty": random.choice(["hard"]),
            "question_type": "multiple_choice",
            "question": p["question"],
            "options": p["options"],
            "correct_answer": p["correct_answer"],
            "explanation": f"P(A|B) = P(B|A) × P(A) / P(B) = {p_b_given_a:.2f} × {p_a:.2f} / {p_b:.2f} = {p_a_given_b:.4f}",
            "formulas_used": ["bayes_theorem"],
            "tags": ["ベイズ統計", "事後確率"]
        })
    
    # 既存の問題を読み込んで追加
    existing_reg = []
    if (base_path / "regression_advanced.json").exists():
        with open(base_path / "regression_advanced.json", "r", encoding="utf-8") as f:
            existing_reg = json.load(f)
    
    existing_anova = []
    if (base_path / "anova.json").exists():
        with open(base_path / "anova.json", "r", encoding="utf-8") as f:
            existing_anova = json.load(f)
    
    existing_multi = []
    if (base_path / "multivariate.json").exists():
        with open(base_path / "multivariate.json", "r", encoding="utf-8") as f:
            existing_multi = json.load(f)
    
    existing_ts = []
    if (base_path / "time_series.json").exists():
        with open(base_path / "time_series.json", "r", encoding="utf-8") as f:
            existing_ts = json.load(f)
    
    existing_bayes = []
    if (base_path / "bayes.json").exists():
        with open(base_path / "bayes.json", "r", encoding="utf-8") as f:
            existing_bayes = json.load(f)
    
    # 既存の問題と新規問題を結合
    all_reg = existing_reg + regression_advanced_problems
    all_anova = existing_anova + anova_problems
    all_multi = existing_multi + multivariate_problems
    all_ts = existing_ts + time_series_problems
    all_bayes = existing_bayes + bayes_problems
    
    # ファイルを保存
    with open(base_path / "regression_advanced.json", "w", encoding="utf-8") as f:
        json.dump(all_reg, f, ensure_ascii=False, indent=2)
    
    with open(base_path / "anova.json", "w", encoding="utf-8") as f:
        json.dump(all_anova, f, ensure_ascii=False, indent=2)
    
    with open(base_path / "multivariate.json", "w", encoding="utf-8") as f:
        json.dump(all_multi, f, ensure_ascii=False, indent=2)
    
    with open(base_path / "time_series.json", "w", encoding="utf-8") as f:
        json.dump(all_ts, f, ensure_ascii=False, indent=2)
    
    with open(base_path / "bayes.json", "w", encoding="utf-8") as f:
        json.dump(all_bayes, f, ensure_ascii=False, indent=2)
    
    print(f"準1級の問題を圧倒的に生成しました:")
    print(f"  - regression_advanced: {len(all_reg)}問")
    print(f"  - anova: {len(all_anova)}問")
    print(f"  - multivariate: {len(all_multi)}問")
    print(f"  - time_series: {len(all_ts)}問")
    print(f"  - bayes: {len(all_bayes)}問")
    print(f"  合計: {len(all_reg) + len(all_anova) + len(all_multi) + len(all_ts) + len(all_bayes)}問")

if __name__ == "__main__":
    print("=" * 50)
    print("準1級問題大量生成スクリプト")
    print("=" * 50)
    print()
    generate_massive_pre1_problems()
    print()
    print("=" * 50)
    print("問題生成が完了しました！")
    print("=" * 50)
