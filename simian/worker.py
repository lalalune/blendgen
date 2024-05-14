import json
import subprocess
import sys
import os
import ssl

from celery import Celery

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))

from simian.utils import check_imports, get_blender_path, get_redis_values

ssl._create_default_https_context = ssl._create_unverified_context

check_imports()

app = Celery("tasks", broker=get_redis_values())

@app.task(name="render_object", acks_late=True, reject_on_worker_lost=True)
def render_object(
    combination_index: int,
    combination: list,
    width: int,
    height: int,
    output_dir: str,
    hdri_path: str,
) -> None:
    """
    Renders a 3D object based on the provided combination index and settings.

    Args:
    - combination_index (int): The index of the camera combination to use.
    - combination (list): The list of objects to render.
    - width (int): The width of the rendered output.
    - height (int): The height of the rendered output.
    - output_dir (str): The directory where the rendered video will be saved.
    - hdri_path (str): The path to the background HDRs.

    Returns:
    - None
    """
    
    # json stringify the combination list
    combination = json.dumps(combination)
    
    # escape the combination string for CLI
    combination = "\"" + combination.replace('"', '\\"') + "\""
    
    args = f"--width {width} --height {height} --combination_index {combination_index}"
    args += f" --output_dir {output_dir}"
    args += f" --hdri_path {hdri_path}"
    args += f" --combination {combination}"
    application_path = get_blender_path()

    command = f"{application_path} --background --python simian/render.py -- {args}"
    print("Worker running: ", command)
    subprocess.run(["bash", "-c", command], timeout=10000, check=False)