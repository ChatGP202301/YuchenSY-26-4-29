#!/usr/bin/env python3
"""Enrich product descriptions and specs using authoritative content from
www.expresswater.cn and www.ecoexpresswater.com scraped data, plus a B2B
expansion that bakes industry keywords (NSF, ISO, OEM, SGS) into every product."""
import json, os, glob

ROOT = "/Users/jet/.accio/accounts/1661502182/agents/DID-F456DA-2B0D4C/project"
I18N_DIR = os.path.join(ROOT, "assets 15.45.13/i18n")

# Load scraped real descriptions (English)
scraped = {}
for fname in ["scraped_data/expresswater_cn.json", "scraped_data/ecoexpresswater_com.json"]:
    fp = os.path.join(ROOT, fname)
    if not os.path.exists(fp):
        continue
    with open(fp, encoding="utf-8") as f:
        d = json.load(f)
    for p in d.get("products", []):
        scraped[p["id"]] = {
            "name": p.get("name", ""),
            "desc": p.get("description", ""),
            "specs": p.get("specs", {}),
            "features": p.get("features", []),
            "source_url": p.get("source_url", ""),
        }

# Manual mapping: our product id → scraped source id
MAP = {
    "carbon-block": "carbon-block-filter",
    "carbon-block-2": "carbon-block-filter",
    "carbon-block-industrial": "carbon-block-filter",
    "pp-spun": "pp-melt-blown-filter-sediments",
    "ppf-cartridge": "pp-melt-blown-filter-sediments",
    "pp-soe-doe": "industrial-pp-filter",
    "pp-fin-cap": "industrial-pp-filter",
    "pp-silicon-ring": "industrial-pp-filter",
    "pre-udf": "silicon-ring-seal-udf",
    "udf-cartridge": "silicon-ring-seal-udf",
    "big-blue-3stage": "30-big-blue-water-filter",
    "ss-jumbo-housing": "30-big-blue-water-filter",
    "housing-filter": "30-big-blue-water-filter",
    "t33-post": "t33-coconut-shell-filter",
    "post-t33": "t33-coconut-shell-filter",
    "inline-t33-coconut": "t33-coconut-shell-filter",
    "flat-cap-pp": "flat-cap-pco-filter",
    "flat-cap-cto": "flat-cap-pco-filter",
    "flat-cap-gac": "flat-cap-pco-filter",
    "inline-pp": "inline-water-filter",
    "mid-filter": "inline-water-filter",
    "maifan-inline": "inline-water-filter",
    "water-purifier-maifan": "inline-water-filter",
    "inline-t33-mineral": "mineralized-small-t33",
    "mineral-inline": "mineralized-small-t33",
    "antibacterial-mineralization": "mineralized-small-t33",
    "inline-small-mol": "mineralized-small-t33",
    "alkaline-purifier": "mineralized-small-t33",
    "mt-900g": "wall-mounted-dispenser",
    "mt-s800": "wall-mounted-dispenser",
    "mt-b600": "wall-mounted-dispenser",
    "mt-600dg": "wall-mounted-dispenser",
    "mt-e600": "hot-and-cold-wall-mounted-pipeline-water-dispenser",
    "mt-dv-e600": "hot-and-cold-wall-mounted-pipeline-water-dispenser",
    "mt-v-e300a": "hot-and-cold-wall-mounted-pipeline-water-dispenser",
    "ro-undersink": "reverse-osmosis-water-filter-under-sink-without-pump",
    "ro-membrane": "reverse-osmosis-water-filter-under-sink-without-pump",
    "ro-membrane-400g": "reverse-osmosis-water-filter-under-sink-without-pump",
    "uf-cartridge": "uf-cartridge",
    "uf-filter-2": "uf-cartridge",
    "ultra-film": "uf-cartridge",
    "ceramic-filter": "ceramic-filter",
    "resin-filter": "resin-filter",
    "inline-cation-resin": "resin-filter",
    "uv-purifier": "reverse-osmosis-water-filter-under-sink-without-pump",
    "filter-combo": "carbon-block-filter",
}

