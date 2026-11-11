import random
import streamlit as st
from game_data import VACCINES, IMMUNE, BODY, LAB, BODY_MAP, LAB_MAP
from game_utils import game, new_game, coin_change, notify, move, render_map, controls

st.set_page_config(page_title="LIFE CODE",page_icon="🧬",layout="wide")
st.markdown("""<style>.stApp{background:#101827;color:#eef6ff}.block-container{max-width:1050px}h1,h2,h3{color:#9cebd9}.stButton button{border-radius:12px}div[data-testid='stMetric']{background:#1e3044;padding:10px;border-radius:12px}</style>""",unsafe_allow_html=True)
g=game()
st.title("🧬 LIFE CODE")
st.caption("생명의 비밀과 마지막 탈출 | 예방접종 × 면역학 × 독성학 × RPG")
with st.sidebar:
    st.header("🎮 플레이어")
    st.write("이름:",g["name"] or "탄생 전")
    st.metric("🪙 코인",g["coins"])
    st.metric("❤️ 체력",g["hp"])
    st.progress(min(g["stage"],5)/5)
    st.write("챕터",g["stage"]+1)
    if st.button("🔄 처음부터 다시 시작"):
        new_game();st.rerun()
if g["notice"]:
    st.info(g["notice"])
    g["notice"]=""

