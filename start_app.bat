@echo off
cd /d "C:\Users\nishi\Life\statics_test"
call C:\Users\nishi\anaconda3\Scripts\activate.bat statics_test
python -m streamlit run main.py
if errorlevel 1 (
    echo Streamlitが見つかりません。インストール中...
    pip install streamlit
    python -m streamlit run main.py
)
pause
