$b='C:\Program Files\Blender Foundation\Blender 5.0\blender.exe'
$root='C:\Users\olear\Pictures\Screenshots\characters'
$py="$root\asteroth\quad+topo\assess_fbx.py"
$sets=@(
 @{n='agmundr';   f="$root\agmundr\QUAD_8K+TOPO\base_basic_pbr.fbx";        a="$root\agmundr\assessment_pbr"},
 @{n='nyxen';     f="$root\nyxen\QUAD_8K+TOPO\base_basic_pbr.fbx";          a="$root\nyxen\assessment_pbr"},
 @{n='rose';      f="$root\rose\QUAD_8K+TOPO\base_basic_pbr.fbx";           a="$root\rose\assessment_pbr"},
 @{n='sylas_adult';f="$root\Sylas\adult\QUAD_8K+TOPO\base_basic_pbr.fbx";   a="$root\Sylas\adult\assessment_pbr"},
 @{n='sylas_kid'; f="$root\Sylas\kid\QUAD_8K+TOPO\base_basic_pbr.fbx";      a="$root\Sylas\kid\assessment_pbr"},
 @{n='lilith_adult_quad';f="$root\Lilith\adult\QUAD_8K+TOPO\quad\base_basic_pbr.fbx"; a="$root\Lilith\adult\assessment_pbr"},
 @{n='lilith_adult_topo';f="$root\Lilith\adult\QUAD_8K+TOPO\topo\base_basic_pbr.fbx"; a="$root\Lilith\adult\assessment_pbr"},
 @{n='lilith_kid_quad';f="$root\Lilith\kid\QUAD_8K+TOPO\quad\base_basic_pbr.fbx";     a="$root\Lilith\kid\assessment_pbr"},
 @{n='lilith_kid_topo';f="$root\Lilith\kid\QUAD_8K+TOPO\topo\base_basic_pbr.fbx";     a="$root\Lilith\kid\assessment_pbr"}
)
$out="$root\_quad_assessment"
New-Item -ItemType Directory -Force -Path $out | Out-Null
foreach ($s in $sets) {
  $o="$out\$($s.n)"
  & $b -b --factory-startup --python $py -- $s.f $o > "$o`_log.txt" 2> "$o`_err.txt"
}
$sheet=@'
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
'@
Set-Content "$out\sheets.py" $sheet
$pairs = @(); foreach ($s in $sets) { $pairs += ,@($s.n,$s.a) }
$json = '[' + (($pairs | ForEach-Object { '["' + $_[0] + '","' + ($_[1] -replace '\\','\\\\') + '"]' }) -join ',') + ']'
Set-Content "$out\sets.json" $json
python "$out\sheets.py" $out > "$out\stats_summary.txt" 2>&1
'DONE' | Set-Content "$out\DONE.txt"
