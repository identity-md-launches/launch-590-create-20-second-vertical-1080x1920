"""Dependency-free pixel animation and chip synthesizer. Run from repository root."""
import math, struct, wave, subprocess, os
W,H,FPS=270,480,30
GREEN=(104,255,139); GOLD=(255,211,80)
FONT={}
patterns={'A':'010/101/111/101/101','B':'110/101/110/101/110','C':'011/100/100/100/011','D':'110/101/101/101/110','E':'111/100/110/100/111','F':'111/100/110/100/100','G':'011/100/101/101/011','H':'101/101/111/101/101','I':'111/010/010/010/111','J':'001/001/001/101/010','K':'101/101/110/101/101','L':'100/100/100/100/111','M':'10001/11011/10101/10001/10001','N':'1001/1101/1011/1001/1001','O':'010/101/101/101/010','P':'110/101/110/100/100','Q':'010/101/101/111/011','R':'110/101/110/101/101','S':'011/100/010/001/110','T':'111/010/010/010/010','U':'101/101/101/101/111','V':'101/101/101/101/010','W':'10001/10001/10101/11011/10001','X':'101/101/010/101/101','Y':'101/101/010/010/010','Z':'111/001/010/100/111','?':'110/001/010/000/010','.':'0/0/0/0/1','0':'111/101/101/101/111','1':'010/110/010/010/111','%':'101/001/010/100/101','-':'000/000/111/000/000','>':'100/010/001/010/100'}
patterns.update({'2':'110/001/010/100/111','3':'110/001/010/001/110','4':'101/101/111/001/001','5':'111/100/110/001/110','6':'011/100/110/101/010','7':'111/001/010/010/010','8':'010/101/010/101/010','9':'010/101/011/001/110'})
FONT={k:v.split('/') for k,v in patterns.items()}
def rect(x,y,w,h,c):
 x,y,w,h=map(int,(x,y,w,h)); x0=max(0,x); x1=min(W,x+w)
 if x1<=x0:return
 row=bytes(c)*(x1-x0)
 for yy in range(max(0,y),min(H,y+h)): buf[(yy*W+x0)*3:(yy*W+x1)*3]=row

def text(s,y,scale=2,c=GREEN,x=None):
 s=s.upper(); width=sum((len(FONT.get(ch,['000'])[0])+1)*scale for ch in s)-scale
 if x is None:x=(W-width)//2
 for ch in s:
  rows=FONT.get(ch,['000']*5)
  for j,row in enumerate(rows):
   for i,p in enumerate(row):
    if p=='1':rect(x+i*scale,y+j*scale,scale,scale,c)
  x+=(len(rows[0])+1)*scale

