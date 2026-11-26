from PIL import Image, ImageDraw
import sys
d=sys.argv[1]
cols=[]
for label,p in [('2M tri clay', d+r'\assessment_pbr\clay_FRONT.png'),('50k quad clay', d+r'\quad+topo\quad\assessment\clay_FRONT.png'),('9.6k topo clay', d+r'\quad+topo\topo\assessment\clay_FRONT.png'),('2M tri tex', d+r'\assessment_pbr\textured_FRONT.png'),('50k quad tex', d+r'\quad+topo\quad\assessment\textured_FRONT.png'),('9.6k topo tex', d+r'\quad+topo\topo\assessment\textured_FRONT.png'),('50k quad R', d+r'\quad+topo\quad\assessment\clay_RIGHT.png'),('9.6k topo R', d+r'\quad+topo\topo\assessment\clay_RIGHT.png'),('50k quad back', d+r'\quad+topo\quad\assessment\clay_BACK.png'),('9.6k topo back', d+r'\quad+topo\topo\assessment\clay_BACK.png')]:
    im=Image.open(p).convert('RGB'); im=im.resize((int(im.width*900/im.height),900)); cols.append((label,im))
W=sum(c[1].width for c in cols)+10*len(cols); sheet=Image.new('RGB',(W,930),(40,40,40)); x=0; dr=ImageDraw.Draw(sheet)
for label,im in cols:
    sheet.paste(im,(x,30)); dr.text((x+6,8),label,fill=(255,255,255)); x+=im.width+10
sheet.save(d+r'\quad+topo\sheet_quad_vs_topo_vs_2M.png')
print(sheet.size)
