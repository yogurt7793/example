"""LIFE CODE: keyboard-controlled, self-contained 2D RPG."""
import asyncio
import random
import pygame
from world import MAPS, OBJECTS, SPAWN, TILE, can_move

W,H=800,560
GAME_H=400
BG=(19,29,43); WHITE=(239,244,245); GOLD=(255,210,96)
QUESTIONS={
 'v0':('출생 직후 접종을 시작하는 백신은?', ['B형간염','MMR','HPV'],0,'예방접종 1/4'),
 'v1':('생후 2개월에 시작하는 기초접종 조합은?', ['MMR만','DTaP·IPV·Hib','HPV만'],1,'예방접종 2/4'),
 'v2':('생후 12~15개월에 권장되는 백신 중 하나는?', ['MMR','HPV','대상포진'],0,'예방접종 3/4'),
 'v3':('만 4~6세에 추가접종하는 백신 조합은?', ['B형간염 출생 1차','DTaP·IPV·MMR','Hib 출생 1차'],1,'예방접종 4/4'),
 'immune':('침입한 병원체를 포식하는 세포는?', ['적혈구','대식세포','혈소판'],1,'면역 방어전'),
 'immune2':('항체를 분비하는 형질세포로 분화할 수 있는 세포는?', ['B세포','적혈구','혈소판'],0,'항체 퍼즐'),
 'memory':('백신의 보호 효과와 관련 깊은 현상은?', ['혈액 응고','면역기억','산소 생산'],1,'면역기억'),
 'lead':('납 노출을 줄이기 위한 적절한 조치는?', ['오염원 관리','맨손 취급','보호구 생략'],0,'납 분석실'),
 'cadmium':('가상 농도 2×노출 시간 3의 단순 지표는?', ['5','6','9'],1,'카드뮴 분석실'),
 'co':('일산화탄소가 산소 운반을 방해하는 이유는?', ['산소 생성','헤모글로빈 결합','항체 제거'],1,'CO 감지실'),
}

def font(size):
    # Korean font fallback, with local system font selection
    return pygame.font.SysFont('malgungothic,applegothic,nanumgothic,notosanscjkkr,arial',size)

def txt(surface,message,x,y,size=21,color=WHITE):
    surface.blit(font(size).render(str(message),True,color),(x,y))

def box(surface,rect,color,rad=10): pygame.draw.rect(surface,color,rect,border_radius=rad)