def coin(x,y,r,spin=1):
 rx=max(2,int(r*abs(spin)))
 for yy in range(-r,r+1):
  extent=int(rx*math.sqrt(max(0,1-(yy/r)**2)))
  rect(x-extent,y+yy,2*extent+1,1,(126,80,24) if abs(yy)>r-3 else GOLD)
 rect(x-rx//2,y-r+4,max(1,rx//3),2,(255,245,169))
 if rx>r*.55:text('?',y-5,2,(124,76,25),x-3)

def pepe(x,y,s=1,variant=0,wink=False,pocket=False):
 # Block-built original frog portrait: bulging eyes, wide mouth, shirt and thumb.
 skin=[(72,181,91),(67,158,140),(129,181,66),(62,133,92),(126,127,193),(167,148,67)][variant%6]
 def R(a,b,c,d,col):rect(x+a*s,y+b*s,c*s,d*s,col)
 dark=(13,50,32)
 R(-20,8,40,35,dark); R(-17,6,34,31,skin);R(-22,20,44,12,skin)
 R(-16,2,14,13,dark);R(2,2,14,13,dark)
 R(-14,4,10,10,(227,240,197));R(4,4,10,10,(227,240,197))
 R(-10,7,4,6,(10,19,17))
 if wink:R(5,9,8,2,dark)
 else:R(7,7,4,6,(10,19,17))
 R(-14,23,29,3,dark);R(-12,27,25,3,(158,67,67));R(-8,31,18,2,dark)
 shirt=[(44,78,125),(122,54,119),(43,102,87)][variant%3]
 R(-21,39,42,21,shirt);R(-16,43,5,14,(70,111,142))
 R(20,36,10,7,skin);R(26,29 if not pocket else 43,5,14,skin)
 if variant%3==1:R(-20,-2,40,5,(200,86,143));R(-12,-13,24,12,(139,52,105))
 if variant%3==2:R(-18,-3,36,5,(76,158,217));R(-15,-10,29,8,(42,97,146));R(17,-3,10,4,(76,158,217))

def audio(path):
 rate=44100; notes=[64,67,71,74,71,67,62,67,69,72,76,79,76,72,67,62]
 with wave.open(path,'wb') as out:
  out.setparams((2,2,rate,0,'NONE','not compressed')); data=bytearray()
  for n in range(rate*20):
   t=n/rate; beat=t%0.5; step=int(t/.25); phase=t%.25
   freq=440*2**((notes[step%16]-69)/12)
   env=max(0,1-phase/.22); lead=(1 if (t*freq)%1<.25 else -1)*env*.075*(min(1,t/4))
   bassfreq=440*2**(([40,40,45,43][int(t/2)%4]-69)/12)
   bass=(1 if (t*bassfreq)%1<.5 else -1)*.045*max(0,1-beat/.42)
   kick=math.sin(2*math.pi*(45*beat+8*(1-math.exp(-beat*30))))*math.exp(-beat*28)*.13
   flip=t%1; ting=0
   if t<10 and flip<.2:ting=(math.sin(2*math.pi*1760*flip)+.4*math.sin(2*math.pi*3520*flip))*math.exp(-flip*24)*.14
   rise=.03*math.sin(2*math.pi*(400*t+60*max(0,t-10)**2)) if 10<t<15 else 0
   fade=min(1,t/.1,(20-t)/.3); v=int(max(-1,min(1,(lead+bass+kick+ting+rise)*fade))*32767)
   data+=struct.pack('<hh',v,v)
  out.writeframes(data)

os.makedirs('artifacts',exist_ok=True)
audio('/tmp/swarmpepe-audio.wav')
p=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','270x480','-framerate','30','-i','pipe:0','-i','/tmp/swarmpepe-audio.wav','-vf','split[a][b];[b]gblur=sigma=2[bloom];[a][bloom]blend=all_mode=screen:all_opacity=0.20,scale=1080:1920:flags=neighbor','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t','20','-movflags','+faststart','artifacts/video.mp4'],stdin=subprocess.PIPE)
for frame in range(600):
 t=frame/FPS;buf=bytearray(bytes((3,10,9))*(W*H))
 # Restrained CRT border and animated green phosphor dust.
 rect(8,8,254,1,(24,67,41));rect(8,471,254,1,(24,67,41));rect(8,8,1,464,(24,67,41));rect(261,8,1,464,(24,67,41))
 for i in range(34):
  xx=(i*83+17)%248+11; yy=(i*137+int(t*3))%446+16
  rect(xx,yy,1,1,(18,46,32))
 if t>=4:text('SWARM PEPES',35,3);text('FULLY ONCHAIN',59,1,(53,126,78))
 if t<4:
  pepe(126,263,2); cy=313-95*math.sin(math.pi*(t%1))
  coin(188,int(cy),8,math.cos(t*math.pi*4))
 elif t<10:
  count=min(9,1+int((t-4)/.6))
  for i in range(count):
   x=52+(i%3)*82;y=141+(i//3)*96
   pepe(x,y,1,i);coin(x+28,int(y+31-24*math.sin(math.pi*(t%1))),7,math.cos(t*math.pi*4+i*.2))
  text('SOMETHING IS LOADING',437,2,(73,159,97))
 elif t<15:
  u=(t-10)/5
  for i in range(9):
   x=52+(i%3)*82;y=141+(i//3)*96
   pepe(x,y,1,i)
   if u<.65:
    a=min(1,u/.65);coin(int((x+28)*(1-a)+135*a),int((y+5)*(1-a)+210*a),7,math.cos(t*8))
  coin(135,210,int(12+38*min(1,u/.65)),math.cos((t-10)*7))
  rect(23,383,224,58,(3,17,12));text('TESTNET -> MAINNET',392,2)
  rect(28,414,214,10,(34,81,48));rect(30,416,int(210*u),6,GREEN)
  text(str(int(u*100))+'%',431,1,GREEN)
  if frame%37 in (0,1):rect(10,104,250,3,(107,196,131));rect(13,258,241,2,(63,122,86))
 else:
  coin(135,203,50,1); # Final coin remains blank except mystery question mark.
  for i in range(8):
   a=i*math.pi/4+t*.12; x=135+int(math.cos(a)*69);y=203+int(math.sin(a)*69)
   rect(x-2,y,5,1,GOLD);rect(x,y-2,1,5,GOLD)
  text('IMD MAINNET',300,4);text('IS COMING',330,4);text('swarmpepe.xyz',373,2,(102,204,131))
  text('TESTNET -> MAINNET',99,2);rect(40,120,190,7,GREEN);text('100%',137,1)
  pocket=t>=19.4;pepe(134,408,1,0,t>=19.0,pocket)
  if not pocket:coin(164,int(436-12*math.sin(max(0,t-18)*math.pi)),6,1)
 # Scanline attenuation preserves the native chunky pixels.
 for yy in range(1,H,3):
  start=yy*W*3
  buf[start:start+W*3]=bytes(v*84//100 for v in buf[start:start+W*3])
 p.stdin.write(buf)
p.stdin.close()
if p.wait():raise SystemExit('encode failed')
print('Created artifacts/video.mp4')
