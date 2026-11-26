from PIL import Image, ImageDraw
import sys
out=sys.argv[1];root=sys.argv[2]
for n in ['rose','agmundr','nyxen']:
    a=root+'\\'+n+'\\assessment_pbr'
    cols=[('2M clay F',a+'\\clay_FRONT.png'),('50k clay F',out+'\\'+n+'_50k\\clay_FRONT.png'),('50k tex F',out+'\\'+n+'_50k\\textured_FRONT.png'),('2M clay R',a+'\\clay_RIGHT-PROFILE.png'),('50k clay R',out+'\\'+n+'_50k\\clay_RIGHT.png'),('50k clay B',out+'\\'+n+'_50k\\clay_BACK.png'),('50k tex FL',out+'\\'+n+'_50k\\textured_FRONT-LEFT.png')]
    ims=[]
    for lab,p in cols:
        im=Image.open(p).convert('RGB');im=im.resize((int(im.width*900/im.height),900));ims.append((lab,im))
    W=sum(i.width for _,i in ims)+10*len(ims);s=Image.new('RGB',(W,930),(30,30,30));d=ImageDraw.Draw(s);x=0
    for lab,im in ims:
        s.paste(im,(x,30));d.text((x+6,8),n+'  '+lab,fill=(255,255,255));x+=im.width+10
    s.save(out+'\\SHEET_'+n+'_50k.png')
print('ok')
