from PIL import Image

img = Image.open(r"d:\galatamaapp\papan-skor-tiktok\scratch\step_12_view.png")
w, h = img.size
print(f"Modal Preview Dimensions: {w}x{h}")

# Search for cyan pixels in step_12_view.png
cyan_pixels = []
for x in range(0, w, 5):
    for y in range(0, h, 5):
        r, g, b = img.getpixel((x, y))[:3]
        if r < 50 and g > 180 and b > 200:
            cyan_pixels.append((x, y, (r, g, b)))

print(f"Total cyan pixels in screenshot preview: {len(cyan_pixels)}")
if cyan_pixels:
    print("Example cyan pixels:", cyan_pixels[:10])
