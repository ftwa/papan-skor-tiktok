import urllib.request
import json
import re

# Let's inspect the page content or test via urllib
url = "http://127.0.0.1:8089/?room=fatwa&theme=comic"
req = urllib.request.urlopen(url)
html = req.read().decode('utf-8')

# Search for any occurrences of PlayerDua or avatar URLs
matches = re.findall(r'PlayerDua', html)
print(f"Occurrences of PlayerDua in html: {len(matches)}")
