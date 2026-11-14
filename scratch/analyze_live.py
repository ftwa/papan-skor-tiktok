from PIL import Image

img = Image.open(r"d:\galatamaapp\papan-skor-tiktok\scratch\live_podium_step4.png")
w, h = img.size
print(f"Dimensions: {w}x{h}")

# Background corners (should be radial gradient orange/yellow)
print("Top Left (20, 20):", img.getpixel((20, 20)))
print("Center Top (w//2, 50):", img.getpixel((w//2, 50)))
print("Center (w//2, h//2):", img.getpixel((w//2, h//2)))

# Let's inspect Rank 2 avatar area
# Let's find any pure cyan pixels (0, 229, 255) or similar in the image
cyan_pixels = []
for x in range(0, w, 5):
    for y in range(0, h, 5):
        r, g, b = img.getpixel((x, y))[:3]
        if r < 50 and g > 180 and b > 200: # cyan-like
            cyan_pixels.append((x, y, (r, g, b)))

print(f"Total cyan-like sampled pixels: {len(cyan_pixels)}")
if cyan_pixels:
    print("Example cyan pixels:", cyan_pixels[:5])
