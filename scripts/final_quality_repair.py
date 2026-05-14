#!/usr/bin/env python3
"""Final static-site quality repairs for localization and repeated UI.

This pass is intentionally conservative: it does not try to machine-translate
long product prose, but it removes repeated visible English UI leftovers,
repairs malformed Russian product-card titles, and deduplicates product
category filters.
"""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LANGS = [
    "en", "es", "fr", "de", "pt", "ru", "ar", "ja", "ko", "it", "tr",
    "hi", "bn", "id", "vi", "th", "pl", "nl", "fa", "ur", "ms", "tl",
    "he", "el", "cs", "hu", "ro", "sv", "da", "fi", "no", "uk", "bg",
    "hr", "sr", "sk", "sl", "lt", "et", "lv", "sw", "ha", "zu", "ta", "kk",
]

COMMON = {
    "es": {"related": "Productos relacionados", "years": "Años de experiencia", "countries": "Países atendidos", "factory": "m² de fábrica", "skus": "Referencias de producto", "email": "Correo electrónico", "leading": "Fabricante líder de filtros de agua en China | Fábrica certificada NSF e ISO"},
    "fr": {"related": "Produits associés", "years": "Années d'expérience", "countries": "Pays desservis", "factory": "m² de surface d'usine", "skus": "Références produit", "email": "E-mail", "leading": "Fabricant chinois leader de filtres à eau | Usine certifiée NSF et ISO"},
    "de": {"related": "Verwandte Produkte", "years": "Jahre Erfahrung", "countries": "Belieferte Länder", "factory": "m² Werksfläche", "skus": "Produkt-SKUs", "email": "E-Mail", "leading": "Führender Wasserfilter-Hersteller in China | NSF- und ISO-zertifizierte Fabrik"},
    "pt": {"related": "Produtos relacionados", "years": "Anos de experiência", "countries": "Países atendidos", "factory": "m² de área fabril", "skus": "SKUs de produto", "email": "E-mail", "leading": "Fabricante líder de filtros de água na China | Fábrica certificada NSF e ISO"},
    "ru": {"related": "Похожие товары", "years": "Лет опыта", "countries": "Стран поставок", "factory": "м² площадь фабрики", "skus": "Артикулов продукции", "email": "Электронная почта", "leading": "Ведущий китайский производитель фильтров для воды | Фабрика с сертификатами NSF и ISO"},
    "ar": {"related": "منتجات ذات صلة", "years": "سنوات الخبرة", "countries": "الدول المخدومة", "factory": "م² مساحة المصنع", "skus": "رموز المنتجات", "email": "البريد الإلكتروني", "leading": "شركة صينية رائدة في تصنيع فلاتر المياه | مصنع معتمد من NSF و ISO"},
    "ja": {"related": "関連製品", "years": "年の経験", "countries": "対応国", "factory": "m² 工場面積", "skus": "製品SKU", "email": "メール", "leading": "中国の水フィルターメーカー | NSF・ISO認定工場"},
    "ko": {"related": "관련 제품", "years": "업력", "countries": "수출 국가", "factory": "m² 공장 면적", "skus": "제품 SKU", "email": "이메일", "leading": "중국 대표 정수 필터 제조사 | NSF 및 ISO 인증 공장"},
    "it": {"related": "Prodotti correlati", "years": "Anni di esperienza", "countries": "Paesi serviti", "factory": "m² di area produttiva", "skus": "SKU prodotto", "email": "E-mail", "leading": "Produttore leader cinese di filtri per acqua | Fabbrica certificata NSF e ISO"},
    "tr": {"related": "İlgili ürünler", "years": "Yıllık deneyim", "countries": "Hizmet verilen ülke", "factory": "m² fabrika alanı", "skus": "Ürün SKU'ları", "email": "E-posta", "leading": "Çin'in önde gelen su filtresi üreticisi | NSF ve ISO sertifikalı fabrika"},
    "hi": {"related": "संबंधित उत्पाद", "years": "वर्षों का अनुभव", "countries": "सेवा प्राप्त देश", "factory": "m² फैक्टरी क्षेत्र", "skus": "उत्पाद SKU", "email": "ईमेल", "leading": "चीन का अग्रणी जल फ़िल्टर निर्माता | NSF और ISO प्रमाणित फैक्टरी"},
    "bn": {"related": "সম্পর্কিত পণ্য", "years": "বছরের অভিজ্ঞতা", "countries": "সেবা দেওয়া দেশ", "factory": "m² কারখানা এলাকা", "skus": "পণ্য SKU", "email": "ইমেইল", "leading": "চীনের শীর্ষস্থানীয় জল ফিল্টার প্রস্তুতকারক | NSF ও ISO সার্টিফায়েড কারখানা"},
    "id": {"related": "Produk terkait", "years": "Tahun pengalaman", "countries": "Negara terlayani", "factory": "m² area pabrik", "skus": "SKU produk", "email": "Email", "leading": "Produsen filter air terkemuka di China | Pabrik bersertifikat NSF dan ISO"},
    "vi": {"related": "Sản phẩm liên quan", "years": "Năm kinh nghiệm", "countries": "Quốc gia phục vụ", "factory": "m² diện tích nhà máy", "skus": "Mã sản phẩm", "email": "Email", "leading": "Nhà sản xuất lõi lọc nước hàng đầu Trung Quốc | Nhà máy đạt chứng nhận NSF và ISO"},
    "th": {"related": "สินค้าที่เกี่ยวข้อง", "years": "ปีประสบการณ์", "countries": "ประเทศที่ให้บริการ", "factory": "ม² พื้นที่โรงงาน", "skus": "SKU สินค้า", "email": "อีเมล", "leading": "ผู้ผลิตไส้กรองน้ำชั้นนำของจีน | โรงงานได้รับรอง NSF และ ISO"},
    "pl": {"related": "Produkty powiązane", "years": "Lat doświadczenia", "countries": "Obsługiwane kraje", "factory": "m² powierzchni fabryki", "skus": "SKU produktów", "email": "E-mail", "leading": "Wiodący chiński producent filtrów do wody | Fabryka z certyfikatami NSF i ISO"},
    "nl": {"related": "Gerelateerde producten", "years": "Jaar ervaring", "countries": "Bediende landen", "factory": "m² fabrieksoppervlak", "skus": "Product-SKU's", "email": "E-mail", "leading": "Toonaangevende Chinese fabrikant van waterfilters | NSF- en ISO-gecertificeerde fabriek"},
    "fa": {"related": "محصولات مرتبط", "years": "سال تجربه", "countries": "کشورهای تحت پوشش", "factory": "متر مربع مساحت کارخانه", "skus": "کدهای محصول", "email": "ایمیل", "leading": "تولیدکننده پیشرو فیلتر آب در چین | کارخانه دارای گواهی NSF و ISO"},
    "ur": {"related": "متعلقہ مصنوعات", "years": "سال کا تجربہ", "countries": "خدمات یافتہ ممالک", "factory": "م² فیکٹری رقبہ", "skus": "مصنوعات SKU", "email": "ای میل", "leading": "چین کا معروف واٹر فلٹر مینوفیکچرر | NSF اور ISO تصدیق شدہ فیکٹری"},
    "ms": {"related": "Produk berkaitan", "years": "Tahun pengalaman", "countries": "Negara dilayani", "factory": "m² kawasan kilang", "skus": "SKU produk", "email": "E-mel", "leading": "Pengeluar penapis air terkemuka China | Kilang diperakui NSF dan ISO"},
    "tl": {"related": "Kaugnay na produkto", "years": "Taon ng karanasan", "countries": "Mga bansang naserbisyuhan", "factory": "m² lawak ng pabrika", "skus": "SKU ng produkto", "email": "Email", "leading": "Nangungunang tagagawa ng water filter sa China | NSF at ISO certified na pabrika"},
    "he": {"related": "מוצרים קשורים", "years": "שנות ניסיון", "countries": "מדינות פעילות", "factory": "מ״ר שטח מפעל", "skus": "מק״טי מוצר", "email": "דוא״ל", "leading": "יצרן סיני מוביל של מסנני מים | מפעל מוסמך NSF ו-ISO"},
    "el": {"related": "Σχετικά προϊόντα", "years": "Χρόνια εμπειρίας", "countries": "Χώρες εξυπηρέτησης", "factory": "m² έκταση εργοστασίου", "skus": "Κωδικοί προϊόντων", "email": "Email", "leading": "Κορυφαίος Κινέζος κατασκευαστής φίλτρων νερού | Εργοστάσιο πιστοποιημένο NSF και ISO"},
    "cs": {"related": "Související produkty", "years": "Let zkušeností", "countries": "Obsluhované země", "factory": "m² plocha továrny", "skus": "Produktové SKU", "email": "E-mail", "leading": "Přední čínský výrobce vodních filtrů | Továrna certifikovaná NSF a ISO"},
    "hu": {"related": "Kapcsolódó termékek", "years": "Év tapasztalat", "countries": "Kiszolgált országok", "factory": "m² gyárterület", "skus": "Termék SKU-k", "email": "E-mail", "leading": "Vezető kínai vízszűrőgyártó | NSF és ISO tanúsított gyár"},
    "ro": {"related": "Produse conexe", "years": "Ani de experiență", "countries": "Țări deservite", "factory": "m² suprafață fabrică", "skus": "SKU-uri produse", "email": "E-mail", "leading": "Producător chinez lider de filtre de apă | Fabrică certificată NSF și ISO"},
    "sv": {"related": "Relaterade produkter", "years": "Års erfarenhet", "countries": "Betjänade länder", "factory": "m² fabriksyta", "skus": "Produkt-SKU:er", "email": "E-post", "leading": "Ledande kinesisk tillverkare av vattenfilter | NSF- och ISO-certifierad fabrik"},
    "da": {"related": "Relaterede produkter", "years": "Års erfaring", "countries": "Betjente lande", "factory": "m² fabriksareal", "skus": "Produkt-SKU'er", "email": "E-mail", "leading": "Førende kinesisk producent af vandfiltre | NSF- og ISO-certificeret fabrik"},
    "fi": {"related": "Aiheeseen liittyvät tuotteet", "years": "Vuoden kokemus", "countries": "Palvellut maat", "factory": "m² tehdasala", "skus": "Tuote-SKU:t", "email": "Sähköposti", "leading": "Johtava kiinalainen vedensuodatinvalmistaja | NSF- ja ISO-sertifioitu tehdas"},
    "no": {"related": "Relaterte produkter", "years": "Års erfaring", "countries": "Land betjent", "factory": "m² fabrikkområde", "skus": "Produkt-SKU-er", "email": "E-post", "leading": "Ledende kinesisk produsent av vannfiltre | NSF- og ISO-sertifisert fabrikk"},
    "uk": {"related": "Схожі товари", "years": "Років досвіду", "countries": "Країн постачання", "factory": "м² площа фабрики", "skus": "Артикулів продукції", "email": "Електронна пошта", "leading": "Провідний китайський виробник фільтрів для води | Фабрика з сертифікатами NSF та ISO"},
    "bg": {"related": "Свързани продукти", "years": "Години опит", "countries": "Обслужвани държави", "factory": "м² площ на фабриката", "skus": "Продуктови SKU", "email": "Имейл", "leading": "Водещ китайски производител на водни филтри | NSF и ISO сертифицирана фабрика"},
    "hr": {"related": "Povezani proizvodi", "years": "Godina iskustva", "countries": "Opslužene zemlje", "factory": "m² površina tvornice", "skus": "SKU proizvoda", "email": "E-pošta", "leading": "Vodeći kineski proizvođač filtera za vodu | Tvornica certificirana prema NSF i ISO"},
    "sr": {"related": "Повезани производи", "years": "Година искуства", "countries": "Земље испоруке", "factory": "м² површина фабрике", "skus": "SKU производа", "email": "Е-пошта", "leading": "Водећи кинески произвођач филтера за воду | Фабрика са NSF и ISO сертификатима"},
    "sk": {"related": "Súvisiace produkty", "years": "Rokov skúseností", "countries": "Obsluhované krajiny", "factory": "m² plocha továrne", "skus": "Produktové SKU", "email": "E-mail", "leading": "Popredný čínsky výrobca vodných filtrov | Továreň certifikovaná NSF a ISO"},
    "sl": {"related": "Sorodni izdelki", "years": "Let izkušenj", "countries": "Države dobave", "factory": "m² površina tovarne", "skus": "SKU izdelkov", "email": "E-pošta", "leading": "Vodilni kitajski proizvajalec vodnih filtrov | Tovarna s certifikatoma NSF in ISO"},
    "lt": {"related": "Susiję produktai", "years": "Metų patirtis", "countries": "Aptarnaujamos šalys", "factory": "m² gamyklos plotas", "skus": "Produktų SKU", "email": "El. paštas", "leading": "Pirmaujantis Kinijos vandens filtrų gamintojas | NSF ir ISO sertifikuota gamykla"},
    "et": {"related": "Seotud tooted", "years": "Aastat kogemust", "countries": "Teenindatud riigid", "factory": "m² tehase pindala", "skus": "Toote SKU-d", "email": "E-post", "leading": "Juhtiv Hiina veefiltrite tootja | NSF ja ISO sertifikaadiga tehas"},
    "lv": {"related": "Saistītie produkti", "years": "Gadu pieredze", "countries": "Apkalpotās valstis", "factory": "m² rūpnīcas platība", "skus": "Produktu SKU", "email": "E-pasts", "leading": "Vadošais Ķīnas ūdens filtru ražotājs | NSF un ISO sertificēta rūpnīca"},
    "sw": {"related": "Bidhaa zinazohusiana", "years": "Miaka ya uzoefu", "countries": "Nchi zinazohudumiwa", "factory": "m² eneo la kiwanda", "skus": "SKU za bidhaa", "email": "Barua pepe", "leading": "Mtengenezaji mkuu wa vichujio vya maji China | Kiwanda kilichoidhinishwa na NSF na ISO"},
    "ha": {"related": "Kayayyaki masu alaƙa", "years": "Shekarun gogewa", "countries": "Kasashen da ake hidima", "factory": "m² fadin masana'anta", "skus": "SKU na kaya", "email": "Imel", "leading": "Babban mai kera matatun ruwa a China | Masana'anta mai takardar NSF da ISO"},
    "zu": {"related": "Imikhiqizo ehlobene", "years": "Iminyaka yesipiliyoni", "countries": "Amazwe asetshenziwe", "factory": "m² indawo yefektri", "skus": "Ama-SKU omkhiqizo", "email": "I-imeyili", "leading": "Umkhiqizi ohamba phambili waseChina wezihlungi zamanzi | Ifektri eqinisekiswe i-NSF ne-ISO"},
    "ta": {"related": "தொடர்புடைய தயாரிப்புகள்", "years": "ஆண்டுகள் அனுபவம்", "countries": "சேவை நாடுகள்", "factory": "m² தொழிற்சாலை பரப்பு", "skus": "தயாரிப்பு SKU", "email": "மின்னஞ்சல்", "leading": "சீனாவின் முன்னணி நீர் வடிகட்டி உற்பத்தியாளர் | NSF மற்றும் ISO சான்றளிக்கப்பட்ட தொழிற்சாலை"},
    "kk": {"related": "Ұқсас өнімдер", "years": "Жыл тәжірибе", "countries": "Қызмет көрсетілген елдер", "factory": "м² зауыт аумағы", "skus": "Өнім SKU", "email": "Электрондық пошта", "leading": "Қытайдың жетекші су сүзгі өндірушісі | NSF және ISO сертификатталған зауыт"},
}

