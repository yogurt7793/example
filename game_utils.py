"""게임 화면 디자인 및 게임 흐름 담당 모듈.

JavaScript와 CSS를 별도 파일로 관리하지 않고 Python 문자열에 포함했습니다.
모든 이동·애니메이션은 브라우저에서 처리되어 Streamlit CPU 사용량을 줄입니다.
"""

GAME_CSS = r'''
/* LIFE CODE premium · warm cozy pixel-RPG interface */
:root{--bg:#f8f5ee;--ink:#30434a;--muted:#6c7e82;--paper:#fffefb;--mint:#bfead6;--green:#448a72;--deep:#2e6e62;--rose:#ffd1cd;--gold:#f7d889;--line:#d5e2d7;--shadow:#d7e0d6;--dark:#244d4f}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;min-height:100vh;color:var(--ink);font-family:'Trebuchet MS','Apple SD Gothic Neo','Malgun Gothic',system-ui,sans-serif;background:radial-gradient(circle at 0% 15%,#e1f5d980 0,transparent 26%),radial-gradient(circle at 97% 46%,#ffddd870 0,transparent 29%),linear-gradient(180deg,#f9f8f1,#f5f8f0)}
body:before{content:"✿       ·       ✧       ·       ✿";position:absolute;top:90px;right:4%;font-size:28px;color:#ddede1;pointer-events:none;letter-spacing:18px}
a{text-decoration:none;color:inherit}button,input{font:inherit}button{cursor:pointer;transition:transform .16s,background .16s,box-shadow .16s}button:disabled{cursor:not-allowed;opacity:.48}button:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid #efb56f;outline-offset:3px}
.shell{max-width:1140px;width:min(96%,1140px);margin:auto;padding:16px 0 38px;position:relative}.topbar{border:2px solid #c8ddcd;background:#fffefaed;border-radius:21px;padding:16px 24px;display:flex;align-items:center;justify-content:space-between;gap:12px;box-shadow:0 6px 0 #d8e5d9;margin:14px 0 18px}.brand{font-weight:1000;letter-spacing:1px;color:#397f71;font-size:clamp(22px,3vw,29px)}.brand strong{color:#e39393}.status-bar{display:flex;gap:10px;flex-wrap:wrap}.status-bar span{background:#f1f8ee;border:1.5px solid #dce9da;color:#3d6461;border-radius:40px;padding:8px 12px;font-weight:750;font-size:14px}.status-bar b{color:#3b7c6d}
.progress-nav{display:flex;gap:8px;overflow-x:auto;scrollbar-width:thin;padding:6px 0 10px}.nav-item{white-space:nowrap;border:1.5px solid #e0e6dd;background:#fffdf9;color:#668079;border-radius:20px;padding:10px 14px;font-size:13px;font-weight:800;transition:.18s}.nav-item:hover{transform:translateY(-2px)}.nav-item.selected{border-color:#76bf9e;background:#daf4e7;color:#397760;box-shadow:0 3px 0 #b1dac3}.nav-item.locked{opacity:.48;background:#eeeee9}
.page-heading{padding:29px 11px 21px;text-align:center}.eyebrow{color:#d48b84;font-weight:900;font-size:12px;letter-spacing:2px}.page-heading h1{font-size:clamp(27px,4.2vw,45px);line-height:1.22;margin:10px 0 9px;color:#3a7e69;font-weight:1000;letter-spacing:-1.4px}.page-heading p{margin:0;color:#758b85;font-size:15px}.panel{background:var(--paper);border:2px solid #dbe5d9;border-bottom:6px solid #d0ddd2;border-radius:22px;padding:26px;margin:8px 0 22px;box-shadow:0 10px 29px #9eb3aa22}.panel h2,.panel h3{color:#377b6a;margin:0 0 14px;font-weight:950}.panel h2{font-size:23px}.panel h3{font-size:17px}.panel p{line-height:1.83;color:#647974}.center{text-align:center}.small-note{background:#f3f8f2;color:#647c75!important;border-radius:14px;padding:15px;font-size:12px!important;line-height:1.7}.caption,.hint{font-size:12px!important;line-height:1.75!important;color:#79938b!important}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:46px;vertical-align:middle;background:#64ab8b;border:2px solid #4c907b;border-bottom:5px solid #3b7769;color:#fff;border-radius:15px;padding:11px 19px;font-weight:900;box-shadow:0 4px 13px #70ab8a30;margin:5px 6px 5px 0}.btn:hover:not(:disabled){transform:translateY(-2px);background:#4f997f}.btn:active{transform:translateY(2px)}.btn.secondary{background:#fffaf5;color:#648377;border-color:#d5e3d7;border-bottom-color:#b7cebd}.btn.secondary:hover{background:#f2f7ee}.btn.choice{background:#f5faf5;color:#3c6f60;border-color:#dbebdd;border-bottom-color:#cce4d1;text-align:left;display:block;width:100%;padding:16px 18px}.btn.choice:hover{background:#e0f3e9}.button-row{display:flex;gap:7px;flex-wrap:wrap}.tag{display:inline-block;color:#c07d6d;background:#fff1e9;border:1px solid #f5ddcb;border-radius:30px;padding:8px 14px;font-weight:900;font-size:12px}.question{font-size:21px!important;font-weight:900;color:#3d6459!important;line-height:1.6!important}.choices{display:grid;gap:7px;margin:20px 0}
.hero{display:grid;grid-template-columns:1fr 1.02fr;align-items:center;gap:35px;background:linear-gradient(140deg,#fffef9,#f4f9f1);border:2px solid #dbe9d9;border-bottom:8px solid #caddcb;border-radius:28px;padding:32px;box-shadow:0 18px 40px #9cbaa423}.hero h2{font-size:clamp(25px,3.5vw,35px);line-height:1.4;margin:12px 0;color:#376c60}.hero p{color:#647a75;line-height:1.9;font-size:15px}.hero-art{border:8px solid #fff9e8;background:#daf1df;box-shadow:0 0 0 2px #cae0cb,0 12px 18px #7fa58e30;border-radius:20px;overflow:hidden;text-align:center}.hero-art canvas{width:100%;display:block;height:auto;image-rendering:pixelated;aspect-ratio:520/370}.hero-art-caption{font-size:12px;font-weight:900;padding:11px 0;color:#577e6c;background:#f8ffe8;letter-spacing:.3px}.pixel-stars,.hero-character{display:none}.feature-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:15px;margin:18px 0}.feature-grid .panel{margin:0;padding:23px;transition:transform .2s}.feature-grid .panel:hover{transform:translateY(-3px)}.feature-grid .panel:nth-child(2){border-color:#dbefd9}.feature-grid .panel:nth-child(3){border-color:#f0ddda}
.two-column{display:grid;grid-template-columns:1fr 1fr;gap:20px}.nursery{min-height:345px;background:radial-gradient(circle at 50% 25%,#f9ffe8 2%,transparent 34%),repeating-linear-gradient(90deg,#eef8e6,#eef8e6 32px,#e7f2e1 32px,#e7f2e1 64px);text-align:center;padding:20px}.baby-garland{color:#eeb2aa;font-weight:900;letter-spacing:12px}.baby-stars{font-size:25px;margin:18px 0}.nursery .caption{color:#65856d!important}.window-pixel{margin:15px auto 15px;border:9px solid #fffdfa;border-bottom:13px solid #f0dfb8;box-shadow:0 4px 0 #d1e5db;background:linear-gradient(#95d9f3,#d1f1ff);border-radius:13px;width:120px;height:95px;font-size:43px;padding:7px}.crib{width:190px;margin:10px auto 0;background:#f8d9b8;border:10px solid #d4a28e;border-bottom:20px solid #c89c83;border-radius:17px;padding:20px;box-shadow:0 8px 0 #b5caaa}.baby{font-size:60px}.label{display:block;font-weight:900;color:#66867e;margin:18px 0 6px}.input{width:100%;padding:16px;border:2px solid #c9ded1;background:#f8fcf6;border-radius:13px;outline:0;color:#35574d;font-size:17px;margin:6px 0}.input:focus{border-color:#75be9e}
.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse}th,td{padding:15px;border-bottom:1px solid #e3e9dc;text-align:left;font-size:14px}th{background:#e9f5e8;color:#467f6d}tr.highlight{background:#fdf4db;font-weight:900}.progress-track{border-radius:30px;height:15px;overflow:hidden;background:#e7e9de;margin:0 0 25px}.progress-track>div{height:100%;border-radius:30px;background:linear-gradient(90deg,#f7cc84,#80c7a5);transition:width .5s}
.scene-story{background:linear-gradient(100deg,#e6f7e9,#fff8e2);border:1px solid #d1e8c9;border-left:6px solid #83be90;color:#547b69;line-height:1.9;padding:17px 25px;border-radius:17px;margin:7px 0 21px;font-size:14px}.rpg-layout{display:grid;grid-template-columns:minmax(0,1fr) 256px;gap:16px;align-items:start}.game-frame{min-width:0;padding:10px;border:2px solid #d7e9d1;background:#fffefb;border-bottom:6px solid #c6dfcd;border-radius:21px;box-shadow:0 12px 31px #bacfba30}.world-banner{padding:9px 13px;background:#f0f8e9;border-radius:11px;margin:1px 0 10px;display:flex;gap:9px;align-items:center;color:#557d65;font-size:11px;flex-wrap:wrap}.world-banner strong{letter-spacing:1px;font-size:10px}.world-banner-dot{background:#83ce96;width:8px;height:8px;border-radius:50%;box-shadow:0 0 0 4px #d9edda}.game-frame canvas{width:100%;height:auto;image-rendering:pixelated;border:5px solid #e6f2df;border-radius:13px;outline:none;aspect-ratio:768/448;display:block;cursor:crosshair;box-shadow:0 4px 0 #cbdfc8}.game-frame canvas:focus{border-color:#f5dc90}.quest-panel{margin:0;padding:21px}.quest-panel h2{font-size:20px}.quest{padding:11px 0;border-bottom:1px dashed #d7e3d9;font-size:13px;color:#5d7e71;font-weight:800}.quest-panel hr{border:0;border-top:1px solid #e0eadc;margin:19px 0}.quest-panel p{font-size:13px}.game-controls{display:flex;justify-content:center;gap:50px;align-items:center;margin:17px 0 8px}.game-controls button{background:#ecf6e7;color:#397364;border:2px solid #b9d7bf;border-bottom:5px solid #a4c5b0;min-width:54px;min-height:45px;border-radius:13px;touch-action:none;user-select:none;font-weight:950;font-size:19px;box-shadow:0 2px 7px #b4ccae20}.game-controls button:active{background:#caead8;transform:translateY(2px)}.horizontal-control{display:flex;gap:7px;margin-top:7px}.game-controls>div{text-align:center}.game-controls .interact-button{background:#ffd8b9;border-color:#e7b995;border-bottom-color:#d9ab86;color:#835b51;height:66px;min-width:88px;font-size:16px;line-height:1.2}
.story-panel{max-width:790px;text-align:center;padding:44px 38px;margin:auto}.storybook{font-size:clamp(28px,5vw,60px);background:#eff9ea;padding:24px;border-radius:18px;margin-bottom:25px}.storybook span{color:#80bb9a}.outfit-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.outfit-grid .panel{margin:0}.outfit-icon{font-size:77px;background:#eff9ea;padding:23px 0;border-radius:18px;margin-bottom:19px}.ending-panel{max-width:820px;margin:auto;text-align:center;padding:35px}.ending-art{font-size:90px}.ending-panel blockquote{background:#fff7e3;border:2px solid #f0e2c7;border-radius:20px;padding:23px;font-size:20px;line-height:1.8;color:#98704f;font-weight:850;margin:21px 0}.ending-panel .button-row{justify-content:center}.record{display:flex;justify-content:center;gap:9px;flex-wrap:wrap;margin:23px 0}.record span{background:#eff8ec;color:#53816a;border-radius:40px;padding:10px;font-size:13px;font-weight:800}.footer{text-align:center;color:#a0ada4;font-size:12px;margin:45px 0 10px}
.modal-backdrop{position:fixed;inset:0;background:#1e3c33a8;backdrop-filter:blur(7px);z-index:1000;display:grid;place-items:center;padding:18px}.modal-box{width:min(575px,100%);max-height:91vh;overflow:auto;background:linear-gradient(#fffff9,#f8fbf2);border:4px solid #fff;border-bottom:10px solid #b5d8bf;border-radius:25px;padding:28px;box-shadow:0 20px 75px #24443d70;outline:3px solid #b5d6ba}.modal-box h2{margin:0 0 14px;color:#3e7d69;font-size:24px}.modal-content{line-height:1.85;color:#657971}.modal-actions{display:grid;gap:8px;margin-top:20px}.modal-actions .btn{width:100%;margin:0;text-align:left}.shop-list{display:grid;gap:11px}.shop-list button{background:#f4faf1;border:2px solid #d7e7d4;border-bottom:4px solid #c5deca;padding:13px 15px;text-align:left;border-radius:13px;color:#3e7061}.shop-list button strong,.shop-list button small,.shop-list button em{display:block}.shop-list button small{color:#748b7d;margin-top:5px}.shop-list button em{color:#c68c74}.toast{position:fixed;left:50%;bottom:24px;transform:translate(-50%,25px);opacity:0;pointer-events:none;background:#467e69;color:#fff;padding:13px 20px;border-radius:40px;font-weight:900;font-size:13px;max-width:90%;text-align:center;z-index:2000;box-shadow:0 9px 28px #47695a50;transition:.25s}.toast.show{opacity:1;transform:translate(-50%,0)}
@media(max-width:850px){.shell{width:97%}.hero{grid-template-columns:1fr;padding:21px;gap:24px}.hero-art{max-width:500px;margin:auto}.rpg-layout{grid-template-columns:1fr}.quest-panel{margin-top:0}.two-column{grid-template-columns:1fr}.feature-grid{grid-template-columns:1fr}.topbar{flex-wrap:wrap}.page-heading{padding:20px 8px}.outfit-grid{grid-template-columns:1fr}.game-controls{gap:27px}.panel{padding:19px}}
@media(max-width:470px){.topbar{padding:13px}.status-bar span{font-size:12px;padding:7px 9px}.page-heading h1{font-size:26px}.brand{font-size:21px}.hero{padding:12px}.game-frame{padding:5px}.game-controls button{min-width:43px;min-height:41px}.game-controls .interact-button{min-width:72px}.panel{border-radius:17px}.scene-story{padding:15px}}

/* 캐릭터 탐험 화면을 더 선명하게 구분하고 모바일에서 조작 영역을 고정적으로 확보 */
.game-frame{background:linear-gradient(#fffefb,#f9fcf4)}
.game-frame canvas{touch-action:manipulation;image-rendering:pixelated}
.game-controls button:hover{filter:brightness(.97)}
.quest-panel .quest{line-height:1.5}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;transition:none!important;animation:none!important}}


/* LIFE CODE original identity: 성장 앨범 + 포근한 방 + 진료실 + 미시적인 몸속 세계 */
:root {--ink:#534c60;--muted:#807b8e;--paper:#fffdf9;--mint:#bfead6;--green:#8c719b;--deep:#695681;--line:#e9dce3;--shadow:#e8d8de}
body{background:linear-gradient(135deg,#fff6ef 0%,#fff9f4 47%,#f9f0fc 100%);color:var(--ink);transition:background .4s}
body::before{content:none}
body.chapter-growth{background:radial-gradient(circle at 15% 10%,#e0f9f4,transparent 40%),#f6fcf9}
body.chapter-book{background:radial-gradient(circle at 8% 20%,#f4d6f5,transparent 45%),radial-gradient(circle at 93% 60%,#fff0de,transparent 40%),#fff9ff}
body.chapter-lab{background:linear-gradient(145deg,#e5e8f2,#d4dbe5)}
body.chapter-story{background:#fff8f0}
.shell{max-width:1240px}
.story-topbar{background:#fffefa;border:0;border-radius:0 0 25px 25px;box-shadow:0 5px 27px #998b9821;padding:15px 26px;margin:0}
.story-topbar .brand{letter-spacing:-.8px;color:#6b567b;font-size:25px}.story-topbar .brand strong{color:#e5a095}.story-topbar .brand-mark{font-size:26px;color:#e1a4b2}
.story-topbar .brand small{font-size:9px;display:block;letter-spacing:2px;margin-left:33px;color:#b3a0b7}
.status-bar span{background:#f7f0f7;color:#796885;border:1px solid #ebe0ed;font-size:12px}
.status-bar b{color:#68557a}
.chapter-spine{margin:18px 0 3px;display:flex;align-items:center;gap:20px}.chapter-spine>span{white-space:nowrap;color:#9a839e;font-size:12px;font-weight:900}
.progress-nav{padding:8px 0 12px;gap:6px;flex:1}.nav-item{font-size:12px;position:relative;border:0;background:transparent;color:#93859a;border-radius:0;padding:12px 14px;border-bottom:3px solid #eadfea}
.nav-item.selected{color:#785c8e;background:#faedf6;box-shadow:none;border-bottom:3px solid #c190b3}.nav-item.locked{background:transparent;opacity:.48}
.page-heading h1{color:#745c80;letter-spacing:-1px}.eyebrow{color:#c396a7}.page-heading{padding:23px 9px 25px}.page-heading p{color:#968396}
.panel{border:1px solid #efe4eb;border-bottom:4px solid #e5d7e4;box-shadow:0 8px 25px #b09bba1e}
.panel h2,.panel h3{color:#79618c}.btn{background:#916f9c;border-color:#84628f;border-bottom-color:#674e73;box-shadow:none}.btn:hover:not(:disabled){background:#785a88}
.btn.secondary{background:#fffefa;color:#826b8e;border-color:#e7dce7;border-bottom-color:#cbb7d3}.btn.choice{background:#fffdfa;color:#63586b;border-color:#ede1ea;border-bottom-color:#e6d6e4}.btn.choice:hover{background:#f5eef9}
.life-cover{display:grid;grid-template-columns:1.05fr 1fr;gap:0;align-items:stretch;border-radius:28px;background:#fffdfb;overflow:hidden;border:8px solid #fff;box-shadow:0 16px 45px #b6a3ae37;margin-bottom:26px}
.life-cover-art{position:relative;background:#ffede1;display:flex;align-items:center;justify-content:center;min-height:355px}.life-cover-art canvas{width:100%;aspect-ratio:520/370;image-rendering:pixelated}
.cover-sticker{position:absolute;bottom:18px;left:20px;padding:9px 15px;background:#fff6fc;color:#997b9e;font-size:12px;font-weight:900;border-radius:10px;box-shadow:0 3px 0 #ebcbdc}
.cover-copy{padding:42px 37px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start}.intro-line{font-size:11px;letter-spacing:2px;color:#d499a5;font-weight:950}
.cover-copy h2{font-size:clamp(28px,3.7vw,45px);line-height:1.4;color:#695b6f;margin:19px 0}.cover-copy h2 em{font-style:normal;background:linear-gradient(transparent 65%,#ffe7bc 0)}
.cover-copy p{line-height:1.9;color:#89808d;font-size:15px}.cover-postit{font-size:12px;color:#9e8998;padding:12px 13px;background:#fff8eb;border-left:4px solid #edcba5;margin-top:25px;line-height:1.6}
.life-route{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.life-route>div{background:#fffdfa;border:1px solid #f0e3e4;border-radius:18px;padding:22px;display:flex;flex-direction:column;gap:6px;box-shadow:0 4px 0 #f0e6e8}.life-route>div:nth-child(2){background:#fbf3fc}.life-route>div:nth-child(3){background:#f5f5fb}
.life-route span{font-size:12px;color:#db9db5;font-weight:950}.life-route b{color:#665c75;font-size:17px}.life-route small{color:#93889a;font-size:13px}
.birth-story{display:grid;grid-template-columns:1.15fr 1fr;gap:20px;align-items:stretch;margin:4px 0 25px}
.birth-illustration{background:#fff0e9;border:8px solid #fffdfb;border-radius:23px;box-shadow:0 11px 30px #d0a9a42d;position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:center}
.birth-illustration canvas{width:100%;height:auto;aspect-ratio:520/370;image-rendering:pixelated}.scene-label{position:absolute;top:20px;left:20px;background:#fff9f4dc;padding:9px 13px;border-radius:8px;font-size:11px;letter-spacing:1px;color:#a4898f;font-weight:900}.scene-bottom{text-align:center;padding:15px;background:#fffaf6;color:#aa838d;font-weight:900}
.birth-paper{position:relative;background:repeating-linear-gradient(#fffdfb,#fffdfb 39px,#f8ebed 40px);border:2px solid #f0e0e0;border-radius:23px;padding:35px 29px;box-shadow:0 9px 0 #efdce1;display:flex;flex-direction:column;justify-content:center}.paper-tape{font-size:12px;color:#c18d9f;text-align:center;font-weight:900;letter-spacing:1px}
.baby-symbol{font-size:50px;color:#e4a4b6;text-align:center;margin:10px}.birth-paper h2{text-align:center;color:#6e5c75;font-size:28px;margin:7px 0}.birth-paper p{line-height:1.9;color:#928390;text-align:center}.birth-paper .label{color:#806b84}.birth-paper .input{background:#fffdfa;border-color:#f0d9e3}
.visit-top{display:flex;align-items:center;justify-content:space-between;padding:16px 22px;margin-bottom:14px;background:#fff;box-shadow:0 4px 14px #94c6bf18;border-radius:17px}.visit-top>div:first-child{display:flex;gap:16px;align-items:center}.visit-top span{font-size:12px;color:#83a9a4;font-weight:900}.visit-top b{color:#4f8178}.age-segments{display:flex;gap:8px}.age-segments i{width:35px;height:8px;background:#e2eee9;border-radius:20px}.age-segments i.on{background:#9bcbb9}
.clinic-layout{display:grid;grid-template-columns:.92fr 1.1fr;gap:17px;align-items:stretch;margin-bottom:28px}
.clinic-scene{position:relative;background:#eaf7f2;border:7px solid #fff;border-radius:23px;overflow:hidden;box-shadow:0 8px 22px #b2d6c226;display:flex;flex-direction:column;justify-content:center}
.clinic-small-title{position:absolute;top:20px;left:20px;background:#f9fffbeb;padding:8px 12px;border-radius:8px;font-size:11px;font-weight:900;color:#83aba5;letter-spacing:1px}.clinic-scene canvas{width:100%;height:auto;aspect-ratio:520/370;image-rendering:pixelated}.clinic-scene p{margin:0;text-align:center;background:#fff;font-size:12px;color:#729d90;padding:13px 8px}
.journal-wrap{background:#fff;border:1px solid #d4e5dd;padding:15px;border-radius:22px;box-shadow:0 6px 22px #a1cfc023}.journal-page{border:2px dashed #d6e7db;border-radius:16px;padding:28px 23px;background:linear-gradient(90deg,#fffdfa 0 32px,#fff4f2 33px,#fff4f2 35px,#fffdfa 36px);min-height:100%;padding-left:49px}
.journal-label{display:inline-block;background:#e0f2e8;color:#6ca38c;padding:8px 14px;border-radius:20px;font-size:11px;font-weight:900}.journal-page h2{font-size:23px;color:#528b80;margin:20px 0 6px}.journal-page p{color:#708f85;line-height:1.8}.journal-page .question{color:#456e6a!important}.journal-page .btn{background:#6ea999;border-color:#5e9389;border-bottom-color:#467c73}.journal-page .btn.choice{color:#548579;background:#f5fcf8;border-color:#d9ece0}.journal-page .btn.secondary{background:#fffdfb;color:#71958a;border-color:#d5e6de}
.journal-page th{background:#e9f5ed;color:#508c7e}.journal-page tr.highlight{background:#fff7e5}.journal-page .table-wrap{margin:17px 0}.journal-page td{padding:13px 8px}
.milestone-finish{padding:57px 20px;background:#fffefc;border:6px solid #fff;border-radius:25px;text-align:center;box-shadow:0 10px 40px #d5c8d724}.milestone-finish h2{font-size:31px;color:#896f99}.milestone-finish p{color:#908598;line-height:2}.finish-emoji{font-size:72px}
.chapter-book .game-frame{border-color:#ddcce9;border-bottom-color:#bdabd3}.chapter-book .game-frame canvas{border-color:#e5d1ee;box-shadow:0 4px 0 #bea4cc}.chapter-book .world-banner{background:#fbf0ff;color:#8d70a1}.chapter-book .world-banner-dot{background:#bb88cd;box-shadow:0 0 0 4px #f2d8fa}
.chapter-lab .page-heading h1{color:#45546a}.chapter-lab .scene-story{border-color:#8b98a9;background:#e4eaf1;color:#5c6d7b}.chapter-lab .quest-panel h2{color:#45546a}
@media(max-width:900px){.birth-story,.clinic-layout,.life-cover{grid-template-columns:1fr}.life-cover-art{min-height:auto}.life-route{grid-template-columns:1fr}.cover-copy{padding:30px 21px}.chapter-spine{display:block}.chapter-spine>span{padding-left:12px}.journal-page{padding:25px 18px 25px 38px}}
@media(max-width:520px){.story-topbar{padding:14px 12px}.birth-paper{padding:30px 19px}.birth-paper h2{font-size:25px}.visit-top{display:block}.age-segments{margin-top:12px}.page-heading h1{font-size:27px}}

/* 책 속 모험은 사이드바를 따라 하지 않고 한 장의 넓은 펼친 책처럼 배치 */
.book-rpg-layout{display:flex;flex-direction:column;gap:15px}
.book-rpg-layout .game-frame{width:100%;max-width:none;background:#fff8ff;padding:17px}
.book-rpg-layout .game-frame canvas{border-radius:12px;border:7px solid #e4cbed;max-width:100%}
.book-rpg-layout .quest-panel{border:2px solid #e6d8ea;border-left:9px solid #c9a8d6;background:#fffaff;border-radius:17px;padding:18px 25px}
.book-rpg-layout .quest-panel h2{color:#9e7ab0;margin:0 0 6px}
.book-rpg-layout .quest-panel .quest{display:inline-block;padding:9px 15px;margin:6px 5px;background:#fbf3fe;border:1px solid #eddaf5;border-radius:50px;color:#896ba0}
.book-rpg-layout .quest-panel hr{margin:12px 0}
.book-rpg-layout .quest-panel .small-note{background:#fff4fd}
.chapter-book .scene-story{background:linear-gradient(95deg,#faeafa,#fff5ef);border-left:7px solid #caa5d4;border-color:#ead8f0;color:#8b709c}

'''

