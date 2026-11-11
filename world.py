"""책 속 세포 세계와 연구소의 이동, 충돌 및 도트 그래픽 렌더러

이 파일은 LIFE CODE 게임의 Python 모듈입니다.
게임 중 실시간 캐릭터 이동은 HTML Canvas/JavaScript로 브라우저에서만 처리합니다.
따라서 Streamlit 서버에서 CPU를 소비하는 게임 루프를 실행하지 않습니다.
"""

WORLD_JS = r'''
/* 캔버스 기반 이동·충돌·NPC 상호작용. 서버에서 반복 실행하지 않습니다. */
window.LIFE_WORLD = (() => {
  const W=24, H=14, TILE=32;
  function buildMap(scene) {
    const g=Array.from({length:H},(_,y)=>Array.from({length:W},(_,x)=>(x===0||y===0||x===W-1||y===H-1)?'#':'.'));
    function wallH(y,x1,x2,holes=[]) {for(let x=x1;x<=x2;x++)if(!holes.includes(x))g[y][x]='#';}
    function wallV(x,y1,y2,holes=[]) {for(let y=y1;y<=y2;y++)if(!holes.includes(y))g[y][x]='#';}
    if(scene==='book') {
      wallH(6,2,10,[4,9]); wallV(9,2,10,[4,8]);
      wallH(9,11,20,[12,17]); wallV(17,3,8,[5,7]);
      [[7,3],[14,2],[15,10],[3,8]].forEach(([x,y])=>g[y][x]='#');
    } else {
      wallH(6,1,21,[3,11,18]); wallV(9,1,5,[3]);
      wallV(16,7,12,[10]);
      [[6,3],[13,3],[18,8],[11,8],[19,10],[3,9]].forEach(([x,y])=>g[y][x]='!');
      // 통로 및 오브젝트 칸은 항상 지나갈 수 있게 보정
    }
    const objects=scene==='book'?LIFE_DATA.bookObjects:LIFE_DATA.labObjects;
    for(const o of objects) g[o.y][o.x]='.';
    g[2][2]='.';
    return g;
  }
  function start(scene, state, interact, danger, positionChanged) {
    const canvas=document.getElementById('gameCanvas');
    if(!canvas) return {stop(){}};
    const ctx=canvas.getContext('2d');
    canvas.width=W*TILE;canvas.height=H*TILE;
    const grid=buildMap(scene), objs=scene==='book'?LIFE_DATA.bookObjects:LIFE_DATA.labObjects;
    const pos=state.positions[scene]||{x:2.5,y:2.5};
    const p={x:pos.x,y:pos.y};
    if(!isFree(p.x,p.y)){p.x=2.5;p.y=2.5;}
    let active=true, last=performance.now(), saveElapsed=0, walk=0, lastHazard='', lastPaint=0;
    const down=new Set();
    const deco=(x,y)=>(x*17+y*31+x*y*7)%17;
    const pixel=(x,y,w,h,color)=>{ctx.fillStyle=color;ctx.fillRect(x,y,w,h)};
    const center=(x,y)=>[x*TILE+TILE/2,y*TILE+TILE/2];
    function isFree(x,y) {
      const r=.24;
      for(const xx of [x-r,x+r])for(const yy of [y-r,y+r]){
        const cx=Math.floor(xx),cy=Math.floor(yy);
        if(cx<0||cy<0||cx>=W||cy>=H||grid[cy][cx]==='#')return false;
      }
      return true;
    }
    function keys(e,pressed){
      const k=e.key.toLowerCase();
      if(['arrowleft','arrowright','arrowup','arrowdown',' ','w','a','s','d','e','shift'].includes(k))e.preventDefault();
      if(pressed)down.add(k);else down.delete(k);
      if(pressed&&!e.repeat&&(k==='e'||k===' '))attemptInteraction();
    }
    const onDown=e=>keys(e,true),onUp=e=>keys(e,false),onBlur=()=>down.clear();
    window.addEventListener('keydown',onDown);window.addEventListener('keyup',onUp);window.addEventListener('blur',onBlur);
    const buttons=document.querySelectorAll('[data-move]');
    const mobileListeners=[];
    buttons.forEach(b=>{
      const k=b.dataset.move;
      const a=e=>{e.preventDefault();if(k==='e'){attemptInteraction();return;}down.add(k);};
      const z=e=>{e.preventDefault();down.delete(k);};
      b.addEventListener('pointerdown',a);b.addEventListener('pointerup',z);
      b.addEventListener('pointerleave',z);b.addEventListener('pointercancel',z);
      mobileListeners.push([b,a,z]);
    });
    function attemptInteraction(){
      if(document.querySelector('.modal-backdrop'))return;
      const near=objs.map(o=>({o,d:Math.hypot(p.x-(o.x+.5),p.y-(o.y+.5))})).filter(z=>z.d<1.85).sort((a,b)=>a.d-b.d)[0];
      if(near)interact(near.o.id);else if(window.LIFE_UI) LIFE_UI.toast('가까운 사물이나 NPC 앞에서 E를 눌러주세요.');
    }
    function move(dt){
      if(document.querySelector('.modal-backdrop')){down.clear();return;}
      let dx=Number(down.has('arrowright')||down.has('d'))-Number(down.has('arrowleft')||down.has('a'));
      let dy=Number(down.has('arrowdown')||down.has('s'))-Number(down.has('arrowup')||down.has('w'));
      if(!dx&&!dy)return;
      const norm=Math.hypot(dx,dy);dx/=norm;dy/=norm;
      const step=Math.min(dt,.05)*(down.has('shift')?4.7:3.1);
      if(isFree(p.x+dx*step,p.y))p.x+=dx*step;
      if(isFree(p.x,p.y+dy*step))p.y+=dy*step;
      walk+=dt*12;
      const tx=Math.floor(p.x),ty=Math.floor(p.y),tile=grid[ty]?.[tx];
      const current=`${tx},${ty}`;
      if(tile==='!'&&current!==lastHazard){lastHazard=current;danger();}
      if(tile!=='!')lastHazard='';
      saveElapsed+=dt;
      if(saveElapsed>.65){positionChanged({x:p.x,y:p.y});saveElapsed=0;}
    }
    function tile(x,y,v,t){
      const px=x*TILE,py=y*TILE,shade=deco(x,y);
      if(scene==='book'){
        // 3D 게임의 숲이 아니라 책 속 환상적인 '세포 도시'를 표현합니다.
        // 세포질 같은 분홍/보랏빛 바닥, 막·소기관을 닮은 장애물
        pixel(px,py,TILE,TILE,shade%3===0?'#f4dce9':'#f8e3ed');
        pixel(px+1,py+1,30,30,shade%2===0?'#f9e6ee':'#f3dfea');
        if(v==='#'){
          pixel(px,py+14,32,18,'#b28ab9');
          pixel(px+1,py+7,30,24,'#c9a4d0');
          pixel(px+3,py+2,26,23,'#dbb9e4');
          pixel(px+6,py+3,20,16,'#e7cdec');
          pixel(px+10,py+8,12,11,'#a98bbd');
          pixel(px+13,py+10,7,7,'#f1d4f3');
          if(shade%4===0){pixel(px+5,py+4,4,4,'#fff5c9');pixel(px+24,py+11,3,3,'#ffecff');}
          return;
        }
        if(shade<5){
          pixel(px+5,py+12,3,3,'#d9b9e4');pixel(px+19,py+8,4,4,'#ffe8b8');
          pixel(px+21,py+21,3,3,'#c5a9e6');
        }else if(shade===9||shade===10){
          // 둥근 세포 소기관 / 반짝이는 미세 입자
          pixel(px+9,py+12,13,11,'#e7b6d4');
          pixel(px+12,py+9,8,16,'#f3c9df');
          pixel(px+13,py+14,6,6,'#fff5ca');
          pixel(px+20,py+12,4,4,'#b393c7');
        }else if(shade===11){
          pixel(px+8,py+11,14,5,'#b9a0df');pixel(px+11,py+8,8,12,'#d6c2f5');
          pixel(px+14,py+10,3,3,'#f6efff');
        }else if(shade===15){
          pixel(px+11,py+19,9,4,'#f3c4d4');pixel(px+9,py+15,13,4,'#fff1e6');
        }
      }else{
        // 연구소의 타일 바닥, 장비, 비상 위험 구역
        pixel(px,py,TILE,TILE,shade%2===0?'#34465e':'#3a5065');
        pixel(px+1,py+1,30,30,shade%2===0?'#506577':'#566d7c');
        pixel(px+2,py+2,27,2,'#718896');
        pixel(px+1,py+28,30,2,'#35465b');
        if(v==='#'){
          pixel(px,py,32,32,'#344558');
          pixel(px+1,py+1,30,13,'#617b8b');
          pixel(px+3,py+4,26,6,'#839da5');
          pixel(px+2,py+16,28,13,'#42576a');
          pixel(px+7,py+19,18,4,'#637c8b');
          pixel(px+28,py+4,2,25,'#283f54');
        }else if(v==='!'){
          pixel(px+2,py+2,28,28,'#a3635c');
          for(let k=0;k<4;k++){
            pixel(px+k*8,py+11,5,7,'#efc174');
            pixel(px+1+k*8,py+14,5,4,'#f5dd99');
          }
          pixel(px+9,py+21,13,3,'#ffe7aa');
        }else if(shade===5){pixel(px+11,py+16,10,2,'#668290');}
      }
    }
    function drawSprite(cx,cy,shirt='#88bee8',isPlayer=false){
      // 오리지널 2D 도트 캐릭터: 걷기 프레임 / 그림자 / 가방 / 머리카락 / 눈동자
      const walking=isPlayer&&walk%2<1;
      const wobble=walking?1:0;
      const x=Math.round(cx-13),y=Math.round(cy-22+wobble);
      // 그림자와 신발
      pixel(x+5,y+33,23,3,'#34494d45');
      pixel(x+5,y+29+(walking?1:0),9,5,'#4b4c68');
      pixel(x+18,y+29+(walking?-1:0),9,5,'#4b4c68');
      pixel(x+6,y+20,19,11,shirt);
      pixel(x+3,y+20,5,9,shirt);pixel(x+24,y+20,5,9,shirt);
      pixel(x+8,y+21,3,9,'#3d6b6e');
      pixel(x+19,y+21,3,9,'#407f84');
      pixel(x+10,y+22,12,4,'#e9eff0');
      // 머리카락 아래 피부와 반짝이는 볼
      pixel(x+8,y+4,18,17,'#e6b18b');
      pixel(x+9,y+6,16,13,'#f5cb9e');
      pixel(x+5,y+5,22,9,'#51435b');
      pixel(x+7,y+1,18,8,'#594762');
      pixel(x+10,y,13,4,'#70516a');
      pixel(x+6,y+12,4,6,'#594762');
      pixel(x+24,y+10,4,7,'#594762');
      pixel(x+12,y+13,2,3,'#272b40');pixel(x+22,y+13,2,3,'#272b40');
      pixel(x+9,y+17,3,2,'#ed9b9b');pixel(x+25,y+17,2,2,'#ed9b9b');
      pixel(x+17,y+18,3,1,'#c97e83');
      if(isPlayer){
        // 작은 크로스백: 두 세계에서 계속 가지고 다니는 모험가 가방
        pixel(x+22,y+20,5,9,'#b98659');pixel(x+21,y+22,7,6,'#d8b57b');
        pixel(x+10,y+20,2,9,'#fff2cf');
      } else {
        // NPC의 분홍색 머리 리본
        pixel(x+8,y+2,6,4,'#ff9ac1');pixel(x+13,y+4,4,3,'#fff3aa');
      }
    }
    function object(o,t){
      const [cx,cy]=center(o.x+.0,o.y+.0);
      const x=o.x*TILE,y=o.y*TILE;
      const cleared=scene==='book'?(o.id==='immune'?state.immuneDone:o.id.startsWith('cp')?state.bodyDone[Number(o.id.slice(-1))]:state.bookDone):(
        ['A','B','C'].includes(o.id)?state.keys.includes(o.id):o.id==='note'?state.note:o.id.startsWith('chest')?state.foundCoins.includes(o.id):false);
      if(o.icon==='npc'){drawSprite(cx,cy,'#e88dad');}
      else if(o.icon==='star'){
        pixel(x+8,y+6,16,21,cleared?'#8ceac1':'#fff0a6');
        pixel(x+4,y+12,24,7,cleared?'#5fb79e':'#ffc878');
        pixel(x+13,y+3,6,26,'#fff6d5');
      }else if(o.icon==='door'){
        pixel(x+4,y+2,24,30,'#7e77a5');pixel(x+7,y+4,18,26,cleared?'#8ee7a7':'#776c9e');
        pixel(x+20,y+18,3,3,'#fff2bc');
      }else if(o.icon==='shelf'){
        pixel(x+4,y+2,24,29,'#8b6b78');
        for(let j=0;j<3;j++)for(let i=0;i<4;i++)pixel(x+7+i*5,y+6+j*8,4,7,['#e7a6b5','#a6c6ff','#f8dd8d'][j]);
      }else{
        pixel(x+4,y+9,25,20,cleared?'#6a9c8c':o.color);
        pixel(x+3,y+7,27,5,'#ddedf0');pixel(x+12,y+13,8,6,'#4c5c70');
        if(o.icon==='chest')pixel(x+14,y+16,5,5,'#fff7b8');
      }
      if(!cleared){
        const pulse=Math.sin(t/360);pixel(x+14,y-8+pulse*2,4,4,'#fff4aa');
      }
      const near=Math.hypot(p.x-(o.x+.5),p.y-(o.y+.5))<1.85;
      if(near){
        ctx.font='bold 12px system-ui, sans-serif';
        const text='E · '+o.name;
        const width=Math.min(184,ctx.measureText(text).width+16);
        pixel(Math.max(2,cx-width/2),y-23,width,19,'#1d2b42');
        ctx.fillStyle='#ffffff';ctx.textAlign='center';ctx.fillText(text,cx,y-9);
      }
    }
    function draw(t){
      ctx.clearRect(0,0,canvas.width,canvas.height);
      for(let y=0;y<H;y++)for(let x=0;x<W;x++)tile(x,y,grid[y][x],t);
      // 책 속 세계의 반짝이는 공기 입자. CPU가 아닌 브라우저 Canvas에서만 렌더링.
      if(scene==='book'){
        for(let i=0;i<22;i++){
          const xx=36+(i*71)%696;
          const yy=30+(i*109)%385+Math.sin(t/840+i)*4;
          if((i%4)!==0){
            pixel(xx,yy,2,2,i%2?'#fef5bc':'#e6fff5');
            if(i%5===0){pixel(xx-2,yy+1,6,1,'#ffffff99');pixel(xx+1,yy-2,1,6,'#ffffff99');}
          }
        }
      }
      // 공간 장식과 플레이어 표시
      objs.forEach(o=>object(o,t));
      const cx=p.x*TILE,cy=p.y*TILE;
      const shirt=scene==='lab'?(state.outfit==='보호복'?'#d7e6a1':state.outfit==='실험복'?'#e9f6f6':'#92c0f4'):'#97c3ff';
      drawSprite(cx,cy,shirt,true);
      pixel(4,4,196,22,'#17283d');
      ctx.font='bold 13px system-ui, sans-serif';ctx.textAlign='left';ctx.fillStyle='#f7f6f1';
      ctx.fillText(scene==='book'?'✦ BODY WORLD · 세포 속 모험':'🧪 TOXIC LAB · 야간 연구소',12,20);
    }
    function frame(now){
      if(!active)return;
      requestAnimationFrame(frame);
      if(now-lastPaint<30)return;
      lastPaint=now;
      const dt=Math.min((now-last)/1000,.06);last=now;
      move(dt);draw(now);
    }
    requestAnimationFrame(frame);
    return {stop(){active=false;positionChanged({x:p.x,y:p.y});window.removeEventListener('keydown',onDown);window.removeEventListener('keyup',onUp);window.removeEventListener('blur',onBlur);mobileListeners.forEach(([b,a,z])=>{b.removeEventListener('pointerdown',a);for(const k of ['pointerup','pointerleave','pointercancel'])b.removeEventListener(k,z);});}};
  }
  // 별도 이미지 파일 없이 그리는 탄생/진료실 픽셀아트 씬.
  function paintInterior(id, clinic=false, age=0){
    const cv=document.getElementById(id);if(!cv)return;
    const c=cv.getContext('2d');c.imageSmoothingEnabled=false;
    c.clearRect(0,0,520,370);c.setTransform(2,0,0,2,0,0);
    const r=(x,y,w,h,col)=>{c.fillStyle=col;c.fillRect(x,y,w,h)};
    // 출생은 복숭아 빛 벽지, 진료실은 밝은 민트 빛 벽지
    r(0,0,260,185,clinic?'#eff8f5':'#fff0e9');
    for(let x=8;x<260;x+=24)for(let y=8;y<123;y+=23){
      if(clinic){r(x+9,y+4,2,7,'#d6ece7');r(x+6,y+7,8,2,'#d6ece7');}
      else {r(x+2,y+5,3,3,'#f8d5d0');r(x+13,y+9,2,2,'#f5d9af');}
    }
    r(0,123,260,62,clinic?'#c9e3df':'#e7c7ac');
    r(0,121,260,6,clinic?'#a9d2ca':'#daa88d');
    for(let y=136;y<185;y+=18)r(0,y,260,1,clinic?'#bad8d4':'#ddbaa2');
    for(let x=8;x<260;x+=26)r(x,128,1,57,clinic?'#bad8d4':'#ddbaa2');
    // 큰 창문 + 파란 하늘 + 흰 구름
    r(16,19,86,69,'#d0bbad');r(20,16,78,67,'#fffaf3');r(25,21,68,56,'#a7dbe8');
    r(27,50,64,27,'#ccece9');r(33,39,27,6,'#faffff');r(42,34,19,13,'#fff');
    r(72,31,14,6,'#fff');r(66,34,22,7,'#fff');
    r(57,21,4,55,'#fffaf6');r(24,47,69,4,'#fffaf6');
    if(!clinic){
      // 아기 모빌과 별장식
      r(166,12,3,24,'#bf9b9d');r(131,30,74,3,'#bf9b9d');
      for(const [x,l,col] of [[134,12,'#ffc99a'],[164,19,'#e4bfef'],[197,14,'#ffcfba']]){
        r(x,31,2,l,'#bf9b9d');r(x-5,31+l,12,5,col);r(x-2,28+l,6,13,col);
      }
      // 테디베어 / 낮은 장난감 수납장
      r(18,123,71,38,'#d8b194');r(20,125,67,5,'#fae5c7');
      r(25,133,23,22,'#f1d9b5');r(55,133,23,22,'#f1d9b5');
      r(34,141,5,5,'#c69b8d');r(64,141,5,5,'#c69b8d');
      r(36,107,8,8,'#d9ab7d');r(52,107,8,8,'#d9ab7d');
      r(34,112,28,19,'#e9ba8a');r(40,117,17,10,'#f8dcae');
      r(41,117,3,4,'#684f58');r(52,117,3,4,'#684f58');
      // 침대 / 베개 / 이불 / 아기 얼굴
      r(103,108,140,69,'#d29fa0');r(111,109,125,47,'#fff7df');
      r(102,153,141,14,'#dbada1');r(106,161,9,16,'#c99491');r(229,161,9,16,'#c99491');
      r(122,115,35,22,'#fffefa');r(150,116,22,20,'#f3c19e');
      r(155,112,14,7,'#8b665d');r(152,119,20,15,'#f7d0ad');
      r(157,123,2,3,'#654f59');r(167,123,2,3,'#654f59');
      r(159,129,8,2,'#d59d9e');
      r(150,135,67,21,'#efbaae');r(153,139,61,14,'#ffd3c1');
      r(210,142,4,4,'#fff6e7');r(213,137,3,11,'#fff6e7');
    } else {
      // 접종 안내 액자, 소아청소년과 의사, 아기/아이와 보호자
      r(133,18,79,61,'#d1e6dd');r(137,22,71,53,'#fffdf5');
      r(150,31,48,4,'#89bfb7');r(157,42,34,3,'#d7e3dd');
      r(149,52,50,3,'#d7e3dd');r(157,62,34,3,'#d7e3dd');
      r(111,107,74,42,'#b4d6d0');r(112,104,72,10,'#ecf7ee');
      r(116,148,5,22,'#88b4ae');r(174,148,5,22,'#88b4ae');
      r(117,93,34,12,'#eff9f1');r(120,86,29,13,'#ffdfb4');
      // 아기 · 아이를 안고 앉은 보호자
      r(21,132,40,28,'#b3d1e3');r(26,105,29,30,'#e4b389');
      r(23,99,34,13,'#6c5a61');r(25,104,6,15,'#6c5a61');
      r(35,117,3,4,'#493c4b');r(49,117,3,4,'#493c4b');
      r(41,136,25,20,'#f1c7a5');r(42,132,22,7,'#785f62');
      r(47,140,3,3,'#493c4b');r(58,140,3,3,'#493c4b');
      // 의사 - 밝은 흰 가운
      r(199,123,34,41,'#fffefa');r(199,127,5,29,'#dfedeb');
      r(205,93,26,31,'#edbd96');r(201,88,32,15,'#625462');
      r(209,108,3,4,'#494452');r(223,108,3,4,'#494452');
      r(210,126,8,10,'#92caba');r(223,127,6,17,'#a4d9cc');
      r(212,147,8,5,'#88bfb6');
    }
    c.setTransform(1,0,0,1,0,0);
  }
  function nursery(id){paintInterior(id,false)}
  function clinic(id,age){paintInterior(id,true,age)}
  function cover(id){nursery(id)}
  return {start,buildMap,cover,nursery,clinic};
})();

'''
