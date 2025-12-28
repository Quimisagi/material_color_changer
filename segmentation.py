import bpy

bpy.context.scene.view_settings.view_transform = 'Standard'

for world in bpy.data.worlds:
    if world.name.startswith("World"):
        print(f"Configuring world: {world.name}")
        if world.use_nodes and "Background" in world.node_tree.nodes:
            world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

for obj in bpy.data.objects:
    if obj.type == 'MESH':
        if "OH_OUTLINE" in obj.modifiers:
            outline_mod = obj.modifiers.get("OH_OUTLINE")
            obj.modifiers.remove(outline_mod)
            print(f"Removed OH_OUTLINE modifier from {obj.name}")

COLOR_HAIR      = (243/255, 0/255, 255/255, 1)
COLOR_FACE      = (255/255, 196/255, 0/255, 1)
COLOR_EYE       = (255/255, 249/255, 233/255, 1)
COLOR_SKIN      = (248/255, 129/255, 33/255, 1)
COLOR_CLOTHES   = (0/255, 255/255, 0/255, 1)
COLOR_MOUTH     = (255/255, 0/255, 0/255, 1)

category_colors = {
    "eye": COLOR_EYE,
    "hair": COLOR_HAIR,
    "face": COLOR_FACE,
    "skin": COLOR_SKIN,
    "cloth": COLOR_CLOTHES,
    "mouth": COLOR_MOUTH,
}

def make_flat_mat(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for n in nodes:
        nodes.remove(n)
        
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = color

    output = nodes.new("ShaderNodeOutputMaterial")

    links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return mat

for obj in bpy.data.objects:
    if obj.type != 'MESH':
        continue

    for slot in obj.material_slots:
        if not slot.material:
            continue

        mat_name = slot.material.name.lower()

        for key, color in category_colors.items():
            if key in mat_name:
                seg_mat_name = f"SEG_{key.upper()}"

                if seg_mat_name in bpy.data.materials:
                    seg_mat = bpy.data.materials[seg_mat_name]
                else:
                    seg_mat = make_flat_mat(seg_mat_name, color)

                slot.material = seg_mat

                print(f"Assigned {seg_mat_name} to slot '{slot.material.name}' in {obj.name}")
                break
