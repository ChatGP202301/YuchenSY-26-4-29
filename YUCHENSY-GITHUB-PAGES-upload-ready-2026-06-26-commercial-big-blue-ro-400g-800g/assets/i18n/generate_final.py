
import json
import os

base_path = "/Users/jet/.accio/accounts/1661502182/agents/DID-F456DA-2B0D4C/project/assets/i18n/"
with open(os.path.join(base_path, "en.json"), 'r', encoding='utf-8') as f:
    en_data = json.load(f)

# Master translation dictionary
trans_map = {
    "vi": {
        "ui": {"nav_home": "Trang chủ", "nav_products": "Sản phẩm", "nav_about": "Về chúng tôi", "nav_workshop": "Nhà xưởng", "nav_exhibition": "Triển lãm", "nav_contact": "Liên hệ", "cta_whatsapp": "WhatsApp", "topbar_tag": "Bán buôn Toàn cầu · Chuyên gia OEM/ODM · Từ năm 1998", "hero_title": "Giải pháp Lọc nước Công nghiệp & OEM", "hero_desc": "Nhà cung cấp bán buôn toàn cầu các loại lõi lọc PP, CTO, GAC và màng RO. Từ năm 1998, cung cấp dịch vụ OEM/ODM đạt chuẩn NSF/ISO.", "about_title": "Hơn 20 năm xuất sắc trong ngành Lọc nước", "footer_rights": "Bản quyền đã được bảo lưu.", "product_view_details": "Xem chi tiết", "form_btn": "Gửi yêu cầu", "modal_specs_title": "Thông số kỹ thuật"},
        "cats": {"Filter Cartridge": "Lõi lọc", "Filter Housing": "Vỏ lọc", "Flat Cap Filter": "Lõi lọc nắp phẳng", "Industrial Filter": "Lõi lọc công nghiệp", "Inline Filter": "Lõi lọc Inline", "RO System": "Hệ thống RO", "Water Dispenser": "Máy cấp nước", "Water Purifier": "Máy lọc nước"},
        "specs": {"Filtration Stages": "Giai đoạn lọc", "Daily Output": "Công suất ngày", "Material": "Vật liệu", "Working Pressure": "Áp suất làm việc", "Certifications": "Chứng nhận", "Warranty": "Bảo hành", "Application": "Ứng dụng"}
    },
    "th": {
        "ui": {"nav_home": "หน้าแรก", "nav_products": "ผลิตภัณฑ์", "nav_about": "เกี่ยวกับเรา", "nav_workshop": "โรงงาน", "nav_exhibition": "นิทรรศการ", "nav_contact": "ติดต่อ", "cta_whatsapp": "WhatsApp", "topbar_tag": "ขายส่งทั่วโลก · ผู้เชี่ยวชาญ OEM/ODM · ตั้งแต่ปี 1998", "hero_title": "โซลูชันการกรองน้ำระดับอุตสาหกรรมและ OEM", "hero_desc": "ซัพพลายเออร์ขายส่งไส้กรอง PP, CTO, GAC และเมมเบรน RO คุณภาพสูงทั่วโลก ให้บริการ OEM/ODM ตั้งแต่ปี 1998", "about_title": "กว่า 20 ปีแห่งความเป็นเลิศด้านการกรองน้ำ", "footer_rights": "สงวนลิขสิทธิ์", "product_view_details": "ดูรายละเอียด", "form_btn": "ส่งคำขอ", "modal_specs_title": "ข้อมูลทางเทคนิค"},
        "cats": {"Filter Cartridge": "ไส้กรอง", "Filter Housing": "กระบอกกรอง", "Flat Cap Filter": "ไส้กรองฝาเรียบ", "Industrial Filter": "ไส้กรองอุตสาหกรรม", "Inline Filter": "ไส้กรองอินไลน์", "RO System": "ระบบ RO", "Water Dispenser": "ตู้กดน้ำ", "Water Purifier": "เครื่องกรองน้ำ"},
        "specs": {"Filtration Stages": "ขั้นตอนการกรอง", "Daily Output": "กำลังการผลิต", "Material": "วัสดุ", "Working Pressure": "แรงดันใช้งาน", "Certifications": "การรับรอง", "Warranty": "การรับประกัน", "Application": "การใช้งาน"}
    },
    "id": {
        "ui": {"nav_home": "Beranda", "nav_products": "Produk", "nav_about": "Tentang Kami", "nav_workshop": "Bengkel", "nav_exhibition": "Pameran", "nav_contact": "Kontak", "cta_whatsapp": "WhatsApp", "topbar_tag": "Grosir Global · Spesialis OEM/ODM · Sejak 1998", "hero_title": "Solusi Pemurnian Air Industri & OEM", "hero_desc": "Pemasok grosir global untuk filter PP, CTO, GAC, dan membran RO. Sejak 1998, menyediakan layanan OEM/ODM standar NSF/ISO.", "about_title": "20+ Tahun Keunggulan Filtrasi Air", "footer_rights": "Seluruh hak cipta dilindungi.", "product_view_details": "Lihat Detail", "form_btn": "Kirim Pertanyaan", "modal_specs_title": "Spesifikasi Teknis"},
        "cats": {"Filter Cartridge": "Kartrid Filter", "Filter Housing": "Rumah Filter", "Flat Cap Filter": "Filter Tutup Rata", "Industrial Filter": "Filter Industri", "Inline Filter": "Filter Inline", "RO System": "Sistem RO", "Water Dispenser": "Dispenser Air", "Water Purifier": "Pemurni Air"},
        "specs": {"Filtration Stages": "Tahap Filtrasi", "Daily Output": "Output Harian", "Material": "Bahan", "Working Pressure": "Tekanan Kerja", "Certifications": "Sertifikasi", "Warranty": "Garansi", "Application": "Aplikasi"}
    },
    "bn": {
        "ui": {"nav_home": "হোম", "nav_products": "পণ্য", "nav_about": "আমাদের সম্পর্কে", "nav_workshop": "ওয়ার্কশপ", "nav_exhibition": "প্রদর্শনী", "nav_contact": "যোগাযোগ", "cta_whatsapp": "WhatsApp", "topbar_tag": "গ্লোবাল হোলসেল · OEM/ODM বিশেষজ্ঞ · ১৯৯৮ থেকে", "hero_title": "শিল্প জল বিশুদ্ধকরণ সমাধান", "hero_desc": "উচ্চ মানের PP, CTO, GAC এবং RO মেমব্রেনের পাইকারি সরবরাহকারী। ১৯৯৮ থেকে OEM/ODM পরিষেবা।", "about_title": "জল পরিস্রাবণে ২০+ বছরের শ্রেষ্ঠত্ব", "footer_rights": "সর্বস্বত্ব সংরক্ষিত।", "product_view_details": "বিস্তারিত", "form_btn": "পাঠান", "modal_specs_title": "প্রযুক্তিগত বৈশিষ্ট্য"},
        "cats": {"Filter Cartridge": "ফিল্টার কার্টিজ", "Filter Housing": "হাউজিং", "Flat Cap Filter": "ফ্ল্যাট ক্যাপ", "Industrial Filter": "শিল্প ফিল্টার", "Inline Filter": "ইনলাইন", "RO System": "আরও সিস্টেম", "Water Dispenser": "ডিস্পেনসার", "Water Purifier": "পিউরিফায়ার"},
        "specs": {"Filtration Stages": "ফিল্ট্রেশন পর্যায়", "Daily Output": "দৈনিক আউটপুট", "Material": "উপাদান", "Working Pressure": "কাজের চাপ", "Certifications": "সার্টিফিকেশন", "Warranty": "ওয়ারেন্টি", "Application": "প্রয়োগ"}
    },
    "ms": {
        "ui": {"nav_home": "Laman Utama", "nav_products": "Produk", "nav_about": "Tentang Kami", "nav_workshop": "Bengkel", "nav_exhibition": "Pameran", "nav_contact": "Hubungi", "cta_whatsapp": "WhatsApp", "topbar_tag": "Borong Global · Pakar OEM/ODM · Sejak 1998", "hero_title": "Penyelesaian Penulenan Air Industri", "hero_desc": "Pembekal borong global untuk penapis PP, CTO, GAC dan membran RO. Sejak 1998, menyediakan perkhidmatan OEM/ODM.", "about_title": "20+ Tahun Kecemerlangan Penapisan Air", "footer_rights": "Hak cipta terpelihara.", "product_view_details": "Lihat Butiran", "form_btn": "Hantar", "modal_specs_title": "Spesifikasi Teknikal"},
        "cats": {"Filter Cartridge": "Katrij Penapis", "Filter Housing": "Perumahan", "Flat Cap Filter": "Tudung Rata", "Industrial Filter": "Penapis Industri", "Inline Filter": "Penapis Segaris", "RO System": "Sistem RO", "Water Dispenser": "Dispenser", "Water Purifier": "Penulen"},
        "specs": {"Filtration Stages": "Tahap Penapisan", "Daily Output": "Output Harian", "Material": "Bahan", "Working Pressure": "Tekanan Kerja", "Certifications": "Pensijilan", "Warranty": "Waranti", "Application": "Aplikasi"}
    },
    "tl": {
        "ui": {"nav_home": "Home", "nav_products": "Mga Produkto", "nav_about": "Tungkol sa Amin", "nav_workshop": "Workshop", "nav_exhibition": "Eksibisyon", "nav_contact": "Kontak", "cta_whatsapp": "WhatsApp", "topbar_tag": "Global Wholesale · Eksperto sa OEM/ODM · Simula 1998", "hero_title": "Industrial Water Purification Solutions", "hero_desc": "Supplier ng PP, CTO, GAC filters at RO membranes. Simula 1998, nagbibigay ng OEM/ODM services.", "about_title": "20+ Taon ng Kahusayan sa Pag-filter", "footer_rights": "Reserbado ang lahat de karapatan.", "product_view_details": "Tingnan", "form_btn": "Ipadala", "modal_specs_title": "Teknikal na Spesifikasyon"},
        "cats": {"Filter Cartridge": "Filter Cartridge", "Filter Housing": "Housing", "Flat Cap Filter": "Flat Cap", "Industrial Filter": "Industrial", "Inline Filter": "Inline", "RO System": "RO System", "Water Dispenser": "Dispenser", "Water Purifier": "Purifier"},
        "specs": {"Filtration Stages": "Filtration Stages", "Daily Output": "Daily Output", "Material": "Material", "Working Pressure": "Working Pressure", "Certifications": "Certifications", "Warranty": "Warranty", "Application": "Application"}
    },
    "he": {
        "ui": {"nav_home": "בית", "nav_products": "מוצרים", "nav_about": "אודות", "nav_workshop": "סדנא", "nav_exhibition": "תערוכות", "nav_contact": "קשר", "cta_whatsapp": "וואטסאפ", "topbar_tag": "סיטונאות גלובלית · מומחי OEM/ODM · מאז 1998", "hero_title": "פתרונות טיהור מים תעשייתיים", "hero_desc": "ספק סיטונאי למסנני PP, CTO, GAC וממברנות RO. שירותי OEM/ODM מאז 1998.", "about_title": "20+ שנות מצוינות בסינון מים", "footer_rights": "כל הזכויות שמורות.", "product_view_details": "פרטים", "form_btn": "שלח", "modal_specs_title": "מפרט טכני"},
        "cats": {"Filter Cartridge": "מחסנית", "Filter Housing": "בית מסנן", "Flat Cap Filter": "קצה שטוח", "Industrial Filter": "תעשייתי", "Inline Filter": "אינליין", "RO System": "מערכת RO", "Water Dispenser": "דיספנסר", "Water Purifier": "מטהר"},
        "specs": {"Filtration Stages": "שלבי סינון", "Daily Output": "תפוקה", "Material": "חומר", "Working Pressure": "לחץ", "Certifications": "אישורים", "Warranty": "אחריות", "Application": "יישום"}
    },
    "ur": {
        "ui": {"nav_home": "ہوم", "nav_products": "مصنوعات", "nav_about": "ہمارے بارے میں", "nav_workshop": "ورکشاپ", "nav_exhibition": "نمائشیں", "nav_contact": "رابطہ", "cta_whatsapp": "واٹس ایپ", "topbar_tag": "عالمی ہول سیل · 1998 سے", "hero_title": "صنعتی واٹر پیوریفیکیشن", "hero_desc": "PP، CTO، GAC اور RO میمبرین کے سپلائر۔ 1998 سے خدمات۔", "about_title": "فلٹریشن میں 20+ سال کا تجربہ", "footer_rights": "جملہ حقوق محفوظ۔", "product_view_details": "تفصیل", "form_btn": "بھیجیں", "modal_specs_title": "تکنیکی وضاحتیں"},
        "cats": {"Filter Cartridge": "কার্টরিজ", "Filter Housing": "ہاؤسنگ", "Flat Cap Filter": "فلیٹ کیپ", "Industrial Filter": "صنعتی", "Inline Filter": "ان لائن", "RO System": "آر او سسٹم", "Water Dispenser": "ڈسپنسر", "Water Purifier": "پیوریفائر"},
        "specs": {"Filtration Stages": "مراحل", "Daily Output": "پیداوار", "Material": "مواد", "Working Pressure": "دباؤ", "Certifications": "تصدیق", "Warranty": "وارنٹی", "Application": "درخواست"}
    },
    "fa": {
        "ui": {"nav_home": "خانه", "nav_products": "محصولات", "nav_about": "درباره ما", "nav_workshop": "کارگاه", "nav_exhibition": "نمایشگاه", "nav_contact": "تماس", "cta_whatsapp": "واتس‌اپ", "topbar_tag": "عمده فروشی جهانی · از 1998", "hero_title": "تصفیه آب صنعتی", "hero_desc": "تامین‌کننده فیلترهای PP, CTO, GAC. خدمات از 1998.", "about_title": "20 سال تجربه فیلتراسیon", "footer_rights": "حقوق محفوظ است.", "product_view_details": "جزئیات", "form_btn": "ارسال", "modal_specs_title": "مشخصات فنی"},
        "cats": {"Filter Cartridge": "کارتریج", "Filter Housing": "هوزینگ", "Flat Cap Filter": "تخت", "Industrial Filter": "صنعتی", "Inline Filter": "اینلاین", "RO System": "سیستم RO", "Water Dispenser": "دیسپنسر", "Water Purifier": "تصفیه"},
        "specs": {"Filtration Stages": "مراحل", "Daily Output": "خروجی", "Material": "جنس", "Working Pressure": "فشار", "Certifications": "گواهی", "Warranty": "گارانتی", "Application": "کاربرد"}
    },
    "ha": {
        "ui": {"nav_home": "Gida", "nav_products": "Kayayyaki", "nav_about": "Game da mu", "nav_workshop": "Ma'aikata", "nav_exhibition": "Nune-nune", "nav_contact": "Tuntuɓa", "cta_whatsapp": "WhatsApp", "topbar_tag": "Jumla ta Duniya · Tun 1998", "hero_title": "Tace Ruwa", "hero_desc": "Dillalin matatun ruwa. Tun 1998.", "about_title": "Shekaru 20+ na Kwarewa", "footer_rights": "An kiyaye haƙƙoƙi.", "product_view_details": "Bayani", "form_btn": "Aika", "modal_specs_title": "Bayanan Fasaha"},
        "cats": {"Filter Cartridge": "Kwashin Tace", "Filter Housing": "Gidan Tace", "Flat Cap Filter": "Tace mai Murfi", "Industrial Filter": "Masana'antu", "Inline Filter": "Inline", "RO System": "RO", "Water Dispenser": "Injin Ruwa", "Water Purifier": "Injin Tace"},
        "specs": {"Filtration Stages": "Matakai", "Daily Output": "Samfura", "Material": "Kayan aiki", "Working Pressure": "Karfi", "Certifications": "Shaida", "Warranty": "Garanti", "Application": "Amfani"}
    },
    "zu": {
        "ui": {"nav_home": "Ikhaya", "nav_products": "Imikhiqizo", "nav_about": "Mayelana nathi", "nav_workshop": "Indawo yokusebenzela", "nav_exhibition": "Imibukiso", "nav_contact": "Oxhumana nabo", "cta_whatsapp": "WhatsApp", "topbar_tag": "Ukuthengisa ngenqwaba · Kusukela ngo-1998", "hero_title": "Ukuhlanzwa kwamanzi", "hero_desc": "Umhlinzeki wezithengiso ze-PP, CTO. Kusukela ngo-1998.", "about_title": "Iminyaka engu-20+ yobungcweti", "footer_rights": "Amalungelo agodliwe.", "product_view_details": "Imininingwane", "form_btn": "Thumela", "modal_specs_title": "Imininingwane yezobuchwepheshe"},
        "cats": {"Filter Cartridge": "Cartridge", "Filter Housing": "Housing", "Flat Cap Filter": "Flat Cap", "Industrial Filter": "Industrial", "Inline Filter": "Inline", "RO System": "RO", "Water Dispenser": "Dispenser", "Water Purifier": "Purifier"},
        "specs": {"Filtration Stages": "Izitezi", "Daily Output": "Okukhishwayo", "Material": "Izinto", "Working Pressure": "Ingcindezi", "Certifications": "Izitifiketi", "Warranty": "Iwaranti", "Application": "Ukusetshenziswa"}
    },
    "sw": {
        "ui": {"nav_home": "Nyumbani", "nav_products": "Bidhaa", "nav_about": "Kuhusu Sisi", "nav_workshop": "Kiwanda", "nav_exhibition": "Maonyesho", "nav_contact": "Wasiliana", "cta_whatsapp": "WhatsApp", "topbar_tag": "Uuzaji wa Jumla · Tangu 1998", "hero_title": "Usafishaji wa Maji", "hero_desc": "Msambazaji wa vichujio. Tangu 1998.", "about_title": "Zaidi ya Miaka 20 ya Ubora", "footer_rights": "Haki zimehifadhiwa.", "product_view_details": "Maelezo", "form_btn": "Tuma", "modal_specs_title": "Maelezo ya Kiufundi"},
        "cats": {"Filter Cartridge": "Katridi", "Filter Housing": "Nyumba", "Flat Cap Filter": "Kifuniko Bapa", "Industrial Filter": "Viwandani", "Inline Filter": "Laini", "RO System": "RO", "Water Dispenser": "Kitawanya", "Water Purifier": "Kusafisha"},
        "specs": {"Filtration Stages": "Hatua", "Daily Output": "Uzalishaji", "Material": "Nyenzo", "Working Pressure": "Shinikizo", "Certifications": "Vyeti", "Warranty": "Udhamini", "Application": "Matumizi"}
    },
    "ta": {
        "ui": {"nav_home": "முகப்பு", "nav_products": "தயாரிப்புகள்", "nav_about": "எங்களைப் பற்றி", "nav_workshop": "பணிமனை", "nav_exhibition": "கண்காட்சிகள்", "nav_contact": "தொடர்பு", "cta_whatsapp": "வாட்ஸ்அப்", "topbar_tag": "மொத்த விற்பனை · 1998 முதல்", "hero_title": "நீர் சுத்திகரிப்பு", "hero_desc": "வடிகட்டி சப்ளையர். 1998 முதல்.", "about_title": "20+ வருட அனுபவம்", "footer_rights": "உரிமைகள் பாதுகாக்கப்பட்டவை.", "product_view_details": "விவரங்கள்", "form_btn": "அனுப்பு", "modal_specs_title": "தொழில்நுட்ப விவரங்கள்"},
        "cats": {"Filter Cartridge": "கார்ட்ரிட்ஜ்", "Filter Housing": "வீடுகள்", "Flat Cap Filter": "பிளாட் கேப்", "Industrial Filter": "தொழில்துறை", "Inline Filter": "இன்லைன்", "RO System": "RO", "Water Dispenser": "டிஸ்பென்சர்", "Water Purifier": "சுத்திகரிப்பு"},
        "specs": {"Filtration Stages": "நிலைகள்", "Daily Output": "வெளியீடு", "Material": "பொருள்", "Working Pressure": "அழுத்தம்", "Certifications": "சான்றிதழ்கள்", "Warranty": "உத்தரவாதம்", "Application": "பயன்பாடு"}
    },
    "kk": {
        "ui": {"nav_home": "Басты бет", "nav_products": "Өнімдер", "nav_about": "Біз туралы", "nav_workshop": "Шеберхана", "nav_exhibition": "Көрмелер", "nav_contact": "Байланыс", "cta_whatsapp": "WhatsApp", "topbar_tag": "Көтерме сауда · 1998 жылдан", "hero_title": "Суды тазарту", "hero_desc": "Сүзгі жеткізушісі. 1998 жылдан.", "about_title": "20+ жылдық тәжірибе", "footer_rights": "Құқықтар қорғалған.", "product_view_details": "Мәлімет", "form_btn": "Жіберу", "modal_specs_title": "Техникалық сипаттар"},
        "cats": {"Filter Cartridge": "Картридж", "Filter Housing": "Корпус", "Flat Cap Filter": "Қақпақ", "Industrial Filter": "Өнеркәсіптік", "Inline Filter": "Инлайн", "RO System": "RO", "Water Dispenser": "Диспенсер", "Water Purifier": "Тазартқыш"},
        "specs": {"Filtration Stages": "Кезеңдер", "Daily Output": "Өнім", "Material": "Материал", "Working Pressure": "Қысым", "Certifications": "Сертификаттар", "Warranty": "Кепілдік", "Application": "Қолдану"}
    }
}

def apply_trans(node, t_map):
    if isinstance(node, dict):
        res = {}
        for k, v in node.items():
            if k in t_map.get("ui", {}):
                res[k] = t_map["ui"][k]
            elif k in t_map.get("specs", {}):
                res[k] = t_map["specs"][k]
            else:
                res[k] = apply_trans(v, t_map)
        return res
    elif isinstance(node, list):
        return [apply_trans(i, t_map) for i in node]
    elif isinstance(node, str):
        # Specific handling for categories and names if needed
        return node
    return node

for lang, t_map in trans_map.items():
    translated = apply_trans(en_data, t_map)
    # Patch categories specifically
    for cat_en, cat_tr in t_map.get("cats", {}).items():
        if cat_en in translated["categories"]:
            translated["categories"][cat_en] = cat_tr
    
    with open(os.path.join(base_path, f"{lang}.json"), 'w', encoding='utf-8') as f:
        json.dump(translated, f, ensure_ascii=False, indent=2)
print("Finished.")
