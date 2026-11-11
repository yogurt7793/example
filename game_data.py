"""교육용 게임 문제 데이터 (예방접종·면역학·독성학)

이 파일은 LIFE CODE 게임의 Python 모듈입니다.
게임 중 실시간 캐릭터 이동은 HTML Canvas/JavaScript로 브라우저에서만 처리합니다.
따라서 Streamlit 서버에서 CPU를 소비하는 게임 루프를 실행하지 않습니다.
"""

GAME_DATA_JS = r'''
/* LIFE CODE: 게임에서 사용하는 학습 자료와 맵 설정 */
window.LIFE_DATA = {
  vaccines: [
    {age:'출생', question:'출생 직후 실시하는 대표적인 예방접종은?', options:['B형간염 1차','MMR 1차','DTaP 추가접종'], answer:0, explain:'B형간염 1차 접종은 출생 직후 권고됩니다.'},
    {age:'생후 2개월', question:'생후 2개월부터 시작되는 대표적인 기초접종의 묶음은?', options:['MMR · HPV','DTaP · IPV · Hib','MMR 추가접종만'], answer:1, explain:'DTaP, IPV, Hib 등 여러 백신의 기초접종이 시작되는 시기입니다.'},
    {age:'생후 12~15개월', question:'생후 12~15개월에 권고되는 대표적인 접종은?', options:['HPV','B형간염 출생 1차','MMR 1차'], answer:2, explain:'홍역·유행성이하선염·풍진을 예방하는 MMR 1차 접종 시기입니다.'},
    {age:'만 4~6세', question:'만 4~6세 시기의 대표적인 추가접종 묶음은?', options:['DTaP · IPV · MMR','B형간염 출생 1차만','Hib 최초 접종만'], answer:0, explain:'DTaP, IPV, MMR 등의 추가접종을 확인하는 시기입니다.'}
  ],
  immune: [
    {question:'세균 등 이물질을 포식하여 제거하는 데 관여하는 세포는?',options:['적혈구','대식세포','혈소판'],answer:1,explain:'대식세포는 선천면역에 참여하는 식세포입니다.'},
    {question:'항체를 분비하는 형질세포는 주로 어느 세포에서 분화할까요?',options:['B세포','적혈구','신경세포'],answer:0,explain:'활성화된 B세포는 형질세포와 기억 B세포 등으로 분화할 수 있습니다.'},
    {question:'예방접종을 통해 형성하려는 중요한 면역학적 특징은?',options:['혈액형 변화','항상 감염되지 않음','면역기억'],answer:2,explain:'면역기억은 이후 같은 항원에 대한 반응을 빠르게 할 수 있습니다.'}
  ],
  checkpoints: [
    {title:'피부 장벽',question:'건강한 피부의 중요한 방어 기능은?',options:['산소 운반','물리·화학적 장벽 형성','항체만 생산'],answer:1,explain:'피부는 병원체 침입을 막는 1차 방어선입니다.'},
    {title:'림프절',question:'림프절에서 관찰할 수 있는 중요한 면역 과정은?',options:['면역세포 활성화','혈액 속 산소 생성','모든 독소 즉시 파괴'],answer:0,explain:'림프절은 면역세포가 항원을 만나고 반응하는 장소입니다.'},
    {title:'면역기억',question:'예방접종 수첩이 면역기억과 연결되는 이유는?',options:['세균을 모두 없애기 때문','체온이 늘 높아지기 때문','특정 항원에 대한 기억반응 형성을 돕기 때문'],answer:2,explain:'접종은 병원체의 항원에 대한 면역학적 대비를 돕습니다.'}
  ],
  lab: {
    A:{name:'납 분석실',color:'#6fb7ff',question:'납(Pb)의 유해성을 줄이기 위한 바람직한 대책은?',options:['맨손 취급','노출원 파악과 적절한 관리','측정 기록 삭제'],answer:1,explain:'납은 신경계와 아동의 발달에 위해를 줄 수 있어 노출을 관리해야 합니다.'},
    B:{name:'카드뮴 분석실',color:'#ffd16a',question:'가상의 노출지표를 농도×시간으로 정의했습니다. 농도 2단위, 시간 3이면 지표는?',options:['5','9','6'],answer:2,explain:'2×3=6입니다. 실제 위해성 평가는 노출 경로·기간·독성 특성 등을 함께 고려합니다.'},
    C:{name:'일산화탄소 감지실',color:'#ff898d',question:'일산화탄소(CO)가 위험한 주요 이유는?',options:['헤모글로빈에 결합해 산소 운반을 방해','산소를 만들어서','항체 생성을 촉진해서'],answer:0,explain:'CO는 헤모글로빈과 결합해 산소 전달을 방해할 수 있습니다.'}
  },
  bookObjects: [
    {x:4,y:2,id:'immune',name:'면역수호자',color:'#ffa8bb',icon:'npc'},
    {x:6,y:4,id:'cp0',name:'피부 장벽',color:'#8ce2bd',icon:'star'},
    {x:12,y:5,id:'cp1',name:'림프절',color:'#8ce2bd',icon:'star'},
    {x:19,y:9,id:'cp2',name:'면역기억',color:'#8ce2bd',icon:'star'},
    {x:21,y:11,id:'bookExit',name:'책 속 출구',color:'#bcb5ff',icon:'door'}
  ],
  labObjects: [
    {x:4,y:3,id:'shop',name:'비상 보관함',color:'#fedb7a',icon:'chest'},
    {x:7,y:3,id:'A',name:'납 분석실',color:'#78bfff',icon:'desk'},
    {x:15,y:4,id:'B',name:'카드뮴 분석실',color:'#ffe18a',icon:'desk'},
    {x:20,y:9,id:'C',name:'CO 감지실',color:'#ff9b9b',icon:'desk'},
    {x:4,y:10,id:'note',name:'오래된 책장',color:'#b6a1ff',icon:'shelf'},
    {x:12,y:2,id:'chest1',name:'숨은 코인',color:'#ffe292',icon:'chest'},
    {x:10,y:10,id:'chest2',name:'숨은 코인',color:'#ffe292',icon:'chest'},
    {x:21,y:11,id:'labExit',name:'비상 출입문',color:'#a1f0d9',icon:'door'}
  ]
};

'''
