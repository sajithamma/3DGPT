import bpy
import random

# Clear existing objects and animation data
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 200

clear_scene()

# Add a camera and set its position and orientation
bpy.ops.object.camera_add(location=(5, -10, 5))
camera = bpy.context.object
camera.name = "Camera"
camera.rotation_euler = (1.109, 0, 0.785)  # Adjust rotation to point at the objects

# Set the camera as the active camera
bpy.context.scene.camera = camera

# Parameters
input_size = (32, 32)  # 32x32 input layer matrix
output_size = 10       # 10 nodes in the output layer
cube_size = 0.1        # Size of each cube

# Positions
input_start = (-2, -1, -1)  # Adjusted to position in 3D
output_start = (4, 0, 0)    # Starting position for the output layer
highlight_index = 2         # Index for the highlighted output cube (for digit "2")

# Create a green material for the signal spheres
green_material = bpy.data.materials.new(name="GreenMaterial")
green_material.diffuse_color = (0, 1, 0, 1)  # Simple green color without glow

# Create the 32x32 Input Layer (3D layout)
input_nodes = []
for i in range(input_size[0]):
    for j in range(input_size[1]):
        if i % 4 == 0 and j % 4 == 0:  # Only create every 4th node to reduce complexity
            bpy.ops.mesh.primitive_cube_add(size=cube_size, location=(input_start[0], input_start[1] + i * cube_size * 1.5, input_start[2] + j * cube_size * 1.5))
            cube = bpy.context.object
            cube.name = f"Input_Node_{i}_{j}"
            input_nodes.append(cube)

# Create the 1x10 Output Layer (Aligned horizontally)
output_nodes = []
for i in range(output_size):
    bpy.ops.mesh.primitive_cube_add(size=cube_size, location=(output_start[0], output_start[1] + i * cube_size * 2, output_start[2]))
    cube = bpy.context.object
    cube.name = f"Output_Node_{i}"
    output_nodes.append(cube)

    # Highlight the third cube to represent "2"
    if i == highlight_index:
        mat = bpy.data.materials.new(name="Highlight")
        mat.diffuse_color = (1, 0, 0, 1)  # Red color
        cube.data.materials.append(mat)

# Add connections between input and output nodes
connections = []
for input_node in input_nodes:
    for output_node in output_nodes:
        # Create a curve for each connection
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.curve.primitive_bezier_curve_add()
        curve = bpy.context.object
        curve.name = f"Connection_{input_node.name}_to_{output_node.name}"
        
        # Set curve to have two points: start at input_node, end at output_node
        curve.data.splines[0].bezier_points[0].co = input_node.location
        curve.data.splines[0].bezier_points[1].co = output_node.location

        # Adjust control points to curve the line smoothly
        mid_y = (input_node.location[1] + output_node.location[1]) / 2
        mid_z = (input_node.location[2] + output_node.location[2]) / 2
        curve.data.splines[0].bezier_points[0].handle_right.y = mid_y
        curve.data.splines[0].bezier_points[0].handle_right.z = mid_z
        curve.data.splines[0].bezier_points[1].handle_left.y = mid_y
        curve.data.splines[0].bezier_points[1].handle_left.z = mid_z
        curve.data.bevel_depth = 0.002  # Thickness of the line

        # Store connection information for signal animation
        connections.append((input_node.location, output_node.location))

# Function to create an animated sphere (signal) moving from an input node to an output node
def create_signal(start_loc, end_loc, start_frame):
    # Create a small sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=start_loc)
    signal = bpy.context.object
    signal.name = "Signal"
    signal.data.materials.append(green_material)  # Apply simple green material to the sphere

    # Animate the signal's movement
    signal.location = start_loc
    signal.keyframe_insert(data_path="location", frame=start_frame)
    
    signal.location = end_loc
    signal.keyframe_insert(data_path="location", frame=start_frame + 20)  # 20 frames for each signal animation

    # Fade out the signal after it reaches the destination
    signal.scale = (1, 1, 1)
    signal.keyframe_insert(data_path="scale", frame=start_frame + 20)
    signal.scale = (0, 0, 0)
    signal.keyframe_insert(data_path="scale", frame=start_frame + 30)

# Generate multiple signals at each frame interval
for frame in range(1, 200, 10):  # Adjusting interval to add more frequent signals
    for _ in range(5):  # Create 5 signals at each interval
        start_loc, end_loc = random.choice(connections)  # Choose a random connection path
        create_signal(start_loc, end_loc, frame + random.randint(0, 5))  # Randomize start slightly for variation

# Set output path for the .glb file
output_path = "output_scene.glb"
bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB', export_animations=True)

