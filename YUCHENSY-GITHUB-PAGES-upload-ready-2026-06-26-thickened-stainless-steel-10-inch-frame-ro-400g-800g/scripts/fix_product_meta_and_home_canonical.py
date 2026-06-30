from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.yuchensy.com/"
OLD_NAME = "PP Melt Blown" + "F Polypropylene Fiber Cartridge"
NEW_NAME = "PP Melt Blown Filter"
OLD_FILE = "pp-melt-blown" + "f-polypropylene-fiber-cartridge-oem.webp"
NEW_FILE = "pp-melt-blown-filter-polypropylene-fiber-cartridge-oem.webp"


def load_product_names() -> dict[str, str]:
    path = ROOT / "scripts" / "products.json"
    names: dict[str, str] = {}
    if not path.exists():
        data = {"products": []}
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
    names.update({item["id"]: item["name"] for item in data.get("products", []) if item.get("id") and item.get("name")})

    # Some translated-only legacy product pages are not in products.json. Use
    # the English page H1 when it exists so their metadata can still be unique.
    for page in (ROOT / "en").glob("product-*.html"):
        product_id = page.stem.removeprefix("product-")
        if product_id in names:
            continue
        text = page.read_text(encoding="utf-8", errors="ignore")
        h1 = extract(r"<h1>(.*?)</h1>", text)
        if h1:
            names[product_id] = h1
    return names


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def html_escape(value: str) -> str:
    return html.escape(value, quote=True)


def site_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0].startswith("YUCHENSY-GITHUB-PAGES-upload-ready"):
            continue
        if path.suffix.lower() in {".html", ".xml", ".json", ".js", ".css"}:
            files.append(path)
    return files


def replace_pp_typo() -> int:
    src = ROOT / "assets" / "products" / OLD_FILE
    dst = ROOT / "assets" / "products" / NEW_FILE
    if src.exists() and not dst.exists():
        shutil.copy2(src, dst)

    changed = 0
    for path in site_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        new = text.replace(OLD_NAME, NEW_NAME)
        new = new.replace("PP Melt Blown" + "F", "PP Melt Blown Filter")
        new = new.replace("PP%20Melt%20Blown" + "F%20Polypropylene%20Fiber%20Cartridge", "PP%20Melt%20Blown%20Filter")
        new = new.replace(OLD_FILE, NEW_FILE)
        new = new.replace("pp-melt-blown" + "f-polypropylene-fiber-cartridge-oem", "pp-melt-blown-filter-polypropylene-fiber-cartridge-oem")
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def extract(pattern: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.I | re.S)
    return clean_text(match.group(1)) if match else ""


