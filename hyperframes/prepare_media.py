"""Rebuild the edit's local media from the user's original MP4 using the saved cuts."""
import argparse,array,json,subprocess,wave
from pathlib import Path

def main():
 parser=argparse.ArgumentParser();parser.add_argument('original',type=Path)
 args=parser.parse_args();original=args.original.resolve(strict=True)
 root=Path(__file__).resolve().parent;assets=root/'assets';build=root/'.build'
 assets.mkdir(exist_ok=True);build.mkdir(exist_ok=True)
 plan=json.loads((root/'edit-plan.json').read_text());fps=plan['fps'];keep=plan['keep_frames']
 def run(*args):subprocess.run(['ffmpeg','-nostdin','-y','-hide_banner','-loglevel','error','-xerror',*map(str,args)],check=True)
 run('-i',original,'-vn','-ac',2,'-ar',48000,'-c:a','pcm_s16le',build/'original-audio.wav')
 with wave.open(str(build/'original-audio.wav'),'rb') as f:
  rate=f.getframerate();channels=f.getnchannels();data=array.array('h',f.readframes(f.getnframes()))
 with wave.open(str(assets/'speech-cut.wav'),'wb') as f:
  f.setparams((channels,2,rate,0,'NONE','not compressed'))
  for a,b in keep:
   chunk=data[round(a/fps*rate)*channels:round(b/fps*rate)*channels]
   nf=min(round(.006*rate),len(chunk)//channels//2)
   for i in range(nf):
    gain=i/max(1,nf-1)
    for ch in range(channels):
     chunk[i*channels+ch]=round(chunk[i*channels+ch]*gain)
     j=len(chunk)-(i+1)*channels+ch;chunk[j]=round(chunk[j]*gain)
   f.writeframes(chunk.tobytes())
 expr='+'.join(f'between(n,{a},{b-1})' for a,b in keep)
 filt=build/'cut-filter.txt';filt.write_text(f"fps={fps},select='{expr}',setpts=N/({fps}*TB),setsar=1")
 run('-threads',2,'-i',original,'-an','-filter_script:v',filt,'-r',fps,'-fps_mode','cfr','-c:v','libx264','-preset','veryfast','-crf',18,'-g',fps,'-keyint_min',fps,'-threads',4,'-pix_fmt','yuv420p','-movflags','+faststart',assets/'speech-cut.mp4')
 correction=json.loads((root/'color-correction.json').read_text())
 run('-i',root/correction['source'],'-an','-vf',correction['filters'],'-c:v','libx264','-preset','veryfast','-crf',18,'-g',fps,'-keyint_min',fps,'-threads',4,'-pix_fmt','yuv420p','-movflags','+faststart',root/correction['output'])
 print('Media prepared. Run npm run check, then npm run render.')

if __name__=='__main__':main()
