"""LIFE CODE: 생명의 비밀과 마지막 탈출.

GitHub 저장소의 실행 시작 파일입니다. Streamlit 메인 파일을 main.py로 지정하세요.
이 앱은 Python 기반이며, 필요한 브라우저 그래픽 코드가 .py 모듈에 포함됩니다.
"""

import streamlit as st
import streamlit.components.v1 as components

from game_data import GAME_DATA_JS
from world import WORLD_JS
from game_utils import GAME_CSS, GAME_LOGIC_JS


st.set_page_config(
    page_title="LIFE CODE · 생명의 비밀과 마지막 탈출",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def build_game_html() -> str:
    """외부 JS/CSS 파일 없이 iframe에서 독립 실행되는 전체 게임 화면 생성."""
    # '<script>' 종료 문자열이 JS 안에 포함되어 HTML 파서가 잘못 인식하는 것을 방지
    scripts = [GAME_DATA_JS, WORLD_JS, GAME_LOGIC_JS]
    safe_scripts = [script.replace("</script", "<\\/script") for script in scripts]
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LIFE CODE | 성장형 스토리 RPG</title>
<style>{GAME_CSS}</style>
</head>
<body>
<main id="app" aria-live="polite"></main>
<script>{safe_scripts[0]}</script>
<script>{safe_scripts[1]}</script>
<script>{safe_scripts[2]}</script>
</body>
</html>"""


st.markdown(
    """<style>
    #MainMenu, footer {visibility: hidden !important}
    header[data-testid="stHeader"] {background: transparent !important}
    div.block-container {max-width: 1320px !important; padding: 0 0 1rem !important}
    [data-testid="stAppViewContainer"] {background: #fff8f3 !important}
    iframe[title="streamlit.components.v1.html"] {border: 0 !important}
    </style>""",
    unsafe_allow_html=True,
)

# Streamlit 서버가 아닌 브라우저 iframe 안에서 캐릭터의 이동·충돌을 처리합니다.
try:
    components.html(build_game_html(), height=1450, scrolling=True)
except Exception as exc:
    st.error("게임 화면 생성에 실패했습니다. 파일 이름과 코드를 확인해 주세요.")
    st.exception(exc)