RUSSIAN_SLUG_TITLES = {
    "product-alkaline-purifier.html": "Щелочная система очистки воды",
    "product-antibacterial-mineralization.html": "Антибактериальный минерализующий фильтрующий картридж",
    "product-big-blue-3stage.html": "30-дюймовый трехступенчатый фильтр Big Blue",
    "product-carbon-block.html": "CTO-картридж из угольного блока кокосовой скорлупы",
    "product-carbon-block-2.html": "Прессованный активированный CTO угольный блок",
    "product-carbon-block-industrial.html": "Промышленный высокопоточный CTO угольный фильтр",
    "product-ceramic-filter.html": "Керамический фильтрующий картридж",
    "product-filter-combo.html": "Многоступенчатый комплект фильтрующих картриджей",
    "product-flat-cap-cto.html": "CTO угольный фильтр с плоской крышкой",
    "product-flat-cap-gac.html": "GAC фильтр с плоской крышкой",
    "product-flat-cap-pp.html": "PP melt-blown осадочный фильтр с плоской крышкой",
    "product-housing-filter.html": "Корпус фильтра Eco Express Water",
    "product-inline-cation-resin.html": "Линейный картридж с катионообменной смолой",
    "product-inline-pp.html": "Линейный PP-картридж",
    "product-inline-small-mol.html": "Антибактериальный минерализующий фильтр малой молекулы",
    "product-inline-t33-coconut.html": "Линейный T33 фильтр с кокосовым углем",
    "product-inline-t33-mineral.html": "Минерализующий линейный T33 фильтр для воды",
    "product-maifan-inline.html": "Линейный фильтр с камнем Майфан",
    "product-mid-filter.html": "Средний фильтр для воды с медным соединителем",
    "product-mineral-inline.html": "Линейный минерализующий фильтр",
    "product-mt-600dg.html": "Темно-зеленый диспенсер воды MT-600DG",
    "product-mt-900g.html": "Золотистый диспенсер воды MT-900G",
    "product-mt-b600.html": "Белый диспенсер воды MT-B600",
    "product-mt-dv-e600.html": "Вертикальный диспенсер воды 1000W MT-DV-E600",
    "product-mt-e600.html": "Настенный диспенсер воды MT-E600",
    "product-mt-s800.html": "Золотистый диспенсер воды MT-S800",
    "product-mt-v-e300a.html": "Вертикальный диспенсер воды MT-V-E300A",
    "product-post-t33.html": "Линейный угольный постфильтр T33",
    "product-pp-fin-cap.html": "PP melt-blown фильтр с ребристой торцевой крышкой",
    "product-pp-silicon-ring.html": "PP melt-blown фильтр с силиконовым кольцом",
    "product-pp-soe-doe.html": "Промышленный PP melt-blown осадочный фильтр (SOE/DOE)",
    "product-pp-spun.html": "PP melt-blown осадочный фильтрующий картридж",
    "product-ppf-cartridge.html": "PP melt-blown картридж из полипропиленового волокна",
    "product-pre-udf.html": "Предварительный UDF-картридж с активированным углем",
    "product-resin-filter.html": "Фильтр с ионообменной смолой",
    "product-ro-membrane.html": "Мембранный элемент обратного осмоса (RO)",
    "product-ro-membrane-400g.html": "Высокопоточная RO-мембрана 400GPD",
    "product-ro-undersink.html": "Подмоечный фильтр обратного осмоса",
    "product-ss-jumbo-housing.html": "Промышленный корпус Jumbo из нержавеющей стали 304/316L",
    "product-t33-post.html": "Постфильтрующий картридж T33",
    "product-udf-cartridge.html": "GAC/UDF картридж с гранулированным активированным углем",
    "product-uf-cartridge.html": "Ультрафильтрационный (UF) картридж",
    "product-uf-filter-2.html": "UF фильтр с полым волокном",
    "product-ultra-film.html": "Ультрафильтрационный пленочный картридж",
    "product-uv-purifier.html": "Трехступенчатый УФ-очиститель воды",
    "product-water-purifier-maifan.html": "Минерализующий очиститель с камнем Майфан",
}


