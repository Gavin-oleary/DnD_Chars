from PIL import Image, ImageDraw
import sys, json, os
out=sys.argv[1]; sets=json.load(open(out+'\\sets.json'))
for n,a in sets:
    cols=[('2M clay F',a+r'\clay_FRONT.png'),('8k clay F',out+'\\'+n+r'\clay_FRONT.png'),('8k tex F',out+'\\'+n+r'\textured_FRONT.png'),('2M clay R',a+r'\clay_RIGHT-PROFILE.png'),('8k clay R',out+'\\'+n+r'\clay_RIGHT.png'),('8k clay B',out+'\\'+n+r'\clay_BACK.png'),('8k tex FL',out+'\\'+n+r'\textured_FRONT-LEFT.png')]
    ims=[]
    for lab,p in cols:
        if not os.path.exists(p): continue
        im=Image.open(p).convert('RGB'); im=im.resize((int(im.width*900/im.height),900)); ims.append((lab,im))
    W=sum(i.width for _,i in ims)+10*len(ims); s=Image.new('RGB',(W,930),(30,30,30)); d=ImageDraw.Draw(s); x=0
    for lab,im in ims:
        s.paste(im,(x,30)); d.text((x+6,8),n+'  '+lab,fill=(255,255,255)); x+=im.width+10
    s.save(out+'\\SHEET_'+n+'.png')
    st=json.load(open(out+'\\'+n+r'\stats.json'))[0]
    print(n, 'faces',st['faces'],'quads',st['quads'],'tris',st['tris'],'shells',st['components'],'nonmanifold',st['non_manifold_edges'],'boundary',st['boundary_edges'],'dims',st['dimensions'])