def extract_specs(text: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for label, value in re.findall(r"<tr>\s*<th>(.*?)</th>\s*<td>(.*?)</td>\s*</tr>", text, flags=re.I | re.S):
        label_text = clean_text(label)
        value_text = clean_text(value)
        if not label_text or not value_text:
            continue
        low_label = label_text.lower()
        low_value = value_text.lower()
        if low_label in {"item", "項目", "项目", "пункт", "élément", "artículo", "artikel"}:
            continue
        if low_value in {"specification", "specifications", "спецификация", "spécification", "especificación", "spezifikation"}:
            continue
        if len(value_text) > 95:
            value_text = value_text.split(";")[0].strip()
        generic_bits = r"PP\s*/\s*CTO\s*/\s*GAC\s*/\s*UF\s*/\s*RO|10\s*/\s*20\s*/\s*30\s*/\s*40\s*inch|μm\s*/\s*GPD\s*/\s*LPH|FOB\s*/\s*CIF\s*/\s*DDP|ISO\s*9001\s*/\s*CE\s*/\s*SGS"
        generic_value = re.search(generic_bits, value_text, flags=re.I) or low_value in {"oem", "odm", "oem/odm", "✓", "yes"}
        generic_label = re.search(r"^(OEM/ODM|MOQ)$", label_text, flags=re.I) or re.search(generic_bits, label_text, flags=re.I)
        if generic_value or generic_label:
            continue
        pairs.append((label_text, value_text))
    return pairs


def compact_title(h1: str, category: str) -> str:
    h1 = h1.strip()
    category = category.strip()
    if not h1:
        return "Yuchen Water OEM Water Filtration Product"
    with_brand = f"{h1} | Yuchen Water"
    if len(with_brand) <= 75:
        return with_brand
    if len(h1) <= 82:
        return h1
    capacities = re.findall(
        r"\d[\d,]*(?:[-–/]\d[\d,]*)*(?:\s*(?:G|L\s*/\s*h|L/h|l/h|L/ora|L/oras|L/saa|L/saat|L/soat|L/sa|L/ihora|л/ч|л/саат|л/соат|л/сағ|t/h|т/ч|TPH|升/小时|لیتر/ساعت))",
        h1,
        flags=re.I,
    )
    suffix = f" {'/'.join(capacities[:2])}" if capacities else ""
    if category:
        candidate = f"{category}{suffix} | Yuchen Water"
        if len(candidate) <= 78:
            return candidate
        candidate = f"{category}{suffix}"
        if len(candidate) <= 82:
            return candidate
    return h1


DISTINCTIVE_BY_ID = {
    "post-t33": "Post Carbon T33",
    "inline-t33-mineral": "Mineral Inline T33",
    "inline-t33-coconut": "Coconut Carbon T33",
    "t33-post": "T33 Post Carbon",
    "ppf-cartridge": "Polypropylene Fiber PP",
    "pp-spun": "Sediment PP Spun",
    "uf-filter-2": "Hollow Fiber UF",
    "uf-cartridge": "Ultrafiltration UF",
    "uf-inline-filter": "UF Inline",
    "alkaline-inline": "Alkaline Inline",
    "quick-connect-inline": "Quick Connect Inline",
    "cto-cartridge": "CTO Carbon Block",
    "pp-melt-blown": "PP Melt Blown",
}


def product_signature(english_name: str, product_id: str = "") -> str:
    if product_id in DISTINCTIVE_BY_ID:
        return DISTINCTIVE_BY_ID[product_id]

    tokens: list[str] = []
    patterns = [
        r"Single-Tank",
        r"Dual-Tank",
        r"Three-Tank",
        r"Desktop",
        r"Commercial",
        r"Industrial",
        r"Integrated",
        r"Skid",
        r"Big Blue",
        r"Pressure Tank",
        r"PP Melt Blown",
        r"Polypropylene Fiber",
        r"Sediment",
        r"Post Carbon",
        r"Post T33",
        r"Inline",
        r"Mineralized",
        r"Coconut Shell",
        r"Carbon Block",
        r"Activated Carbon",
        r"CTO",
        r"GAC",
        r"UDF",
        r"T33",
        r"UF",
        r"RO Membrane",
        r"Reverse Osmosis",
        r"Big Blue",
        r"Stainless Steel",
        r"304/316L",
        r"Ceramic",
        r"Resin",
        r"Antibacterial",
        r"Mineralization",
        r"Small Molecule",
        r"Maifan",
        r"Pre-UDF",
        r"Flat Cap",
        r"Pleated",
        r"UV",
        r"Alkaline",
        r"Copper Connector",
        r"Fin End Cap",
        r"Silicon Ring",
        r"SOE/DOE",
        r"\d+(?:/\d+)?GPD",
        r"\d+(?:/\d+)+G",
        r"\d+\s*G",
        r"\d+\s*TPH",
        r"\d+(?:[-–]\d+)?\s*L/h",
        r"\d+\s*inch",
    ]
    for pattern in patterns:
        for match in re.findall(pattern, english_name, flags=re.I):
            value = match if isinstance(match, str) else match[0]
            value = re.sub(r"\s+", " ", value).strip()
            canonical = value.upper() if value.upper() in {"PP", "CTO", "GAC", "UDF", "T33", "UF", "UV"} else value
            if canonical and canonical.lower() not in {t.lower() for t in tokens}:
                tokens.append(canonical)
            if len(tokens) >= 5:
                break
        if len(tokens) >= 5:
            break
    if product_id:
        skip = {
            "product",
            "filter",
            "cartridge",
            "water",
            "equipment",
            "system",
            "purifier",
            "machine",
            "oem",
            "odm",
        }
        for token in product_id.replace("-", " ").split():
            if token in skip or len(token) < 2:
                continue
            canonical = token.upper() if token in {"pp", "cto", "gac", "udf", "t33", "uf", "uv", "ro"} else token.title()
            if canonical and canonical.lower() not in {t.lower() for t in tokens}:
                tokens.append(canonical)
            if len(tokens) >= 5:
                break
    if not tokens:
        tokens = english_name.split()[:5]
    return " ".join(tokens[:5])


def should_add_signature(h1: str, repeat_count: int) -> bool:
    compact = re.sub(r"[^A-Za-z0-9\u0080-\uffff]+", "", h1)
    has_specific_token = bool(re.search(r"PP|CTO|GAC|UDF|T33|UF|RO|UV|304|316|GPD|\d", h1, flags=re.I))
    return repeat_count > 1 or (len(compact) <= 24 and not has_specific_token)


def effective_product_name(path: Path, h1: str, repeat_count: int, product_names: dict[str, str]) -> str:
    product_id = path.stem.removeprefix("product-")
    english_name = product_names.get(product_id, "")
    if english_name and len(h1) > 82:
        signature = product_signature(english_name, product_id)
        capacities = re.findall(
            r"\d[\d,]*(?:[-–/]\d[\d,]*)*(?:\s*(?:G|GPD|L\s*/\s*h|L/h|l/h|L/ora|L/oras|L/saa|L/saat|L/soat|L/sa|L/ihora|л/ч|л/саат|л/соат|л/сағ|t/h|т/ч|TPH|升/小时|لیتر/ساعت))",
            h1 + " " + english_name,
            flags=re.I,
        )
        suffix = f" {'/'.join(capacities[:2])}" if capacities else ""
        short = f"{signature}{suffix}".strip()
        if short:
            return short[:82].rstrip(" -–/")

    if not english_name and product_id not in DISTINCTIVE_BY_ID:
        return h1
    if not should_add_signature(h1, repeat_count):
        return h1
    signature = product_signature(english_name, product_id)
    if signature.lower() in h1.lower():
        return h1
    candidate = f"{h1} {signature}".strip()
    return candidate if len(candidate) <= 82 else f"{h1} {signature.split()[0]}".strip()


def compact_description(h1: str, category: str, specs: list[tuple[str, str]]) -> str:
    base = h1 or category or "Yuchen Water OEM water filtration product"
    parts = [base.rstrip(".。！？!?") + "."]
    for label, value in specs:
        clause = f"{label}: {value}."
        if len(" ".join(parts + [clause])) <= 168:
            parts.append(clause)
        if len(parts) >= 4:
            break
    desc = " ".join(parts)
    if len(desc) <= 180:
        return desc

    # Fall back to a complete sentence without cutting a word in half.
    if len(parts[0]) <= 180:
        return parts[0]
    words = parts[0].split()
    shortened: list[str] = []
    for word in words:
        if len(" ".join(shortened + [word])) > 176:
            break
        shortened.append(word)
    return (" ".join(shortened).rstrip(".") + ".") if shortened else parts[0][:176].rstrip() + "."


def set_meta(text: str, title: str, desc: str) -> str:
    escaped_title = html_escape(title)
    escaped_desc = html_escape(desc)
    replacements = [
        (r"<title>.*?</title>", f"<title>{escaped_title}</title>"),
        (r'(<meta\s+name=["\']description["\']\s+content=["\']).*?(["\']\s*/?>)', rf"\g<1>{escaped_desc}\2"),
        (r'(<meta\s+property=["\']og:title["\']\s+content=["\']).*?(["\']\s*/?>)', rf"\g<1>{escaped_title}\2"),
        (r'(<meta\s+property=["\']og:description["\']\s+content=["\']).*?(["\']\s*/?>)', rf"\g<1>{escaped_desc}\2"),
        (r'(<meta\s+name=["\']twitter:title["\']\s+content=["\']).*?(["\']\s*/?>)', rf"\g<1>{escaped_title}\2"),
        (r'(<meta\s+name=["\']twitter:description["\']\s+content=["\']).*?(["\']\s*/?>)', rf"\g<1>{escaped_desc}\2"),
    ]
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text, flags=re.I | re.S)
    return text


