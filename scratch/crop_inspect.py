from PIL import Image

img_path = r"C:\Users\User\.gemini\antigravity\brain\7b4d737f-92e9-4bb4-ab5b-dbc65a9c5bfa\browser_evidence\478d3308-86d0-45de-9457-46160b5d9c34\final_step_12.png"
img = Image.open(img_path)

# Crop the preview area
# Let's save a crop of rank 2 and rank 3
w, h = img.size
print("Width:", w, "Height:", h)

# Sample some pixel colors
# Background at top left of preview
print("Pixel at 100, 100:", img.getpixel((100, 100)))
print("Pixel at 400, 100:", img.getpixel((400, 100)))
print("Pixel at 200, 300 (around rank 2):", img.getpixel((200, 300)))
print("Pixel at 600, 300 (around rank 3):", img.getpixel((600, 300)))
