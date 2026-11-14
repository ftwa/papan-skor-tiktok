import os
from PIL import Image

path = r"C:\Users\User\.gemini\antigravity\brain\478d3308-86d0-45de-9457-46160b5d9c34\.system_generated\logs\media\step_12_media_0.png"
if os.path.exists(path):
    img = Image.open(path)
    print("Step 12 Media 0 size:", img.size)
    # Save a copy to scratch so we can link or inspect
    out_path = r"d:\galatamaapp\papan-skor-tiktok\scratch\step_12_view.png"
    img.save(out_path)
    print("Saved copy to", out_path)
else:
    print("File not found:", path)
