"""
システム全体の動作確認
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.problem_manager import ProblemManager
from src.knowledge_base import KnowledgeBase
from src.utils import load_json

def test_system():
    """システム全体をテスト"""
    print("=" * 50)
    print("システム全体確認")
    print("=" * 50)
    print()
    
    # 問題管理システム
    pm = ProblemManager()
    print(f"問題ディレクトリ: {pm.problems_dir}")
    print()
    
    # 各級の問題数を確認
    g2 = pm.load_problems("2")
    g1 = pm.load_problems("1")
    pre1 = pm.load_problems("pre1")
    
    print(f"2級: {len(g2)}問")
    print(f"準1級: {len(pre1)}問")
    print(f"1級: {len(g1)}問")
    print(f"合計: {len(g2) + len(pre1) + len(g1)}問")
    print()
    
    # 設定ファイルの確認
    settings_path = Path(__file__).parent / "config" / "settings.json"
    settings = load_json(settings_path)
    if isinstance(settings, dict):
        print("設定カテゴリ:")
        print(f"  - grade2: {settings.get('categories', {}).get('grade2', [])}")
        print(f"  - grade_pre1: {settings.get('categories', {}).get('grade_pre1', [])}")
        print(f"  - grade1: {settings.get('categories', {}).get('grade1', [])}")
    else:
        print(f"⚠️ 設定ファイルの形式が正しくありません: {type(settings)}")
    print()
    
    # 知識ベースの確認
    kb = KnowledgeBase()
    f2 = kb.get_formulas("2")
    f1 = kb.get_formulas("1")
    fp1 = kb.get_formulas("pre1")
    
    print("公式データ:")
    print(f"  - 2級: {len(f2)}カテゴリ")
    print(f"  - 準1級: {len(fp1)}カテゴリ")
    print(f"  - 1級: {len(f1)}カテゴリ")
    print()
    
    # カテゴリごとの問題数確認
    if isinstance(settings, dict):
        print("カテゴリ別問題数:")
        for grade, grade_name in [("2", "2級"), ("pre1", "準1級"), ("1", "1級")]:
            print(f"  {grade_name}:")
            category_key = {"2": "grade2", "pre1": "grade_pre1", "1": "grade1"}.get(grade)
            categories = settings.get("categories", {}).get(category_key, [])
            for cat in categories:
                problems = pm.load_problems(grade, cat)
                print(f"    - {cat}: {len(problems)}問")
        print()
    
    print("=" * 50)
    print("✅ システム確認完了")
    print("=" * 50)

if __name__ == "__main__":
    test_system()
