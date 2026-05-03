import json, os

ROOT = "/Users/jet/.accio/accounts/1661502182/agents/DID-F456DA-2B0D4C/project"
I18N_DIR = os.path.join(ROOT, "assets/i18n")

with open(os.path.join(I18N_DIR, "en.json"), encoding="utf-8") as f:
    en_data = json.load(f)
    en_products = en_data["products"]

langs = "en es fr de pt ru ar ja ko it tr hi bn id vi th pl nl fa ur ms tl he el cs hu ro sv da fi no uk bg hr sr sk sl lt et lv sw ha zu ta kk".split()

for lang in langs:
    fp = os.path.join(I18N_DIR, f"{lang}.json")
    if not os.path.exists(fp): continue
    
    with open(fp, encoding="utf-8") as f:
        data = json.load(f)
    
    # If products missing or empty, sync from EN
    if "products" not in data or len(data["products"]) < 10:
        print(f"Syncing products for {lang}...")
        data["products"] = en_products
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

print("Product sync complete.")
