# Blender Bounding Box Automation

This repository contains a script for automatically creating bounding boxes for 3D models in Blender. The script run on a supplied `.blend` file with preconfigured mesh and camera settings.

## Features

- **Bounding Box Calculation**: To calculate the bounding box for specified frames and mesh objects.
- **JSON Input**: Accepts JSON information to do bounding box Calculation. Here's the format for the JSON input:

    ```json
    {
        "scene_name": "your_scene_name",
        "object_name": "your_object_name",
        "route": "your_route",
        "output_format": "your_output_format",
        "frame_number": your_frame_number
    }
    ```

- **Rendering and Output**: The calculated bounding box and the frame are rendered, and the image is prepared for upload to AWS S3 (Note: S3 upload not currently implemented).

```
{
    "detected_object_name": "your_object_name",
    "position": "bounding_box_coordinates",
    "frame": "frame_number",
    "frame_url": "uploaded_image_url_on_S3"
}

```

## Usage

To run the script, navigate to the directory containing your `.blend` file and execute:

```bash
blender -b MorningGateSetup.blend -P test.py
```

check the test.py file to modify which feature to test, the bounding box calculations or JSON handler as needed.

## Future Work
-----------

*   **Support for Empty Objects**: Extend bounding box detection to include empty objects that have mesh children by combining them into one mesh.
*   **Implementation and conceptualization for path input**: currently does not utilze path.
*   **S3 Upload**: Implement functionality to upload rendered images directly to AWS S3.
*   **Code Refinement**: Improve code cleanliness, modularity, and professionalism.
