from PIL import Image, ImageDraw
import sys
d=sys.argv[1]
cols=[]
q=d+r'\quad+topo\quad\assessment'; k=d+r'\quad+topo\TOPO_QUAD_8K\assessment'
for label,p in [('50k quad clay F', q+r'\clay_FRONT.png'),('8k quad clay F', k+r'\clay_FRONT.png'),('50k quad clay R', q+r'\clay_RIGHT.png'),('8k quad clay R', k+r'\clay_RIGHT.png'),('50k quad clay B', q+r'\clay_BACK.png'),('8k quad clay B', k+r'\clay_BACK.png'),('8k quad tex F', k+r'\textured_FRONT.png'),('8k quad tex FL', k+r'\textured_FRONT-LEFT.png')]:
    im=Image.open(p).convert('RGB'); im=im.resize((int(im.width*900/im.height),900)); cols.append((label,im))
W=sum(c[1].width for c in cols)+10*len(cols); sheet=Image.new('RGB',(W,930),(40,40,40)); x=0; dr=ImageDraw.Draw(sheet)
for label,im in cols:
    sheet.paste(im,(x,30)); dr.text((x+6,8),label,fill=(255,255,255)); x+=im.width+10
sheet.save(d+r'\quad+topo\sheet_50k_vs_8k.png'); print(sheet.size)
