"""
問題管理システム
"""
import json
import random
from pathlib import Path
from typing import List, Dict, Optional
from .utils import get_project_root, load_json, save_json


class ProblemManager:
    """問題の管理を行うクラス"""
    
    def __init__(self):
        self.root = get_project_root()
        self.problems_dir = self.root / "data" / "problems"
        self.problems_cache = {}
    
    def load_problems(self, grade: str, category: Optional[str] = None) -> List[Dict]:
        """問題を読み込む"""
        cache_key = f"{grade}_{category or 'all'}"
        if cache_key in self.problems_cache:
            return self.problems_cache[cache_key]
        
        problems = []
        # 級名をディレクトリ名に変換
        grade_dir_name = {"2": "grade2", "pre1": "grade_pre1", "1": "grade1"}.get(grade, f"grade{grade}")
        grade_dir = self.problems_dir / grade_dir_name
        
        if not grade_dir.exists():
            return problems
        
        if category:
            # 特定のカテゴリのみ
            file_path = grade_dir / f"{category}.json"
            if file_path.exists():
                problems.extend(load_json(file_path))
        else:
            # 全カテゴリ
            for file_path in grade_dir.glob("*.json"):
                problems.extend(load_json(file_path))
        
        self.problems_cache[cache_key] = problems
        return problems
    
    def get_problem(self, problem_id: str) -> Optional[Dict]:
        """問題IDから問題を取得"""
        # 全級から検索
        grade_dirs = [
            self.problems_dir / "grade2",
            self.problems_dir / "grade_pre1",
            self.problems_dir / "grade1"
        ]
        
        for grade_dir in grade_dirs:
            if not grade_dir.exists() or not grade_dir.is_dir():
                continue
            
            for file_path in grade_dir.glob("*.json"):
                problems = load_json(file_path)
                for problem in problems:
                    if problem.get("problem_id") == problem_id:
                        return problem
        return None
    
    def add_problem(self, problem: Dict, grade: str, category: str):
        """問題を追加"""
        # 級名をディレクトリ名に変換
        grade_dir_name = {"2": "grade2", "pre1": "grade_pre1", "1": "grade1"}.get(grade, f"grade{grade}")
        grade_dir = self.problems_dir / grade_dir_name
        grade_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = grade_dir / f"{category}.json"
        
        if file_path.exists():
            problems = load_json(file_path)
        else:
            problems = []
        
        # 問題IDが既に存在する場合は更新
        problem_id = problem.get("problem_id")
        if problem_id:
            for i, p in enumerate(problems):
                if p.get("problem_id") == problem_id:
                    problems[i] = problem
                    save_json(problems, file_path)
                    self._clear_cache(grade, category)
                    return
        
        # 新規追加
        if not problem_id:
            problem["problem_id"] = self._generate_problem_id(grade, category, len(problems))
        
        problems.append(problem)
        save_json(problems, file_path)
        self._clear_cache(grade, category)
    
    def delete_problem(self, problem_id: str):
        """問題を削除"""
        for grade_dir in self.problems_dir.iterdir():
            if not grade_dir.is_dir():
                continue
            
            for file_path in grade_dir.glob("*.json"):
                problems = load_json(file_path)
                updated = [p for p in problems if p.get("problem_id") != problem_id]
                
                if len(updated) != len(problems):
                    save_json(updated, file_path)
                    # キャッシュをクリア
                    grade = grade_dir.name.replace("grade", "")
                    self._clear_cache(grade)
                    return True
        return False
    
    def get_random_problems(self, grade: str, num: int, category: Optional[str] = None, 
                           difficulty: Optional[str] = None) -> List[Dict]:
        """ランダムに問題を取得"""
        problems = self.load_problems(grade, category)
        
        # 難易度でフィルタ
        if difficulty:
            problems = [p for p in problems if p.get("difficulty") == difficulty]
        
        # ランダムに選択
        if len(problems) <= num:
            return problems
        return random.sample(problems, num)
    
    def filter_problems(self, grade: str, category: Optional[str] = None,
                       difficulty: Optional[str] = None,
                       tags: Optional[List[str]] = None) -> List[Dict]:
        """問題をフィルタリング"""
        problems = self.load_problems(grade, category)
        
        if difficulty:
            problems = [p for p in problems if p.get("difficulty") == difficulty]
        
        if tags:
            filtered = []
            for p in problems:
                problem_tags = p.get("tags", [])
                if any(tag in problem_tags for tag in tags):
                    filtered.append(p)
            problems = filtered
        
        return problems
    
    def _generate_problem_id(self, grade: str, category: str, index: int) -> str:
        """問題IDを生成"""
        grade_prefix = {"2": "G2", "pre1": "GP1", "1": "G1"}.get(grade, "G")
        return f"{grade_prefix}_{category}_{index+1:03d}"
    
    def _clear_cache(self, grade: str, category: Optional[str] = None):
        """キャッシュをクリア"""
        if category:
            cache_key = f"{grade}_{category}"
            self.problems_cache.pop(cache_key, None)
        else:
            # その級の全キャッシュをクリア
            keys_to_remove = [k for k in self.problems_cache.keys() if k.startswith(f"{grade}_")]
            for key in keys_to_remove:
                self.problems_cache.pop(key, None)
