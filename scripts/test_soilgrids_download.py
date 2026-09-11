import requests

url = "https://files.isric.org/soilgrids/latest/data/clay/clay_0-5cm_mean.vrt"

r = requests.get(url, timeout=60)

print("Status:", r.status_code)
print(r.text[:300])