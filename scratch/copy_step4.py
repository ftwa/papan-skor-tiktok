from PIL import Image

path4 = r"C:\Users\User\.gemini\antigravity\brain\478d3308-86d0-45de-9457-46160b5d9c34\.system_generated\logs\media\step_4_media_0.png"
img4 = Image.open(path4)
print("Step 4 size:", img4.size)
img4.save(r"d:\galatamaapp\papan-skor-tiktok\scratch\live_podium_step4.png")
print("Saved live podium to scratch/live_podium_step4.png")