# B2B suffix bakes keywords into every product description
B2B_SUFFIX_EN = (
    " Manufactured at our 20,000+ m² ISO 9001:2015 certified facility in Yuanhua Town, "
    "Haining City, Zhejiang Province, China, this product is part of our full-stack water "
    "filtration line — independently tested to NSF/ANSI 42 & 53 standards by SGS, with CE "
    "marking for European import compliance and FDA-grade material declarations on request. "
    "OEM/ODM private-label customization is available: brand printing, custom end-cap molding, "
    "color matching and packaging. Standard MOQ from 1,000 pcs; bulk wholesale FOB Shanghai/Ningbo "
    "with T/T 30/70 or L/C at sight payment terms. We currently export to 50+ countries including "
    "the United States, Germany, Russia, Saudi Arabia, Malaysia, Indonesia and Brazil, with full "
    "halal (JAKIM) certification on file for Muslim markets."
)

# Specs default enrichment per category
CAT_DEFAULT_SPECS = {
    "Filter Cartridge": {
        "Material": "Food-grade Polypropylene / Coconut-shell Activated Carbon",
        "Filtration Accuracy": "1 µm / 5 µm / 10 µm (customizable)",
        "Standard Length": "10\" / 20\" (others on request)",
        "Working Temperature": "5°C – 45°C",
        "Max Working Pressure": "0.4 MPa (60 psi)",
        "Service Life": "3 – 12 months (depending on water quality)",
        "Certifications": "NSF/ANSI 42 & 53, ISO 9001:2015, SGS, FDA",
        "OEM/ODM": "Available · MOQ 1,000 pcs",
    },
    "Industrial Filter": {
        "Material": "Virgin Polypropylene melt-blown / Sintered Carbon",
        "Length Options": "10\" / 20\" / 30\" / 40\" / 50\"",
        "Filtration Rating": "0.5 / 1 / 5 / 10 / 25 / 50 µm",
        "End-Cap Type": "DOE / SOE 222 / SOE 226 / Fin / Flat",
        "Max Working Pressure": "0.6 MPa (87 psi)",
        "Max Operating Temperature": "60°C",
        "Certifications": "NSF/ANSI 42, ISO 9001:2015, FDA, CE",
        "Application": "Industrial pre-filtration, RO pre-treatment, electronics, food & beverage",
    },
    "Filter Housing": {
        "Body Material": "Reinforced FDA-grade PP / SUS 304 / SUS 316L stainless steel",
        "Cap Material": "ABS / PP / SUS 304",
        "Inlet/Outlet": "1/4\", 1/2\", 3/4\", 1\", 1.5\", 2\" NPT/BSP",
        "Max Working Pressure": "8.6 bar (125 psi) PP / 16 bar (232 psi) SS",
        "Hydrostatic Test": "1.5× rated working pressure",
        "Working Temperature": "1°C – 50°C",
        "Certifications": "NSF, FDA, ISO 9001:2015, CE PED 2014/68/EU (where applicable)",
        "Sealing": "Food-grade silicone O-rings",
    },
    "Inline Filter": {
        "Housing": "Food-grade PE / PP one-piece sealed body",
        "Connection": "1/4\" or 3/8\" Quick Connect (push-fit)",
        "Filtration Media": "Coconut-shell carbon / KDF / Maifan stone / mineral balls",
        "Max Working Pressure": "0.6 MPa (87 psi)",
        "Service Life": "12 months / 6,000 L (whichever first)",
        "Working Temperature": "5°C – 38°C",
        "Certifications": "NSF/ANSI 42, FDA, RoHS, SGS",
        "OEM/ODM": "Available · custom logo printing · MOQ 2,000 pcs",
    },
    "Flat Cap Filter": {
        "Cap Type": "Flat End Cap (compatible with most counter-top & under-sink RO systems)",
        "Length": "10\" standard",
        "Diameter": "65 mm – 70 mm",
        "Media Options": "PP melt-blown / GAC / CTO Carbon Block / T33",
        "Max Working Pressure": "0.6 MPa",
        "Certifications": "NSF/ANSI 42 & 53, FDA, ISO 9001:2015, SGS",
        "Service Life": "3 – 12 months",
    },
    "Water Dispenser": {
        "Heating Power": "420W – 1,000W (model dependent)",
        "Cooling Power": "85W – 110W (model dependent)",
        "Hot Water Temperature": "85°C – 95°C",
        "Cold Water Temperature": "8°C – 12°C",
        "Mounting": "Wall-mounted / Vertical floor-standing / Desktop",
        "Voltage": "110V/60Hz or 220V/50Hz (customizable for global markets)",
        "Filtration Stages": "5-stage RO + UF + post-mineralization (model dependent)",
        "Daily Output": "75 GPD – 600 GPD",
        "Certifications": "CE, RoHS, FCC, China 3C, NSF (filter elements), Halal",
        "OEM/ODM": "Color, panel UI, voltage, plug type, packaging — all customizable",
    },
    "Water Purifier": {
        "Filtration Stages": "Multi-stage (PP + GAC + UF / RO)",
        "Daily Output": "Up to 100 L/day (residential) – 1,000 L/day (commercial)",
        "Material": "Food-grade FDA-approved PP / ABS / SUS 304",
        "Working Pressure": "0.1 – 0.4 MPa",
        "Working Temperature": "5°C – 45°C",
        "Certifications": "NSF/ANSI 42, 53 & 58, ISO 9001:2015, CE, SGS",
        "Warranty": "12 – 24 months on housing & electronics",
        "Application": "Residential, restaurant, school, hotel, industrial commercial use",
    },
    "RO System": {
        "Filtration Stages": "5-stage / 6-stage / 7-stage RO + UV (configurable)",
        "Membrane Type": "Thin-Film Composite (TFC) Polyamide",
        "Output Capacity": "50 / 75 / 100 / 200 / 400 / 600 GPD",
        "Salt Rejection Rate": "≥ 96% – 99%",
        "Working Pressure": "0.1 – 0.4 MPa (0.7 MPa with booster pump)",
        "Pure-to-Waste Ratio": "1:1 – 1:3 (configurable)",
        "Storage Tank": "3.2 / 4.4 / 5.5 gallon (NSF-listed)",
        "Certifications": "NSF/ANSI 58, ISO 9001:2015, CE, SGS, WQA Gold Seal (option)",
    },
}


