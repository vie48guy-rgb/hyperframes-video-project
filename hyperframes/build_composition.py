from pathlib import Path
import json,html,sys
C=Path(__file__).resolve().parent;P=C;p=json.loads((P/'edit-plan.json').read_text());D=p['duration']
correction=json.loads((C/'color-correction.json').read_text())
footage_src=correction['output']
cards=json.loads((C/'image-cards.json').read_text()) if '--without-cards' not in sys.argv else []
missing=[c['src'] for c in cards if not (C/c['src']).is_file()]
if missing:
 raise SystemExit('Bilddateien fehlen: '+', '.join(missing)+'. --without-cards dient nur zur Textdesign-Vorschau.')
highlights=[]
for original in p['highlights']:
 h=dict(original)
 if any(c['start']<=h['start']<c['start']+c['duration'] for c in cards):continue
 for c in cards:
  if h['start']<c['start']<h['end']:h['end']=min(h['end'],c['start']-.15)
 if h['end']-h['start']>.8:highlights.append(h)
def clips(data,prefix,lane,cls):
 return '\n'.join(f'<div id="{prefix}-{i}" class="clip {cls}" data-start="{c["start"]:.4f}" data-duration="{c["end"]-c["start"]:.4f}" data-track-index="{lane}"><span class="pill">{html.escape(c["text"])}</span></div>' for i,c in enumerate(data))
words=json.loads((C/'transcript.json').read_text())
karaoke=[];caption_html=[]
for i,c in enumerate(p['captions']):
 group=[]
 for w in words:
  if c['start']-.001<=w['start']<c['end']-.001:
   w=dict(w)
   if w['text'].startswith('-') and group:
    group[-1]['text']+=w['text'];group[-1]['end']=w['end']
   else:group.append(w)
 spans=[]
 for j,w in enumerate(group):
  word_id=f'word-{i}-{j}'
  spans.append(f'<span id="{word_id}" class="word" data-word-start="{w["start"]}" data-word-end="{w["end"]}">{html.escape(w["text"])}</span>')
  karaoke.append(dict(w,id=word_id,group=i))
 caption_html.append(f'<div id="caption-{i}" class="clip caption" data-start="{c["start"]:.4f}" data-duration="{c["end"]-c["start"]:.4f}" data-track-index="2"><span class="pill">{" ".join(spans)}</span></div>')
caption='\n'.join(caption_html)
high=clips(highlights,'highlight',3,'highlight')
card_html=[]
for c in cards:
 card_html.append(f'<div id="promo-{c["id"]}" class="clip image-card" data-start="{c["start"]}" data-duration="{c["duration"]}" data-track-index="4"><div class="card-backdrop" data-layout-ignore="true"></div><div class="card-stage"><img class="card-image" src="{html.escape(c["src"])}" alt="{html.escape(c["title"])}"></div></div>')
card_markup='\n'.join(card_html)
(C/'karaoke-words.json').write_text(json.dumps(karaoke,ensure_ascii=False,indent=2))
anim=[]
for z in p['zooms']:
 if z['time']==0:
  anim.append(f'tl.set("#camera", {{scale:{z["scale"]}}}, 0);')
 else:
  anim.append(f'tl.to("#camera", {{scale:{z["scale"]},duration:1.3,ease:"sine.inOut"}}, {z["time"]});')
for i,c in enumerate(p['captions']):
 anim.append(f'tl.set("#caption-{i}", {{opacity:0}}, {c["end"]});')
for w in karaoke:
 anim.append(f'tl.set("#{w["id"]}", {{backgroundColor:"#365D7D"}}, {w["start"]});')
 anim.append(f'tl.set("#{w["id"]}", {{backgroundColor:"rgba(54,93,125,0)"}}, {w["end"]});')
for i,c in enumerate(highlights):
 fade=min(0.55,(c['end']-c['start'])*0.25)
 anim.append(f'tl.fromTo("#highlight-{i} .pill", {{opacity:0,filter:"blur(8px)"}}, {{opacity:1,filter:"blur(0px)",duration:{fade},ease:"sine.inOut",immediateRender:false}}, {c["start"]});')
 anim.append(f'tl.to("#highlight-{i} .pill", {{opacity:0,filter:"blur(8px)",duration:{fade},ease:"sine.inOut"}}, {c["end"]-fade});')
 anim.append(f'tl.set("#highlight-{i}", {{opacity:0}}, {c["end"]});')
