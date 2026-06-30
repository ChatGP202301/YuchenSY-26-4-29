#!/usr/bin/env python3
"""Make product/page names specific in priority language versions.

The generated multilingual pages had several generic names such as "filter
cartridge" or "water purifier" reused across different SKUs. This script keeps
the existing layout untouched and only updates visible names, title metadata,
card alt text, and matching JSON-LD product/breadcrumb names.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANGS = ["ru", "es", "de", "fr", "vi", "ja", "uz", "kk", "ky"]


PRODUCT_NAMES = {
    "ru": {
        "product-alkaline-purifier.html": "Щелочная система очистки воды",
        "product-uv-purifier.html": "Трехступенчатый УФ-очиститель воды Plus",
        "product-water-purifier-maifan.html": "Минерализующий очиститель воды с камнем Майфан",
        "product-antibacterial-mineralization.html": "Антибактериальный минерализующий фильтрующий картридж",
        "product-ceramic-filter.html": "Керамический фильтрующий картридж",
        "product-filter-combo.html": "Многоступенчатый комплект фильтрующих картриджей",
        "product-inline-small-mol.html": "Антибактериальный минерализующий фильтр малой молекулы",
        "product-mid-filter.html": "Средний фильтр для воды с медным соединителем",
        "product-carbon-block.html": "CTO фильтр из кокосового угольного блока",
        "product-carbon-block-2.html": "Прессованный активированный CTO угольный блок",
        "product-inline-cation-resin.html": "Линейный картридж с катионообменной смолой",
        "product-maifan-inline.html": "Линейный фильтр с камнем Майфан",
        "product-mineral-inline.html": "Линейный минерализующий фильтр",
        "product-inline-t33-coconut.html": "Линейный T33 фильтр с кокосовым углем",
        "product-inline-t33-mineral.html": "Минерализующий линейный фильтр T33",
        "product-post-t33.html": "Линейный угольный постфильтр T33",
        "product-t33-post.html": "Постфильтрующий картридж T33",
        "product-pp-fin-cap.html": "PP melt-blown фильтр с ребристой торцевой крышкой",
        "product-pp-silicon-ring.html": "PP melt-blown фильтр с силиконовым кольцом",
        "product-pp-spun.html": "PP melt-blown осадочный фильтрующий картридж",
        "product-ppf-cartridge.html": "PP melt-blown картридж из полипропиленового волокна",
        "product-uf-cartridge.html": "Ультрафильтрационный (UF) картридж",
        "product-uf-filter-2.html": "UF фильтр с полым волокном",
        "product-resin-filter.html": "Фильтр с ионообменной смолой",
        "product-ultra-film.html": "Ультрафильтрационный пленочный картридж",
        "product-built-in-pressure-tank-ro.html": "RO очиститель воды со встроенным баком 100G/200G",
        "product-custom-5-6-7-stage-ro-water-purifier.html": "Настраиваемый 5/6/7-ступенчатый RO очиститель воды",
    },
    "es": {
        "product-alkaline-purifier.html": "Sistema purificador de agua alcalina",
        "product-uv-purifier.html": "Purificador de agua UV Plus de tres etapas",
        "product-water-purifier-maifan.html": "Purificador mineralizante con piedra Maifan",
        "product-antibacterial-mineralization.html": "Cartucho filtrante antibacteriano y mineralizante",
        "product-ceramic-filter.html": "Cartucho filtrante cerámico",
        "product-filter-combo.html": "Combinación de cartuchos filtrantes multietapa",
        "product-inline-small-mol.html": "Filtro antibacteriano mineralizante de molécula pequeña",
        "product-mid-filter.html": "Filtro de agua mediano con conector de cobre",
        "product-carbon-block.html": "Filtro CTO de carbón de cáscara de coco",
        "product-carbon-block-2.html": "Bloque CTO de carbón activado comprimido",
        "product-inline-cation-resin.html": "Cartucho en línea de resina catiónica",
        "product-maifan-inline.html": "Filtro en línea de piedra Maifan",
        "product-mineral-inline.html": "Filtro mineral en línea",
        "product-inline-t33-coconut.html": "Filtro T33 en línea de carbón de coco",
        "product-inline-t33-mineral.html": "Filtro de agua T33 en línea mineralizado",
        "product-post-t33.html": "Postfiltro de carbón T33 en línea",
        "product-t33-post.html": "Cartucho postfiltro T33",
        "product-pp-fin-cap.html": "Filtro PP melt blown con tapa de aletas",
        "product-pp-silicon-ring.html": "Filtro PP melt blown con anillo de silicona",
        "product-pp-spun.html": "Cartucho sedimentario PP melt blown",
        "product-ppf-cartridge.html": "Cartucho PP de fibra de polipropileno melt blown",
        "product-uf-cartridge.html": "Cartucho de ultrafiltración (UF)",
        "product-uf-filter-2.html": "Filtro UF de fibra hueca",
        "product-resin-filter.html": "Filtro de resina de intercambio iónico",
        "product-ultra-film.html": "Cartucho de membrana de ultrafiltración",
        "product-built-in-pressure-tank-ro.html": "Purificador RO con tanque integrado 100G/200G",
        "product-custom-5-6-7-stage-ro-water-purifier.html": "Purificador RO personalizable de 5/6/7 etapas",
    },
    "de": {
        "product-alkaline-purifier.html": "Alkalisches Wasserreinigungssystem",
        "product-uv-purifier.html": "Dreistufiger UV-Wasserreiniger Plus",
        "product-water-purifier-maifan.html": "Mineralisierender Maifan-Stein-Wasserreiniger",
        "product-antibacterial-mineralization.html": "Antibakterielle Mineralisierungs-Filterkartusche",
        "product-ceramic-filter.html": "Keramik-Filterkartusche",
        "product-filter-combo.html": "Mehrstufige Filterkartuschen-Kombination",
        "product-inline-small-mol.html": "Antibakterieller Mineralisierungsfilter für kleine Moleküle",
        "product-mid-filter.html": "Mittelgroßer Wasserfilter mit Kupferanschluss",
        "product-carbon-block.html": "CTO-Kokosnussschalen-Kohlenstoffblockfilter",
        "product-carbon-block-2.html": "Gepresster CTO-Aktivkohleblock",
        "product-inline-cation-resin.html": "Inline-Kationenaustauscherharz-Filterkartusche",
        "product-maifan-inline.html": "Maifan-Stein-Inline-Filter",
        "product-mineral-inline.html": "Inline-Mineralfilter",
        "product-inline-t33-coconut.html": "T33-Inline-Kokosnuss-Kohlenstofffilter",
        "product-inline-t33-mineral.html": "Mineralisierter T33-Inline-Wasserfilter",
        "product-post-t33.html": "T33-Inline-Kohlenstoff-Nachfilter",
        "product-t33-post.html": "T33-Nachfilterkartusche",
        "product-pp-fin-cap.html": "PP-Melt-Blown-Filter mit Lamellen-Endkappe",
        "product-pp-silicon-ring.html": "PP-Melt-Blown-Filter mit Silikonring",
        "product-pp-spun.html": "PP-Melt-Blown-Sedimentfilterkartusche",
        "product-ppf-cartridge.html": "PP-Melt-Blown-Polypropylenfaser-Kartusche",
        "product-uf-cartridge.html": "Ultrafiltrationskartusche (UF)",
        "product-uf-filter-2.html": "UF-Hohlfaserfilter",
        "product-resin-filter.html": "Ionenaustauscherharz-Filter",
        "product-ultra-film.html": "Ultrafiltrations-Membrankartusche",
        "product-built-in-pressure-tank-ro.html": "RO-Wasserreiniger mit integriertem Tank 100G/200G",
        "product-custom-5-6-7-stage-ro-water-purifier.html": "Anpassbarer 5/6/7-stufiger RO-Wasserreiniger",
    },
    "fr": {
        "product-alkaline-purifier.html": "Système purificateur d'eau alcaline",
        "product-uv-purifier.html": "Purificateur d'eau UV Plus à trois étapes",
        "product-water-purifier-maifan.html": "Purificateur minéralisant à pierre Maifan",
        "product-antibacterial-mineralization.html": "Cartouche filtrante antibactérienne et minéralisante",
        "product-ceramic-filter.html": "Cartouche filtrante céramique",
        "product-filter-combo.html": "Ensemble de cartouches filtrantes multi-étapes",
        "product-inline-small-mol.html": "Filtre antibactérien minéralisant à petites molécules",
        "product-mid-filter.html": "Filtre à eau moyen avec raccord en cuivre",
        "product-carbon-block.html": "Filtre bloc de charbon CTO en coque de noix de coco",
        "product-carbon-block-2.html": "Bloc de charbon actif CTO comprimé",
        "product-inline-cation-resin.html": "Cartouche filtrante en ligne à résine cationique",
        "product-maifan-inline.html": "Filtre en ligne à pierre Maifan",
        "product-mineral-inline.html": "Filtre minéral en ligne",
        "product-inline-t33-coconut.html": "Filtre T33 en ligne au charbon de coco",
        "product-inline-t33-mineral.html": "Filtre à eau T33 minéralisant en ligne",
        "product-post-t33.html": "Post-filtre charbon T33 en ligne",
        "product-t33-post.html": "Cartouche post-filtre T33",
        "product-pp-fin-cap.html": "Filtre PP melt blown avec embout à ailettes",
        "product-pp-silicon-ring.html": "Filtre PP melt blown avec bague silicone",
        "product-pp-spun.html": "Cartouche sédiments PP melt blown",
        "product-ppf-cartridge.html": "Cartouche PP en fibre de polypropylène melt blown",
        "product-uf-cartridge.html": "Cartouche d'ultrafiltration (UF)",
        "product-uf-filter-2.html": "Filtre UF à fibres creuses",
        "product-resin-filter.html": "Filtre à résine échangeuse d'ions",
        "product-ultra-film.html": "Cartouche membrane d'ultrafiltration",
        "product-built-in-pressure-tank-ro.html": "Purificateur RO avec réservoir intégré 100G/200G",
        "product-custom-5-6-7-stage-ro-water-purifier.html": "Purificateur RO personnalisable 5/6/7 étapes",
    },
    "vi": {
        "product-alkaline-purifier.html": "Hệ thống máy lọc nước kiềm",
        "product-uv-purifier.html": "Máy lọc nước UV ba cấp Plus",
        "product-water-purifier-maifan.html": "Máy lọc khoáng đá Maifan",
        "product-antibacterial-mineralization.html": "Lõi lọc kháng khuẩn khoáng hóa",
        "product-ceramic-filter.html": "Lõi lọc gốm",
        "product-filter-combo.html": "Bộ lõi lọc nhiều cấp",
        "product-inline-small-mol.html": "Lõi lọc khoáng hóa kháng khuẩn phân tử nhỏ",
        "product-mid-filter.html": "Bộ lọc nước cỡ trung với đầu nối đồng",
        "product-carbon-block.html": "Lõi lọc CTO carbon gáo dừa",
        "product-carbon-block-2.html": "Khối carbon hoạt tính CTO nén",
        "product-inline-cation-resin.html": "Lõi lọc inline nhựa cation",
        "product-maifan-inline.html": "Lõi lọc inline đá Maifan",
        "product-mineral-inline.html": "Lõi lọc khoáng inline",
        "product-inline-t33-coconut.html": "Lõi lọc T33 inline carbon gáo dừa",
        "product-inline-t33-mineral.html": "Lõi lọc nước T33 inline khoáng hóa",
        "product-post-t33.html": "Lõi hậu lọc carbon T33 inline",
        "product-t33-post.html": "Lõi hậu lọc T33",
        "product-pp-fin-cap.html": "Lõi PP melt blown nắp cánh",
        "product-pp-silicon-ring.html": "Lõi PP melt blown vòng silicone",
        "product-pp-spun.html": "Lõi lọc cặn PP melt blown",
        "product-ppf-cartridge.html": "Lõi PP sợi polypropylene melt blown",
        "product-uf-cartridge.html": "Lõi siêu lọc (UF)",
        "product-uf-filter-2.html": "Lõi UF sợi rỗng",
        "product-resin-filter.html": "Lõi lọc nhựa trao đổi ion",
        "product-ultra-film.html": "Lõi màng siêu lọc",
        "product-built-in-pressure-tank-ro.html": "Máy lọc RO bình áp tích hợp 100G/200G",
        "product-custom-5-6-7-stage-ro-water-purifier.html": "Máy lọc RO tùy chỉnh 5/6/7 cấp",
    },
    "ja": {
        "product-alkaline-purifier.html": "アルカリ浄水システム",
        "product-uv-purifier.html": "三段式Plus UV浄水器",
        "product-water-purifier-maifan.html": "麦飯石ミネラル浄水器",
        "product-antibacterial-mineralization.html": "抗菌ミネラル化フィルターカートリッジ",
        "product-ceramic-filter.html": "セラミックフィルターカートリッジ",
        "product-filter-combo.html": "多段式フィルターカートリッジセット",
        "product-inline-small-mol.html": "小分子抗菌ミネラル化フィルター",
        "product-mid-filter.html": "銅コネクター付き中型浄水フィルター",
        "product-carbon-block.html": "ココナッツシェルCTOカーボンブロックフィルター",
        "product-carbon-block-2.html": "圧縮活性CTOカーボンブロック",
        "product-inline-cation-resin.html": "カチオン樹脂インラインフィルターカートリッジ",
        "product-maifan-inline.html": "麦飯石インラインフィルター",
        "product-mineral-inline.html": "インラインミネラルフィルター",
        "product-inline-t33-coconut.html": "T33インラインココナッツカーボンフィルター",
        "product-inline-t33-mineral.html": "ミネラル化T33インライン浄水フィルター",
        "product-post-t33.html": "T33インラインカーボンポストフィルター",
        "product-t33-post.html": "T33ポストフィルターカートリッジ",
        "product-pp-fin-cap.html": "フィンエンドキャップ付きPPメルトブローンフィルター",
        "product-pp-silicon-ring.html": "シリコンリング付きPPメルトブローンフィルター",
        "product-pp-spun.html": "PPメルトブローン沈殿物フィルターカートリッジ",
        "product-ppf-cartridge.html": "PPメルトブローンポリプロピレン繊維カートリッジ",
        "product-uf-cartridge.html": "限外ろ過（UF）カートリッジ",
        "product-uf-filter-2.html": "UF中空糸フィルター",
        "product-resin-filter.html": "イオン交換樹脂フィルター",
        "product-ultra-film.html": "限外ろ過膜カートリッジ",
        "product-built-in-pressure-tank-ro.html": "内蔵タンク式RO浄水器 100G/200G",
        "product-custom-5-6-7-stage-ro-water-purifier.html": "カスタム5/6/7段式RO浄水器",
    },
    "uz": {
        "product-alkaline-purifier.html": "Ishqoriy suv tozalash tizimi",
        "product-uv-purifier.html": "Uch bosqichli Plus UV suv tozalagich",
        "product-water-purifier-maifan.html": "Maifan toshli minerallashtiruvchi tozalagich",
        "product-antibacterial-mineralization.html": "Antibakterial minerallashtiruvchi filtr kartriji",
        "product-ceramic-filter.html": "Keramik filtr kartriji",
        "product-filter-combo.html": "Ko'p bosqichli filtr kartrijlari to'plami",
        "product-inline-small-mol.html": "Kichik molekulali antibakterial minerallashtiruvchi filtr",
        "product-mid-filter.html": "Mis ulagichli o'rta o'lchamli suv filtri",
        "product-carbon-block.html": "Kokos qobig'i CTO karbon blok filtri",
        "product-carbon-block-2.html": "Siqilgan faol CTO karbon bloki",
        "product-inline-cation-resin.html": "Kation smolali inline filtr kartriji",
        "product-maifan-inline.html": "Maifan toshli inline filtr",
        "product-mineral-inline.html": "Inline mineral filtr",
        "product-inline-t33-coconut.html": "T33 inline kokos karbon filtri",
        "product-inline-t33-mineral.html": "Minerallashtirilgan T33 inline suv filtri",
        "product-post-t33.html": "T33 inline karbon postfiltri",
        "product-t33-post.html": "T33 postfiltr kartriji",
        "product-pp-fin-cap.html": "Qanotli uch qopqoqli PP melt blown filtr",
        "product-pp-silicon-ring.html": "Silikon halqali PP melt blown filtr",
        "product-pp-spun.html": "PP melt blown cho'kindi filtr kartriji",
        "product-ppf-cartridge.html": "PP melt blown polipropilen tolali kartrij",
        "product-uf-cartridge.html": "Ultrafiltratsiya (UF) kartriji",
        "product-uf-filter-2.html": "UF ichi bo'sh tolali filtr",
        "product-resin-filter.html": "Ion almashuvchi smolali filtr",
        "product-ultra-film.html": "Ultrafiltratsiya membrana kartriji",
        "product-built-in-pressure-tank-ro.html": "Ichki bakli RO suv tozalagich 100G/200G",
        "product-custom-5-6-7-stage-ro-water-purifier.html": "Moslashtiriladigan 5/6/7 bosqichli RO suv tozalagich",
    },
    "kk": {
        "product-alkaline-purifier.html": "Сілтілі су тазарту жүйесі",
        "product-uv-purifier.html": "Үш сатылы Plus UV су тазартқыш",
        "product-water-purifier-maifan.html": "Maifan тасты минералдандырғыш тазартқыш",
        "product-antibacterial-mineralization.html": "Антибактериялық минералдандырғыш сүзгі картриджі",
        "product-ceramic-filter.html": "Керамикалық сүзгі картриджі",
        "product-filter-combo.html": "Көп сатылы сүзгі картридждері жиынтығы",
        "product-inline-small-mol.html": "Кіші молекулалы антибактериялық минералдандырғыш сүзгі",
        "product-mid-filter.html": "Мыс қосқышы бар орта өлшемді су сүзгісі",
        "product-carbon-block.html": "Кокос қабығы CTO көмір блок сүзгісі",
        "product-carbon-block-2.html": "Сығымдалған белсенді CTO көмір блогы",
        "product-inline-cation-resin.html": "Катион шайыры бар inline сүзгі картриджі",
        "product-maifan-inline.html": "Maifan тасты inline сүзгі",
        "product-mineral-inline.html": "Inline минерал сүзгі",
        "product-inline-t33-coconut.html": "T33 inline кокос көмір сүзгісі",
        "product-inline-t33-mineral.html": "Минералдандырылған T33 inline су сүзгісі",
        "product-post-t33.html": "T33 inline көмір постфильтрі",
        "product-t33-post.html": "T33 постфильтр картриджі",
        "product-pp-fin-cap.html": "Қанатты қақпағы бар PP melt blown сүзгі",
        "product-pp-silicon-ring.html": "Силикон сақинасы бар PP melt blown сүзгі",
        "product-pp-spun.html": "PP melt blown шөгінді сүзгі картриджі",
        "product-ppf-cartridge.html": "PP melt blown полипропилен талшық картриджі",
        "product-uf-cartridge.html": "Ультрафильтрация (UF) картриджі",
        "product-uf-filter-2.html": "UF қуыс талшық сүзгісі",
        "product-resin-filter.html": "Ион алмастырғыш шайыр сүзгісі",
        "product-ultra-film.html": "Ультрафильтрациялық мембрана картриджі",
        "product-built-in-pressure-tank-ro.html": "Кіріктірілген бакты RO су тазартқыш 100G/200G",
        "product-custom-5-6-7-stage-ro-water-purifier.html": "Бапталатын 5/6/7 сатылы RO су тазартқыш",
    },
    "ky": {
        "product-alkaline-purifier.html": "Шелочтуу суу тазалоо системасы",
        "product-uv-purifier.html": "Үч баскычтуу Plus UV суу тазалагыч",
        "product-water-purifier-maifan.html": "Maifan таштуу минералдаштыруучу тазалагыч",
        "product-antibacterial-mineralization.html": "Антибактериалдык минералдаштыруучу сүзгү картриджи",
        "product-ceramic-filter.html": "Керамикалык сүзгү картриджи",
        "product-filter-combo.html": "Көп баскычтуу сүзгү картридждеринин топтому",
        "product-inline-small-mol.html": "Кичине молекулалуу антибактериалдык минералдаштыруучу сүзгү",
        "product-mid-filter.html": "Жез туташтыргычы бар орточо көлөмдөгү суу сүзгүсү",
        "product-carbon-block.html": "Кокос кабыгынан CTO көмүр блок сүзгү",
        "product-carbon-block-2.html": "Кысылган активдүү CTO көмүр блогу",
        "product-inline-cation-resin.html": "Катион чайыры бар inline сүзгү картриджи",
        "product-maifan-inline.html": "Maifan таштуу inline сүзгү",
        "product-mineral-inline.html": "Inline минерал сүзгү",
        "product-inline-t33-coconut.html": "T33 inline кокос көмүр сүзгү",
        "product-inline-t33-mineral.html": "Минералдаштырылган T33 inline суу сүзгүсү",
        "product-post-t33.html": "T33 inline көмүр постфильтри",
        "product-t33-post.html": "T33 постфильтр картриджи",
        "product-pp-fin-cap.html": "Канаттуу уч капкагы бар PP melt blown сүзгү",
        "product-pp-silicon-ring.html": "Силикон шакеги бар PP melt blown сүзгү",
        "product-pp-spun.html": "PP melt blown чөкмө сүзгү картриджи",
        "product-ppf-cartridge.html": "PP melt blown полипропилен була картриджи",
        "product-uf-cartridge.html": "Ультрафильтрация (UF) картриджи",
        "product-uf-filter-2.html": "UF көңдөй була сүзгүсү",
        "product-resin-filter.html": "Ион алмаштыруучу чайыр сүзгүсү",
        "product-ultra-film.html": "Ультрафильтрация мембрана картриджи",
        "product-built-in-pressure-tank-ro.html": "Ички бактуу RO суу тазалагыч 100G/200G",
        "product-custom-5-6-7-stage-ro-water-purifier.html": "Ыңгайлаштырылуучу 5/6/7 баскычтуу RO суу тазалагыч",
    },
}


CATEGORY_NAMES = {
    "ru": {
        "pp-melt-blown-filter-cartridge.html": "Категория PP melt-blown фильтрующих картриджей",
        "cto-carbon-block-filter.html": "Категория CTO угольных блок-фильтров",
        "gac-udf-filter-cartridge.html": "Категория GAC/UDF фильтрующих картриджей",
        "t33-inline-filter.html": "Категория линейных фильтров T33",
        "ro-membrane.html": "Категория мембран обратного осмоса RO",
        "uf-membrane-filter.html": "Категория UF мембранных фильтров",
        "water-dispenser.html": "Категория диспенсеров воды",
        "ro-water-purifier.html": "Категория RO систем очистки воды",
        "filter-housing.html": "Категория корпусов фильтров",
        "privacy-policy.html": "Политика конфиденциальности",
    },
    "es": {
        "pp-melt-blown-filter-cartridge.html": "Categoría de cartuchos PP melt blown",
        "cto-carbon-block-filter.html": "Categoría de filtros CTO de bloque de carbón",
        "gac-udf-filter-cartridge.html": "Categoría de cartuchos GAC/UDF",
        "t33-inline-filter.html": "Categoría de filtros en línea T33",
        "ro-membrane.html": "Categoría de membranas RO",
        "uf-membrane-filter.html": "Categoría de filtros de membrana UF",
        "water-dispenser.html": "Categoría de dispensadores de agua",
        "ro-water-purifier.html": "Categoría de purificadores de agua RO",
        "filter-housing.html": "Categoría de carcasas de filtro",
        "privacy-policy.html": "Política de privacidad",
    },
    "de": {
        "pp-melt-blown-filter-cartridge.html": "Kategorie PP-Melt-Blown-Filterkartuschen",
        "cto-carbon-block-filter.html": "Kategorie CTO-Kohlenstoffblockfilter",
        "gac-udf-filter-cartridge.html": "Kategorie GAC/UDF-Filterkartuschen",
        "t33-inline-filter.html": "Kategorie T33-Inline-Filter",
        "ro-membrane.html": "Kategorie RO-Membranen",
        "uf-membrane-filter.html": "Kategorie UF-Membranfilter",
        "water-dispenser.html": "Kategorie Wasserspender",
        "ro-water-purifier.html": "Kategorie RO-Wasserreiniger",
        "filter-housing.html": "Kategorie Filtergehäuse",
        "privacy-policy.html": "Datenschutzerklärung",
    },
    "fr": {
        "pp-melt-blown-filter-cartridge.html": "Catégorie cartouches PP melt blown",
        "cto-carbon-block-filter.html": "Catégorie filtres bloc de charbon CTO",
        "gac-udf-filter-cartridge.html": "Catégorie cartouches GAC/UDF",
        "t33-inline-filter.html": "Catégorie filtres en ligne T33",
        "ro-membrane.html": "Catégorie membranes RO",
        "uf-membrane-filter.html": "Catégorie filtres membrane UF",
        "water-dispenser.html": "Catégorie distributeurs d'eau",
        "ro-water-purifier.html": "Catégorie purificateurs d'eau RO",
        "filter-housing.html": "Catégorie boîtiers de filtre",
        "privacy-policy.html": "Politique de confidentialité",
    },
    "vi": {
        "pp-melt-blown-filter-cartridge.html": "Danh mục lõi lọc PP melt blown",
        "cto-carbon-block-filter.html": "Danh mục lõi lọc CTO carbon block",
        "gac-udf-filter-cartridge.html": "Danh mục lõi lọc GAC/UDF",
        "t33-inline-filter.html": "Danh mục lõi lọc inline T33",
        "ro-membrane.html": "Danh mục màng RO",
        "uf-membrane-filter.html": "Danh mục màng lọc UF",
        "water-dispenser.html": "Danh mục máy nóng lạnh nước",
        "ro-water-purifier.html": "Danh mục máy lọc nước RO",
        "filter-housing.html": "Danh mục vỏ lọc",
        "privacy-policy.html": "Chính sách bảo mật",
    },
    "ja": {
        "pp-melt-blown-filter-cartridge.html": "PPメルトブローンフィルターカートリッジカテゴリ",
        "cto-carbon-block-filter.html": "CTOカーボンブロックフィルターカテゴリ",
        "gac-udf-filter-cartridge.html": "GAC/UDFフィルターカートリッジカテゴリ",
        "t33-inline-filter.html": "T33インラインフィルターカテゴリ",
        "ro-membrane.html": "RO膜カテゴリ",
        "uf-membrane-filter.html": "UF膜フィルターカテゴリ",
        "water-dispenser.html": "ウォーターディスペンサーカテゴリ",
        "ro-water-purifier.html": "RO浄水器カテゴリ",
        "filter-housing.html": "フィルターハウジングカテゴリ",
        "privacy-policy.html": "プライバシーポリシー",
    },
    "uz": {
        "pp-melt-blown-filter-cartridge.html": "PP melt blown filtr kartrijlari toifasi",
        "cto-carbon-block-filter.html": "CTO karbon blok filtrlari toifasi",
        "gac-udf-filter-cartridge.html": "GAC/UDF filtr kartrijlari toifasi",
        "t33-inline-filter.html": "T33 inline filtrlari toifasi",
        "ro-membrane.html": "RO membranalari toifasi",
        "uf-membrane-filter.html": "UF membrana filtrlari toifasi",
        "water-dispenser.html": "Suv dispenserlari toifasi",
        "ro-water-purifier.html": "RO suv tozalagichlari toifasi",
        "filter-housing.html": "Filtr korpuslari toifasi",
        "privacy-policy.html": "Maxfiylik siyosati",
    },
    "kk": {
        "pp-melt-blown-filter-cartridge.html": "PP melt blown сүзгі картридждері санаты",
        "cto-carbon-block-filter.html": "CTO көмір блок сүзгілері санаты",
        "gac-udf-filter-cartridge.html": "GAC/UDF сүзгі картридждері санаты",
        "t33-inline-filter.html": "T33 inline сүзгілері санаты",
        "ro-membrane.html": "RO мембраналары санаты",
        "uf-membrane-filter.html": "UF мембраналық сүзгілер санаты",
        "water-dispenser.html": "Су диспенсерлері санаты",
        "ro-water-purifier.html": "RO су тазартқыштары санаты",
        "filter-housing.html": "Сүзгі корпустары санаты",
        "privacy-policy.html": "Құпиялылық саясаты",
    },
    "ky": {
        "pp-melt-blown-filter-cartridge.html": "PP melt blown сүзгү картридждери категориясы",
        "cto-carbon-block-filter.html": "CTO көмүр блок сүзгүлөрү категориясы",
        "gac-udf-filter-cartridge.html": "GAC/UDF сүзгү картридждери категориясы",
        "t33-inline-filter.html": "T33 inline сүзгүлөрү категориясы",
        "ro-membrane.html": "RO мембраналары категориясы",
        "uf-membrane-filter.html": "UF мембрана сүзгүлөрү категориясы",
        "water-dispenser.html": "Суу диспенсерлери категориясы",
        "ro-water-purifier.html": "RO суу тазалагычтар категориясы",
        "filter-housing.html": "Сүзгү корпустары категориясы",
        "privacy-policy.html": "Купуялык саясаты",
    },
}


def page_names(lang: str) -> dict[str, str]:
    merged = {}
    merged.update(PRODUCT_NAMES.get(lang, {}))
    merged.update(CATEGORY_NAMES.get(lang, {}))
    return merged


def set_title_meta(page: str, name: str) -> str:
    new_title = f"{name} | Yuchen Water"
    page = re.sub(
        r"<title>.*?</title>",
        f"<title>{html.escape(new_title)}</title>",
        page,
        count=1,
        flags=re.S,
    )
    for pattern in [
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        r'(<meta\s+name="twitter:title"\s+content=")[^"]*(")',
    ]:
        page = re.sub(
            pattern,
            lambda m: f'{m.group(1)}{html.escape(new_title, quote=True)}{m.group(2)}',
            page,
            count=1,
            flags=re.S,
        )
    return page


def set_first_h1(page: str, name: str) -> str:
    return re.sub(
        r"(<h1[^>]*>)(.*?)(</h1>)",
        lambda m: f"{m.group(1)}{html.escape(name)}{m.group(3)}",
        page,
        count=1,
        flags=re.S,
    )


def update_json_obj(obj, filename: str, lang: str, name: str):
    if isinstance(obj, dict):
        obj_type = obj.get("@type")
        types = obj_type if isinstance(obj_type, list) else [obj_type]
        current_url = str(obj.get("url", ""))
        current_id = str(obj.get("@id", ""))
        if "Product" in types and f"/{lang}/{filename}" in (current_url + current_id):
            obj["name"] = name
        if obj_type == "BreadcrumbList":
            for item in obj.get("itemListElement", []):
                if isinstance(item, dict) and filename in str(item.get("item", "")):
                    item["name"] = name
        for value in obj.values():
            update_json_obj(value, filename, lang, name)
    elif isinstance(obj, list):
        for item in obj:
            update_json_obj(item, filename, lang, name)


def update_json_ld(page: str, filename: str, lang: str, name: str) -> str:
    def repl(match: re.Match[str]) -> str:
        raw = match.group(1)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return match.group(0)
        update_json_obj(data, filename, lang, name)
        dumped = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        return f'<script type="application/ld+json">{dumped}</script>'

    return re.sub(
        r'<script type="application/ld\+json">(.*?)</script>',
        repl,
        page,
        flags=re.S,
    )


def update_cards(page: str, names: dict[str, str]) -> str:
    def rewrite(match: re.Match[str]) -> str:
        card = match.group(0)
        href = re.search(r'href="(?:\./)?([^"#?]+\.html)"', card)
        if not href:
            return card
        filename = Path(href.group(1)).name
        name = names.get(filename)
        if not name:
            return card
        card = re.sub(
            r"(<h3[^>]*>)(.*?)(</h3>)",
            lambda m: f"{m.group(1)}{html.escape(name)}{m.group(3)}",
            card,
            count=1,
            flags=re.S,
        )
        card = re.sub(
            r'alt="[^"]*"',
            f'alt="{html.escape(name, quote=True)}"',
            card,
            count=1,
        )
        return card

    return re.sub(r'<article class="product-card"[^>]*>.*?</article>', rewrite, page, flags=re.S)


def fix_file(path: Path, lang: str) -> bool:
    original = path.read_text(encoding="utf-8")
    page = original
    names = page_names(lang)
    name = names.get(path.name)
    if name:
        page = set_first_h1(page, name)
        page = set_title_meta(page, name)
        page = update_json_ld(page, path.name, lang, name)
    page = update_cards(page, PRODUCT_NAMES.get(lang, {}))
    if page != original:
        path.write_text(page, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    scanned = 0
    for lang in LANGS:
        folder = ROOT / lang
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.html")):
            scanned += 1
            if fix_file(path, lang):
                changed += 1
    print(f"Scanned {scanned} priority-language HTML files; changed {changed} files.")


if __name__ == "__main__":
    main()
