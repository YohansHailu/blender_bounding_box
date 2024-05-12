import bpy
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import sys
import os

sys.path.append('./')

from bounding_box import calculate_2d_bounds_of_mesh_in_camera_view
from object_detection_json_handler import detect_object_form_json


def print_separator():
    print("-" * 50)

def display_image_with_bounds(filepath, bounding_boxs):
    im = mpimg.imread(filepath)
    _, ax = plt.subplots(1)
    ax.imshow(im)

    for x, y, width, height in bounding_boxs:
        rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='yellow', facecolor='none')
        ax.add_patch(rect)
    plt.show()

def bounding_box_test(scene_name, camera_name, mesh_names):
    
    # get objects objects
    scene = bpy.data.scenes[scene_name]

    camera = bpy.data.objects[camera_name]
    bounding_boxs = []


    for mesh_name in mesh_names:

        mesh = bpy.data.objects[mesh_name]

        ## set render settings

        if not mesh.type == 'MESH':
            return

        res = calculate_2d_bounds_of_mesh_in_camera_view(scene, camera, mesh)
        if not res:
            print("Mesh is not in view.")
            return

        x, y, width, height = res

        print_separator()
        print("Bounding box coordinates:, for ", mesh_name)
        print(x, y, width, height)
        bounding_boxs.append((x, y, width, height))
        


    bpy.ops.render.render(write_still=True)
    render_filepath = bpy.context.scene.render.filepath
    display_image_with_bounds(render_filepath, bounding_boxs)


def detect_object_from_json_test(frame_number):
    obj_names = ['BrickColumn', 'HumanCollider', 'Cone', 'FireHydrant']
    res = []
    for obj_name in obj_names:
        json_input = {
            "scene_name": "Scene",
            "object_name": obj_name,
            "route": "s3://renders/<uuid>.jpeg",
            "output_format": "jpeg",
            "frame_number": frame_number
        }
        res.append(detect_object_form_json(json_input))
        
    return res

def main():

    scene_name = 'Scene'
    camera_name = 'Camera'
    dirname = os.path.dirname(__file__)
    render_filepath = os.path.join(dirname, 'renders/renders.jpg')
    
    # render settings
    bpy.context.scene.render.image_settings.file_format='JPEG'
    bpy.context.scene.render.filepath = render_filepath
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    obj_names = ['BrickColumn', 'HumanCollider', 'Cone', 'FireHydrant']
    # render single frame
    bpy.context.scene.frame_set(25)
    bounding_box_test(scene_name, camera_name, obj_names)


    # Animation output json
    # res = []
    # for i in range(0, 175):
    #     bpy.context.scene.frame_set(i)
    #     res.extend(detect_object_from_json_test(i))

    # # write res into json file
    # with open(os.path.join(dirname, 'output.json'), 'w') as f:
    #     json.dump(res, f, indent=4)






if __name__ == '__main__':
    main()