class Game:
    def __init__(self):
        self.reset()
    def reset(self):
        self.world='nursery'; self.x,self.y=SPAWN[self.world]
        self.coins=5;self.hp=100;self.name='새싹';self.sex=random.choice(['여아','남아'])
        self.age='신생아';self.vax=0;self.done=set();self.failed=set();self.keys=set()
        self.suit='평상복';self.upgrade=False;self.case=False;self.note=False
        self.revive=0;self.heal=0;self.hint=0;self.found_coin=False
        self.mode='name';self.msg='아기가 태어났습니다! 이름을 입력하세요.'
        self.name_entry='';self.quiz_id=None;self.ending=None;self.book=False
        self.dialog=[];self.choices=[];self.callback=None
        self.pulse=0
    def say(self,lines,choices=None,callback=None):
        self.mode='dialog';self.dialog=lines if isinstance(lines,list) else [lines]
        self.choices=choices or [];self.callback=callback
    def finish_dialog(self):
        if len(self.dialog)>1:
            self.dialog.pop(0);return
        if self.choices:return
        self.mode='walk';cb=self.callback;self.callback=None
        if cb:cb()
    def change(self,world):
        self.world=world;self.x,self.y=SPAWN[world]
    def start_quiz(self,qid):
        if qid in self.done:
            self.say('이미 해결한 미션입니다.');return
        self.quiz_id=qid;self.mode='quiz'
    def answer(self,index):
        qid=self.quiz_id
        question,options,correct,label=QUESTIONS[qid]
        if index==correct:
            first=qid not in self.failed
            reward=2 if qid.startswith('v') else 3
            if first:self.coins+=reward
            self.done.add(qid)
            if qid.startswith('v'):
                self.vax+=1
                self.age=['신생아','생후 2개월','생후 12~15개월','만 4~6세','유치원생'][self.vax]
            if qid in ('lead','cadmium','co'):self.keys.add(qid)
            self.say(('정답! ' + (f'+{reward} 코인' if first else '재도전 성공 (보상 없음)')),
                     callback=self.after_quiz)
        else:
            self.failed.add(qid)
            if qid.startswith('v'):
                self.coins-=1
                if self.coins<=0:
                    self.ending='bad';self.mode='ending';return
                self.say('예방접종 시기를 다시 확인해 주세요. 코인 -1',callback=lambda:self.start_quiz(qid))
            else:
                if self.world=='lab':
                    self.hp=max(0,self.hp-12)
                    if self.check_hp():return
                self.say('아쉽습니다. 다시 생각해 보세요!',callback=lambda:self.start_quiz(qid))
    def after_quiz(self):
        if self.world=='nursery' and self.vax>=4:
            self.say('예방접종 수첩을 완성했어요! 이제 마을로 떠나세요.',callback=lambda:self.change('village'))
        elif self.world=='body' and all(q in self.done for q in ('immune','immune2','memory')):
            self.say('면역 세계의 세 단서를 모았어요! 입구로 돌아가세요.')
    def check_hp(self):
        if self.hp>0:return False
        if self.revive>0:
            self.revive-=1;self.hp=60;self.x,self.y=SPAWN['lab']
            self.say('부활권을 사용해 입구로 돌아왔습니다.');return True
        self.mode='ending';self.ending='bad';return True
    def interact(self):
        for (ox,oy),(kind,label) in OBJECTS[self.world].items():
            if abs(self.x-ox)+abs(self.y-oy)>1:continue
            self.activate(kind);return
        self.say('주변에 조사할 물건이 없습니다. 가까이 다가가세요.')
    def activate(self,kind):
        if kind=='crib':self.say(f'{self.name}의 첫 번째 방입니다. 생명의 모험이 시작됩니다!')
        elif kind=='nurse':
            if self.vax<4:self.start_quiz('v'+str(self.vax))
            else:self.say('예방접종 수첩 완료!')
        elif kind=='door':
            if self.world=='nursery':
                if self.vax<4:self.say('예방접종 미션을 모두 완료해야 나갈 수 있습니다.')
                else:self.change('village')
            elif self.world=='village':
                if not self.book:self.say('먼저 집에 있는 신비로운 과학책을 읽어보세요.')
                else:self.change('body')
            elif self.world=='body':
                if not all(q in self.done for q in ('immune','immune2','memory')):
                    self.say('면역 세계의 세 가지 미션을 먼저 해결하세요.')
                else:
                    self.age='성인 연구원'
                    self.say('세월이 흘렀습니다. 당신은 독성학 연구원이 되었습니다.',
                             callback=lambda:self.change('lab'))
            else:self.say('시설 폐쇄 중입니다. 비상 출입문을 찾아야 합니다.')
        elif kind=='book':
            self.book=True
            self.say(['『보이지 않는 침입자와 생명의 방패』를 펼쳤습니다.',
                      '납은 신경계, 카드뮴은 신장, CO는 산소 운반에 영향을 줄 수 있습니다.',
                      '책 속으로 들어갈 수 있게 되었습니다!'])
        elif kind=='mentor':self.say('선생님: 책 속 세계에서 면역세포를 만나 보렴!')
        elif kind in ('immune','immune2','memory','lead','cadmium','co'):
            self.start_quiz(kind)
        elif kind=='shop':self.open_shop()
        elif kind=='secret':
            if self.case:
                self.note=True;self.say('숨겨진 연구 기록을 안전하게 확보했습니다!')
            else:self.say('비밀 연구 기록 발견! 보관 케이스(2코인)가 필요합니다.')
        elif kind=='exit':
            if len(self.keys)<3:self.say(f'열쇠 {len(self.keys)}/3. 분석실을 모두 해결하세요.')
            else:
                self.ending='secret' if self.note else 'good';self.mode='ending'
    def open_shop(self):
        self.mode='shop'
    def buy(self,index):
        items=[('보호구 업그레이드',3),('회복권 +30',2),('부활권',5),('기록 보관 케이스',2),('힌트 카드',1)]
        if index>=len(items):return
        label,price=items[index]
        if self.coins<price:self.say('코인이 부족합니다.');return
        if index==0 and self.upgrade:self.say('이미 업그레이드했습니다.');return
        if index==3 and self.case:self.say('이미 보관 케이스를 구매했습니다.');return
        self.coins-=price
        if index==0:self.upgrade=True
        elif index==1:self.hp=min(100,self.hp+30)
        elif index==2:self.revive+=1
        elif index==3:self.case=True
        else:self.hint+=1
        self.say(label+' 구매 완료!')
    def move(self,dx,dy):
        nx,ny=self.x+dx,self.y+dy
        if not can_move(self.world,nx,ny):return
        # Interactable objects occupy a tile: approach from adjacent tiles.
        if (nx,ny) in OBJECTS[self.world]:return
        self.x,self.y=nx,ny
        if self.world=='lab':
            # Imaginary hazard: occasional damage in lab corridors.
            if (nx+ny)%7==0:
                damage=3 if self.upgrade or self.suit=='보호복' else 9
                self.hp=max(0,self.hp-damage)
                self.check_hp()
            if not self.found_coin and (nx,ny)==(9,7):
                self.found_coin=True;self.coins+=2
                self.say('숨겨진 코인 2개를 발견했습니다!')
    def event(self,event):
        if event.type!=pygame.KEYDOWN:return
        k=event.key
        if self.mode=='name':
            if k==pygame.K_RETURN:
                name=self.name_entry.strip()
                if not name:self.msg='이름을 한 글자 이상 입력하세요.';return
                self.name=name[:12]
                # Korean Hangul initial consonant check
                initials=[]
                for ch in self.name:
                    n=ord(ch)-0xAC00
                    if 0<=n<11172:initials.append(n//588)
                if any(i in (11,12,18) for i in initials):self.coins+=3
                self.say(f'{self.name} ({self.sex}) 탄생! 예방접종 간호사를 만나세요.')
            elif k==pygame.K_BACKSPACE:self.name_entry=self.name_entry[:-1]
            elif event.unicode and event.unicode.isprintable() and len(self.name_entry)<12:
                self.name_entry+=event.unicode
        elif self.mode=='dialog':
            if k in (pygame.K_RETURN,pygame.K_SPACE,pygame.K_e):self.finish_dialog()
        elif self.mode=='quiz':
            if k in (pygame.K_1,pygame.K_2,pygame.K_3):self.answer(k-pygame.K_1)
        elif self.mode=='shop':
            if k==pygame.K_ESCAPE:self.mode='walk'
            elif pygame.K_1<=k<=pygame.K_5:self.buy(k-pygame.K_1)
        elif self.mode=='ending':
            if k==pygame.K_r:self.reset()
        elif self.mode=='walk':
            if k in (pygame.K_e,pygame.K_SPACE):self.interact()
            elif k in (pygame.K_UP,pygame.K_w):self.move(0,-1)
            elif k in (pygame.K_DOWN,pygame.K_s):self.move(0,1)
            elif k in (pygame.K_LEFT,pygame.K_a):self.move(-1,0)
            elif k in (pygame.K_RIGHT,pygame.K_d):self.move(1,0)
    def draw_tile(self,s,xx,yy,ch):
        x,y=xx*TILE,yy*TILE
        indoor=self.world in ('nursery','lab')
        ground=(79,112,123) if indoor else (109,174,122)
        box(s,(x,y,TILE,TILE),ground,0)
        pygame.draw.rect(s,(0,0,0,20),(x,y,TILE,TILE),1)
        if ch=='#':
            c=(53,76,98) if indoor else (53,112,83)
            box(s,(x,y,TILE,TILE),c,0)
            pygame.draw.line(s,(98,134,143),(x,y+TILE-4),(x+TILE,y+TILE-4),3)
        elif not indoor and (xx*13+yy*7)%9==0:
            pygame.draw.circle(s,(210,225,130),(x+11,y+18),3)
    def draw_object(self,s,x,y,kind):
        px,py=x*TILE,y*TILE
        colors={'crib':(243,184,198),'nurse':(236,241,249),'door':(209,149,91),
                'book':(154,100,202),'mentor':(244,201,98),'immune':(241,157,104),
                'immune2':(118,189,255),'memory':(233,144,219),
                'lead':(95,165,255),'cadmium':(248,211,84),'co':(246,111,104),
                'shop':(123,221,173),'secret':(172,126,95),'exit':(129,245,173)}
        c=colors.get(kind,WHITE)
        box(s,(px+5,py+8,30,27),(31,48,64),5)
        box(s,(px+8,py+4,24,26),c,5)
        pygame.draw.rect(s,(24,38,51),(px+12,py+11,5,5))
        pygame.draw.rect(s,(24,38,51),(px+23,py+11,5,5))
    def draw_player(self,s):
        px,py=self.x*TILE,self.y*TILE
        pygame.draw.ellipse(s,(41,72,67),(px+7,py+30,27,7))
        body=(239,241,246) if self.world=='lab' else (255,188,110)
        box(s,(px+10,py+16,21,18),body,4)
        box(s,(px+9,py+4,23,20),(255,218,179),7)
        box(s,(px+8,py+2,25,8),(85,57,55),4)
        for ex in (15,25):pygame.draw.rect(s,(40,46,54),(px+ex,py+14,3,3))
        pygame.draw.rect(s,(48,56,69),(px+13,py+33,5,5))
        pygame.draw.rect(s,(48,56,69),(px+24,py+33,5,5))
    def draw(self,s):
        s.fill(BG)
        for y,row in enumerate(MAPS[self.world]):
            for x,ch in enumerate(row):self.draw_tile(s,x,y,ch)
        for (x,y),(kind,label) in OBJECTS[self.world].items():self.draw_object(s,x,y,kind)
        self.draw_player(s)
        box(s,(0,400,800,160),(19,29,43),0)
        world_names={'nursery':'CHAPTER 1 · 탄생','village':'CHAPTER 2 · 마을',
                     'body':'CHAPTER 2 · 면역 세계','lab':'CHAPTER 4 · 독성학 연구소'}
        txt(s,world_names[self.world],18,409,23,(151,239,220))
        txt(s,f'이름: {self.name}  |  성장: {self.age}',18,445,18)
        txt(s,f'🪙 {self.coins}   ♥ {self.hp}   🔑 {len(self.keys)}/3',18,478,21,GOLD)
        txt(s,'이동: 방향키/WASD     조사: E/Space     선택: 숫자키',18,521,17,(169,190,204))
        if self.mode!='walk':self.overlay(s)
    def overlay(self,s):
        layer=pygame.Surface((W,H),pygame.SRCALPHA)
        layer.fill((5,12,23,205));s.blit(layer,(0,0))
        box(s,(70,120,660,330),(36,56,74),18)
        pygame.draw.rect(s,(119,203,184),(70,120,660,330),3,border_radius=18)
        if self.mode=='name':
            txt(s,'LIFE CODE',245,150,42,(159,244,223))
            txt(s,'생명의 비밀과 마지막 탈출',225,207,22)
            txt(s,'아기의 이름을 입력하세요:',170,270,23)
            box(s,(170,307,460,52),(19,33,48))
            txt(s,self.name_entry+'|',186,318,25)
            txt(s,'Enter: 시작',323,388,21,GOLD)
        elif self.mode=='dialog':
            txt(s,'STORY / DIALOGUE',102,147,25,(164,236,219))
            for i,line in enumerate(self.wrap(self.dialog[0],33)):
                txt(s,line,102,210+i*35,23)
            txt(s,'Enter / E: 계속',510,398,18,GOLD)
        elif self.mode=='quiz':
            question,options,correct,label=QUESTIONS[self.quiz_id]
            txt(s,label,102,147,26,(164,236,219))
            for i,line in enumerate(self.wrap(question,35)):txt(s,line,102,191+i*29,21)
            for i,opt in enumerate(options):txt(s,f'{i+1}. {opt}',120,274+i*43,20,GOLD)
        elif self.mode=='shop':
            txt(s,'비상 물품 보관함',102,147,26,(164,236,219))
            for i,item in enumerate(['보호구 업그레이드 - 3','회복권 +30 - 2','부활권 - 5',
                                      '기록 보관 케이스 - 2','힌트 카드 - 1']):
                txt(s,f'{i+1}. {item}',115,192+i*39,20)
            txt(s,'1~5 구매 / ESC 닫기',410,402,18,GOLD)
        elif self.mode=='ending':
            heading={'bad':'BAD ENDING','good':'GOOD ENDING','secret':'SECRET ENDING'}[self.ending]
            txt(s,heading,213,158,37,GOLD)
            lines={'bad':['연구가 중단되었습니다.','다시 도전해 생명을 지키는 지식을 모아보세요.'],
                   'good':['세 개의 열쇠로 연구소를 탈출했습니다!','분석 자료가 안전관리팀에 전달되었습니다.'],
                   'secret':['감춰진 연구 기록을 확보했습니다!','독립적인 재검증으로 안전 기준이 개선됩니다.',
                             '예방, 이해, 그리고 지식의 실천.']}[self.ending]
            for i,line in enumerate(lines):txt(s,line,130,247+i*37,21)
            txt(s,'R: 처음부터 다시 시작',260,402,20,GOLD)
    @staticmethod
    def wrap(text,n):
        return [text[i:i+n] for i in range(0,len(text),n)] or ['']

async def main():
    pygame.init()
    pygame.display.set_caption('LIFE CODE — 생명의 비밀과 마지막 탈출')
    screen=pygame.display.set_mode((W,H))
    clock=pygame.time.Clock();game=Game();running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:running=False
            game.event(event)
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
    pygame.quit()

if __name__=='__main__':
    asyncio.run(main())
