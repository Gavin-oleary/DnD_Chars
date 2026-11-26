from PIL import Image, ImageDraw
import sys
out=sys.argv[1]
for n in ['agmundr','nyxen']:
    cols=[('8k clay F',out+'\\'+n+'\\clay_FRONT.png'),('new clay F',out+'\\'+n+'_new\\clay_FRONT.png'),('new tex F',out+'\\'+n+'_new\\textured_FRONT.png'),('8k clay R',out+'\\'+n+'\\clay_RIGHT.png'),('new clay R',out+'\\'+n+'_new\\clay_RIGHT.png'),('new tex FL',out+'\\'+n+'_new\\textured_FRONT-LEFT.png')]
    ims=[]
    for lab,p in cols:
        im=Image.open(p).convert('RGB');im=im.resize((int(im.width*900/im.height),900));ims.append((lab,im))
    W=sum(i.width for _,i in ims)+10*len(ims);s=Image.new('RGB',(W,930),(30,30,30));d=ImageDraw.Draw(s);x=0
    for lab,im in ims:
        s.paste(im,(x,30));d.text((x+6,8),n+'  '+lab,fill=(255,255,255));x+=im.width+10
    s.save(out+'\\SHEET_'+n+'_new.png')
print('ok')
