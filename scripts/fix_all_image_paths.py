import json, os, glob

ROOT = "/Users/jet/.accio/accounts/1661502182/agents/DID-F456DA-2B0D4C/project"
I18N_DIR = os.path.join(ROOT, "assets/i18n")
PROD_IMG_DIR = os.path.join(ROOT, "assets/products")

# Get list of all actual images
actual_images = os.listdir(PROD_IMG_DIR)

def find_best_image(prod_id, current_img):
    # Strip path from current_img
    fname = os.path.basename(current_img)
    if fname in actual_images:
        return f"../assets/products/{fname}"
    
    # Try match by ID
    for img in actual_images:
        if prod_id in img:
            return f"../assets/products/{img}"
    
    # Fallback to first available or 1.png
    return "../assets/products/1.png"

langs = [f.replace(".json", "") for f in os.listdir(I18N_DIR) if f.endswith(".json")]

for lang in langs:
    fp = os.path.join(I18N_DIR, f"{lang}.json")
    with open(fp, encoding="utf-8") as f:
        data = json.load(f)
    
    if "products" in data:
        for p in data["products"]:
            p["image"] = find_best_image(p.get("id", ""), p.get("image", ""))
            
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Fixed image paths for {len(langs)} languages.")
