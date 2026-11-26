# DnD_Chars

This repo holds 3D character models for a Dungeons & Dragons cast. The models were generated with Rodin from multi-view reference images. The repo stores the images and text around them: reference views, texture sets, review renders and assessment sheets. The mesh files themselves stay on the local working copy (see [What is not in the repo](#what-is-not-in-the-repo)).

## Characters

| Character | Folder | Current-gen exports |
|---|---|---|
| Agmundr | `Agmundr/` | 2M, 200K quad |
| Astaroth | `Astaroth/` | 2M, 200K quad, 10K n-gon, BANG 200K quad |
| Lilith (adult) | `Lilith/` | 2M, 200K quad, BANG 200K quad |
| Lilith (kid) | `lilith-kid/` | none yet |
| Nyxen | `Nyxen/` | 2M, 200K quad |
| Rose | `Rose/` | 2M, 200K quad |
| Sylas (adult) | `Sylas/` | 2M, 200K quad |
| Sylas (kid) | `Sylas-kid/` | none yet |
| Umbral serpent | `Umbral_serpent/` | none yet |

The number in an export name is its polygon budget. "Quad" and "n-gon" give the face type of the remeshed version. A BANG export is a parts breakdown of the model.

Every character also has an older generation folder (see below). Umbral serpent has only that.

## Character folder layout

```
<Character>/
  references/                 turnaround views: front, front three-quarter, back, left and right profile
  <Character>_OBJ_<budget>/   one folder per current-gen export
  assesments/                 review and comparison sheets for the current-gen exports
  _OLD_GEN_2026-11-22_to_24/  earlier generations, kept for comparison
```

**references/** holds the reference images for the character. Sylas also has a full turnaround sheet here.

**\<Character\>_OBJ_\<budget\>/** holds the texture set for one export: `texture_diffuse`, `texture_metallic`, `texture_normal`, `texture_roughness` and `texture_pbr`, plus a `shaded.png` preview. The matching `base.obj` is local only.

**assesments/** holds the sheets used to judge each export. These include export reviews, single-view reviews of the 2M meshes, comparison sheets between passes, ID-prep sheets, and for Nyxen a series of DAZ review renders.

**_OLD_GEN_2026-11-22_to_24/** holds the work from November 22 to 24, 2026. The pipeline has changed since then, so these sets are older and are kept for comparison only. A typical old-gen folder has:

- `ref/`: the reference images used for that generation
- `OBJ/`, `FBX/`: export folders, with their texture PNGs in the repo and the meshes local
- `GLB/`, `USDZ/`: export folders that are local only
- `QUAD_8K+TOPO/`: quad and topology passes with 8K textures
- `assessment_pbr/`: PBR assessment renders and their JSON results
- `_quad_assessment/`: assessment sheets, logs and stats for the quad, topology and 50K runs
- `sheet_<character>.png`: the character's overview sheet from that round

Folder names inside old-gen sets were kept as they were when the work was done, so their capitalization varies.

## Top-level files

- `_OLD_GEN_2026-11-22_to_24_shared_pipeline/`: the PowerShell and Python scripts that produced the old-gen assessment sheets, including `fbx_to_obj.py`, plus the shared run logs and stats summaries.
- `cast_faces.jpg`: a face sheet across the cast.

## What is not in the repo

`.gitignore` excludes the model binaries: `.obj`, `.fbx`, `.glb`, `.usdz`, `.blend`, `.blend1` and `.iAvatar`. Together they come to about 7.5 GB, and 26 of them are over GitHub's 100 MB file limit. They remain in the local working copy next to their textures.

`_FINAL_CANDIDATES/` holds the current candidate for Agmundr, Astaroth, Lilith, Nyxen, Rose and Sylas. The repo has a preview image for each one, and the candidate FBX files are local only.