def nav_label(text: str, href: str) -> str | None:
    match = re.search(
        rf'<a href="{re.escape(href)}" class="nav-link(?: active)?">([^<]+)</a>',
        text,
    )
    return html.unescape(match.group(1).strip()) if match else None


def dedupe_category_buttons(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        block = match.group(0)
        seen: set[str] = set()

        def keep(button: re.Match[str]) -> str:
            label = re.sub(r"<[^>]+>", "", button.group(0)).strip()
            if label in seen:
                return ""
            seen.add(label)
            return button.group(0)

        return re.sub(r'\s*<button class="cat-btn[^>]*>.*?</button>', keep, block, flags=re.S)

    return re.sub(r'<div class="cat-filter">.*?</div>', repl, text, flags=re.S)


def repair_russian_cards(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        prefix, href = match.group(1), match.group(2)
        title = RUSSIAN_SLUG_TITLES.get(href)
        if not title:
            return match.group(0)
        return f"{prefix}<h3>{html.escape(title)}</h3>"

    return re.sub(
        r'(<article class="product-card"[\s\S]*?<a href="(product-[^"]+\.html)"[\s\S]*?<div class="product-body">\s*)(?:<h3>[\s\S]*?</h3>|[^<]{1,180}</h3>)',
        repl,
        text,
    )


def repair_file(path: Path, lang: str) -> bool:
    old = path.read_text(encoding="utf-8", errors="ignore")
    text = old
    common = COMMON.get(lang, {})

    products_label = nav_label(text, "products.html") or common.get("skus") or "Products"
    contact_label = nav_label(text, "contact.html") or "Contact"

    if lang != "en":
        replacements = {
            ">Products<": f">{products_label}<",
            ">Contact<": f">{contact_label}<",
            ">Related Products<": f">{common.get('related', products_label)}<",
            "<!-- Related Products -->": f"<!-- {common.get('related', products_label)} -->",
            ">Years Experience<": f">{common.get('years', 'Years')}<",
            ">Countries Served<": f">{common.get('countries', 'Countries')}<",
            ">m² Factory Area<": f">{common.get('factory', 'm²')}<",
            ">Product SKUs<": f">{common.get('skus', products_label)}<",
            "✦ Leading China Water Filter Manufacturer | NSF &amp; ISO Certified Factory": f"✦ {common.get('leading', 'OEM/ODM · NSF · ISO')}",
            ">Email<": f">{common.get('email', 'Email')}<",
            'alt="Express Water Factory"': f'alt="Express Water"',
        }
        for src, dst in replacements.items():
            text = text.replace(src, dst)

        # Localize simple contact meta copy that appears in many non-English heads.
        text = text.replace(
            "Contact Express Water for bulk OEM water filter quotes. WhatsApp +86-19908311885 · expresswater025@gmail.com · Factory: Haining, Zhejiang, China.",
            f"{contact_label} Express Water · OEM/ODM · WhatsApp +86-19908311885 · expresswater025@gmail.com · Haining, Zhejiang, China.",
        )

    text = dedupe_category_buttons(text)
    if lang == "ru":
        text = text.replace("X-дюймовый", "30-дюймовый")
        text = repair_russian_cards(text)

    if text != old:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for lang in LANGS:
        folder = ROOT / lang
        if not folder.exists():
            continue
        for path in folder.glob("*.html"):
            if repair_file(path, lang):
                changed += 1
    print(f"Final quality repair changed {changed} files.")


if __name__ == "__main__":
    main()
