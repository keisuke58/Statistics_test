"""
全級の問題を圧倒的に大量生成
"""
import json
import random
import numpy as np
from pathlib import Path

def generate_massive_grade2_problems():
    """2級の問題を圧倒的に大量生成"""
    base_path = Path(__file__).parent / "data" / "problems" / "grade2"
    base_path.mkdir(parents=True, exist_ok=True)
    
    # data_description分野 - 200問
    data_description_problems = []
    for i in range(200):
        data_values = [random.randint(10, 100) for _ in range(random.randint(5, 20))]
        mean = sum(data_values) / len(data_values)
        sorted_data = sorted(data_values)
        median = sorted_data[len(sorted_data)//2] if len(sorted_data) % 2 == 1 else (sorted_data[len(sorted_data)//2-1] + sorted_data[len(sorted_data)//2]) / 2
        variance = sum((x - mean)**2 for x in data_values) / len(data_values)
        std = variance ** 0.5
        
        problem_types = [
            {
                "question": f"次のデータの平均値は？\n{data_values}",
                "options": [f"{mean:.1f}", f"{mean+5:.1f}", f"{mean-5:.1f}", f"{mean*1.1:.1f}"],
                "correct_answer": 0,
                "explanation": f"平均値 = {sum(data_values)} / {len(data_values)} = {mean:.2f}"
            },
            {
                "question": f"次のデータの中央値は？\n{sorted(data_values)}",
                "options": [f"{median:.1f}", f"{median+2:.1f}", f"{median-2:.1f}", f"{mean:.1f}"],
                "correct_answer": 0,
                "explanation": f"データを小さい順に並べると {sorted(data_values)}。中央値は{median:.2f}。"
            },
            {
                "question": f"次のデータの分散は？（母分散）\n{data_values}",
                "options": [f"{variance:.1f}", f"{variance*2:.1f}", f"{std:.1f}", f"{std**2*2:.1f}"],
                "correct_answer": 0,
                "explanation": f"平均 = {mean:.2f}\n分散 = {variance:.2f}"
            },
            {
                "question": f"次のデータの標準偏差は？\n{data_values}",
                "options": [f"{std:.2f}", f"{std*2:.2f}", f"{variance:.2f}", f"{mean:.2f}"],
                "correct_answer": 0,
                "explanation": f"標準偏差 = √分散 = {std:.2f}"
            }
        ]
        
        p = random.choice(problem_types)
        data_description_problems.append({
            "problem_id": f"G2_data_{i+1:04d}",
            "grade": "2",
            "category": "data_description",
            "difficulty": random.choice(["easy", "medium", "hard"]),
            "question_type": "multiple_choice",
            "question": p["question"],
            "options": p["options"],
            "correct_answer": p["correct_answer"],
            "explanation": p["explanation"],
            "formulas_used": ["mean", "median", "variance", "std"],
            "tags": ["基本統計量", "データの記述"]
        })
    
    # probability分野 - 200問
    probability_problems = []
    for i in range(200):
        problem_types = [
            {
                "question": f"サイコロを1回振ったとき、{random.choice([3, 4, 5, 6])}以上の目が出る確率は？",
                "options": ["1/2", "1/3", "2/3", "1/6"],
                "correct_answer": 0,
                "explanation": "3以上の目は3, 4, 5, 6の4通り。確率 = 4/6 = 2/3"
            },
            {
                "question": f"コインを{random.randint(2, 5)}回投げたとき、表がちょうど2回出る確率は？",
                "options": ["3/8", "1/2", "1/4", "5/8"],
                "correct_answer": 0,
                "explanation": "二項分布の計算"
            },
            {
                "question": "52枚のトランプから1枚引いたとき、ハートのカードが出る確率は？",
                "options": ["1/4", "1/13", "1/52", "13/52"],
                "correct_answer": 0,
                "explanation": "ハートは13枚。確率 = 13/52 = 1/4"
            },
            {
                "question": "2つのサイコロを振ったとき、目の和が7になる確率は？",
                "options": ["1/6", "1/12", "1/36", "7/36"],
                "correct_answer": 0,
                "explanation": "和が7になる組み合わせは(1,6), (2,5), (3,4), (4,3), (5,2), (6,1)の6通り。確率 = 6/36 = 1/6"
            }
        ]
        p = random.choice(problem_types)
        probability_problems.append({
            "problem_id": f"G2_prob_{i+1:04d}",
            "grade": "2",
            "category": "probability",
            "difficulty": random.choice(["easy", "medium", "hard"]),
            "question_type": "multiple_choice",
            "question": p["question"],
            "options": p["options"],
            "correct_answer": p["correct_answer"],
            "explanation": p["explanation"],
            "formulas_used": ["probability", "binomial"],
            "tags": ["確率", "基礎"]
        })
    
    # inference分野 - 150問
    inference_problems = []
    for i in range(150):
        n = random.randint(20, 200)
        mean = random.uniform(50, 100)
        std = random.uniform(5, 25)
        se = std / (n ** 0.5)
        
        problem_types = [
            {
                "question": f"標本サイズ{n}、標本平均{mean:.1f}、標準偏差{std:.1f}のとき、標準誤差は？",
                "options": [f"{se:.3f}", f"{std:.3f}", f"{mean:.3f}", f"{n:.3f}"],
                "correct_answer": 0,
                "explanation": f"標準誤差 = 標準偏差 / √n = {std:.1f} / √{n} = {se:.3f}"
            },
            {
                "question": f"標本サイズ{n}、標本平均{mean:.1f}、標準偏差{std:.1f}のとき、95%信頼区間の幅は？（z=1.96）",
                "options": [f"{se*1.96*2:.2f}", f"{se*1.96:.2f}", f"{std*1.96:.2f}", f"{mean*0.05:.2f}"],
                "correct_answer": 0,
                "explanation": f"信頼区間の幅 = 2 × z × 標準誤差 = 2 × 1.96 × {se:.3f} = {se*1.96*2:.2f}"
            }
        ]
        p = random.choice(problem_types)
        inference_problems.append({
            "problem_id": f"G2_inf_{i+1:04d}",
            "grade": "2",
            "category": "inference",
            "difficulty": random.choice(["medium", "hard"]),
            "question_type": "multiple_choice",
            "question": p["question"],
            "options": p["options"],
            "correct_answer": p["correct_answer"],
            "explanation": p["explanation"],
            "formulas_used": ["standard_error", "confidence_interval"],
            "tags": ["推測統計", "信頼区間"]
        })
    
    # regression分野 - 150問
    regression_problems = []
    for i in range(150):
        x_values = [random.randint(1, 20) for _ in range(10)]
        slope = random.uniform(0.5, 3.0)
        intercept = random.uniform(-10, 10)
        y_pred = slope * 10 + intercept
        
        problem_types = [
            {
                "question": f"単回帰分析で、回帰係数（傾き）が{slope:.2f}、切片が{intercept:.2f}のとき、x=10の予測値yは？",
                "options": [f"{y_pred:.2f}", f"{slope*10:.2f}", f"{intercept:.2f}", f"{slope+intercept:.2f}"],
                "correct_answer": 0,
                "explanation": f"y = {slope:.2f} × 10 + {intercept:.2f} = {y_pred:.2f}"
            }
        ]
        p = random.choice(problem_types)
        regression_problems.append({
            "problem_id": f"G2_reg_{i+1:04d}",
            "grade": "2",
            "category": "regression",
            "difficulty": random.choice(["medium", "hard"]),
            "question_type": "multiple_choice",
            "question": p["question"],
            "options": p["options"],
            "correct_answer": p["correct_answer"],
            "explanation": p["explanation"],
            "formulas_used": ["linear_regression"],
            "tags": ["回帰分析", "単回帰"]
        })
    
    # 既存の問題を読み込んで追加
    existing_data_desc = []
    if (base_path / "data_description.json").exists():
        with open(base_path / "data_description.json", "r", encoding="utf-8") as f:
            existing_data_desc = json.load(f)
    
    existing_prob = []
    if (base_path / "probability.json").exists():
        with open(base_path / "probability.json", "r", encoding="utf-8") as f:
            existing_prob = json.load(f)
    
    existing_inf = []
    if (base_path / "inference.json").exists():
        with open(base_path / "inference.json", "r", encoding="utf-8") as f:
            existing_inf = json.load(f)
    
    existing_reg = []
    if (base_path / "regression.json").exists():
        with open(base_path / "regression.json", "r", encoding="utf-8") as f:
            existing_reg = json.load(f)
    
    # 既存の問題と新規問題を結合
    all_data_desc = existing_data_desc + data_description_problems
    all_prob = existing_prob + probability_problems
    all_inf = existing_inf + inference_problems
    all_reg = existing_reg + regression_problems
    
    # ファイルを保存
    with open(base_path / "data_description.json", "w", encoding="utf-8") as f:
        json.dump(all_data_desc, f, ensure_ascii=False, indent=2)
    
    with open(base_path / "probability.json", "w", encoding="utf-8") as f:
        json.dump(all_prob, f, ensure_ascii=False, indent=2)
    
    with open(base_path / "inference.json", "w", encoding="utf-8") as f:
        json.dump(all_inf, f, ensure_ascii=False, indent=2)
    
    with open(base_path / "regression.json", "w", encoding="utf-8") as f:
        json.dump(all_reg, f, ensure_ascii=False, indent=2)
    
    print(f"2級の問題を圧倒的に生成しました:")
    print(f"  - data_description: {len(all_data_desc)}問")
    print(f"  - probability: {len(all_prob)}問")
    print(f"  - inference: {len(all_inf)}問")
    print(f"  - regression: {len(all_reg)}問")
    print(f"  合計: {len(all_data_desc) + len(all_prob) + len(all_inf) + len(all_reg)}問")

def generate_massive_grade1_problems():
    """1級の問題を圧倒的に大量生成"""
    base_path = Path(__file__).parent / "data" / "problems" / "grade1"
    base_path.mkdir(parents=True, exist_ok=True)
    
    # statistics_math分野 - 200問
    statistics_math_problems = []
    for i in range(200):
        problem_types = [
            {
                "question": "確率変数Xが正規分布N(μ, σ²)に従うとき、Y = aX + b (a≠0)の分布は？",
                "question_type": "essay",
                "correct_answer": "N(aμ+b, a²σ²)",
                "explanation": "正規分布の線形変換の性質より、Y = aX + bはN(aμ+b, a²σ²)に従う。"
            },
            {
                "question": "中心極限定理の内容を簡潔に説明せよ。",
                "question_type": "essay",
                "correct_answer": "独立同分布の確率変数の和は、サンプルサイズが大きくなると正規分布に近づく",
                "explanation": "中心極限定理は、独立同分布の確率変数X₁, X₂, ..., Xₙの和や平均が、nが大きくなると正規分布に近づくことを示す。"
            },
            {
                "question": "最尤推定量の定義を述べよ。",
                "question_type": "essay",
                "correct_answer": "観測データに対する尤度関数を最大化するパラメータの推定量",
                "explanation": "最尤推定量は、観測されたデータが得られる確率（尤度）を最大にするパラメータの値である。"
            },
            {
                "question": "フィッシャー情報量I(θ)の定義式を書け。",
                "question_type": "essay",
                "correct_answer": "I(θ) = E[(-∂²log f(X;θ)/∂θ²)]",
                "explanation": "フィッシャー情報量は、対数尤度関数の2階偏微分の期待値の負の値として定義される。"
            },
            {
                "question": "不偏推定量の定義を述べよ。",
                "question_type": "essay",
                "correct_answer": "推定量の期待値が母数に等しい推定量",
                "explanation": "不偏推定量は、E[θ̂] = θ を満たす推定量である。"
            },
            {
                "question": "一致性推定量の定義を述べよ。",
                "question_type": "essay",
                "correct_answer": "サンプルサイズが大きくなると、真の母数に確率収束する推定量",
                "explanation": "一致性推定量は、n→∞のとき、θ̂ → θ (確率収束) を満たす推定量である。"
            }
        ]
        p = random.choice(problem_types)
        statistics_math_problems.append({
            "problem_id": f"G1_math_{i+1:04d}",
            "grade": "1",
            "category": "statistics_math",
            "difficulty": random.choice(["hard"]),
            "question_type": p["question_type"],
            "question": p["question"],
            "correct_answer": p["correct_answer"],
            "explanation": p["explanation"],
            "formulas_used": ["probability_theory", "estimation"],
            "tags": ["統計数理", "理論"]
        })
    
    # statistics_applied分野 - 150問
    statistics_applied_problems = []
    for i in range(150):
        problem_types = [
            {
                "question": "実験計画法における完全無作為化法と乱塊法の違いを説明せよ。",
                "question_type": "essay",
                "correct_answer": "完全無作為化法は全ての処理を完全にランダムに割り当てる。乱塊法はブロック内でランダムに割り当て、ブロック間の変動を制御する。",
                "explanation": "完全無作為化法は単純だが、ブロック効果を考慮しない。乱塊法はブロックを設けることで、ブロック間の変動を除去し、より精密な検定が可能。"
            },
            {
                "question": "ロジスティック回帰分析におけるオッズ比の解釈を説明せよ。",
                "question_type": "essay",
                "correct_answer": "オッズ比は、説明変数が1単位増加したとき、目的変数が1になるオッズが何倍になるかを示す。",
                "explanation": "オッズ比が2.0の場合、説明変数が1単位増加すると、目的変数が1になるオッズが2倍になることを意味する。"
            },
            {
                "question": "生存時間解析におけるハザード関数の意味を説明せよ。",
                "question_type": "essay",
                "correct_answer": "ハザード関数は、時点tまで生存していた場合に、その直後にイベントが発生する瞬間的な確率を表す。",
                "explanation": "ハザード関数h(t)は、h(t) = lim(Δt→0) P(t ≤ T < t+Δt | T ≥ t) / Δt で定義される。"
            },
            {
                "question": "ベイズ統計における事前分布の選択について説明せよ。",
                "question_type": "essay",
                "correct_answer": "事前分布は、事前知識を反映する分布を選択する。共役事前分布を使うと計算が容易になる。",
                "explanation": "事前分布の選択は、事前知識の有無、計算の容易さ、解釈のしやすさなどを考慮して決定する。"
            }
        ]
        p = random.choice(problem_types)
        statistics_applied_problems.append({
            "problem_id": f"G1_app_{i+1:04d}",
            "grade": "1",
            "category": "statistics_applied",
            "difficulty": random.choice(["hard"]),
            "question_type": p["question_type"],
            "question": p["question"],
            "correct_answer": p["correct_answer"],
            "explanation": p["explanation"],
            "formulas_used": ["experimental_design", "logistic_regression"],
            "tags": ["統計応用", "実践"]
        })
    
    # 既存の問題を読み込んで追加
    existing_math = []
    if (base_path / "statistics_math.json").exists():
        with open(base_path / "statistics_math.json", "r", encoding="utf-8") as f:
            existing_math = json.load(f)
    
    existing_app = []
    if (base_path / "statistics_applied.json").exists():
        with open(base_path / "statistics_applied.json", "r", encoding="utf-8") as f:
            existing_app = json.load(f)
    
    # 既存の問題と新規問題を結合
    all_math = existing_math + statistics_math_problems
    all_app = existing_app + statistics_applied_problems
    
    # ファイルを保存
    with open(base_path / "statistics_math.json", "w", encoding="utf-8") as f:
        json.dump(all_math, f, ensure_ascii=False, indent=2)
    
    with open(base_path / "statistics_applied.json", "w", encoding="utf-8") as f:
        json.dump(all_app, f, ensure_ascii=False, indent=2)
    
    print(f"1級の問題を圧倒的に生成しました:")
    print(f"  - statistics_math: {len(all_math)}問")
    print(f"  - statistics_applied: {len(all_app)}問")
    print(f"  合計: {len(all_math) + len(all_app)}問")

if __name__ == "__main__":
    print("=" * 50)
    print("全級問題大量生成スクリプト")
    print("=" * 50)
    print()
    generate_massive_grade2_problems()
    print()
    generate_massive_grade1_problems()
    print()
    print("=" * 50)
    print("全ての問題生成が完了しました！")
    print("=" * 50)
