#!/usr/bin/env python3
"""Localize visible category labels and Product JSON-LD categories."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LANGS = ["ru", "es", "de", "fr", "vi", "ja", "uz", "kk", "ky"]

CATEGORY_LABELS = {
    "ru": {
        "CTO Filter": "CTO-фильтр",
        "GAC UDF Filter": "Фильтр GAC/UDF",
        "Inline Filter": "Линейный фильтр",
        "PP Filter": "PP-фильтр",
        "RO Filter": "RO-фильтр",
        "RO Water Purifier": "RO очиститель воды",
        "Water Purifier": "Очиститель воды",
        "Water Dispenser": "Диспенсер воды",
        "Filter Housing": "Корпус фильтра",
        "Industrial Filter": "Промышленный фильтр",
        "Big Blue water filter": "Фильтр Big Blue",
    },
    "es": {
        "CTO Filter": "Filtro CTO",
        "GAC UDF Filter": "Filtro GAC/UDF",
        "Inline Filter": "Filtro en línea",
        "PP Filter": "Filtro PP",
        "RO Filter": "Filtro RO",
        "RO Water Purifier": "Purificador de agua RO",
        "Water Purifier": "Purificador de agua",
        "Water Dispenser": "Dispensador de agua",
        "Filter Housing": "Carcasa de filtro",
        "Industrial Filter": "Filtro industrial",
        "Big Blue water filter": "Filtro Big Blue",
    },
    "de": {
        "CTO Filter": "CTO-Filter",
        "GAC UDF Filter": "GAC/UDF-Filter",
        "Inline Filter": "Inline-Filter",
        "PP Filter": "PP-Filter",
        "RO Filter": "RO-Filter",
        "RO Water Purifier": "RO-Wasserreiniger",
        "Water Purifier": "Wasserreiniger",
        "Water Dispenser": "Wasserspender",
        "Filter Housing": "Filtergehäuse",
        "Industrial Filter": "Industriefilter",
        "Big Blue water filter": "Big-Blue-Filter",
    },
    "fr": {
        "CTO Filter": "Filtre CTO",
        "GAC UDF Filter": "Filtre GAC/UDF",
        "Inline Filter": "Filtre en ligne",
        "PP Filter": "Filtre PP",
        "RO Filter": "Filtre RO",
        "RO Water Purifier": "Purificateur d'eau RO",
        "Water Purifier": "Purificateur d'eau",
        "Water Dispenser": "Distributeur d'eau",
        "Filter Housing": "Boîtier de filtre",
        "Industrial Filter": "Filtre industriel",
        "Big Blue water filter": "Filtre Big Blue",
    },
    "vi": {
        "CTO Filter": "Lõi lọc CTO",
        "GAC UDF Filter": "Lõi lọc GAC/UDF",
        "Inline Filter": "Lõi lọc inline",
        "PP Filter": "Lõi lọc PP",
        "RO Filter": "Lọc RO",
        "RO Water Purifier": "Máy lọc nước RO",
        "Water Purifier": "Máy lọc nước",
        "Water Dispenser": "Cây nước",
        "Filter Housing": "Vỏ lọc",
        "Industrial Filter": "Bộ lọc công nghiệp",
        "Big Blue water filter": "Bộ lọc Big Blue",
    },
    "ja": {
        "CTO Filter": "CTOフィルター",
        "GAC UDF Filter": "GAC/UDFフィルター",
        "Inline Filter": "インラインフィルター",
        "PP Filter": "PPフィルター",
        "RO Filter": "ROフィルター",
        "RO Water Purifier": "RO浄水器",
        "Water Purifier": "浄水器",
        "Water Dispenser": "ウォーターディスペンサー",
        "Filter Housing": "フィルターハウジング",
        "Industrial Filter": "産業用フィルター",
        "Big Blue water filter": "Big Blueフィルター",
    },
    "uz": {
        "CTO Filter": "CTO filtri",
        "GAC UDF Filter": "GAC/UDF filtri",
        "Inline Filter": "Inline filtr",
        "PP Filter": "PP filtri",
        "RO Filter": "RO filtri",
        "RO Water Purifier": "RO suv tozalagich",
        "Water Purifier": "Suv tozalagich",
        "Water Dispenser": "Suv dispenseri",
        "Filter Housing": "Filtr korpusi",
        "Industrial Filter": "Sanoat filtri",
        "Big Blue water filter": "Big Blue filtri",
    },
    "kk": {
        "CTO Filter": "CTO сүзгісі",
        "GAC UDF Filter": "GAC/UDF сүзгісі",
        "Inline Filter": "Inline сүзгісі",
        "PP Filter": "PP сүзгісі",
        "RO Filter": "RO сүзгісі",
        "RO Water Purifier": "RO су тазартқыш",
        "Water Purifier": "Су тазартқыш",
        "Water Dispenser": "Су диспенсері",
        "Filter Housing": "Сүзгі корпусы",
        "Industrial Filter": "Өнеркәсіптік сүзгі",
        "Big Blue water filter": "Big Blue сүзгісі",
    },
    "ky": {
        "CTO Filter": "CTO сүзгү",
        "GAC UDF Filter": "GAC/UDF сүзгү",
        "Inline Filter": "Inline сүзгү",
        "PP Filter": "PP сүзгү",
        "RO Filter": "RO сүзгү",
        "RO Water Purifier": "RO суу тазалагыч",
        "Water Purifier": "Суу тазалагыч",
        "Water Dispenser": "Суу диспенсери",
        "Filter Housing": "Сүзгү корпусу",
        "Industrial Filter": "Өнөр жай сүзгүсү",
        "Big Blue water filter": "Big Blue сүзгү",
    },
}

EXTRA_REPLACEMENTS = {
    "uz": {
        "Sintered carbon · Coconut-shell media · selected NSF/ANSI test options": "Pishirilgan karbon · kokos qobig'i materiali · tanlangan NSF/ANSI sinov variantlari",
    },
    "ky": {
        "Sintered carbon · Coconut-shell media · selected NSF/ANSI test options": "Күйгүзүлгөн көмүр · кокос кабыгы материалы · тандалган NSF/ANSI сыноо варианттары",
        "CTO carbon block filter production line with coconut shell activated carbon media": "Кокос кабыгынан активдештирилген көмүр материалы бар CTO көмүр блок сүзгү өндүрүш линиясы",
    },
}


def localize_page(page: str, lang: str) -> str:
    for source, target in CATEGORY_LABELS[lang].items():
        page = page.replace(f">{source}<", f">{target}<")
        page = page.replace(f'"category":"{source}"', f'"category":"{target}"')
        page = page.replace(f'"category": "{source}"', f'"category": "{target}"')
    for source, target in EXTRA_REPLACEMENTS.get(lang, {}).items():
        page = page.replace(source, target)
    return page


def main() -> None:
    changed = 0
    scanned = 0
    for lang in LANGS:
        for path in (ROOT / lang).glob("*.html"):
            scanned += 1
            original = path.read_text(encoding="utf-8", errors="ignore")
            page = localize_page(original, lang)
            if page != original:
                path.write_text(page, encoding="utf-8")
                changed += 1
    print(f"Scanned {scanned} priority-language HTML files; changed {changed} files.")


if __name__ == "__main__":
    main()
