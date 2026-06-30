
import json
import os

languages = ["vi", "th", "id", "bn", "ms", "tl", "he", "ur", "fa", "ha", "zu", "ta", "kk", "sw"]
base_dir = "/Users/jet/.accio/accounts/1661502182/agents/DID-F456DA-2B0D4C/project/assets/i18n/"

with open(os.path.join(base_dir, "en.json"), "r", encoding="utf-8") as f:
    en_data = json.load(f)

# Common translations for UI and Categories
trans = {
    "vi": {
        "ui": {
            "nav_home": "Trang chủ", "nav_products": "Sản phẩm", "nav_about": "Về chúng tôi", "nav_workshop": "Nhà xưởng", "nav_exhibition": "Triển lãm", "nav_contact": "Liên hệ", "cta_whatsapp": "WhatsApp cho chúng tôi",
            "topbar_tag": "Bán buôn số lượng lớn toàn cầu · Chuyên gia OEM/ODM · Từ năm 1998",
            "hero_title": "Giải pháp lọc nước cấp công nghiệp & OEM",
            "hero_desc": "Nhà cung cấp bán buôn toàn cầu cho các loại lõi lọc PP, CTO, GAC và màng RO. Từ năm 1998, cung cấp dịch vụ OEM/ODM đạt chuẩn NSF/ISO.",
            "about_title": "Hơn 20 năm xuất sắc trong ngành lọc nước",
            "about_desc": "Eco Express Water là doanh nghiệp bảo vệ môi trường công nghệ cao chuyên về vật liệu và thiết bị lọc nước. Thành lập năm 1998 tại Hải Ninh, Chiết Giang.",
            "footer_brand_desc": "Nhà sản xuất giải pháp lọc nước hàng đầu Trung Quốc từ năm 1998.",
            "footer_rights": "Mọi quyền được bảo lưu.",
            "product_view_details": "Xem chi tiết",
            "form_btn": "Gửi yêu cầu"
        },
        "categories": {
            "Filter Cartridge": "Lõi lọc", "Filter Housing": "Vỏ lọc", "Flat Cap Filter": "Lõi lọc nắp phẳng", "Industrial Filter": "Lõi lọc công nghiệp", "Inline Filter": "Lõi lọc Inline", "RO System": "Hệ thống RO", "Water Dispenser": "Máy cấp nước", "Water Purifier": "Máy lọc nước"
        }
    },
    "th": {
        "ui": {
            "nav_home": "หน้าแรก", "nav_products": "ผลิตภัณฑ์", "nav_about": "เกี่ยวกับเรา", "nav_workshop": "โรงงาน", "nav_exhibition": "นิทรรศการ", "nav_contact": "ติดต่อ", "cta_whatsapp": "WhatsApp หาเรา",
            "topbar_tag": "ขายส่งจำนวนมากทั่วโลก · ผู้เชี่ยวชาญ OEM/ODM · ตั้งแต่ปี 1998",
            "hero_title": "โซลูชันการกรองน้ำระดับอุตสาหกรรมและ OEM",
            "hero_desc": "ซัพพลายเออร์ขายส่งไส้กรอง PP, CTO, GAC และเมมเบรน RO คุณภาพสูงทั่วโลก ให้บริการ OEM/ODM ตั้งแต่ปี 1998",
            "about_title": "กว่า 20 ปีแห่งความเป็นเลิศด้านการกรองน้ำ",
            "about_desc": "Eco Express Water เป็นองค์กรเทคโนโลยีขั้นสูงที่เชี่ยวชาญด้านวัสดุกรองและอุปกรณ์กรองน้ำ ก่อตั้งขึ้นในปี 1998 ในเมืองไห่หนิง มณฑลเจ้อเจียง",
            "footer_brand_desc": "ผู้ผลิตโซลูชันการกรองน้ำชั้นนำของจีนตั้งแต่ปี 1998",
            "footer_rights": "สงวนลิขสิทธิ์",
            "product_view_details": "ดูรายละเอียด",
            "form_btn": "ส่งคำขอ"
        },
        "categories": {
            "Filter Cartridge": "ไส้กรอง", "Filter Housing": "กระบอกกรอง", "Flat Cap Filter": "ไส้กรองฝาเรียบ", "Industrial Filter": "ไส้กรองอุตสาหกรรม", "Inline Filter": "ไส้กรองอินไลน์", "RO System": "ระบบ RO", "Water Dispenser": "ตู้กดน้ำ", "Water Purifier": "เครื่องกรองน้ำ"
        }
    },
    "id": {
        "ui": {
            "nav_home": "Beranda", "nav_products": "Produk", "nav_about": "Tentang Kami", "nav_workshop": "Bengkel", "nav_exhibition": "Pameran", "nav_contact": "Kontak", "cta_whatsapp": "WhatsApp Kami",
            "topbar_tag": "Grosir Massal Global · Spesialis OEM/ODM · Sejak 1998",
            "hero_title": "Solusi Pemurnian Air Kelas Industri & OEM",
            "hero_desc": "Pemasok grosir global untuk filter PP, CTO, GAC, dan membran RO. Sejak 1998, menyediakan layanan OEM/ODM standar NSF/ISO.",
            "about_title": "20+ Tahun Keunggulan dalam Filtrasi Air",
            "about_desc": "Eco Express Water adalah perusahaan teknologi tinggi perlindungan lingkungan yang berfokus pada bahan dan peralatan filter air. Didirikan tahun 1998 di Haining, Zhejiang.",
            "footer_brand_desc": "Produsen solusi filtrasi air terkemuka di Cina sejak 1998.",
            "footer_rights": "Seluruh hak cipta dilindungi.",
            "product_view_details": "Lihat Detail",
            "form_btn": "Kirim Pertanyaan"
        },
        "categories": {
            "Filter Cartridge": "Kartrid Filter", "Filter Housing": "Rumah Filter", "Flat Cap Filter": "Filter Tutup Rata", "Industrial Filter": "Filter Industri", "Inline Filter": "Filter Inline", "RO System": "Sistem RO", "Water Dispenser": "Dispenser Air", "Water Purifier": "Pemurni Air"
        }
    },
    "bn": {
        "ui": {
            "nav_home": "হোম", "nav_products": "পণ্য", "nav_about": "আমাদের সম্পর্কে", "nav_workshop": "ওয়ার্কশপ", "nav_exhibition": "প্রদর্শনী", "nav_contact": "যোগাযোগ", "cta_whatsapp": "আমাদের হোয়াটসঅ্যাপ করুন",
            "topbar_tag": "গ্লোবাল বাল্ক হোলসেল · OEM/ODM বিশেষজ্ঞ · ১৯৯৮ সাল থেকে",
            "hero_title": "শিল্প-মানের জল বিশুদ্ধকরণ এবং OEM সমাধান",
            "hero_desc": "উচ্চ-মানের PP, CTO, GAC ফিল্টার এবং RO মেমব্রেনের বিশ্বব্যাপী পাইকারি সরবরাহকারী। ১৯৯৮ থেকে NSF/ISO মানের OEM/ODM পরিষেবা প্রদান করছি।",
            "about_title": "জল পরিস্রাবণে ২০ বছরেরও বেশি শ্রেষ্ঠত্ব",
            "about_desc": "Eco Express Water হলো জল বিশুদ্ধকরণ সামগ্রী এবং যন্ত্রপাতির বিশেষজ্ঞ একটি উচ্চ-প্রযুক্তি প্রতিষ্ঠান। ১৯৯৮ সালে চীনের ঝেজিয়াংয়ের হাইনিংয়ে প্রতিষ্ঠিত।",
            "footer_brand_desc": "১৯৯৮ সাল থেকে চীনের শীর্ষস্থানীয় জল পরিস্রাবণ সমাধান প্রস্তুতকারক।",
            "footer_rights": "সর্বস্বত্ব সংরক্ষিত।",
            "product_view_details": "বিস্তারিত দেখুন",
            "form_btn": "তদন্ত পাঠান"
        },
        "categories": {
            "Filter Cartridge": "ফিল্টার কার্টিজ", "Filter Housing": "ফিল্টার হাউজিং", "Flat Cap Filter": "ফ্ল্যাট ক্যাপ ফিল্টার", "Industrial Filter": "শিল্প ফিল্টার", "Inline Filter": "ইনলাইন ফিল্টার", "RO System": "আরও সিস্টেম", "Water Dispenser": "ওয়াটার ডিস্পেনসার", "Water Purifier": "ওয়াটার পিউরিফায়ার"
        }
    },
    "ms": {
        "ui": {
            "nav_home": "Laman Utama", "nav_products": "Produk", "nav_about": "Tentang Kami", "nav_workshop": "Bengkel", "nav_exhibition": "Pameran", "nav_contact": "Hubungi", "cta_whatsapp": "WhatsApp Kami",
            "topbar_tag": "Borong Pukal Global · Pakar OEM/ODM · Sejak 1998",
            "hero_title": "Penyelesaian Penulenan Air Gred Industri & OEM",
            "hero_desc": "Pembekal borong global untuk penapis PP, CTO, GAC dan membran RO. Sejak 1998, menyediakan perkhidmatan OEM/ODM standard NSF/ISO.",
            "about_title": "Lebih 20 Tahun Kecemerlangan Penapisan Air",
            "about_desc": "Eco Express Water ialah syarikat teknologi tinggi perlindungan alam sekitar yang menumpukan pada bahan dan peralatan penapis air. Ditubuhkan pada tahun 1998 di Haining, Zhejiang.",
            "footer_brand_desc": "Pengeluar penyelesaian penapisan air terkemuka di China sejak 1998.",
            "footer_rights": "Hak cipta terpelihara.",
            "product_view_details": "Lihat Butiran",
            "form_btn": "Hantar Pertanyaan"
        },
        "categories": {
            "Filter Cartridge": "Katrij Penapis", "Filter Housing": "Perumahan Penapis", "Flat Cap Filter": "Penapis Tudung Rata", "Industrial Filter": "Penapis Industri", "Inline Filter": "Penapis Segaris", "RO System": "Sistem RO", "Water Dispenser": "Dispenser Air", "Water Purifier": "Penulen Air"
        }
    },
    "tl": {
        "ui": {
            "nav_home": "Home", "nav_products": "Mga Produkto", "nav_about": "Tungkol sa Amin", "nav_workshop": "Workshop", "nav_exhibition": "Eksibisyon", "nav_contact": "Kontak", "cta_whatsapp": "WhatsApp sa Amin",
            "topbar_tag": "Global Bulk Wholesale · Eksperto sa OEM/ODM · Mula noong 1998",
            "hero_title": "Industrial-Grade na Paglilinis ng Tubig at mga Solusyong OEM",
            "hero_desc": "Global wholesale supplier para sa PP, CTO, GAC filters at RO membranes. Mula noong 1998, nagbibigay ng NSF/ISO standard na serbisyong OEM/ODM.",
            "about_title": "20+ Taon ng Kahusayan sa Pag-filter ng Tubig",
            "about_desc": "Ang Eco Express Water ay isang high-tech na kumpanya sa proteksyon ng kapaligiran na nakatuon sa mga materyales at kagamitan sa pagsasala ng tubig. Itinatag noong 1998 sa Haining, Zhejiang.",
            "footer_brand_desc": "Nangungunang manufacturer ng water filtration solution sa China mula noong 1998.",
            "footer_rights": "Lahat ng karapatan ay nakareserba.",
            "product_view_details": "Tingnan ang Detalye",
            "form_btn": "Ipadala ang Inquiry"
        },
        "categories": {
            "Filter Cartridge": "Filter Cartridge", "Filter Housing": "Filter Housing", "Flat Cap Filter": "Flat Cap Filter", "Industrial Filter": "Pang-industriyang Filter", "Inline Filter": "Inline Filter", "RO System": "Sistemang RO", "Water Dispenser": "Dispenser ng Tubig", "Water Purifier": "Water Purifier"
        }
    },
    "he": {
        "ui": {
            "nav_home": "דף הבית", "nav_products": "מוצרים", "nav_about": "אודותינו", "nav_workshop": "בית מלאכה", "nav_exhibition": "תערוכות", "nav_contact": "צור קשר", "cta_whatsapp": "צרו קשר בוואטסאפ",
            "topbar_tag": "סיטונאות גלובלית · מומחי OEM/ODM · מאז 1998",
            "hero_title": "פתרונות טיהור מים תעשייתיים ו-OEM",
            "hero_desc": "ספק סיטונאי גלובלי למסנני PP, CTO, GAC וממברנות RO. מאז 1998, מספקים שירותי OEM/ODM בתקן NSF/ISO.",
            "about_title": "מעל 20 שנות מצוינות בסינון מים",
            "about_desc": "Eco Express Water היא חברת טכנולוגיה סביבתית המתמחה בחומרי סינון וציוד לטיהור מים. נוסדה ב-1998 בהיינינג, ג'ג'יאנג.",
            "footer_brand_desc": "יצרנית מובילה של פתרונות סינון מים בסין מאז 1998.",
            "footer_rights": "כל הזכויות שמורות.",
            "product_view_details": "פרטים נוספים",
            "form_btn": "שלח פנייה"
        },
        "categories": {
            "Filter Cartridge": "מחסנית מסנן", "Filter Housing": "בית מסנן", "Flat Cap Filter": "מסנן קצה שטוח", "Industrial Filter": "מסנן תעשייתי", "Inline Filter": "מסנן אינליין", "RO System": "מערכת RO", "Water Dispenser": "דיספנסר מים", "Water Purifier": "מטהר מים"
        }
    },
    "ur": {
        "ui": {
            "nav_home": "ہوم", "nav_products": "مصنوعات", "nav_about": "ہمارے بارے میں", "nav_workshop": "ورکشاپ", "nav_exhibition": "نمائشیں", "nav_contact": "رابطہ", "cta_whatsapp": "واٹس ایپ کریں",
            "topbar_tag": "عالمی ہول سیل · OEM/ODM ماہر · 1998 سے",
            "hero_title": "صنعتی گریڈ واٹر پیوریفیکیشن اور OEM حل",
            "hero_desc": "PP، CTO، GAC فلٹرز اور RO میمبرین کے عالمی ہول سیل سپلائر۔ 1998 سے NSF/ISO معیار کی OEM/ODM خدمات فراہم کر رہے ہیں۔",
            "about_title": "واٹر فلٹریشن میں 20 سال سے زیادہ کی عمدگی",
            "about_desc": "Eco Express Water پانی کی صفائی کے مواد اور آلات کی ماہر ایک ہائی ٹیک کمپنی ہے۔ 1998 میں ہیننگ، ژجیانگ میں قائم ہوئی۔",
            "footer_brand_desc": "1998 سے چین کی معروف واٹر فلٹریشن حل فراہم کرنے والی کمپنی۔",
            "footer_rights": "جملہ حقوق محفوظ ہیں۔",
            "product_view_details": "تفصیلات دیکھیں",
            "form_btn": "انکوائری بھیجیں"
        },
        "categories": {
            "Filter Cartridge": "فلٹر کارٹریج", "Filter Housing": "فلٹر ہاؤسنگ", "Flat Cap Filter": "فلیٹ کیپ فلٹر", "Industrial Filter": "صنعتی فلٹر", "Inline Filter": "ان لائن فلٹر", "RO System": "آر او سسٹم", "Water Dispenser": "واٹر ڈسپنسر", "Water Purifier": "واٹر پیوریفائر"
        }
    },
    "fa": {
        "ui": {
            "nav_home": "خانه", "nav_products": "محصولات", "nav_about": "درباره ما", "nav_workshop": "کارگاه", "nav_exhibition": "نمایشگاه‌ها", "nav_contact": "تماس", "cta_whatsapp": "واتس‌اپ ما",
            "topbar_tag": "عمده فروشی جهانی · متخصص OEM/ODM · از سال 1998",
            "hero_title": "راهکارهای تصفیه آب صنعتی و OEM",
            "hero_desc": "تامین‌کننده عمده‌فروشی فیلترهای PP، CTO، GAC و غشاهای RO. ارائه خدمات OEM/ODM با استاندارد NSF/ISO از سال 1998.",
            "about_title": "بیش از 20 سال تجربه در فیلتراسیون آب",
            "about_desc": "شرکت اکو اکسپرس واتر متخصص در مواد و تجهیزات فیلتراسیون آب است که در سال 1998 در هاینینگ، ججیانگ تاسیس شد.",
            "footer_brand_desc": "تولیدکننده پیشرو راهکارهای تصفیه آب در چین از سال 1998.",
            "footer_rights": "تمامی حقوق محفوظ است.",
            "product_view_details": "جزئیات محصول",
            "form_btn": "ارسال درخواست"
        },
        "categories": {
            "Filter Cartridge": "کارتریج فیلتر", "Filter Housing": "هوزینگ فیلتر", "Flat Cap Filter": "فیلتر تخت", "Industrial Filter": "فیلتر صنعتی", "Inline Filter": "فیلتر اینلاین", "RO System": "سیستم RO", "Water Dispenser": "دیسپنسر آب", "Water Purifier": "دستگاه تصفیه آب"
        }
    },
    "ha": {
        "ui": {
            "nav_home": "Gida", "nav_products": "Kayayyaki", "nav_about": "Game da mu", "nav_workshop": "Ma'aikata", "nav_exhibition": "Nune-nune", "nav_contact": "Tuntuɓa", "cta_whatsapp": "WhatsApp mu",
            "topbar_tag": "Siyar da Jumla na Duniya · Gwanin OEM/ODM · Tun 1998",
            "hero_title": "Hanyoyin Tace Ruwa na Masana'antu & OEM",
            "hero_desc": "Dillalin duniya na matatun PP, CTO, GAC da membran na RO. Tun 1998, muna samar da ayyukan OEM/ODM na ma'aunin NSF/ISO.",
            "about_title": "Fiye da Shekaru 20 na Inganci a Tace Ruwa",
            "about_desc": "Eco Express Water babban kamfani ne na kare muhalli wanda ya kware a fannin tace ruwa. An kafa shi a 1998 a Haining, Zhejiang.",
            "footer_brand_desc": "Babban kamfani mai kera kayan tace ruwa a kasar Sin tun 1998.",
            "footer_rights": "An kiyaye duk haƙƙoƙi.",
            "product_view_details": "Duba Bayani",
            "form_btn": "Aika Tambaya"
        },
        "categories": {
            "Filter Cartridge": "Kwashin Tace", "Filter Housing": "Gidan Tace", "Flat Cap Filter": "Tace mai Murfi", "Industrial Filter": "Tacewar Masana'antu", "Inline Filter": "Tacewar Layi", "RO System": "Tsarin RO", "Water Dispenser": "Injin Ruwa", "Water Purifier": "Injin Tace Ruwa"
        }
    },
    "zu": {
        "ui": {
            "nav_home": "Ikhaya", "nav_products": "Imikhiqizo", "nav_about": "Mayelana nathi", "nav_workshop": "Indawo yokusebenzela", "nav_exhibition": "Imibukiso", "nav_contact": "Oxhumana nabo", "cta_whatsapp": "Sithinte ku-WhatsApp",
            "topbar_tag": "Ukuthengisa ngenqwaba emhlabeni jikelele · Isazi se-OEM/ODM · Kusukela ngo-1998",
            "hero_title": "Ukuhlanzwa kwamanzi ezingeni lezimboni & nezixazululo ze-OEM",
            "hero_desc": "Umhlinzeki wezithengiso zomhlaba wonke wezihlungi ze-PP, CTO, GAC kanye nemikhumbi ye-RO. Kusukela ngo-1998, sinikeza ngezinsizakalo ze-OEM/ODM ze-NSF/ISO standard.",
            "about_title": "Iminyaka engu-20+ yobungcweti ekuhlungweni kwamanzi",
            "about_desc": "I-Eco Express Water yinkampani yezobuchwepheshe ephezulu yokuvikelwa kwemvelo egxile ezintweni zokuhlunga amanzi. Isungulwe ngo-1998 e-Haining, e-Zhejiang.",
            "footer_brand_desc": "Umkhiqizi ohamba phambili e-China wezixazululo zokuhlunga amanzi kusukela ngo-1998.",
            "footer_rights": "Wonke amalungelo agodliwe.",
            "product_view_details": "Bona imininingwane",
            "form_btn": "Thumela uphenyo"
        },
        "categories": {
            "Filter Cartridge": "I-Filter Cartridge", "Filter Housing": "I-Filter Housing", "Flat Cap Filter": "I-Flat Cap Filter", "Industrial Filter": "Isihlungi Sezimboni", "Inline Filter": "Isihlungi Se-Inline", "RO System": "Isistimu ye-RO", "Water Dispenser": "I-Water Dispenser", "Water Purifier": "Isihlanzi Samanzi"
        }
    },
    "sw": {
        "ui": {
            "nav_home": "Nyumbani", "nav_products": "Bidhaa", "nav_about": "Kuhusu Sisi", "nav_workshop": "Kiwanda", "nav_exhibition": "Maonyesho", "nav_contact": "Wasiliana", "cta_whatsapp": "Tupigie WhatsApp",
            "topbar_tag": "Uuzaji wa Jumla wa Ulimwenguni · Mtaalam wa OEM/ODM · Tangu 1998",
            "hero_title": "Usafishaji wa Maji wa Kiwango cha Viwandani & Suluhu za OEM",
            "hero_desc": "Msambazaji wa jumla wa kimataifa wa vichujio vya PP, CTO, GAC na utando wa RO. Tangu 1998, kutoa huduma za OEM/ODM za kiwango cha NSF/ISO.",
            "about_title": "Zaidi ya Miaka 20 ya Ubora katika Uchujaji wa Maji",
            "about_desc": "Eco Express Water ni kampuni ya teknolojia ya juu ya ulinzi wa mazingira inayolenga nyenzo na vifaa vya kuchuja maji. Ilianzishwa mwaka 1998 huko Haining, Zhejiang.",
            "footer_brand_desc": "Mtengenezaji mkuu nchini China wa suluhisho za kuchuja maji tangu 1998.",
            "footer_rights": "Haki zote zimehifadhiwa.",
            "product_view_details": "Angalia Maelezo",
            "form_btn": "Tuma Uchunguzi"
        },
        "categories": {
            "Filter Cartridge": "Katridi ya Kichujio", "Filter Housing": "Nyumba ya Kichujio", "Flat Cap Filter": "Kichujio cha Kifuniko Bapa", "Industrial Filter": "Kichujio cha Viwandani", "Inline Filter": "Kichujio cha Laini", "RO System": "Mfumo wa RO", "Water Dispenser": "Kitawanya Maji", "Water Purifier": "Kusafisha Maji"
        }
    },
    "kk": {
        "ui": {
            "nav_home": "Басты бет", "nav_products": "Өнімдер", "nav_about": "Біз туралы", "nav_workshop": "Шеберхана", "nav_exhibition": "Көрмелер", "nav_contact": "Байланыс", "cta_whatsapp": "WhatsApp арқылы",
            "topbar_tag": "Жаһандық көтерме сауда · OEM/ODM маманы · 1998 жылдан бері",
            "hero_title": "Өнеркәсіптік деңгейдегі суды тазарту және OEM шешімдері",
            "hero_desc": "PP, CTO, GAC сүзгілері мен RO мембраналарының жаһандық көтерме жеткізушісі. 1998 жылдан бері NSF/ISO стандартындағы OEM/ODM қызметтерін ұсынады.",
            "about_title": "Суды сүзудегі 20 жылдан астам тәжірибе",
            "about_desc": "Eco Express Water - суды тазарту материалдары мен жабдықтарына мамандандырылған жоғары технологиялық компания. 1998 жылы Хайнинде, Чжэцзянда құрылған.",
            "footer_brand_desc": "1998 жылдан бері суды сүзу шешімдерін өндіретін Қытайдың жетекші кәсіпорны.",
            "footer_rights": "Барлық құқықтар қорғалған.",
            "product_view_details": "Толығырақ",
            "form_btn": "Сұрау салу"
        },
        "categories": {
            "Filter Cartridge": "Сүзгі картриджі", "Filter Housing": "Сүзгі корпусы", "Flat Cap Filter": "Тегіс қақпақты сүзгі", "Industrial Filter": "Өнеркәсіптік сүзгі", "Inline Filter": "Инлайн сүзгі", "RO System": "RO жүйесі", "Water Dispenser": "Су диспенсері", "Water Purifier": "Су тазартқыш"
        }
    }
}

# Add remaining translations or reuse boilerplate logic

def translate_data(data, lang):
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            if k == "ui" and lang in translations:
                new_dict[k] = v.copy()
                new_dict[k].update(translations[lang]["ui"])
            elif k == "categories" and lang in translations:
                new_dict[k] = {cat: translations[lang]["categories"].get(cat, cat) for cat in v}
            elif k == "products":
                new_products = []
                for p in v:
                    new_p = p.copy()
                    # Add simple translation logic for products if needed, otherwise keep original
                    new_products.append(new_p)
                new_dict[k] = new_products
            else:
                new_dict[k] = translate_data(v, lang)
        return new_dict
    elif isinstance(data, list):
        return [translate_data(item, lang) for item in data]
    else:
        return data

for lang in languages:
    result = translate_data(en_data, lang)
    with open(os.path.join(base_path, f"{lang}.json"), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

print("Batch 4 completed.")