# CHAPTER 1: 탄생
if g["stage"]==0:
    st.header("CHAPTER 1 · 탄생")
    st.markdown("### 👶 새로운 생명이 태어났습니다!")
    st.write("성별:",g["gender"])
    name=st.text_input("아기의 이름을 지어주세요",max_chars=12)
    if st.button("🎉 아기 탄생시키기",type="primary"):
        if not name.strip():
            st.warning("이름을 입력해야 합니다.")
        else:
            g["name"]=name.strip();g["coins"]=5
            # 한글 완성형 글자에서 초성을 계산하는 이스터에그
            initials=[]
            for ch in g["name"]:
                n=ord(ch)-0xAC00
                if 0<=n<11172:
                    initials.append("ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"[n//588])
            if any(x in ("ㅈ","ㅎ","ㅇ") for x in initials):
                coin_change(3)
                st.balloons()
            g["stage"]=1;st.rerun()

# CHAPTER 2: 예방접종 수첩
elif g["stage"]==1:
    st.header("CHAPTER 2 · 예방접종 수첩")
    i=g["vaccine_index"]
    if i>=len(VACCINES):
        st.success("예방접종 미션 완료! 유치원생으로 성장했습니다.")
        if st.button("📖 신비로운 과학책 펼치기"):
            g["stage"]=2;st.rerun()
    else:
        q=VACCINES[i]
        st.progress(i/len(VACCINES))
        st.subheader(f"성장 단계: {q['age']}")
        if g["vaccine_book"]:
            st.info("📒 예방접종 수첩을 읽고 시기별 백신을 기억하세요.")
            for v in VACCINES:
                st.write(f"**{v['age']}** — {v['answer']}")
            st.caption("학습용 요약이며 실제 접종 일정은 질병관리청 최신 표와 의료진 안내를 확인하세요.")
            if st.button("📕 수첩 덮고 문제 풀기"):
                g["vaccine_book"]=False;st.rerun()
        else:
            st.write(f"**{q['age']}에 해당하는 예방접종은?**")
            choice=st.radio("정답 선택",q["options"],key=f"vac_{i}_{g['vaccine_attempt']}")
            if st.button("정답 확인"):
                if choice==q["answer"]:
                    if g["vaccine_attempt"]==0:coin_change(2)
                    g["vaccine_index"]+=1;g["vaccine_attempt"]=0;g["vaccine_book"]=True
                    notify("정답입니다! "+q["info"]);st.rerun()
                else:
                    coin_change(-1)
                    g["vaccine_attempt"]+=1
                    g["vaccine_book"]=True
                    if g["coins"]==0:
                        g["ending"]="bad";g["stage"]=5
                        notify("코인이 모두 소진되어 성장 미션이 종료되었습니다.")
                    else:
                        notify("예방접종 시기를 놓쳤어요! 수첩을 다시 확인해 주세요.")
                    st.rerun()

# CHAPTER 3: 면역 게임과 인체 미로
elif g["stage"]==2:
    st.header("CHAPTER 3 · 보이지 않는 침입자와 생명의 방패")
    if g["immune_index"]<len(IMMUNE):
        st.subheader("🛡️ GAME 1 · 면역세포 방어전")
        i=g["immune_index"];question,answer,options=IMMUNE[i]
        st.write(f"문제 {i+1}/{len(IMMUNE)} — {question}")
        choice=st.radio("방어 방법 선택",options,key=f"immune_{i}")
        if st.button("방어 실행"):
            if choice==answer:
                if i==len(IMMUNE)-1 and g["immune_attempt"]==0:coin_change(3)
                g["immune_index"]+=1;notify("면역 방어 성공!")
            else:
                g["immune_attempt"]+=1;notify("다시 생각해 보세요. 코인은 차감되지 않습니다.")
            st.rerun()
    else:
        st.subheader("🧭 GAME 2 · 인체 미로 탈출")
        st.write("미로를 이동해 3개의 면역 체크포인트를 해결하세요.")
        render_map(BODY_MAP,g["body_pos"])
        def body_move(direction):
            g["body_pos"]=move(BODY_MAP,g["body_pos"],direction)
            st.rerun()
        controls("body_",body_move)
        st.write("완료한 체크포인트:",len(g["body_done"]),"/ 3")
        if len(g["body_done"])<3:
            idx=len(g["body_done"])
            title,question,answer,options=BODY[idx]
            # 이동 중 체크포인트 버튼을 통해 단서 확인
            if g["body_pos"]!= (1,1):
                st.markdown(f"**🔍 체크포인트: {title}**")
                choice=st.radio(question,options,key=f"body_q_{idx}")
                if st.button("체크포인트 해결"):
                    if choice==answer:
                        g["body_done"].add(idx)
                        if len(g["body_done"])==3 and not g["body_attempt"]:coin_change(3)
                        notify("체크포인트 해결!")
                    else:
                        g["body_attempt"]=True;notify("오답입니다. 다시 도전하세요.")
                    st.rerun()
        else:
            st.success("모든 체크포인트를 해결했습니다. 출구 E로 이동하세요.")
            y,x=g["body_pos"]
            if BODY_MAP[y][x]=="E":
                if st.button("📚 책 밖으로 탈출"):
                    g["stage"]=3;st.rerun()

# CHAPTER 4: 성장
elif g["stage"]==3:
    st.header("CHAPTER 4 · 과학책이 바꾼 진로")
    st.markdown("### 🧑‍🎓 유치원생 → 학생 → 독성학 연구원")
    st.write("어린 시절 읽은 과학책의 마지막 페이지에는 납(Pb), 카드뮴(Cd), 일산화탄소(CO)가 소개되어 있었습니다.")
    st.write("납은 신경계와 발달, 카드뮴은 장기 노출 시 신장, 일산화탄소는 산소 운반에 영향을 줄 수 있습니다.")
    st.write(f"{g['name']}은(는) 화학과 생명과학을 공부하고 독성학 연구원이 되었습니다.")
    if st.button("🌙 연구소 야근 시작",type="primary"):
        g["stage"]=4;st.rerun()

# CHAPTER 5: 독성학 연구소
elif g["stage"]==4:
    st.header("CHAPTER 5 · 독성학 연구소의 야근")
    if not g["outfit_chosen"]:
        st.warning("오늘 입고 갈 옷을 선택하세요.")
        outfit=st.radio("의상",["평상복","실험복","보호복"],horizontal=True)
        if st.button("의상 확정"):
            g["outfit"]=outfit;g["outfit_chosen"]=True;st.rerun()
    else:
        st.write("🚨 센서 이상! 비상 출입문이 폐쇄되었습니다.")
        st.caption("실제 유해물질 사고에서는 위험구역에 진입하지 말고 즉시 대피 및 신고해야 합니다. 체력 수치는 게임용 가상 규칙입니다.")
        st.write("선택 의상:",g["outfit"])
        with st.expander("🛒 비상 물품 보관함 (상점)"):
            shop=[("보호구 업그레이드",3),("비상 회복권",2),("부활권",5),("연구 기록 보관 케이스",2),("힌트 카드",1)]
            for item,price in shop:
                if st.button(f"{item} · {price}코인",key="shop_"+item):
                    if item in g["items"] and item not in ("비상 회복권","힌트 카드"):
                        notify("이미 보유한 아이템입니다.")
                    elif g["coins"]<price:
                        notify("코인이 부족합니다.")
                    else:
                        coin_change(-price)
                        if item=="비상 회복권":g["hp"]=min(100,g["hp"]+30)
                        elif item=="힌트 카드":notify("힌트: A, B, C 실험실에서 열쇠를 모으세요. H에는 비밀 기록이 있습니다.")
                        else:g["items"].add(item)
                    st.rerun()
        c1,c2,c3=st.columns(3)
        c1.metric("❤️ 체력",g["hp"])
        c2.metric("🔑 열쇠",f"{len(g['keys'])}/3")
        c3.metric("🪙 코인",g["coins"])
        render_map(LAB_MAP,g["lab_pos"])
        def lab_move(direction):
            old=g["lab_pos"]
            new=move(LAB_MAP,old,direction)
            g["lab_pos"]=new
            if new!=old:
                y,x=new;tile=LAB_MAP[y][x]
                if tile=="!":
                    reduction={"평상복":0,"실험복":4,"보호복":8}[g["outfit"]]
                    if "보호구 업그레이드" in g["items"]:reduction+=5
                    g["hp"]=max(0,g["hp"]-max(2,15-reduction))
                if tile=="$" and new not in g["collected"]:
                    g["collected"].add(new);coin_change(random.randint(1,2));notify("숨겨진 코인을 발견했습니다!")
            if g["hp"]<=0:
                if "부활권" in g["items"]:
                    g["items"].remove("부활권");g["hp"]=60;g["lab_pos"]=(1,1)
                    notify("부활권을 사용했습니다.")
                elif g["coins"]>=5:
                    notify("체력이 0입니다. 상점에서 부활권을 구매할 수 있습니다.")
                else:
                    g["ending"]="bad";g["stage"]=5
            st.rerun()
        if g["hp"]>0:
            controls("lab_",lab_move)
        else:
            st.error("체력이 0입니다. 부활권을 구매하세요.")
            if st.button("부활권 구매 및 사용 · 5코인"):
                if g["coins"]>=5:
                    coin_change(-5);g["hp"]=60;g["lab_pos"]=(1,1);st.rerun()
        y,x=g["lab_pos"]
        tile=LAB_MAP[y][x]
        if tile in LAB and tile not in g["keys"]:
            title,question,answer,options,color=LAB[tile]
            st.subheader(f"{color} {title}")
            choice=st.radio(question,options,key=f"lab_{tile}")
            if st.button("분석 결과 제출",key=f"submit_{tile}"):
                if choice==answer:
                    if g["lab_attempt"].get(tile,0)==0:coin_change(3)
                    g["keys"].add(tile);notify("정답! 열쇠를 획득했습니다.")
                else:
                    g["lab_attempt"][tile]=g["lab_attempt"].get(tile,0)+1
                    notify("분석이 틀렸습니다. 자료를 다시 확인하세요.")
                st.rerun()
        if tile=="H":
            st.subheader("📚 비밀 기록실")
            if "연구 기록 보관 케이스" in g["items"]:
                if st.button("연구소의 숨겨진 비밀 노트 확보"):
                    g["note"]=True;notify("비밀 연구 노트를 확보했습니다!");st.rerun()
            else:
                st.warning("노트를 안전하게 가져가려면 상점에서 보관 케이스를 구매하세요.")
        if tile=="E":
            if len(g["keys"])==3:
                if st.button("🚪 비상 출입문 열기",type="primary"):
                    g["ending"]="secret" if g["note"] else "good"
                    g["stage"]=5;st.rerun()
            else:
                st.warning(f"열쇠가 {3-len(g['keys'])}개 부족합니다.")

# CHAPTER 6: 엔딩
else:
    st.header("CHAPTER 6 · 마지막 선택의 결과")
    if g["ending"]=="secret":
        st.balloons()
        st.success("🌟 SECRET ENDING — 감춰진 진실")
        st.write("세 개의 열쇠와 숨겨진 연구 노트를 확보해 탈출했습니다.")
        st.write("연구 자료를 독립 검토기관에 제출하고 연구소의 안전 기준을 개선하는 계기가 되었습니다.")
        st.markdown("**생명을 지키는 첫걸음은 예방이었고, 그다음은 이해였으며, 마지막은 그 지식을 다른 사람을 위해 사용하는 것이었다.**")
    elif g["ending"]=="good":
        st.success("🎉 GOOD ENDING — 마지막 문을 열다")
        st.write("연구소를 탈출하고 비상 대응팀에 분석 자료를 전달했습니다.")
    else:
        st.error("💀 BAD ENDING — 끝나지 못한 연구")
        st.write("이번 도전은 여기서 끝났습니다. 다시 도전해 더 나은 선택을 해보세요.")
    st.metric("최종 코인",g["coins"])
    if st.button("🔄 새로운 인생 시작",type="primary"):
        new_game();st.rerun()
