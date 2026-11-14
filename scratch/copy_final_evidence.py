import shutil
import os

media_dir = r"C:\Users\User\.gemini\antigravity\brain\4f17fe5f-2833-4fbd-b37f-1fec141571fa\.system_generated\logs\media"
artifact_dir = r"C:\Users\User\.gemini\antigravity\brain\7b4d737f-92e9-4bb4-ab5b-dbc65a9c5bfa"

copies = [
    ("step_8_media_0.png", "podium_screenshot_fixed.png"),
    ("step_14_media_0.png", "comic_chair_modal_motion.png"),
    ("step_18_media_0.png", "comic_notif_wobble_motion.png")
]

for src, dst in copies:
    src_path = os.path.join(media_dir, src)
    dst_path = os.path.join(artifact_dir, dst)
    if os.path.exists(src_path):
        shutil.copyfile(src_path, dst_path)
        print(f"Copied {src} -> {dst_path}")
    else:
        print(f"Not found: {src_path}")