for c in cards:
 sel=f'#promo-{c["id"]}'
 start=c['start'];end=start+c['duration'];fade=c['fade']
 anim.append(f'tl.fromTo("{sel}", {{opacity:0}}, {{opacity:1,duration:{fade},ease:"sine.inOut",immediateRender:false}}, {start});')
 anim.append(f'tl.fromTo("{sel} .card-image", {{filter:"blur(5px)"}}, {{filter:"blur(0px)",duration:{fade},ease:"sine.inOut",immediateRender:false}}, {start});')
 anim.append(f'tl.to("{sel}", {{opacity:0,duration:{fade},ease:"sine.inOut"}}, {end-fade});')
 anim.append(f'tl.to("{sel} .card-image", {{filter:"blur(5px)",duration:{fade},ease:"sine.inOut"}}, {end-fade});')
 anim.append(f'tl.set("{sel}", {{opacity:0}}, {end});')
source=f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=886,height=1920">
<title>Mach Deutsch zu deinem Deutsch — Talking-Head-Recut</title>
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:'Playfair Display';src:url('assets/PlayfairDisplay.ttf') format('truetype');font-weight:400 900;font-display:block}}\n@font-face{{font-family:'DejaVu Sans';src:url('assets/DejaVuSans.ttf') format('truetype');font-weight:400;font-display:block}}
@font-face{{font-family:'DejaVu Sans';src:url('assets/DejaVuSans-Bold.ttf') format('truetype');font-weight:700;font-display:block}}
*{{box-sizing:border-box}}html,body{{margin:0;width:886px;height:1920px;overflow:hidden;background:#151A20}}
#recut{{position:relative;width:886px;height:1920px;overflow:hidden;font-family:'DejaVu Sans',sans-serif;color:#FAFAF7}}
#camera{{position:absolute;inset:0;transform-origin:50% 43%;will-change:transform}}
#footage{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#caption-rail{{position:absolute;left:0;right:0;bottom:360px;height:180px;z-index:7}}
.caption{{position:absolute;inset:0;display:flex;justify-content:center;align-items:center;padding:0 48px;text-align:center}}
.caption .pill{{max-width:790px;text-wrap:balance;padding:12px 18px;border-radius:14px;background:rgba(10,17,24,.82);color:#FFFFFF;font-family:'Playfair Display',serif;font-size:48px;font-weight:600;line-height:1.4;letter-spacing:0;text-shadow:0 2px 3px rgba(10,17,24,.85),0 0 2px rgba(10,17,24,.9)}}\n.word{{display:inline-block;padding:1px 6px;margin:0 1px;border-radius:7px;background:rgba(54,93,125,0)}}
#highlight-rail{{position:absolute;left:0;right:0;top:245px;height:240px;z-index:4}}
.highlight{{position:absolute;inset:0;display:flex;justify-content:center;align-items:center;padding:0 68px;text-align:center}}
.highlight .pill{{max-width:750px;padding:22px 30px;border:1px solid rgba(213,218,222,.25);border-radius:16px;background:#365D7D;color:#FAFAF7;font-size:50px;font-weight:700;line-height:1.24;letter-spacing:-.02em;font-variant-numeric:tabular-nums}}
.image-card{{position:absolute;inset:0;z-index:5}}
.card-backdrop{{position:absolute;inset:0;background:rgba(10,17,24,.32)}}
.card-stage{{position:absolute;top:60px;bottom:580px;left:54px;right:54px;display:flex;align-items:center;justify-content:center}}
.card-image{{display:block;max-width:100%;max-height:100%;object-fit:contain;box-shadow:0 12px 36px rgba(0,0,0,.2)}}
</style></head><body>
<div id="recut" data-composition-id="recut" data-start="0" data-duration="{D}" data-width="886" data-height="1920" data-fps="30">
<div id="camera" data-layout-ignore="true"><video id="footage" class="clip" src="{footage_src}" data-start="0" data-duration="{D}" data-track-index="0" muted playsinline preload="auto"></video></div>
<audio id="speech" src="assets/speech-cut.wav" data-start="0" data-duration="{D}" data-track-index="1" data-volume="1" preload="auto"></audio>
<div id="caption-rail">{caption}</div><div id="highlight-rail">{high}</div>{card_markup}
</div>
<script>
window.__timelines=window.__timelines||{{}};
const tl=gsap.timeline({{paused:true}});
{chr(10).join(anim)}
window.__timelines.recut=tl;
</script></body></html>'''
(C/'index.html').write_text(source)
(C/'meta.json').write_text(json.dumps({'id':'talking-head-recut','name':'Mach Deutsch zu deinem Deutsch','description':'Playfair-Display-Karaoke-Untertitel, natürlich hellere Farben und sanfte Zoomfahrten.'},ensure_ascii=False,indent=2))
print('Composition built:',C)
