"""
システムテストスクリプト
"""
import sys
from pathlib import Path

# パスを追加
sys.path.insert(0, str(Path(__file__).parent))

from src.problem_manager import ProblemManager
from src.progress_tracker import ProgressTracker
from src.calculator import StatisticsCalculator
from src.knowledge_base import KnowledgeBase

def test_problem_manager():
    """問題管理システムのテスト"""
    print("=" * 50)
    print("問題管理システムのテスト")
    print("=" * 50)
    
    pm = ProblemManager()
    
    # 2級の問題を読み込み
    problems_2 = pm.load_problems("2")
    print(f"✓ 2級問題数: {len(problems_2)}")
    
    # 準1級の問題を読み込み
    problems_pre1 = pm.load_problems("pre1")
    print(f"✓ 準1級問題数: {len(problems_pre1)}")
    
    # 1級の問題を読み込み
    problems_1 = pm.load_problems("1")
    print(f"✓ 1級問題数: {len(problems_1)}")
    
    # ランダム問題取得
    random_problems = pm.get_random_problems("2", 2)
    print(f"✓ ランダム問題取得: {len(random_problems)}問")
    
    print("✓ 問題管理システム: OK\n")

def test_progress_tracker():
    """進捗管理のテスト"""
    print("=" * 50)
    print("進捗管理のテスト")
    print("=" * 50)
    
    pt = ProgressTracker()
    
    # 統計情報取得
    stats = pt.get_statistics()
    print(f"✓ 総セッション数: {stats['total_sessions']}")
    print(f"✓ 平均正答率: {stats['average_accuracy'] * 100:.1f}%")
    
    print("✓ 進捗管理: OK\n")

def test_calculator():
    """統計計算ツールのテスト"""
    print("=" * 50)
    print("統計計算ツールのテスト")
    print("=" * 50)
    
    calc = StatisticsCalculator()
    
    # 基本統計量
    data = [1, 2, 3, 4, 5]
    stats = calc.basic_statistics(data)
    print(f"✓ 基本統計量計算: 平均 = {stats['mean']:.2f}")
    
    # t検定
    t_result = calc.t_test_one_sample(data, 3.0)
    print(f"✓ 1標本t検定: t統計量 = {t_result['t_statistic']:.4f}")
    
    print("✓ 統計計算ツール: OK\n")

def test_knowledge_base():
    """知識ベースのテスト"""
    print("=" * 50)
    print("知識ベースのテスト")
    print("=" * 50)
    
    kb = KnowledgeBase()
    
    # 公式取得
    formulas_2 = kb.get_formulas("2")
    print(f"✓ 2級公式数: {len(formulas_2)}")
    
    # 用語検索
    terms = kb.search_term("平均")
    print(f"✓ 用語検索結果: {len(terms)}件")
    
    print("✓ 知識ベース: OK\n")

if __name__ == "__main__":
    try:
        test_problem_manager()
        test_progress_tracker()
        test_calculator()
        test_knowledge_base()
        
        print("=" * 50)
        print("✅ すべてのテストが完了しました！")
        print("=" * 50)
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
