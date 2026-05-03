#!/usr/bin/env python3
"""Download all product/background images from scraped JSON to local filesystem."""
import json, os, urllib.request, urllib.parse, hashlib

ROOT = "/Users/jet/.accio/accounts/1661502182/agents/DID-F456DA-2B0D4C/project"
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(os.path.join(ASSETS, "products"), exist_ok=True)
os.makedirs(os.path.join(ASSETS, "backgrounds"), exist_ok=True)
os.makedirs(os.path.join(ASSETS, "workshop"), exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

def download(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        return True, "cached"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        with open(dest, 'wb') as f:
            f.write(data)
        return True, f"{len(data)} bytes"
    except Exception as e:
        return False, str(e)[:80]

def ext_from_url(url):
    path = urllib.parse.urlparse(url).path.lower()
    for e in ['.jpg','.jpeg','.png','.webp','.gif']:
        if path.endswith(e):
            return e
    return '.jpg'

stats = {"ok": 0, "fail": 0, "details": []}

# expresswater.cn
with open(os.path.join(ROOT, "scraped_data/expresswater_cn.json")) as f:
    cn = json.load(f)
for url in cn.get("background_images", []):
    dest = os.path.join(ASSETS, "backgrounds", "cn_hero" + ext_from_url(url))
    ok, msg = download(url, dest)
    stats["ok" if ok else "fail"] += 1
    stats["details"].append(("BG", url[-50:], dest, ok, msg))

for p in cn.get("products", []):
    pid = p["id"]
    for i, url in enumerate(p.get("images", [])):
        suffix = "" if i == 0 else f"_{i}"
        dest = os.path.join(ASSETS, "products", f"{pid}{suffix}{ext_from_url(url)}")
        ok, msg = download(url, dest)
        stats["ok" if ok else "fail"] += 1
        stats["details"].append((pid, url[-50:], dest, ok, msg))

# ecoexpresswater.com - some referenced as scraped_data/... paths from origin URLs we need to reconstruct
ECO_BASE = "https://www.ecoexpresswater.com/wp-content/uploads/"
ECO_DIRECT = {
    "scraped_data/images/backgrounds/hero1.jpg": "https://www.ecoexpresswater.com/wp-content/uploads/2022/04/IMG_5611-scaled.jpg",
    "scraped_data/images/workshop/line1.png": "https://www.ecoexpresswater.com/wp-content/uploads/2022/08/PP-%E6%BB%A4%E8%8A%AF-%E7%94%9F%E4%BA%A7%E7%BA%BF.png",
    "scraped_data/images/workshop/line2.png": "https://www.ecoexpresswater.com/wp-content/uploads/2022/08/%E7%82%AD%E5%8C%85-%E7%94%9F%E4%BA%A7%E7%BA%BF.png",
    "scraped_data/images/workshop/line3.png": "https://www.ecoexpresswater.com/wp-content/uploads/2022/08/%E5%BF%AB%E6%8E%A5-%E7%94%9F%E4%BA%A7%E7%BA%BF.png",
    "scraped_data/images/workshop/test1.png": "https://www.ecoexpresswater.com/wp-content/uploads/2022/08/%E6%BC%8F%E6%B0%B4-%E6%B5%8B%E8%AF%95.png",
}

with open(os.path.join(ROOT, "scraped_data/ecoexpresswater_com.json")) as f:
    eco = json.load(f)

# Download direct mappings
for local_path, real_url in ECO_DIRECT.items():
    if "backgrounds" in local_path:
        dest = os.path.join(ASSETS, "backgrounds", "eco_" + os.path.basename(local_path))
    elif "workshop" in local_path:
        dest = os.path.join(ASSETS, "workshop", os.path.basename(local_path))
    else:
        dest = os.path.join(ASSETS, "products", os.path.basename(local_path))
    ok, msg = download(real_url, dest)
    stats["ok" if ok else "fail"] += 1
    stats["details"].append(("ECO_ASSET", real_url[-60:], dest, ok, msg))

print(f"\n=== SUMMARY ===")
print(f"OK: {stats['ok']}, FAIL: {stats['fail']}")
for tag, url, dest, ok, msg in stats["details"]:
    icon = "✓" if ok else "✗"
    print(f"{icon} [{tag}] {os.path.basename(dest)} ← ...{url} ({msg})")