def update_product_meta() -> int:
    changed = 0
    product_names = load_product_names()
    h1_counts: dict[tuple[str, str], int] = {}
    for path in sorted(ROOT.glob("*/product-*.html")):
        if path.parts and any(part.startswith("YUCHENSY-GITHUB-PAGES-upload-ready") for part in path.parts):
            continue
        lang = path.parent.name
        text = path.read_text(encoding="utf-8", errors="ignore")
        h1 = extract(r"<h1>(.*?)</h1>", text)
        h1_counts[(lang, h1)] = h1_counts.get((lang, h1), 0) + 1

    for path in sorted(ROOT.glob("*/product-*.html")):
        if path.parts and any(part.startswith("YUCHENSY-GITHUB-PAGES-upload-ready") for part in path.parts):
            continue
        lang = path.parent.name
        text = path.read_text(encoding="utf-8", errors="ignore")
        h1 = extract(r"<h1>(.*?)</h1>", text)
        category = extract(r'<span class="cat-badge">(.*?)</span>', text)
        specs = extract_specs(text)
        effective_name = effective_product_name(path, h1, h1_counts.get((lang, h1), 1), product_names)
        title = compact_title(effective_name, category)
        desc = compact_description(effective_name, category, specs)
        new = set_meta(text, title, desc)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def update_home_canonicals() -> int:
    changed = 0
    pages = [ROOT / "index.html"] + sorted(ROOT.glob("*/index.html"))
    for path in pages:
        if not path.exists() or "YUCHENSY-GITHUB-PAGES-upload-ready" in str(path):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(ROOT)
        if rel == Path("index.html") or rel == Path("en/index.html"):
            canonical = SITE
        else:
            canonical = f"{SITE}{rel.as_posix()}"
        new = re.sub(r'<link rel="canonical" href="[^"]+" />', f'<link rel="canonical" href="{canonical}" />', text, count=1)
        new = re.sub(r'<link rel="alternate" hreflang="en" href="[^"]+" />', f'<link rel="alternate" hreflang="en" href="{SITE}" />', new)
        new = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]+" />', f'<link rel="alternate" hreflang="x-default" href="{SITE}" />', new)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1

    sitemap = ROOT / "sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8", errors="ignore")
        new = re.sub(
            r"\s*<url>\s*<loc>https://www\.yuchensy\.com/en/index\.html</loc>.*?</url>",
            "",
            text,
            flags=re.S,
        )
        if new != text:
            sitemap.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def main() -> None:
    typo_files = replace_pp_typo()
    meta_files = update_product_meta()
    home_files = update_home_canonicals()
    print(f"PP typo/image refs updated in {typo_files} files")
    print(f"Product meta tags updated in {meta_files} product pages")
    print(f"Home canonical/hreflang/sitemap updated in {home_files} files")


if __name__ == "__main__":
    main()
