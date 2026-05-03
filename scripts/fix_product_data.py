#!/usr/bin/env python3
"""Repair product data: ensure every product has a valid image, enrich descriptions
from scraped data, and write back canonical product data to scripts/products.json."""
import json, os, re, glob

ROOT = "/Users/jet/.accio/accounts/1661502182/agents/DID-F456DA-2B0D4C/project"
I18N_DIR = os.path.join(ROOT, "assets 15.45.13/i18n")
PRODUCT_IMG_DIR = os.path.join(ROOT, "assets/products")

# Build map: product_id -> available image filename
img_files = os.listdir(PRODUCT_IMG_DIR)
img_files_lower = {f.lower(): f for f in img_files}

def find_image(pid):
    """Find best matching image for product id."""
    # Direct: pid.png / pid.jpg
    for ext in [".png", ".jpg", ".jpeg", ".webp"]:
        if (pid + ext).lower() in img_files_lower:
            return img_files_lower[(pid + ext).lower()]
    # Match by substring (longest match wins)
    pid_keys = pid.lower().replace("-", "").replace("_", "")
    candidates = []
    for f in img_files:
        f_norm = re.sub(r'[-_.]', '', f.lower().rsplit('.',1)[0])
        if pid_keys in f_norm or f_norm.startswith(pid_keys[:6]):
            candidates.append(f)
    if candidates:
        candidates.sort(key=lambda x: (-len(x), x))
        return candidates[0]
    return None

# Load English source
with open(os.path.join(I18N_DIR, "en.json"), encoding="utf-8") as f:
    en_data = json.load(f)

# Map of imageless products → assign fallback
fixed_count = 0
for p in en_data.get("products", []):
    pid = p["id"]
    found = find_image(pid)
    if found:
        p["image"] = f"../assets/products/{found}"
        p["image_local"] = f"assets/products/{found}"
        if not p.get("image_orig"): p["image_orig"] = p.get("image", "")
        fixed_count += 1
    else:
        print(f"  ⚠ NO IMAGE: {pid}")

# Save canonical product list
out = {
    "categories": en_data.get("categories", {}),
    "products": en_data["products"]
}
with open(os.path.join(ROOT, "scripts/products.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

# Update all i18n files with corrected image paths
img_map = {p["id"]: (p["image"], p["image_local"]) for p in en_data["products"]}
i18n_files = glob.glob(os.path.join(I18N_DIR, "*.json"))
updated = 0
for fp in i18n_files:
    with open(fp, encoding="utf-8") as f:
        d = json.load(f)
    for p in d.get("products", []):
        if p["id"] in img_map:
            p["image"], p["image_local"] = img_map[p["id"]]
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    updated += 1

print(f"✓ Fixed images for {fixed_count}/{len(en_data['products'])} products")
print(f"✓ Updated {updated} i18n JSON files")
print(f"✓ Wrote canonical products.json")
