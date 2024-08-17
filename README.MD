# Deprecation
This repository will no longer be maintained, as NieR2Blender and Blender2NieR were combined into one plugin. **[I'm now working on a fork of NieR2Blender2NieR, so use that!](https://github.com/cabalex/NieR2Blender2NieR/)**

![AstralChain2Blender](https://user-images.githubusercontent.com/31020729/113838468-a31b2400-9743-11eb-854a-b348fadf3963.png)
<br>
Want to import models back into the game? **[The exporter is here.](https://github.com/cabalex/Blender2NieR)**

<br>

Fork of WoefulWolf's [Nier2Blender 2.8](https://github.com/WoefulWolf/NieR2Blender_2_8) repository that adds Astral Chain support.

<br>

## Why does the original add-on not work with Astral Chain's files?
While the model format and much of the .DAT/.DTT format are similar, if not identical, the texture formats are completely different. Since Astral Chain is made for the Switch, while NieR isn't, it relies on a different texture compression method known as ASTC for many of its textures. ASTC and NieR's texture format (.DDS) are not compatible, and hence the original addon doesn't load textures properly when importing a model from Astral Chain. Along with this, the Switch swizzles its textures, so the textures from AC must be unswizzled in order to be used. This add-on (in theory) should fix this.
<br>
There are some other differences (the last file table in the .WTA, the way .DAT/.DTTs are packed, how header data is dealt with, etc), but those are the main points.
<br>


## Notable things
* **Note: Some models contain DDS BC6H textures, which the converter does not auto-convert.** Blender will not load these (as they are DX10, which Blender does not support), but it's easy to convert it with something like `texconv`. Blender2AstralChain will not autoconvert these back either, so make sure to convert them back to DX10 if you're modding!
  * This add-on sets DDS mipmap counts to 1 (any more and Blender/other image editors will crash). This is probably because the mip map count in the WTA and the actual mip map count can be completely inaccurate, causing many programs that load DDS files to try and read parts of the file that aren't there, causing a crash. I'm not entirely sure why the mip map counts are desynced, but this shouldn't affect much as the exporter is built around this.
* The add-on converts the ASTC textures to PNG; keep this in mind when editing.
* I include `astcenc-avx2.exe` from the [ASTC Encoder](https://github.com/ARM-software/astc-encoder) for decoding ASTC textures, which might not be compatible with many systems. If it doesn't work, you can try replacing the EXE with one that does. The EXE is called in `wmb_importer.py` around line ~598.
* Exporting to OBJ/FBX "works", but I have not modified the existing code there. It probably needs to be changed to include PNG support, but it doesn't throw any errors in my testing (?).
* This addon should still work with NieR models, but I'm not completely sure as I do not own NieR.

### Some credits/ported code
* [WoefulWolf](https://github.com/WoefulWolf) and other contributors to [Nier2Blender](https://github.com/WoefulWolf/NieR2Blender_2_8)
* [aboood40091's BNTX-Extractor](https://github.com/aboood40091/BNTX-Extractor)
* [KillzXGaming's Switch Toolbox](https://github.com/KillzXGaming/Switch-Toolbox)
* The [ASTC Encoder](https://github.com/ARM-software/astc-encoder) included

<br>![Sword Legion](https://user-images.githubusercontent.com/31020729/113498031-19a6f000-94be-11eb-9092-45f519d64c57.png)

* Some useful folders in pkz [(main documentation here)](https://docs.google.com/spreadsheets/d/1qTOnFUdTfPtXfizpqoj2IbcLhTCJWRiF9MI3N8wiP3U/edit?usp=sharing)<br>
    /pl -> human models<br>
    /wp -> weapon models<br>
    /ba /bg /bh -> environment models<br>
    /em -> chimera/legion models<br>
