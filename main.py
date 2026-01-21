"""
統計検定学習支援システム - メインアプリケーション
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path

# パスを追加
sys.path.insert(0, str(Path(__file__).parent))

from src.problem_manager import ProblemManager
from src.exam_simulator import ExamSimulator
from src.progress_tracker import ProgressTracker
from src.calculator import StatisticsCalculator
from src.knowledge_base import KnowledgeBase
from src.utils import load_json, format_time

# ページ設定
st.set_page_config(
    page_title="統計検定学習支援システム",
    page_icon="📊",
    layout="wide"
)

# セッション状態の初期化
if "problem_manager" not in st.session_state:
    st.session_state.problem_manager = ProblemManager()
if "exam_simulator" not in st.session_state:
    st.session_state.exam_simulator = ExamSimulator()
if "progress_tracker" not in st.session_state:
    st.session_state.progress_tracker = ProgressTracker()
if "calculator" not in st.session_state:
    st.session_state.calculator = StatisticsCalculator()
if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = KnowledgeBase()

# サイドバー
st.sidebar.title("📊 統計検定学習支援システム")
page = st.sidebar.selectbox(
    "メニュー",
    ["ホーム", "問題練習", "模擬試験", "進捗確認", "統計計算", "知識ベース"]
)

# メインコンテンツ
if page == "ホーム":
    st.title("📊 統計検定学習支援システム")
    st.markdown("---")
    
    st.markdown("""
    ### ようこそ！
    
    このシステムは、統計検定1級・準1級・2級の合格を支援するための学習ツールです。
    
    ### 主な機能
    
    - **問題練習**: 各級の問題を練習できます
    - **模擬試験**: 本番形式の模擬試験を受験できます
    - **進捗確認**: 学習の進捗を可視化できます
    - **統計計算**: 統計計算ツールを使用できます
    - **知識ベース**: 公式集や用語集を参照できます
    
    ### 統計検定について
    
    - **2級**: 大学教養課程レベル、35問、90分、合格ライン70点
    - **準1級**: 2級を含む応用レベル、25-30問、90分、合格ライン60点
    - **1級**: 大学専門課程・大学院レベル、論述式、各90分
    """)

elif page == "問題練習":
    st.title("📝 問題練習")
    st.markdown("---")
    
    # 級の選択
    grade = st.selectbox("級を選択", ["2", "pre1", "1"], format_func=lambda x: {"2": "2級", "pre1": "準1級", "1": "1級"}[x])
    
    # カテゴリの選択
    settings = load_json(Path(__file__).parent / "config" / "settings.json")
    categories = settings["categories"].get(f"grade{grade}", [])
    category = st.selectbox("分野を選択", ["全分野"] + categories)
    
    # 問題数の設定
    num_questions = st.number_input("問題数", min_value=1, max_value=50, value=10)
    
    # 難易度フィルタ
    difficulty = st.selectbox("難易度", ["全て", "easy", "medium", "hard"])
    
    if st.button("練習開始"):
        # 問題を取得
        selected_category = None if category == "全分野" else category
        selected_difficulty = None if difficulty == "全て" else difficulty
        
        problems = st.session_state.problem_manager.get_random_problems(
            grade, num_questions, selected_category, selected_difficulty
        )
        
        if not problems:
            st.warning("問題が見つかりませんでした。")
        else:
            st.session_state["practice_problems"] = problems
            st.session_state["practice_index"] = 0
            st.session_state["practice_answers"] = {}
            st.rerun()
    
    # 問題表示
    if "practice_problems" in st.session_state:
        problems = st.session_state["practice_problems"]
        index = st.session_state["practice_index"]
        
        if index < len(problems):
            problem = problems[index]
            
            st.markdown(f"### 問題 {index + 1} / {len(problems)}")
            st.markdown(f"**問題ID**: {problem.get('problem_id')}")
            st.markdown(f"**分野**: {problem.get('category')}")
            st.markdown(f"**難易度**: {problem.get('difficulty')}")
            st.markdown("---")
            
            # 問題文
            st.markdown(f"**問題**\n\n{problem.get('question')}")
            
            # 解答欄
            question_type = problem.get("question_type", "multiple_choice")
            
            if question_type == "multiple_choice":
                options = problem.get("options", [])
                answer = st.radio("選択肢", options, key=f"answer_{index}")
            elif question_type == "numeric_input":
                answer = st.number_input("数値を入力", key=f"answer_{index}", step=0.01)
            elif question_type == "essay":
                answer = st.text_area("解答を入力", key=f"answer_{index}", height=200)
            else:
                answer = None
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("前の問題", disabled=index == 0):
                    st.session_state["practice_index"] = index - 1
                    st.rerun()
            
            with col2:
                if st.button("次の問題", disabled=index == len(problems) - 1):
                    st.session_state["practice_answers"][problem["problem_id"]] = answer
                    st.session_state["practice_index"] = index + 1
                    st.rerun()
            
            # 解答を保存
            if answer is not None:
                st.session_state["practice_answers"][problem["problem_id"]] = answer
            
            # 正誤判定ボタン
            if st.button("正誤を確認"):
                user_answer = st.session_state["practice_answers"].get(problem["problem_id"])
                correct_answer = problem.get("correct_answer")
                
                # 簡易判定
                is_correct = False
                if question_type == "multiple_choice":
                    is_correct = user_answer == options[correct_answer] if correct_answer is not None else False
                elif question_type == "numeric_input":
                    try:
                        tolerance = problem.get("tolerance", 0.01)
                        is_correct = abs(float(user_answer) - float(correct_answer)) <= tolerance
                    except:
                        is_correct = False
                
                if is_correct:
                    st.success("✅ 正解です！")
                else:
                    st.error(f"❌ 不正解です。正解は: {correct_answer}")
                
                # 解説
                if problem.get("explanation"):
                    st.info(f"**解説**: {problem.get('explanation')}")
        else:
            # 結果表示
            st.success("全ての問題を完了しました！")
            
            # 採点
            correct_count = 0
            for problem in problems:
                problem_id = problem["problem_id"]
                user_answer = st.session_state["practice_answers"].get(problem_id)
                correct_answer = problem.get("correct_answer")
                
                question_type = problem.get("question_type", "multiple_choice")
                is_correct = False
                
                if question_type == "multiple_choice":
                    options = problem.get("options", [])
                    is_correct = user_answer == options[correct_answer] if correct_answer is not None else False
                elif question_type == "numeric_input":
                    try:
                        tolerance = problem.get("tolerance", 0.01)
                        is_correct = abs(float(user_answer) - float(correct_answer)) <= tolerance
                    except:
                        is_correct = False
                
                if is_correct:
                    correct_count += 1
            
            accuracy = correct_count / len(problems) if problems else 0
            
            st.metric("正答数", f"{correct_count} / {len(problems)}")
            st.metric("正答率", f"{accuracy * 100:.1f}%")
            
            # 結果を保存
            if st.button("結果を保存"):
                session_data = {
                    "grade": grade,
                    "mode": "practice",
                    "total_questions": len(problems),
                    "correct_answers": correct_count,
                    "accuracy": accuracy
                }
                st.session_state.progress_tracker.save_session(session_data)
                st.success("結果を保存しました！")

elif page == "模擬試験":
    st.title("📋 模擬試験")
    st.markdown("---")
    
    grade = st.selectbox("級を選択", ["2", "pre1", "1"], format_func=lambda x: {"2": "2級", "pre1": "準1級", "1": "1級"}[x])
    
    if "current_exam" not in st.session_state or st.session_state.get("exam_grade") != grade:
        if st.button("模擬試験を開始"):
            exam = st.session_state.exam_simulator.start_exam(grade)
            if exam:
                st.session_state["current_exam"] = exam
                st.session_state["exam_grade"] = grade
                st.rerun()
            else:
                st.error("問題が見つかりませんでした。")
    else:
        exam = st.session_state["current_exam"]
        
        # 残り時間表示
        remaining = st.session_state.exam_simulator.get_remaining_time()
        if remaining:
            st.info(f"⏰ 残り時間: {format_time(int(remaining.total_seconds()))}")
        else:
            st.warning("時間切れです！")
        
        # 問題表示
        if not exam.get("is_finished"):
            problems = exam["problems"]
            problem_index = st.session_state.get("exam_problem_index", 0)
            
            if problem_index < len(problems):
                problem = problems[problem_index]
                
                st.markdown(f"### 問題 {problem_index + 1} / {len(problems)}")
                st.markdown(f"**問題ID**: {problem.get('problem_id')}")
                st.markdown("---")
                st.markdown(f"**問題**\n\n{problem.get('question')}")
                
                # 解答欄
                question_type = problem.get("question_type", "multiple_choice")
                problem_id = problem["problem_id"]
                
                if question_type == "multiple_choice":
                    options = problem.get("options", [])
                    answer = st.radio("選択肢", options, key=f"exam_answer_{problem_index}")
                elif question_type == "numeric_input":
                    answer = st.number_input("数値を入力", key=f"exam_answer_{problem_index}", step=0.01)
                else:
                    answer = st.text_area("解答を入力", key=f"exam_answer_{problem_index}", height=200)
                
                # 解答を保存
                st.session_state.exam_simulator.submit_answer(problem_id, answer)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("前の問題", disabled=problem_index == 0):
                        st.session_state["exam_problem_index"] = problem_index - 1
                        st.rerun()
                with col2:
                    if st.button("次の問題", disabled=problem_index == len(problems) - 1):
                        st.session_state["exam_problem_index"] = problem_index + 1
                        st.rerun()
                
                # 提出ボタン
                if st.button("試験を終了して採点"):
                    results = st.session_state.exam_simulator.finish_exam()
                    st.session_state["exam_results"] = results
                    st.session_state["current_exam"]["is_finished"] = True
                    st.rerun()
            else:
                if st.button("試験を終了して採点"):
                    results = st.session_state.exam_simulator.finish_exam()
                    st.session_state["exam_results"] = results
                    st.rerun()
        else:
            # 結果表示
            if "exam_results" in st.session_state:
                results = st.session_state["exam_results"]["results"]
                
                st.success("模擬試験が完了しました！")
                st.metric("正答数", f"{results['correct_count']} / {len(exam['problems'])}")
                st.metric("正答率", f"{results['accuracy'] * 100:.1f}%")
                
                # 分野別成績
                if results.get("category_scores"):
                    st.subheader("分野別成績")
                    category_df = pd.DataFrame(list(results["category_scores"].items()), columns=["分野", "正答率"])
                    category_df["正答率"] = category_df["正答率"] * 100
                    st.bar_chart(category_df.set_index("分野"))
                
                if st.button("新しい試験を開始"):
                    st.session_state.pop("current_exam", None)
                    st.session_state.pop("exam_results", None)
                    st.session_state.pop("exam_problem_index", None)
                    st.rerun()

elif page == "進捗確認":
    st.title("📈 進捗確認")
    st.markdown("---")
    
    grade = st.selectbox("級を選択", ["全て", "2", "pre1", "1"], format_func=lambda x: {"全て": "全て", "2": "2級", "pre1": "準1級", "1": "1級"}[x])
    selected_grade = None if grade == "全て" else grade
    
    # 統計情報
    stats = st.session_state.progress_tracker.get_statistics(selected_grade)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("総セッション数", stats["total_sessions"])
    with col2:
        st.metric("平均正答率", f"{stats['average_accuracy'] * 100:.1f}%")
    with col3:
        st.metric("総問題数", stats["total_questions"])
    with col4:
        st.metric("総正答数", stats["total_correct"])
    
    # セッション履歴
    st.subheader("セッション履歴")
    sessions = st.session_state.progress_tracker.get_all_sessions(selected_grade)
    
    if sessions:
        session_df = pd.DataFrame([
            {
                "日付": s.get("date", ""),
                "級": {"2": "2級", "pre1": "準1級", "1": "1級"}.get(s.get("grade", ""), ""),
                "モード": s.get("mode", ""),
                "問題数": s.get("total_questions", 0),
                "正答数": s.get("correct_answers", 0),
                "正答率": f"{s.get('accuracy', 0) * 100:.1f}%"
            }
            for s in sessions[:20]  # 最新20件
        ])
        st.dataframe(session_df, use_container_width=True)
        
        # 正答率の推移
        if len(sessions) > 1:
            st.subheader("正答率の推移")
            dates = [s.get("date", "") for s in sessions]
            accuracies = [s.get("accuracy", 0) * 100 for s in sessions]
            
            fig = px.line(x=dates, y=accuracies, labels={"x": "日付", "y": "正答率 (%)"})
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("まだセッション履歴がありません。")

elif page == "統計計算":
    st.title("🔢 統計計算ツール")
    st.markdown("---")
    
    calc_type = st.selectbox("計算タイプ", [
        "基本統計量",
        "1標本t検定",
        "2標本t検定",
        "対応のあるt検定",
        "相関係数",
        "単回帰分析"
    ])
    
    # データ入力
    st.subheader("データ入力")
    data_input = st.text_area("データを入力（カンマ区切り）", "1, 2, 3, 4, 5")
    
    try:
        data = [float(x.strip()) for x in data_input.split(",")]
        
        if calc_type == "基本統計量":
            stats_result = st.session_state.calculator.basic_statistics(data)
            
            st.subheader("結果")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("平均", f"{stats_result['mean']:.4f}")
                st.metric("中央値", f"{stats_result['median']:.4f}")
                st.metric("標準偏差", f"{stats_result['std']:.4f}")
                st.metric("分散", f"{stats_result['variance']:.4f}")
            with col2:
                st.metric("最小値", f"{stats_result['min']:.4f}")
                st.metric("最大値", f"{stats_result['max']:.4f}")
                st.metric("範囲", f"{stats_result['range']:.4f}")
                st.metric("IQR", f"{stats_result['iqr']:.4f}")
        
        elif calc_type == "1標本t検定":
            mu0 = st.number_input("帰無仮説の平均値 (μ₀)", value=0.0)
            result = st.session_state.calculator.t_test_one_sample(data, mu0)
            st.metric("t統計量", f"{result['t_statistic']:.4f}")
            st.metric("p値", f"{result['p_value']:.4f}")
            st.metric("自由度", result['df'])
        
        elif calc_type == "相関係数":
            st.subheader("2つ目のデータ")
            data2_input = st.text_area("2つ目のデータ（カンマ区切り）", "2, 4, 6, 8, 10")
            data2 = [float(x.strip()) for x in data2_input.split(",")]
            
            if len(data) == len(data2):
                result = st.session_state.calculator.correlation_test(data, data2)
                st.metric("相関係数", f"{result['correlation']:.4f}")
                st.metric("p値", f"{result['p_value']:.4f}")
            else:
                st.error("データの長さが一致しません。")
        
        elif calc_type == "単回帰分析":
            st.subheader("yデータ")
            y_input = st.text_area("yデータ（カンマ区切り）", "2, 4, 6, 8, 10")
            y_data = [float(x.strip()) for x in y_input.split(",")]
            
            if len(data) == len(y_data):
                result = st.session_state.calculator.linear_regression(data, y_data)
                st.metric("回帰係数（傾き）", f"{result['slope']:.4f}")
                st.metric("切片", f"{result['intercept']:.4f}")
                st.metric("決定係数 (R²)", f"{result['r_squared']:.4f}")
                st.metric("相関係数", f"{result['correlation']:.4f}")
            else:
                st.error("データの長さが一致しません。")
    
    except ValueError:
        st.error("データの形式が正しくありません。数値をカンマ区切りで入力してください。")

elif page == "知識ベース":
    st.title("📚 知識ベース")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["公式集", "用語集"])
    
    with tab1:
        grade = st.selectbox("級を選択", ["2", "pre1", "1"], format_func=lambda x: {"2": "2級", "pre1": "準1級", "1": "1級"}[x], key="formula_grade")
        
        formulas = st.session_state.knowledge_base.get_formulas(grade)
        
        if formulas:
            for category, formula_dict in formulas.items():
                with st.expander(category):
                    for name, formula in formula_dict.items():
                        st.markdown(f"**{name}**: {formula}")
        else:
            st.info("公式データが見つかりませんでした。")
    
    with tab2:
        keyword = st.text_input("用語を検索")
        
        if keyword:
            terms = st.session_state.knowledge_base.search_term(keyword)
            
            if terms:
                for term in terms:
                    with st.expander(term.get("term", "")):
                        st.markdown(f"**カテゴリ**: {term.get('category', '')}")
                        st.markdown(f"**説明**: {term.get('description', '')}")
            else:
                st.info("該当する用語が見つかりませんでした。")
        else:
            st.info("検索キーワードを入力してください。")

if __name__ == "__main__":
    pass
