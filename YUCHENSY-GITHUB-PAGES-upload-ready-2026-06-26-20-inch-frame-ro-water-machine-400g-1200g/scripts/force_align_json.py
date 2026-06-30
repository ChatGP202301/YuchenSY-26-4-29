import json, os, time

ROOT = "/Users/jet/.accio/accounts/1661502182/agents/DID-F456DA-2B0D4C/project"
I18N_DIR = os.path.join(ROOT, "assets/i18n")

def fix_lang_consistency(lang):
    with open(os.path.join(I18N_DIR, "en.json"), "r") as f: en = json.load(f)
    fp = os.path.join(I18N_DIR, f"{lang}.json")
    if os.path.exists(fp):
        with open(fp, "r") as f: tar = json.load(f)
    else: tar = {"ui":{}, "products":[], "categories":{}}

    # 1. Force UI keys alignment
    for k, v in en["ui"].items():
        if k not in tar.get("ui", {}) or len(str(tar["ui"][k])) < 5:
            tar.setdefault("ui", {})[k] = v # Fallback to EN, then subagent will translate

    # 2. Force Products alignment (copy metadata/images from EN, keep existing translations)
    new_prods = []
    en_prods = en["products"]
    tar_prods = {p["id"]: p for p in tar.get("products", [])}
    
    for ep in en_prods:
        pid = ep["id"]
        if pid in tar_prods:
            tp = tar_prods[pid]
            # Ensure critical metadata (id, image, specs keys) match EN exactly
            tp["image"] = ep["image"]
            if "specs" not in tp or not tp["specs"]: tp["specs"] = ep["specs"]
            new_prods.append(tp)
        else:
            new_prods.append(ep) # Add missing product from EN
    
    tar["products"] = new_prods
    tar["categories"] = en["categories"] # Force sync categories

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(tar, f, ensure_ascii=False, indent=2)
    return True

langs = "en es fr de pt ru ar ja ko it tr hi bn id vi th pl nl fa ur ms tl he el cs hu ro sv da fi no uk bg hr sr sk sl lt et lv sw ha zu ta kk".split()
for l in langs:
    fix_lang_consistency(l)
print("Structural alignment for 45 languages complete.")
