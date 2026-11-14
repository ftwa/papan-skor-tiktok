import os
from PIL import Image

img_path = r"C:\Users\User\.gemini\antigravity\brain\7b4d737f-92e9-4bb4-ab5b-dbc65a9c5bfa\browser_evidence\478d3308-86d0-45de-9457-46160b5d9c34\final_step_12.png"
if os.path.exists(img_path):
    img = Image.open(img_path)
    print(f"Image size: {img.size}")
    print(f"Image mode: {img.mode}")
else:
    print("Not found:", img_path)