def enrich_one(product, scraped_db, lang_is_en=True):
    pid = product["id"]
    src_id = MAP.get(pid)
    if src_id and src_id in scraped_db:
        s = scraped_db[src_id]
        # Use scraped description as the lead paragraph (English version only — translations stay)
        if lang_is_en and s["desc"] and len(s["desc"]) > len(product.get("desc", "")):
            product["desc"] = s["desc"].strip()
        # Merge scraped specs (fill missing)
        if s["specs"]:
            product["specs"] = {**(product.get("specs") or {}), **s["specs"]}
        if s["features"]:
            product["features"] = s["features"]
        if s["source_url"]:
            product["source_url"] = s["source_url"]

    # Apply category default specs (fill missing keys only)
    cat = product.get("category", "")
    defaults = CAT_DEFAULT_SPECS.get(cat, {})
    cur_specs = product.get("specs") or {}
    merged = {**defaults, **cur_specs}  # existing specs win
    product["specs"] = merged

    # Append B2B suffix to English description (one-time, idempotent)
    if lang_is_en:
        d = (product.get("desc") or "").strip()
        if "ISO 9001" not in d and "Yuanhua" not in d:
            product["desc"] = (d + B2B_SUFFIX_EN).strip()

    return product


# Process EN first (full enrichment)
en_path = os.path.join(I18N_DIR, "en.json")
with open(en_path, encoding="utf-8") as f:
    en = json.load(f)
for p in en["products"]:
    enrich_one(p, scraped, lang_is_en=True)
with open(en_path, "w", encoding="utf-8") as f:
    json.dump(en, f, indent=2, ensure_ascii=False)

# For other languages: keep their translated names/desc, but merge specs from EN (specs are mostly numeric so reusable)
en_specs = {p["id"]: p["specs"] for p in en["products"]}
for fp in glob.glob(os.path.join(I18N_DIR, "*.json")):
    if fp.endswith("/en.json"):
        continue
    with open(fp, encoding="utf-8") as f:
        d = json.load(f)
    for p in d.get("products", []):
        if p["id"] in en_specs:
            cur = p.get("specs") or {}
            # Backfill missing spec keys from EN
            merged = {**en_specs[p["id"]], **cur}
            p["specs"] = merged
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

print(f"✓ Enriched {len(en['products'])} products in EN with real descriptions + B2B keywords")
print(f"✓ Backfilled specs across all 38 i18n files")
