$B='C:\Program Files\Blender Foundation\Blender 5.3\blender.exe'
$R='C:\Users\olear\Pictures\Screenshots\characters'
$S="$R\asteroth\assess_glb.py"
$jobs=@(
 @{n='agmundr';g="$R\agmundr\glb\base_basic_pbr.glb";o="$R\agmundr\assessment_pbr"},
 @{n='rose';g="$R\rose\GLB\base_basic_pbr.glb";o="$R\rose\assessment_pbr"},
 @{n='lilith_adult';g="$R\Lilith\adult\GLB\base_basic_pbr.glb";o="$R\Lilith\adult\assessment_pbr"},
 @{n='lilith_kid';g="$R\Lilith\kid\GLB\base_basic_pbr.glb";o="$R\Lilith\kid\assessment_pbr"},
 @{n='sylas_adult';g="$R\Sylas\adult\GLB\base_basic_pbr.glb";o="$R\Sylas\adult\assessment_pbr"},
 @{n='sylas_kid';g="$R\Sylas\kid\GLB\base_basic_pbr.glb";o="$R\Sylas\kid\assessment_pbr"}
)
foreach ($j in $jobs) {
  & $B -b --factory-startup --python $S -- $j.g $j.o 2>&1 | Select-String 'ASSESS|Traceback' | Out-File "$($j.o)_log.txt"
}
'ALLDONE' | Out-File "$R\assess_all_done.txt"
