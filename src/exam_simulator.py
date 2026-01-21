"""
模擬試験機能
"""
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .problem_manager import ProblemManager
from .progress_tracker import ProgressTracker
from .utils import get_timestamp, format_time


class ExamSimulator:
    """模擬試験を管理するクラス"""
    
    def __init__(self):
        self.problem_manager = ProblemManager()
        self.progress_tracker = ProgressTracker()
        self.current_exam = None
    
    def start_exam(self, grade: str, num_questions: Optional[int] = None):
        """模擬試験を開始"""
        from .utils import load_json
        import json
        
        # 設定を読み込み
        settings_path = self.problem_manager.root / "config" / "settings.json"
        settings = load_json(settings_path)
        
        grade_config = settings["grades"].get(grade, {})
        
        # 問題数を決定
        if num_questions is None:
            if grade == "1":
                # 1級は特殊（後で実装）
                num_questions = 3
            else:
                num_questions = grade_config.get("questions", 30)
        
        # 問題を取得
        problems = self.problem_manager.get_random_problems(grade, num_questions)
        
        if not problems:
            return None
        
        # 試験時間を設定
        time_minutes = grade_config.get("time_minutes", 90)
        
        self.current_exam = {
            "exam_id": get_timestamp(),
            "grade": grade,
            "problems": problems,
            "answers": {},
            "start_time": datetime.now(),
            "end_time": None,
            "time_limit": timedelta(minutes=time_minutes),
            "is_finished": False
        }
        
        return self.current_exam
    
    def submit_answer(self, problem_id: str, answer):
        """解答を提出"""
        if not self.current_exam:
            return False
        
        self.current_exam["answers"][problem_id] = {
            "answer": answer,
            "submitted_at": datetime.now()
        }
        return True
    
    def finish_exam(self) -> Dict:
        """試験を終了して採点"""
        if not self.current_exam:
            return {}
        
        self.current_exam["end_time"] = datetime.now()
        self.current_exam["is_finished"] = True
        
        # 採点
        results = self._grade_exam()
        
        # 結果を保存
        session_data = {
            "session_id": self.current_exam["exam_id"],
            "grade": self.current_exam["grade"],
            "mode": "exam",
            "total_questions": len(self.current_exam["problems"]),
            "correct_answers": results["correct_count"],
            "accuracy": results["accuracy"],
            "time_spent": (self.current_exam["end_time"] - self.current_exam["start_time"]).total_seconds(),
            "category_scores": results["category_scores"],
            "detailed_results": results["detailed_results"]
        }
        
        self.progress_tracker.save_session(session_data)
        
        return {
            "exam_id": self.current_exam["exam_id"],
            "results": results,
            "session_data": session_data
        }
    
    def _grade_exam(self) -> Dict:
        """試験を採点"""
        correct_count = 0
        category_scores = {}
        detailed_results = []
        
        for problem in self.current_exam["problems"]:
            problem_id = problem["problem_id"]
            user_answer = self.current_exam["answers"].get(problem_id, {}).get("answer")
            correct_answer = problem.get("correct_answer")
            category = problem.get("category", "unknown")
            
            # 正誤判定
            is_correct = self._check_answer(problem, user_answer)
            
            if is_correct:
                correct_count += 1
            
            # 分野別スコア
            if category not in category_scores:
                category_scores[category] = {"correct": 0, "total": 0}
            category_scores[category]["total"] += 1
            if is_correct:
                category_scores[category]["correct"] += 1
            
            detailed_results.append({
                "problem_id": problem_id,
                "is_correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": correct_answer
            })
        
        # 分野別正答率を計算
        category_accuracy = {
            cat: scores["correct"] / scores["total"]
            for cat, scores in category_scores.items()
        }
        
        accuracy = correct_count / len(self.current_exam["problems"]) if self.current_exam["problems"] else 0
        
        return {
            "correct_count": correct_count,
            "accuracy": accuracy,
            "category_scores": category_accuracy,
            "detailed_results": detailed_results
        }
    
    def _check_answer(self, problem: Dict, user_answer) -> bool:
        """解答が正しいかチェック"""
        question_type = problem.get("question_type", "multiple_choice")
        correct_answer = problem.get("correct_answer")
        
        if question_type == "multiple_choice":
            return user_answer == correct_answer
        elif question_type == "numeric_input":
            try:
                user_val = float(user_answer)
                correct_val = float(correct_answer)
                tolerance = problem.get("tolerance", 0.01)
                return abs(user_val - correct_val) <= tolerance
            except (ValueError, TypeError):
                return False
        elif question_type == "essay":
            # 論述式は自己採点のため、常にFalse（後で実装）
            return False
        
        return False
    
    def get_remaining_time(self) -> Optional[timedelta]:
        """残り時間を取得"""
        if not self.current_exam or self.current_exam["is_finished"]:
            return None
        
        elapsed = datetime.now() - self.current_exam["start_time"]
        remaining = self.current_exam["time_limit"] - elapsed
        
        if remaining.total_seconds() <= 0:
            return timedelta(0)
        
        return remaining