GAME_LOGIC_JS = r'''
/* LIFE CODE 메인 게임: 페이지 이동, 저장, 퀴즈, 코인, 연구소 탈출 */
(() => {
  'use strict';
  const D=window.LIFE_DATA;
  const KEY='life-code-storybook-save-v3';
  const PAGES=['birth','growth','book','story','lab','ending'];
  const TITLES=['탄생','예방접종','책 속 탐험','성장 이야기','독성학 연구소','엔딩'];
  let current=(location.hash.match(/^#\/(home|birth|growth|book|story|lab|ending)$/)||[])[1]||'home';
  const pageUrl=p=>`#/${p}`;
  const defaultState=()=>({
    started:false,name:'',gender:'',coins:0,
    ageIndex:0,notebookOpen:true,vaccTried:false,
    immuneIndex:0,immunePerfect:true,immuneDone:false,
    bodyDone:[false,false,false],bodyPerfect:true,bookDone:false,
    storyDone:false,outfit:'',hp:100,gear:false,revives:0,caseOwned:false,hints:0,
    keys:[],labTried:{},foundCoins:[],note:false,ending:null,
    positions:{book:{x:2.5,y:2.5},lab:{x:2.5,y:2.5}}
  });
  let s=load(), world=null, toastTimer=null;
  function load(){
    const fresh=defaultState();
    try{
      const raw=JSON.parse(localStorage.getItem(KEY)||'null');
      if(!raw||typeof raw!=='object')return fresh;
      const merged={...fresh,...raw,positions:{...fresh.positions,...raw.positions}};
      if(!Array.isArray(merged.keys)||!Array.isArray(merged.bodyDone)||!Array.isArray(merged.foundCoins))return fresh;
      merged.coins=Math.max(0,Number(merged.coins)||0);
      merged.hp=Math.max(0,Math.min(100,Number(merged.hp)||0));
      merged.ageIndex=Math.max(0,Math.min(D.vaccines.length,Number(merged.ageIndex)||0));
      return merged;
    }catch{return fresh;}
  }
  function save(){try{localStorage.setItem(KEY,JSON.stringify(s));}catch{/* 저장 공간을 사용할 수 없는 환경도 허용 */}}
  function e(text){return String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
  function reset(){stopWorld();s=defaultState();save();go('birth');}
  function go(p){save();const next=pageUrl(p);if(location.hash===next){renderRoute();}else{location.hash=next;}}
  function unlocked(p){
    return p==='birth'||(p==='growth'&&s.started)||(p==='book'&&s.ageIndex===D.vaccines.length)||
      (p==='story'&&s.bookDone)||(p==='lab'&&s.storyDone)||(p==='ending'&&Boolean(s.ending));
  }
  function header(){
    const nav=PAGES.map((p,i)=>unlocked(p)?`<a class="nav-item ${current===p?'selected':''}" href="${pageUrl(p)}">${i+1}. ${TITLES[i]}</a>`:`<span class="nav-item locked">🔒 ${TITLES[i]}</span>`).join('');
    return `<header class="topbar story-topbar"><a class="brand" href="${pageUrl('home')}"><span class="brand-mark">✿</span> LIFE <strong>CODE</strong><small> MY LIFE SCIENCE DIARY</small></a><div class="status-bar"><span>✦ 기억의 코인 <b id="coinCount">${s.coins}</b></span><span>♡ 체력 <b id="hpCount">${s.hp}</b></span><span>◈ 열쇠 <b id="keyCount">${s.keys.length}</b>/3</span></div></header><div class="chapter-spine"><span>나의 성장 앨범</span><nav class="progress-nav">${nav}</nav></div>`;
  }
  function layout(title,sub,html){
    const root=document.getElementById('app');
    document.body.className='chapter-'+current;
    root.innerHTML=`<div class="shell">${header()}<div class="page-heading"><div class="eyebrow">LIFE CODE · A STORY OF SCIENCE</div><h1>${title}</h1><p>${sub}</p></div>${html}<footer class="footer">교육용 창작 게임 · 예방접종 시기와 실제 안전 수칙은 보건당국 및 전문가의 안내를 확인하세요.</footer></div><div id="toast" role="status" aria-live="polite"></div><div id="modalHost"></div>`;
  }
  function updateHUD(){
    for(const [id,val] of [['coinCount',s.coins],['hpCount',s.hp],['keyCount',s.keys.length]]){
      const el=document.getElementById(id);if(el)el.textContent=val;
    }
  }
  function toast(message){
    const node=document.getElementById('toast');if(!node)return;
    node.textContent=message;node.className='toast show';clearTimeout(toastTimer);
    toastTimer=setTimeout(()=>node.classList.remove('show'),2900);
  }
  function modal(title,content,choices=[]){
    const host=document.getElementById('modalHost');if(!host)return;
    host.innerHTML=`<div class="modal-backdrop"><div class="modal-box" role="dialog" aria-modal="true"><h2>${e(title)}</h2><div class="modal-content">${content}</div><div class="modal-actions" id="modalActions"></div></div></div>`;
    const actions=document.getElementById('modalActions');
    choices.forEach(choice=>{
      const btn=document.createElement('button');btn.className='btn '+(choice.secondary?'secondary':'');
      btn.textContent=choice.label;btn.disabled=Boolean(choice.disabled);
      btn.addEventListener('click',()=>{if(!choice.keepOpen)closeModal();choice.run?.();});actions.appendChild(btn);
    });
  }
  function closeModal(){const host=document.getElementById('modalHost');if(host)host.innerHTML='';}
  function card(title,text,extra=''){return `<section class="panel"><h2>${title}</h2><p>${text}</p>${extra}</section>`;}
  function action(label,id,klass=''){return `<button class="btn ${klass}" data-action="${id}">${label}</button>`;}
  function bindActions(root=document){
    root.querySelectorAll('[data-action]').forEach(b=>b.addEventListener('click',()=>handle(b.dataset.action)));
  }
  function stopWorld(){if(world){world.stop();world=null;}}
  function showLocked(){
    layout('🔒 아직 잠겨 있어요','앞 챕터를 완료해야 다음 이야기가 열립니다.',
      `<section class="panel center">${action('가능한 챕터로 돌아가기','back')}</section>`);
    bindActions();
  }
  function renderHome(){
    layout('작은 생명에서 시작된 커다란 이야기','한 아이의 첫날에서, 세상을 지키는 연구자가 되는 날까지',
      `<section class="life-cover"><div class="life-cover-art"><canvas id="coverCanvas" width="520" height="370" role="img" aria-label="햇살이 드는 아기 방과 아기 침대의 픽셀아트"></canvas><div class="cover-sticker">01 · 첫 번째 페이지</div></div><div class="cover-copy"><span class="intro-line">WELCOME TO YOUR LIFE STORY</span><h2>모든 생명에는<br/><em>첫 페이지</em>가 있어요.</h2><p>오늘 태어날 아기의 이름을 지어 주세요. 작은 예방접종 수첩에서 배운 지식이, 언젠가 연구소의 마지막 문을 여는 힘이 됩니다.</p><div class="button-row">${action(s.started?'내 이야기 이어가기':'아기 만나러 가기',s.started?'continue':'start')}${action('처음부터 시작하기','reset','secondary')}</div><div class="cover-postit">✎ 처음은 따뜻하게, 모험은 신기하게, 마지막은 용감하게.</div></div></section>
      <div class="life-route"><div><span>01</span><b>아기와 첫 건강수첩</b><small>탄생 · 예방접종</small></div><div><span>02</span><b>책 속에 숨은 세계</b><small>면역세포 · 몸속 미로</small></div><div><span>03</span><b>연구원이 된 나</b><small>독성학 · 마지막 탈출</small></div></div>`);
    bindActions();LIFE_WORLD.cover('coverCanvas');
  }
  function nextPage(){for(const p of [...PAGES].reverse())if(unlocked(p))return p;return'birth';}
  function initialsMatch(name){
    const indices=new Set([11,12,18]); // ㅇ, ㅈ, ㅎ
    return [...name].some(ch=>{
      const code=ch.charCodeAt(0);
      if(code>=0xAC00&&code<=0xD7A3)return indices.has(Math.floor((code-0xAC00)/588));
      return ['ㅇ','ㅈ','ㅎ'].includes(ch);
    });
  }
  function renderBirth(){
    if(s.started){
      layout('성장 앨범의 첫 페이지',`이름: ${e(s.name)} · 기억의 코인 ${s.coins}개`,
        card('다음 이야기로', '우리 아기의 탄생 기록이 저장되어 있어요. 이제 첫 건강수첩을 만나볼까요?',action('소아청소년과 방문하기','growth')));
    }else{
      layout('CHAPTER 1 · 아기가 태어났어요','햇살이 들어오는 포근한 아기 방에서 이야기가 시작됩니다.',
        `<div class="birth-story"><div class="birth-illustration"><div class="scene-label">TODAY'S MEMORY · DAY 1</div><canvas id="nurseryCanvas" width="520" height="370" role="img" aria-label="아기 침대와 모빌이 있는 따뜻한 아기 방"></canvas><div class="scene-bottom">☀️ 반가워, 우리 아가!</div></div><section class="birth-paper"><div class="paper-tape">✿ 탄생 기록 카드 ✿</div><div class="baby-symbol">♡</div><h2>세상에 온 걸 환영해!</h2><p>소중한 아기가 태어났어요.<br/>첫 번째 선물로 예쁜 이름을 지어 주세요.</p><label for="babyName" class="label">아기 이름 짓기</label><input id="babyName" class="input" placeholder="이름을 입력해 주세요" maxlength="12" autocomplete="off"/><p class="hint">이름 1~12글자 · 성별은 무작위로 정해져요.</p>${action('탄생 축하하기 ✨','birthCreate')}</section></div>`);
      LIFE_WORLD.nursery('nurseryCanvas');
    }
    bindActions();
    const input=document.getElementById('babyName');
    if(input)input.addEventListener('keydown',ev=>{if(ev.key==='Enter')handle('birthCreate');});
  }
  function renderGrowth(){
    const idx=s.ageIndex;
    if(idx>=D.vaccines.length){
      layout('예방접종 미션을 마쳤어요!','어느새 주인공은 호기심 많은 유치원생으로 성장했습니다.',
        `<div class="milestone-finish"><div class="finish-emoji">🧒📚</div><h2>${e(s.name)}의 다음 호기심</h2><p>예방접종 수첩의 내용을 모두 기억했어요.<br/>이제 집으로 돌아가 신비한 과학책을 펼쳐볼까요?</p>${action('책 속 세계로 들어가기','book')}</div>`);
      bindActions();return;
    }
    const v=D.vaccines[idx];
    const rows=D.vaccines.map((x,i)=>`<tr class="${i===idx?'highlight':''}"><td>${e(x.age)}</td><td>${e(['B형간염','DTaP · IPV · Hib 등','MMR 등','DTaP · IPV · MMR 등 추가접종'][i])}</td></tr>`).join('');
    const choices=v.options.map((op,i)=>action(`${i+1}. ${e(op)}`,`vacc:${i}`,'choice')).join('');
    const journal=s.notebookOpen?
      `<div class="journal-page"><div class="journal-label">건강수첩 · 기억하기</div><h2>우리 아기 예방접종 수첩</h2><p>언제 어떤 접종을 받는지 잠깐 읽어보세요.</p><div class="table-wrap"><table><thead><tr><th>성장 시기</th><th>대표 예방접종</th></tr></thead><tbody>${rows}</tbody></table></div><p class="hint">학습용 대표 접종 예시입니다. 실제 일정은 질병관리청 최신 표와 의료진 안내를 확인하세요.</p>${action('수첩 덮고 문제 풀기','notebookClose')}</div>`:
      `<div class="journal-page"><div class="journal-label">기억력 미션 · ${idx+1}/${D.vaccines.length}</div><h2>${e(v.age)}에는 무엇을 접종할까요?</h2><p class="question">${e(v.question)}</p><div class="choices">${choices}</div>${action('수첩 다시 확인하기','notebookOpen','secondary')}<p class="hint">첫 정답 +2코인 · 오답 -1코인 · 재도전 성공 시 성장</p></div>`;
    layout('CHAPTER 1 · 예방접종하는 날',`${e(s.name)}의 성장 기록 · ${e(v.age)}`,
      `<div class="visit-top"><div><span>아기의 성장 일지</span><b>${e(v.age)}</b></div><div class="age-segments">${D.vaccines.map((_,i)=>`<i class="${i<=idx?'on':''}"></i>`).join('')}</div></div><div class="clinic-layout"><section class="clinic-scene"><div class="clinic-small-title">WELCOME TO LITTLE CLINIC</div><canvas id="clinicCanvas" width="520" height="370" role="img" aria-label="아기와 보호자가 방문하는 밝고 친근한 소아청소년과 진료실"></canvas><p>진료실에서 예방접종 수첩을 확인해 볼까요?</p></section><section class="journal-wrap">${journal}</section></div>`);
    LIFE_WORLD.clinic('clinicCanvas',idx);
    bindActions();
  }
  function mapHtml(scene){
    return `<div class="${scene==='book'?'book-rpg-layout':'rpg-layout'}"><section class="game-frame"><div class="world-banner"><span class="world-banner-dot"></span><strong>EXPLORE & DISCOVER</strong><span>작은 세포의 세계를 직접 탐험해요</span></div><canvas id="gameCanvas" width="768" height="448" aria-label="이동 가능한 2D 게임 월드" tabindex="0"></canvas><div class="game-controls"><div><button data-move="arrowup">▲</button><div class="horizontal-control"><button data-move="arrowleft">◀</button><button data-move="arrowdown">▼</button><button data-move="arrowright">▶</button></div></div><button class="interact-button" data-move="e">E<br/>조사</button></div><p class="hint">🎮 방향키 / WASD : 이동 &nbsp; ✦ &nbsp; Shift : 달리기 &nbsp; ✦ &nbsp; E 또는 Space : 대화 · 조사 &nbsp; ✦ &nbsp; 스마트폰은 화면 버튼</p></section><aside class="panel quest-panel" id="questPanel"></aside></div>`;
  }
  function renderBook(){
    stopWorld();
    layout('CHAPTER 2 · 책 속 몸속 세계','『보이지 않는 침입자와 생명의 방패』 속으로 빠져들었어요!',
      `<div class="scene-story">📖 책장을 넘기는 순간, 세포와 면역세포가 살아 움직이는 작은 몸속 도시가 나타났어요. <strong>WASD / 방향키</strong>로 꽃길을 걷고, 면역 수호자와 반짝이는 표지판 앞에서 <strong>E</strong>를 눌러보세요!</div>${mapHtml('book')}`);
    refreshQuest();
    world=LIFE_WORLD.start('book',s,interactBook,()=>{},pos=>{s.positions.book=pos;save();});
  }
  function refreshQuest(){
    const target=document.getElementById('questPanel');if(!target)return;
    if(current==='book'){
      target.innerHTML=`<h2>📜 모험 수첩</h2><div class="quest">${s.immuneDone?'✅':'⬜'} 면역세포 방어전 (${s.immuneIndex}/3)</div>${s.bodyDone.map((v,i)=>`<div class="quest">${v?'✅':'⬜'} ${D.checkpoints[i].title}</div>`).join('')}<hr/><p>두 게임을 모두 완료하면 출구가 열립니다.</p><div class="small-note">💡 면역세포는 세균·바이러스 등 병원체에 대응하지만, 모든 면역반응이 동일한 방식으로 일어나지는 않습니다.</div>`;
    }else if(current==='lab'){
      target.innerHTML=`<h2>🧰 연구원 가방</h2><div class="quest">🪙 코인: ${s.coins}</div><div class="quest">💗 체력: ${s.hp}/100</div><div class="quest">🥼 의상: ${e(s.outfit)} ${s.gear?'(+ 업그레이드)':''}</div><div class="quest">🗝️ 열쇠: ${s.keys.map(x=>({A:'🔵',B:'🟡',C:'🔴'}[x])).join(' ')||'없음'}</div><div class="quest">📦 보관 케이스: ${s.caseOwned?'보유':'없음'}</div><div class="quest">📓 비밀 노트: ${s.note?'획득':'미획득'}</div><div class="quest">💫 부활권: ${s.revives}</div><div class="quest">💡 힌트: ${s.hints}</div><hr/><div class="small-note">⚠️ 붉은 바닥은 게임 내 가상 위험구역입니다. 실제 연구소에서는 위험구역에 진입하지 말고 시설별 안전 절차를 따라야 합니다.</div>`;
    }
    updateHUD();
  }
  function quiz(title,q,success,fail,canHint=false){
    const buttons=q.options.map((op,i)=>({label:`${i+1}. ${op}`,run:()=>{
      if(i===q.answer){success();modal('✅ 정답!',`<p>${e(q.explain)}</p>`,[{label:'계속 진행',run:()=>{if(current==='book')renderBook();else renderLab();}}]);}
      else {fail();modal('🔎 다시 생각해 봐요',`<p>아직 정답이 아닙니다. 주변 정보를 떠올려 다시 시도하세요.</p>`,[{label:'다시 도전',run:()=>quiz(title,q,success,fail,canHint)}]);}
    }}));
    if(canHint&&s.hints>0)buttons.push({label:`💡 힌트 카드 사용 (${s.hints}장)`,secondary:true,run:()=>{
      s.hints--;save();modal('연구 힌트',`<p>정답 번호는 <b>${q.answer+1}번</b>입니다.</p>`,[{label:'문제로 돌아가기',run:()=>quiz(title,q,success,fail,canHint)}]);
    }});
    buttons.push({label:'나중에 풀기',secondary:true,run:()=>{}});
    modal(title,`<p class="question">${e(q.question)}</p>`,buttons);
  }
  function interactBook(id){
    if(id==='immune'){
      if(s.immuneDone){toast('면역 수호자: 수고했어! 나머지 체크포인트도 살펴봐.');return;}
      const q=D.immune[s.immuneIndex];
      quiz(`🛡️ 면역세포 방어전 ${s.immuneIndex+1}/3`,q,()=>{
        s.immuneIndex++;
        if(s.immuneIndex===D.immune.length){s.immuneDone=true;if(s.immunePerfect)s.coins+=3;}
        save();
      },()=>{s.immunePerfect=false;save();});return;
    }
    if(id.startsWith('cp')){
      const n=Number(id.slice(2));if(s.bodyDone[n]){toast('이미 해결한 체크포인트입니다.');return;}
      quiz('🔬 인체 미로 — '+D.checkpoints[n].title,D.checkpoints[n],()=>{
        s.bodyDone[n]=true;
        if(s.bodyDone.every(Boolean)&&s.bodyPerfect)s.coins+=3;
        save();
      },()=>{s.bodyPerfect=false;save();});return;
    }
    if(id==='bookExit'){
      if(s.immuneDone&&s.bodyDone.every(Boolean)){
        s.bookDone=true;save();modal('📖 책의 마지막 페이지',`<p><b>납(Pb)</b>: 신경계와 발달에 악영향을 줄 수 있습니다.</p><p><b>카드뮴(Cd)</b>: 장기 노출 시 신장 등에 손상을 줄 수 있습니다.</p><p><b>일산화탄소(CO)</b>: 혈액의 산소 운반을 방해할 수 있습니다.</p><p>자료 제공: 독성학 연구소</p>`,[{label:'현실로 돌아가기',run:()=>go('story')}]);
      }else toast('면역 방어전과 체크포인트 3곳을 모두 통과해야 합니다.');
    }
  }
  function renderStory(){
    layout('⏳ CHAPTER 3 — 과학책이 바꾼 진로','시간이 흘러 주인공은 화학과 생명과학을 공부하는 학생이 됩니다.',
      `<section class="panel story-panel"><div class="storybook">📕 <span>→</span> 🧑‍🎓 <span>→</span> 🥼 <span>→</span> 🧪</div><h2>어린 시절의 호기심이 연구가 되다</h2><p>${e(s.name)}은(는) 오래된 책의 마지막 장에서 납·카드뮴·일산화탄소에 관한 기록을 다시 발견합니다.</p><p>“왜 어떤 물질은 우리 몸에 해로울까? 어떻게 위험을 알아내고 막을 수 있을까?”</p><p>화학과 생명과학을 공부한 주인공은 마침내 독성학 연구소의 연구원이 됩니다.</p>${action('🌙 연구소의 야근 시작','storyNext')}</section>`);
    bindActions();
  }
  function renderLab(){
    stopWorld();
    if(!s.outfit){
      layout('🧥 CHAPTER 4 — 오늘의 의상','오늘 입고 갈 옷을 선택하세요.',
        `<div class="outfit-grid"><div class="panel center"><div class="outfit-icon">👕</div><h2>평상복</h2>${action('선택하기','outfit:평상복')}</div><div class="panel center"><div class="outfit-icon">🥼</div><h2>실험복</h2>${action('선택하기','outfit:실험복')}</div><div class="panel center"><div class="outfit-icon">🦺</div><h2>보호복</h2>${action('선택하기','outfit:보호복')}</div></div><p class="hint">게임 속 의상 수치는 가상 설정입니다. 실제 보호구는 물질·노출 경로에 따라 선택하고 안전관리 지침을 따라야 합니다.</p>`);
      bindActions();return;
    }
    layout('🧪 CHAPTER 4 — 독성학 연구소의 야근','비상 안전 시스템이 구역을 폐쇄했습니다. 열쇠 세 개를 모아 출입문을 열어야 합니다.',
      `<div class="scene-story">연구소 경보: “시설 고장이 감지되었습니다. 비상 출입문 잠금.”<br/>연구실을 조사하고, 비상 물품 보관함에서 아이템을 구매하세요.</div>${mapHtml('lab')}`);
    refreshQuest();
    world=LIFE_WORLD.start('lab',s,interactLab,danger,pos=>{s.positions.lab=pos;save();});
  }
  function danger(){
    const damage=Math.max(2,({평상복:20,실험복:12,보호복:6}[s.outfit]||20)-(s.gear?5:0));
    s.hp=Math.max(0,s.hp-damage);save();refreshQuest();
    if(s.hp===0)death();else toast(`⚠️ 가상 위험구역! 체력 -${damage} · 현재 ${s.hp}`);
  }
  function death(){
    if(s.revives>0){s.revives--;revive();modal('💫 부활권 사용',`<p>마지막 안전 체크포인트로 복귀했습니다. 체력 50 회복.</p>`,[{label:'계속 탐험',run:renderLab}]);return;}
    if(s.coins>=5){modal('⚠️ 체력이 0이 되었습니다',`<p>코인 5개로 부활권을 구매해 안전 체크포인트에서 다시 시작할 수 있습니다.</p>`,[
      {label:'5코인으로 부활',run:()=>{s.coins-=5;revive();renderLab();}},
      {label:'BAD ENDING 보기',secondary:true,run:()=>finish('bad')}
    ]);return;}
    finish('bad');
  }
  function revive(){s.hp=50;s.positions.lab={x:2.5,y:2.5};save();refreshQuest();}
  function showShop(){
    const offers=[
      ['gear','🦺 보호구 업그레이드',3,s.gear,'위험구역에서 받는 가상 체력 피해 -5'],
      ['heal','💚 비상 회복권',2,s.hp>=100,'체력 +30 (최대 100)'],
      ['revive','💫 부활권',5,false,'체력 0일 때 안전지점으로 복귀'],
      ['case','📦 연구 기록 보관 케이스',2,s.caseOwned,'비밀 노트 수집 가능'],
      ['hint','💡 힌트 카드',1,false,'독성학 퍼즐에서 힌트 1회']
    ];
    const html=`<p>현재 코인: <b>${s.coins}개</b></p><div class="shop-list">${offers.map(([id,name,price,owned,desc])=>`<button data-buy="${id}" ${owned||s.coins<price?'disabled':''}><strong>${name} · ${price}코인</strong><small>${desc}</small>${owned?'<em>보유 / 사용 불가</em>':''}</button>`).join('')}</div>`;
    modal('🛒 비상 물품 보관함',html,[{label:'상점 닫기',secondary:true,run:()=>{}}]);
    document.querySelectorAll('[data-buy]').forEach(b=>b.addEventListener('click',()=>buy(b.dataset.buy)));
  }
  function buy(id){
    const prices={gear:3,heal:2,revive:5,case:2,hint:1};
    const cost=prices[id];if(cost==null||s.coins<cost){toast('코인이 부족합니다.');return;}
    if(id==='gear'&&s.gear||id==='case'&&s.caseOwned||id==='heal'&&s.hp>=100){toast('이미 보유했거나 지금 사용할 수 없습니다.');return;}
    s.coins-=cost;
    if(id==='gear')s.gear=true;
    if(id==='heal')s.hp=Math.min(100,s.hp+30);
    if(id==='revive')s.revives++;
    if(id==='case')s.caseOwned=true;
    if(id==='hint')s.hints++;
    save();refreshQuest();showShop();
  }
  function interactLab(id){
    if(id==='shop'){showShop();return;}
    if(id.startsWith('chest')){
      if(s.foundCoins.includes(id)){toast('이미 조사한 보관함입니다.');return;}
      s.foundCoins.push(id);const earned=id==='chest1'?2:1;s.coins+=earned;save();refreshQuest();
      modal('🪙 숨겨진 코인 발견!',`<p>구석의 보관함에서 ${earned}코인을 발견했습니다.</p>`,[{label:'가방에 넣기',run:renderLab}]);return;
    }
    if(['A','B','C'].includes(id)){
      if(s.keys.includes(id)){toast('이 분석실의 열쇠는 이미 확보했습니다.');return;}
      const q=D.lab[id];
      quiz(`🔬 ${q.name}`,q,()=>{
        const first=!s.labTried[id];s.keys.push(id);
        if(first)s.coins+=3;save();refreshQuest();
      },()=>{s.labTried[id]=true;save();},true);
      return;
    }
    if(id==='note'){
      if(s.note){toast('비밀 노트를 이미 확보했습니다.');return;}
      if(!s.caseOwned){modal('📚 오래된 책장',`<p>뒤쪽에서 「연구소의 숨겨진 비밀」 노트를 발견했습니다.</p><p>기록을 안전하게 보관하려면 상점에서 연구 기록 보관 케이스(2코인)를 구매해야 합니다.</p>`,[{label:'나중에 돌아오기',run:()=>{}}]);return;}
      s.note=true;save();refreshQuest();modal('📓 연구소의 숨겨진 비밀',`<p>과거의 일부 유해물질 노출 위험 평가가 불충분했다는 기록을 발견했습니다.</p><p>이 기록을 안전하게 확보했습니다. 탈출하면 독립적인 검토 절차에 제출할 수 있습니다.</p>`,[{label:'노트 보관하기',run:renderLab}]);return;
    }
    if(id==='labExit'){
      if(s.keys.length===3)finish(s.note?'secret':'good');
      else toast(`출입문이 잠겨 있습니다. 열쇠 ${3-s.keys.length}개가 더 필요합니다.`);
    }
  }
  function finish(kind){s.ending=kind;save();go('ending');}
  function renderEnding(){
    const type=s.ending;
    const content=type==='secret'?{
      icon:'🌟',title:'SECRET ENDING — 감춰진 진실',sub:'문을 여는 것보다 중요한 선택',
      text:'세 개의 열쇠와 비밀 노트를 확보한 연구원은 안전관리 책임자와 독립 검토기관에 자료를 제출합니다. 재검증 결과, 평가상 문제가 확인되어 연구소의 기준이 개선됩니다. 어린 시절 읽었던 책의 마지막 장을 다시 펼칩니다.',quote:'생명을 지키는 첫걸음은 예방이었고, 그다음은 이해였으며, 마지막은 그 지식을 다른 사람을 위해 사용하는 것이었다.'
    }:type==='good'?{
      icon:'🌈',title:'GOOD ENDING — 마지막 문을 열다',sub:'세 개의 열쇠로 무사히 탈출했습니다.',
      text:'연구원은 분석 결과를 비상 대응팀에 전달했습니다. 연구소의 안전 시스템은 개선되고, 어린 시절부터 쌓은 지식이 문제 해결에 도움이 된다는 사실을 깨닫습니다.',quote:'배운 지식은 누군가를 지키는 힘이 된다.'
    }:{
      icon:'🌑',title:'BAD ENDING — 끝나지 못한 연구',sub:'마지막 안전구역까지 도달하지 못했습니다.',
      text:'가상의 위험구역에서 체력을 모두 잃어 연구를 끝내지 못했습니다. 이번 결과는 실제 중독 경과나 치사량을 뜻하지 않습니다. 다른 의상과 아이템 전략으로 다시 도전해 보세요.',quote:'과학에는 지식만큼 안전한 선택도 중요하다.'
    };
    layout(`${content.icon} ${content.title}`,content.sub,
      `<section class="panel ending-panel"><div class="ending-art">${content.icon}</div><h2>${e(s.name)}의 이야기</h2><p>${content.text}</p><blockquote>“${content.quote}”</blockquote><div class="record"><span>🪙 남은 코인 ${s.coins}</span><span>🗝️ 열쇠 ${s.keys.length}/3</span><span>📓 비밀 노트 ${s.note?'획득':'미획득'}</span></div><div class="button-row">${action('새로운 삶으로 다시 시작','reset')}${action('메인 화면으로','home','secondary')}</div></section>`);
    bindActions();
  }
  function handle(id){
    if(id==='start'){go('birth');return;}
    if(id==='continue'){go(nextPage());return;}
    if(id==='home'){go('home');return;}
    if(id==='reset'){modal('게임을 처음부터 시작할까요?',`<p>현재 게임 기록과 코인이 초기화됩니다.</p>`,[{label:'초기화하기',run:reset},{label:'취소',secondary:true,run:()=>{}}]);return;}
    if(id==='back'){go(nextPage());return;}
    if(['growth','book','story','lab'].includes(id)){go(id);return;}
    if(id==='birthCreate'){
      const input=document.getElementById('babyName');const name=(input?.value||'').trim();
      if(!name||[...name].length>12){toast('이름을 1~12글자로 입력해주세요.');return;}
      if(/[<>]/.test(name)){toast('이름에 사용할 수 없는 문자가 있습니다.');return;}
      const bonus=initialsMatch(name);
      s.started=true;s.name=name;s.gender=Math.random()<.5?'여자':'남자';s.coins=5+(bonus?3:0);save();
      modal('🎉 탄생을 축하합니다!',`<p>${e(name)} · ${s.gender} 아기가 태어났습니다!</p><p>기본 코인 5개${bonus?' + 특별 보너스 3개':''}를 받았습니다.</p>`,[{label:'예방접종 수첩 열기',run:()=>go('growth')}]);updateHUD();return;
    }
    if(id==='notebookClose'){s.notebookOpen=false;save();renderGrowth();return;}
    if(id==='notebookOpen'){s.notebookOpen=true;save();renderGrowth();return;}
    if(id.startsWith('vacc:')){
      const pick=Number(id.split(':')[1]),q=D.vaccines[s.ageIndex];if(!q||s.notebookOpen)return;
      if(pick===q.answer){
        const earned=!s.vaccTried?2:0;s.coins+=earned;s.ageIndex++;
        s.vaccTried=false;s.notebookOpen=true;save();renderGrowth();
        modal('✅ 기억력 미션 성공!',`<p>${e(q.explain)}</p><p>${earned?'+2코인 획득!':'재도전이므로 코인 보상 없이 성장했습니다.'}</p>`,[{label:'계속하기',run:()=>{}}]);
      }else{
        s.coins=Math.max(0,s.coins-1);s.vaccTried=true;s.notebookOpen=true;save();renderGrowth();
        if(s.coins===0){modal('GAME OVER — 코인이 소진되었습니다',`<p>예방접종 수첩을 다시 살펴보며 새로운 게임을 시작하세요.</p>`,[{label:'처음부터 다시 시작',run:reset}]);}
        else modal('💉 예방접종 시기를 놓쳤어요!',`<p>감염병에 노출될 위험이 커질 수 있어요. 수첩을 다시 확인해 주세요.</p><p>코인 -1 · 현재 ${s.coins}개</p>`,[{label:'수첩 다시 확인',run:()=>{}}]);
      }return;
    }
    if(id==='storyNext'){s.storyDone=true;save();go('lab');return;}
    if(id.startsWith('outfit:')){s.outfit=id.slice(7);save();renderLab();return;}
  }
  window.LIFE_UI={toast,updateHUD};
  function renderRoute(){
    stopWorld();
    current=(location.hash.match(/^#\/(home|birth|growth|book|story|lab|ending)$/)||[])[1]||'home';
    if(current==='home')renderHome();
    else if(!unlocked(current))showLocked();
    else if(current==='birth')renderBirth();
    else if(current==='growth')renderGrowth();
    else if(current==='book')renderBook();
    else if(current==='story')renderStory();
    else if(current==='lab')renderLab();
    else if(current==='ending')renderEnding();
    window.scrollTo({top:0,behavior:'instant'});
  }
  window.addEventListener('hashchange',renderRoute);
  renderRoute();
})();

'''
