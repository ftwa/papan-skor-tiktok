# Let's inspect index.html lines 6400 to 6420
with open(r"d:\galatamaapp\papan-skor-tiktok\public\index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(6395, 6425):
    print(f"{i+1}: {lines[i]}", end="")
