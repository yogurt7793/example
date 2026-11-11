import random
import streamlit as st
from game_data import BODY_MAP, LAB_MAP

def new_game():
    st.session_state.game = dict(stage=0,name="",gender=random.choice(["여아","남아"]),coins=0,hp=100,
        vaccine_index=0,vaccine_attempt=0,vaccine_book=True,immune_index=0,immune_attempt=0,
        body_pos=(1,1),body_done=set(),body_attempt=False,body_question=None,
        outfit="평상복",outfit_chosen=False,items=set(),keys=set(),lab_pos=(1,1),
        lab_attempt={},collected=set(),note=False,hidden=False,ending=None,notice="")

def game():
    if "game" not in st.session_state:
        new_game()
    return st.session_state.game

def notify(message):
    game()["notice"] = message

def coin_change(amount):
    g=game()
    g["coins"]=max(0,g["coins"]+amount)

def move(map_data,pos,direction):
    y,x=pos
    dy,dx={"위":(-1,0),"아래":(1,0),"왼쪽":(0,-1),"오른쪽":(0,1)}[direction]
    ny,nx=y+dy,x+dx
    if 0<=ny<len(map_data) and 0<=nx<len(map_data[ny]) and map_data[ny][nx]!="#":
        return (ny,nx)
    return pos

def render_map(map_data,pos):
    icons={"#":"🟫",".":"⬛","S":"⬛","E":"🚪","A":"🧪","B":"🧪","C":"🧪","H":"📚","$":"🪙","!":"☣️"}
    rows=[]
    for y,row in enumerate(map_data):
        rows.append("".join("🧑" if (y,x)==pos else icons.get(ch,"⬛") for x,ch in enumerate(row)))
    st.markdown("<div style='font-size:22px;line-height:1.55;white-space:pre;text-align:center'>"+"<br>".join(rows)+"</div>",unsafe_allow_html=True)

def controls(prefix,callback):
    a,b,c=st.columns([1,1,1])
    with b:
        if st.button("⬆️",key=prefix+"up",use_container_width=True):callback("위")
    a,b,c=st.columns(3)
    with a:
        if st.button("⬅️",key=prefix+"left",use_container_width=True):callback("왼쪽")
    with b:
        if st.button("⬇️",key=prefix+"down",use_container_width=True):callback("아래")
    with c:
        if st.button("➡️",key=prefix+"right",use_container_width=True):callback("오른쪽")
