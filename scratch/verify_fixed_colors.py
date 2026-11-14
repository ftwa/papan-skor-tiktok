from PIL import Image

img = Image.open(r"C:\Users\User\.gemini\antigravity\brain\7b4d737f-92e9-4bb4-ab5b-dbc65a9c5bfa\podium_screenshot_fixed.png")
w, h = img.size
print(f"Podium screenshot preview size: {w}x{h}")

# In step 8 preview modal: the preview image is centered
# Let's sample colors in the inner preview image
# Around (400, 300) should be inside the captured podium screenshot
print("Center area (400, 300):", img.getpixel((400, 300)))
print("Upper center (400, 250):", img.getpixel((400, 250)))
print("Left side of preview (250, 300):", img.getpixel((250, 300)))
print("Right side of preview (550, 300):", img.getpixel((550, 300)))
