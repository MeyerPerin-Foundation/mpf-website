import requests
import time
import json

wait = 1
url = "https://www.meyerperin.org/sitemap.xml"
print(f"Waiting {wait} seconds to submit sitemap...")
time.sleep(wait)

headers = {"Content-Type": "application/json; charset=utf-8"}
headers["Host"]="www.bing.com"

indexnow_url = "https://www.bing.com/indexnow"
with open ("_site/sitemap.json") as fj:
    indexnow_json = json.load(fj)

response = requests.post(indexnow_url, json=indexnow_json, headers=headers)
print(f"Submitted to IndexNow with response {response.status_code}")
