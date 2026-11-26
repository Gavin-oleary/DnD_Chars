$R='C:\Users\olear\Pictures\Screenshots\characters'
$SHEET='Z:\characters\production\character_pipeline\characters\HERO-NY\08_review\base_first\fit_v007\sheet.py'
$py='C:\Users\olear\miniconda3\python.exe'
$sets=@(
 @{n='agmundr';p="$R\agmundr\assessment_pbr";ref="$R\agmundr\ref";f='FRONT.png';fl='LEFT-FRONT.png';r='RIGHT-PROFILE.png';b='BACK.png'},
 @{n='rose';p="$R\rose\assessment_pbr";ref="$R\rose\ref";f='FRONT.png';fl='FRONT-LEFT.png';r='PROFILE_RIGHT.png';b='BACK.png'},
 @{n='lilith_adult';p="$R\Lilith\adult\assessment_pbr";ref="$R\Lilith\adult\ref";f='FRONT.png';fl='FRONT-LEFT.png';r='PROFILE-RIGHT.png';b='BACK.png'},
 @{n='lilith_kid';p="$R\Lilith\kid\assessment_pbr";ref="$R\Lilith\kid\ref";f='FRONT.png';fl='FRONT-LEFT.png';r='PROFILE-RIGHT.png';b='BACK.png'},
 @{n='sylas_adult';p="$R\Sylas\adult\assessment_pbr";ref="$R\Sylas\adult\ref";f='FRONT.png';fl='LEFT-FRONT.png';r='RIGHT-PROFILE.png';b='BACK.png'},
 @{n='sylas_kid';p="$R\Sylas\kid\assessment_pbr";ref="$R\Sylas\kid\REF";f='FRONT.png';fl='FRONT-LEFT.png';r='RIGHT-PROFILE.png';b='BACK.png'}
)
foreach ($s in $sets) {
  $p=$s.p; $ref=$s.ref
  & $py $SHEET "$R\sheet_$($s.n).png" 620 "clay FRONT=$p\clay_FRONT.png" "ref FRONT=$ref\$($s.f)" "clay FRONT-LEFT=$p\clay_FRONT-LEFT.png" "ref=$ref\$($s.fl)" "clay RIGHT=$p\clay_RIGHT-PROFILE.png" "ref RIGHT=$ref\$($s.r)" "clay BACK=$p\clay_BACK.png" "ref BACK=$ref\$($s.b)"
}
