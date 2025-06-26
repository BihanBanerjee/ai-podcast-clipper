import modal

# Modal configuration - MINIMAL VERSION
# Only includes directories that main.py actually imports from
image = (modal.Image.from_registry(
    "nvidia/cuda:12.4.0-devel-ubuntu22.04", add_python="3.12")
    .apt_install(["ffmpeg", "libgl1-mesa-glx", "wget", "libcudnn8", "libcudnn8-dev"])
    .pip_install_from_requirements("requirements.txt")
    .run_commands(["mkdir -p /usr/share/fonts/truetype/custom",
                   "wget -O /usr/share/fonts/truetype/custom/Anton-Regular.ttf https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf",
                   "fc-cache -f -v"])
    .add_local_dir("asd", "/asd", copy=True)
    # ONLY add the directories that main.py actually needs:
    .add_local_dir("config", "/root/config", copy=True)
    .add_local_dir("services", "/root/services", copy=True) 
    .add_local_dir("utils", "/root/utils", copy=True)
    .add_local_dir("video_processing", "/root/video_processing", copy=True)
    .add_local_dir("prompts", "/root/prompts", copy=True)
    .add_local_file("main.py", "/root/main.py"))

volume = modal.Volume.from_name(
    "ai-podcast-clipper-model-cache", create_if_missing=True
)

mount_path = "/root/.cache/torch"