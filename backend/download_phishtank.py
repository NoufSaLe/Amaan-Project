import requests

URL = "https://data.phishtank.com/data/online-valid.json"
OUTPUT_FILE = "phishtank_db.json"

print("Downloading PhishTank database...")

response = requests.get(URL, timeout=60)

if response.status_code == 200:
    with open(OUTPUT_FILE, "wb") as f:
        f.write(response.content)

    print(" Download complete!")
else:
    print(" Failed:", response.status_code)
