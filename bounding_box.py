import numpy as np
import bpy
import json
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def transform_mesh_to_camera_space(mesh_object, camera):

    camera_matrix = camera.matrix_world.normalized().inverted()
    transformed_mesh = mesh_object.to_mesh()
    transformed_mesh.transform(mesh_object.matrix_world)
    transformed_mesh.transform(camera_matrix)
    return transformed_mesh

def project_vertices_to_camera_frame(vertices, camera_frame):

    bounds_x = []
    bounds_y = []
    for vertex in vertices:
        if vertex.co.z >= 0:
            continue  # Vertex is behind the camera; ignore it
        projected_frame = [vector / (vector.z / -vertex.co.z) for vector in camera_frame]
        frame_min_x, frame_max_x = projected_frame[1].x, projected_frame[2].x
        frame_min_y, frame_max_y = projected_frame[0].y, projected_frame[1].y

        normalized_x = (vertex.co.x - frame_min_x) / (frame_max_x - frame_min_x)
        normalized_y = (vertex.co.y - frame_min_y) / (frame_max_y - frame_min_y)
        bounds_x.append(normalized_x)
        bounds_y.append(normalized_y)

    return bounds_x, bounds_y

def calculate_normalized_bounds(bounds_x, bounds_y):

    if not bounds_x or not bounds_y:
        return None

    min_x, max_x = np.clip([min(bounds_x), max(bounds_x)], 0.0, 1.0)
    min_y, max_y = np.clip([min(bounds_y), max(bounds_y)], 0.0, 1.0)

    if min_x == max_x or min_y == max_y:
        return None

    return min_x, max_x, min_y, max_y

def convert_to_pixel_coordinates(bounds, render_settings):

    min_x, max_x, min_y, max_y = bounds
    scale_factor = render_settings.resolution_percentage / 100
    width_pixels = render_settings.resolution_x * scale_factor
    height_pixels = render_settings.resolution_y * scale_factor

    pixel_x = min_x * width_pixels
    pixel_y = height_pixels - max_y * height_pixels
    pixel_width = (max_x - min_x) * width_pixels
    pixel_height = (max_y - min_y) * height_pixels

    return (pixel_x, pixel_y, pixel_width, pixel_height)

def calculate_2d_bounds_of_mesh_in_camera_view(scene, camera, mesh_object):

    if not mesh_object.type == 'MESH':
        raise ValueError("Object is not of type 'MESH'")

    transformed_mesh = transform_mesh_to_camera_space(mesh_object, camera)

    camera_frame = [-vector for vector in camera.data.view_frame(scene=scene)[:3]]

    bounds_x, bounds_y = project_vertices_to_camera_frame(transformed_mesh.vertices, camera_frame)
    normalized_bounds = calculate_normalized_bounds(bounds_x, bounds_y)

    if normalized_bounds is None:
        return None

    render_settings = scene.render

    return convert_to_pixel_coordinates(normalized_bounds, render_settings)

