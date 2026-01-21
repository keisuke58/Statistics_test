"""
学習進捗管理
"""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from .utils import get_project_root, load_json, save_json, get_timestamp


class ProgressTracker:
    """学習進捗を管理するクラス"""
    
    def __init__(self):
        self.root = get_project_root()
        self.history_dir = self.root / "data" / "history"
        self.history_dir.mkdir(parents=True, exist_ok=True)
    
    def save_session(self, session_data: Dict):
        """セッション結果を保存"""
        session_id = session_data.get("session_id") or get_timestamp()
        session_data["session_id"] = session_id
        session_data["date"] = datetime.now().strftime("%Y-%m-%d")
        session_data["timestamp"] = datetime.now().isoformat()
        
        file_path = self.history_dir / f"{session_id}.json"
        save_json(session_data, file_path)
        
        # 履歴一覧にも追加
        self._update_history_list(session_data)
    
    def get_session(self, session_id: str) -> Dict:
        """セッション結果を取得"""
        file_path = self.history_dir / f"{session_id}.json"
        if file_path.exists():
            return load_json(file_path)
        return {}
    
    def get_all_sessions(self, grade: Optional[str] = None, mode: Optional[str] = None) -> List[Dict]:
        """全セッションを取得"""
        sessions = []
        for file_path in self.history_dir.glob("*.json"):
            if file_path.name == "history_list.json":
                continue
            session = load_json(file_path)
            if grade and session.get("grade") != grade:
                continue
            if mode and session.get("mode") != mode:
                continue
            sessions.append(session)
        
        # 日時でソート（新しい順）
        sessions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return sessions
    
    def get_statistics(self, grade: Optional[str] = None) -> Dict:
        """統計情報を取得"""
        sessions = self.get_all_sessions(grade=grade)
        
        if not sessions:
            return {
                "total_sessions": 0,
                "average_accuracy": 0,
                "total_questions": 0,
                "total_correct": 0
            }
        
        total_sessions = len(sessions)
        total_questions = sum(s.get("total_questions", 0) for s in sessions)
        total_correct = sum(s.get("correct_answers", 0) for s in sessions)
        average_accuracy = total_correct / total_questions if total_questions > 0 else 0
        
        # 分野別統計
        category_stats = {}
        for session in sessions:
            category_scores = session.get("category_scores", {})
            for category, score in category_scores.items():
                if category not in category_stats:
                    category_stats[category] = {"total": 0, "sum": 0}
                category_stats[category]["total"] += 1
                category_stats[category]["sum"] += score
        
        category_averages = {
            cat: stats["sum"] / stats["total"]
            for cat, stats in category_stats.items()
        }
        
        return {
            "total_sessions": total_sessions,
            "average_accuracy": average_accuracy,
            "total_questions": total_questions,
            "total_correct": total_correct,
            "category_averages": category_averages
        }
    
    def _update_history_list(self, session_data: Dict):
        """履歴一覧を更新"""
        list_path = self.history_dir / "history_list.json"
        if list_path.exists():
            history_list = load_json(list_path)
        else:
            history_list = []
        
        # 重複チェック
        session_id = session_data.get("session_id")
        history_list = [h for h in history_list if h.get("session_id") != session_id]
        
        # 追加
        history_list.append({
            "session_id": session_id,
            "date": session_data.get("date"),
            "grade": session_data.get("grade"),
            "mode": session_data.get("mode"),
            "accuracy": session_data.get("accuracy", 0)
        })
        
        # ソート（新しい順）
        history_list.sort(key=lambda x: x.get("date", ""), reverse=True)
        
        save_json(history_list, list_path)
