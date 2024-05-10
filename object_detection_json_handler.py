import bpy
import json

import sys

sys.path.append('./')
from bounding_box import calculate_2d_bounds_of_mesh_in_camera_view

def validate_json_input(json_input):
    if isinstance(json_input, str):
        json_data = json.loads(json_input)
    elif isinstance(json_input, dict):
        # Input is already a dictionary, use it directly
        json_data = json_input
    else:
        raise ValueError("Input must be a JSON string or dictionary")

    
    #this should be included scene_name, object_name, route, output_format, frame_number

    if not {'scene_name', 'object_name', 'route', 'output_format', 'frame_number'}.issubset(json_data):
        raise ValueError("Input JSON must contain keys: 'scene_name', 'object_name', 'route', 'output_format', 'frame_number'")

    scene_name = json_data['scene_name']
    object_name = json_data['object_name']
    route = json_data['route']
    output_format = json_data['output_format']
    frame_number = json_data['frame_number']

    # check the frame number is less than the total number of frames
    if frame_number > bpy.data.scenes[scene_name].frame_end:
        raise ValueError("Frame number exceeds the total number of frames in the scene")

    # check if the object exists in the scene
    if object_name not in bpy.data.objects:
        raise ValueError("Object not found in the scene")

    # check output format
    if output_format not in ['jpeg', 'png']:
        raise ValueError("Output format must be either 'jpeg' or 'png'")

    return {'scene_name': scene_name, 'object_name': object_name, 'route': route, 'output_format': output_format, 'frame_number': frame_number}

def render_and_upload_image_to_aws():

    render_filepath = bpy.context.scene.render.filepath
    # render the image
    bpy.ops.render.render(write_still=True)
    # make api call to upload the image to aws


    return "s3://renders/<uuid>.jpeg"


def detect_object_form_json(json_input):
    json_data = validate_json_input(json_input)

    # get objects and camera
    scene = bpy.data.scenes[json_data['scene_name']]
    camera = bpy.data.objects['Camera']
    obj = bpy.data.objects[json_data['object_name']]
    frame_number = json_data['frame_number']

    # set the frame number and format
    scene.frame_set(frame_number)
    bpy.context.scene.render.image_settings.file_format = json_data['output_format'].upper()

    # obj should be type mesh
    if not obj.type == 'MESH':
        raise ValueError("Object is not of type 'MESH'")

    # calculate the bounding box
    bounding_box = calculate_2d_bounds_of_mesh_in_camera_view(scene, camera, obj)


    # upladed the image to aws
    # uploaded_url = render_and_upload_image_to_aws()
    uploaded_url = "s3://renders/<uuid>.jpeg"
    
    # render image and uplad it to aws
    respose_data = {
      'detected_object_name': json_data['object_name'],
      'position': bounding_box,
      'frame': frame_number,
      'frame_url': uploaded_url
    }

    return respose_data
