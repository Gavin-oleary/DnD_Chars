$b='C:\Program Files\Blender Foundation\Blender 5.0\blender.exe'
$r='C:\Users\olear\Pictures\Screenshots\characters'
$py="$r\asteroth\quad+topo\assess_fbx.py"
$out="$r\_quad_assessment"
$sets=@(
 @{n='sylas_adult_50k'; d="$r\Sylas\adult\QUAD_8K+TOPO"; a="$r\Sylas\adult\assessment_pbr"},
 @{n='sylas_kid_50k';   d="$r\Sylas\kid\QUAD_8K+TOPO";   a="$r\Sylas\kid\assessment_pbr"},
 @{n='lilith_adult_50k';d="$r\Lilith\adult\QUAD_8K+TOPO\quad"; a="$r\Lilith\adult\assessment_pbr"},
 @{n='lilith_kid_50k';  d="$r\Lilith\kid\QUAD_8K+TOPO\quad";   a="$r\Lilith\kid\assessment_pbr"},
 @{n='serpent_50k';     d="$r\Umbral_serpent\fbx";       a=""}
)
foreach ($s in $sets) {
  & $b -b --factory-startup --python $py -- "$($s.d)\base_basic_pbr.fbx" "$out\$($s.n)" > "$out\$($s.n)_log.txt" 2> "$out\$($s.n)_err.txt"
  if (-not (Test-Path "$($s.d)\base.obj")) { & $b -b --factory-startup --python "$r\fbx_to_obj.py" -- "$($s.d)\base.fbx" "$($s.d)\base.obj" > "$out\$($s.n)_obj.txt" 2>&1 }
}
$sheet=@'
from PIL import Image, ImageDraw
import sys, json, os
out=sys.argv[1]
sets=[('sylas_adult_50k',r'C:\Users\olear\Pictures\Screenshots\characters\Sylas\adult\assessment_pbr'),('sylas_kid_50k',r'C:\Users\olear\Pictures\Screenshots\characters\Sylas\kid\assessment_pbr'),('lilith_adult_50k',r'C:\Users\olear\Pictures\Screenshots\characters\Lilith\adult\assessment_pbr'),('lilith_kid_50k',r'C:\Users\olear\Pictures\Screenshots\characters\Lilith\kid\assessment_pbr'),('serpent_50k','')]
for n,a in sets:
    cols=[('2M clay F',a+r'\clay_FRONT.png'),('50k clay F',out+'\\'+n+r'\clay_FRONT.png'),('50k tex F',out+'\\'+n+r'\textured_FRONT.png'),('2M clay R',a+r'\clay_RIGHT-PROFILE.png'),('50k clay R',out+'\\'+n+r'\clay_RIGHT.png'),('50k clay B',out+'\\'+n+r'\clay_BACK.png'),('50k tex FL',out+'\\'+n+r'\textured_FRONT-LEFT.png')]
    ims=[]
    for lab,p in cols:
        if not a and lab.startswith('2M'): continue
        if not os.path.exists(p): continue
        im=Image.open(p).convert('RGB'); im=im.resize((int(im.width*900/im.height),900)); ims.append((lab,im))
    W=sum(i.width for _,i in ims)+10*len(ims); s=Image.new('RGB',(W,930),(30,30,30)); d=ImageDraw.Draw(s); x=0
    for lab,im in ims:
        s.paste(im,(x,30)); d.text((x+6,8),n+'  '+lab,fill=(255,255,255)); x+=im.width+10
    s.save(out+'\\SHEET_'+n+'.png')
    st=json.load(open(out+'\\'+n+r'\stats.json'))
    for m in st: print(n, m['name'],'faces',m['faces'],'quads',m['quads'],'tris',m['tris'],'shells',m['components'],'boundary',m['boundary_edges'],'dims',m['dimensions'],'imgs',m.get('images'))
'@
Set-Content "$out\sheets_r3.py" $sheet
python "$out\sheets_r3.py" $out > "$out\stats_r3.txt" 2>&1
'DONE' | Set-Content "$out\DONE_r3.txt"
