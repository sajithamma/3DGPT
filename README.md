# 3DGPT

## Generate GLB file, from the shell
```bash
/Applications/Blender.app/Contents/MacOS/Blender -b -P script.py
```

## The Code to Generate GLB file
```python

# Set output path for the .glb file
output_path = "output_scene.glb"
bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB', export_animations=True)

```

```bash
## Run any web server to serve
 python3 -m http.server 9999
```