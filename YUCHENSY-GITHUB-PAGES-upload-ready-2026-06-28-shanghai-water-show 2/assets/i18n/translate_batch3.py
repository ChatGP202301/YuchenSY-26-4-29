
import json
import os

languages = ["he", "ur", "fa", "ha"]
base_path = "/Users/jet/.accio/accounts/1661502182/agents/DID-F456DA-2B0D4C/project/assets/i18n/"
en_file = os.path.join(base_path, "en.json")

with open(en_file, 'r', encoding='utf-8') as f:
    en_data = json.load(f)

translations = {
    "he": {
        "ui": {
            "nav_home": "בית", "nav_products": "מוצרים", "nav_about": "אודותינו", "nav_workshop": "בית מלאכה",
            "nav_exhibition": "תערוכות", "nav_contact": "צור קשר", "cta_whatsapp": "שלחו לנו הודעה בוואטסאפ",
            "topbar_tag": "סיטונאות גלובלית · מומחי OEM/ODM · מאז 1998",
            "hero_eyebrow": "✦ יצרן מסנני מים מוביל בסין | מפעל מוסמך NSF ו-ISO",
            "hero_title": "פתרונות טיהור מים בדרגה תעשייתית ו-OEM",
            "hero_desc": "ספק סיטונאי גלובלי של מסנני PP Melt Blown, CTO, GAC וממברנות RO בעלי ביצועים גבוהים. מאז 1998, אנו מספקים תמיכה טכנית OEM/ODM מוסמכת NSF/ISO ל-50+ מדינות.",
            "hero_btn_explore": "צפו בפורטפוליו המפעל", "hero_btn_quote": "בקשו הצעת מחיר סיטונאית",
            "stats_years": "שנות ניסיון", "stats_models": "דגמי מוצרים", "stats_countries": "מדינות שירות", "stats_area": "שטח ייצור",
            "about_eyebrow": "אודותינו", "about_title": "20+ שנות מצוינות בסינון מים",
            "about_desc": "Eco Express Water הוא מפעל להגנת הסביבה בהייטק המתמחה בחומרי סינון וציוד סינון לטיהור מים. החברה הוקמה בשנת 1998, ומוצרינו משלבים את הזרם המלא ממחקר ופיתוח, ייצור, שיווק ועד תמיכה טכנית. החברה שלנו ממוקמת בעיר יואנהואה, העיר היינינג, מחוז ג'ג'יאנג, סין. יש לנו צוות מומחים טכניים מהשורה הראשונה, ומרכז ייצור בקנה מידה גדול. אנו ספק מוסמך של מסנני מים חלאל, המספקים מענה לצרכים הייחודיים של צרכנים מוסלמים במלזיה, אינדונזיה ומדינות מוסלמיות אחרות.",
            "why_title": "שותף ייצור מהימן", "why_desc": "מחומרי הגלם ועד לבדיקה הסופית, כל מוצר עובר את מערכת בקרת האיכות הקפדנית שלנו.",
            "footer_brand_desc": "יצרן פתרונות סינון מים מוביל בסין מאז 1998. מתמחה ב-PP Melt Blown, CTO Carbon Block, GAC וממברנות RO לשותפים סיטונאיים גלובליים ו-OEM/ODM.",
            "footer_rights": "כל הזכויות שמורות."
        },
        "categories": {
            "Filter Cartridge": "מחסנית מסנן", "Filter Housing": "בית מסנן", "Flat Cap Filter": "מסנן מכסה שטוח",
            "Industrial Filter": "מסנן תעשייתי", "Inline Filter": "מסנן אינליין", "RO System": "מערכת RO",
            "Water Dispenser": "דיספנסר מים", "Water Purifier": "מטהר מים"
        },
        "boilerplate": "מיוצר במתקן המוסמך ל-ISO 9001:2015 שלנו בשטח של 20,000+ מ\"ר בעיר יואנהואה, העיר היינינג, מחוז ג'ג'יאנג, סין. מוצר זה הוא חלק מקו סינון המים המלא שלנו — נבדק באופן עצמאי לתקני NSF/ANSI 42 ו-53 על ידי SGS, עם סימון CE לתאימות ייבוא אירופית והצהרות חומרים בדרגת FDA לפי דרישה. התאמה אישית של מותג פרטי OEM/ODM זמינה: הדפסת מותג, יציקת מכסה קצה מותאמת אישית, התאמת צבעים ואריזה. MOQ סטנדרטי מ-1,000 יחידות; סיטונאות בתפזורת FOB שנחאי/נינגבו עם תנאי תשלום T/T 30/70 או L/C למראה. אנו מייצאים כיום ל-50+ מדינות כולל ארצות הברית, גרמניה, רוסיה, ערב הסעודית, מלזיה, אינדונזיה וברזיל, עם הסמכת חלאל (JAKIM) מלאה בשוק המוסלמי."
    },
    "ur": {
        "ui": {
            "nav_home": "ہوم", "nav_products": "مصنوعات", "nav_about": "ہمارے بارے میں", "nav_workshop": "ورکشاپ",
            "nav_exhibition": "نمائشیں", "nav_contact": "رابطہ کریں", "cta_whatsapp": "ہمیں واٹس ایپ کریں",
            "topbar_tag": "عالمی بلک ہول سیل · OEM/ODM ماہر · 1998 سے",
            "hero_eyebrow": "✦ چین کا معروف واٹر فلٹر مینوفیکچرر | NSF اور ISO تصدیق شدہ فیکٹری",
            "hero_title": "انڈسٹریل گریڈ واٹر پیوریفیکیشن اور OEM سلوشنز",
            "hero_desc": "اعلی کارکردگی والے PP Melt Blown، CTO، GAC فلٹرز اور RO میمبرینز کے عالمی بلک ہول سیل سپلائر۔ 1998 سے ہم 50 سے زائد ممالک کے لیے NSF/ISO تصدیق شدہ OEM/ODM تکنیکی مدد فراہم کر رہے ہیں۔",
            "hero_btn_explore": "فیکٹری پورٹ فولیو دیکھیں", "hero_btn_quote": "بلک کوٹیشن کی درخواست کریں",
            "stats_years": "سالوں کا تجربہ", "stats_models": "مصنوعات کے ماڈل", "stats_countries": "خدمت کردہ ممالک", "stats_area": "مینوفیکچرنگ ایریا",
            "about_eyebrow": "ہمارے بارے میں", "about_title": "واٹر فلٹریشن میں 20 سال سے زائد کی عمدگی",
            "about_desc": "Eco Express Water ایک ہائی ٹیک ماحولیاتی تحفظ کا ادارہ ہے جو پانی کی صفائی کے لیے فلٹر مواد اور فلٹر آلات میں مہارت رکھتا ہے۔ 1998 میں قائم ہوا، ہماری مصنوعات تحقیق اور ترقی، مینوفیکچرنگ، مارکیٹنگ سے لے کر تکنیکی مدد تک مکمل بہاؤ کو مربوط کرتی ہیں۔ ہماری کمپنی یوانہوا ٹاؤن، ہیننگ سٹی، صوبہ ژجیانگ، چین میں واقع ہے۔ ہمارے پاس فرسٹ کلاس تکنیکی ماہرین کی ٹیم اور بڑے پیمانے پر مینوفیکچرنگ سینٹر ہے۔ ہم حلال واٹر فلٹرز کے تصدیق شدہ فراہم کنندہ ہیں، جو ملائیشیا، انڈونیشیا اور دیگر مسلم ممالک میں مسلم صارفین کی منفرد ضروریات کو پورا کرتے ہیں۔",
            "why_title": "قابل اعتماد مینوفیکچرنگ پارٹنر", "why_desc": "خام مال سے لے کر حتمی معائنہ تک، ہر پروڈکٹ ہمارے سخت کوالٹی کنٹرول سسٹم سے گزرتی ہے۔",
            "footer_brand_desc": "1998 سے واٹر فلٹریشن سلوشنز کا چین کا معروف مینوفیکچرر۔ عالمی بلک ہول سیل اور OEM/ODM شراکت داروں کے لیے PP Melt Blown، CTO Carbon Block، GAC اور RO میمبرینز میں ماہر۔",
            "footer_rights": "جملہ حقوق محفوظ ہیں۔"
        },
        "categories": {
            "Filter Cartridge": "فلٹر کارٹریج", "Filter Housing": "فلٹر ہاؤسنگ", "Flat Cap Filter": "فلیٹ کیپ فلٹر",
            "Industrial Filter": "صنعتی فلٹر", "Inline Filter": "ان لائن فلٹر", "RO System": "RO سسٹم",
            "Water Dispenser": "واٹر ڈسپنسر", "Water Purifier": "واٹر پیوریفائر"
        },
        "boilerplate": "چین کے صوبہ ژجیانگ کے شہر ہیننگ کے ٹاؤن یوانہوا میں ہماری 20,000+ مربع میٹر کی ISO 9001:2015 تصدیق شدہ سہولت میں تیار کردہ، یہ پروڈکٹ ہماری فل سٹیک واٹر فلٹریشن لائن کا حصہ ہے — جو SGS کے ذریعے NSF/ANSI 42 اور 53 معیارات کے مطابق آزادانہ طور پر ٹیسٹ کی گئی ہے، جس میں یورپی امپورٹ کمپلائنس کے لیے CE مارکنگ اور درخواست پر FDA گریڈ میٹریل ڈیکلریشن شامل ہے۔ OEM/ODM پرائیویٹ لیبل حسب ضرورت دستیاب ہے: برانڈ پرنٹنگ، کسٹم اینڈ کیپ مولڈنگ، کلر میچنگ اور پیکیجنگ۔ 1,000 پیس سے اسٹینڈرڈ MOQ؛ T/T 30/70 یا L/C ایٹ سائٹ ادائیگی کی شرائط کے ساتھ FOB شنگھائی/ننگبو بلک ہول سیل۔ ہم اس وقت امریکہ، جرمنی، روس، سعودی عرب، ملائیشیا، انڈونیشیا اور برازیل سمیت 50+ ممالک کو برآمد کر رہے ہیں، مسلم مارکیٹوں کے لیے مکمل حلال (JAKIM) سرٹیفیکیشن کے ساتھ۔"
    },
    "fa": {
        "ui": {
            "nav_home": "صفحه اصلی", "nav_products": "محصولات", "nav_about": "درباره ما", "nav_workshop": "کارگاه",
            "nav_exhibition": "نمایشگاه‌ها", "nav_contact": "تماس با ما", "cta_whatsapp": "در واتس‌اپ پیام دهید",
            "topbar_tag": "عمده‌فروشی جهانی · متخصص OEM/ODM · از سال ۱۹۹۸",
            "hero_eyebrow": "✦ تولیدکننده پیشرو فیلتر آب در چین | کارخانه دارای گواهی NSF و ISO",
            "hero_title": "تصفیه آب در سطح صنعتی و راهکارهای OEM",
            "hero_desc": "تامین‌کننده عمده‌فروشی جهانی فیلترهای با کارایی بالای PP Melt Blown، CTO، GAC و غشاهای RO. از سال ۱۹۹۸، ما پشتیبانی فنی OEM/ODM دارای گواهی NSF/ISO را برای بیش از ۵۰ کشور ارائه می‌دهیم.",
            "hero_btn_explore": "مشاهده پورتفولیوی کارخانه", "hero_btn_quote": "درخواست قیمت عمده",
            "stats_years": "سال تجربه", "stats_models": "مدل‌های محصول", "stats_countries": "کشورهای تحت پوشش", "stats_area": "فضای تولید",
            "about_eyebrow": "درباره ما", "about_title": "بیش از ۲۰ سال برتری در فیلتراسیون آب",
            "about_desc": "شرکت Eco Express Water یک شرکت فناورانه حفاظت از محیط زیست است که در زمینه مواد فیلتر و تجهیزات فیلتر برای تصفیه آب تخصص دارد. این شرکت که در سال ۱۹۹۸ تاسیس شده، محصولات ما تمام مراحل از تحقیق و توسعه، تولید، بازاریابی تا پشتیبانی فنی را در بر می‌گیرد. شرکت ما در شهر یوآن‌هوا، شهر هاینینگ، استان ججیانگ، چین واقع شده است. ما دارای یک تیم متخصص فنی درجه یک و یک مرکز تولید در مقیاس بزرگ هستیم. ما تامین‌کننده تایید شده فیلترهای آب حلال هستیم که نیازهای منحصر به فرد مصرف‌کنندگان مسلمان در مالزی، اندونزی و سایر کشورهای اسلامی را برآورده می‌کنیم.",
            "why_title": "شریک تولیدی قابل اعتماد", "why_desc": "از مواد اولیه تا بازرسی نهایی، هر محصول از سیستم کنترل کیفیت دقیق ما عبور می‌کند.",
            "footer_brand_desc": "تولیدکننده پیشرو راهکارهای فیلتراسیون آب در چین از سال ۱۹۹۸. متخصص در PP Melt Blown، CTO Carbon Block، GAC و غشاهای RO برای شرکای عمده‌فروشی جهانی و OEM/ODM.",
            "footer_rights": "تمامی حقوق محفوظ است."
        },
        "categories": {
            "Filter Cartridge": "کارتریج فیلتر", "Filter Housing": "هوزینگ فیلتر", "Flat Cap Filter": "فیلتر درپوش تخت",
            "Industrial Filter": "فیلتر صنعتی", "Inline Filter": "فیلتر اینلاین", "RO System": "سیستم RO",
            "Water Dispenser": "دستگاه آب‌سردکن", "Water Purifier": "تصفیه‌کننده آب"
        },
        "boilerplate": "تولید شده در مرکز دارای گواهی ISO 9001:2015 ما با مساحت بیش از ۲۰,۰۰۰ متر مربع در شهر یوآن‌هوا، شهر هاینینگ، استان ججیانگ، چین. این محصول بخشی از خط کامل فیلتراسیون آب ماست — که به طور مستقل توسط SGS با استانداردهای NSF/ANSI 42 و 53 آزمایش شده، دارای علامت CE برای انطباق با واردات اروپا و اعلامیه‌های مواد درجه FDA در صورت درخواست است. سفارشی‌سازی برچسب خصوصی OEM/ODM در دسترس است: چاپ برند، قالب‌گیری درپوش انتهایی سفارشی، تطبیق رنگ و بسته‌بندی. حداقل مقدار سفارش استاندارد از ۱,۰۰۰ عدد؛ عمده‌فרוشی FOB شانگهای/نینگبو با شرایط پرداخت T/T 30/70 یا L/C در دید. ما در حال حاضر به بیش از ۵۰ کشور از جمله ایالات متحده، آلمان، روسیه، عربستان سعودی، مالزی، اندونزی و برزیل صادر می‌کنیم، با گواهی کامل حلال (JAKIM) در پرونده برای بازارهای اسلامی."
    },
    "ha": {
        "ui": {
            "nav_home": "Gida", "nav_products": "Kayayyaki", "nav_about": "Game da Mu", "nav_workshop": "Bitoci",
            "nav_exhibition": "Nune-nune", "nav_contact": "Tuntuɓi Mu", "cta_whatsapp": "Aiko Mana Sako a WhatsApp",
            "topbar_tag": "Siyarwa ta Jumla ta Duniya · Kwararre kan OEM/ODM · Tun 1998",
            "hero_eyebrow": "✦ Jagoran Ma'aikatar Tace Ruwa a Sin | Ma'aikata Mai Takardar Shaidar NSF & ISO",
            "hero_title": "Tace Ruwa na Masana'antu & Hanyoyin OEM",
            "hero_desc": "Mai samar da kayayyaki ta jumla na duniya na PP Melt Blown, CTO, GAC filters, da RO membranes. Tun 1998, muna samar da tallafin fasaha na OEM/ODM mai takardar shaidar NSF/ISO ga kasashe 50+.",
            "hero_btn_explore": "Duba Portfolio na Ma'aikata", "hero_btn_quote": "Nemi Farashin Jumla",
            "stats_years": "Shekarun Kwarewa", "stats_models": "Samfuran Kayayyaki", "stats_countries": "Kasashen da ake Hidimawa", "stats_area": "Yankin Masana'antu",
            "about_eyebrow": "Game da Mu", "about_title": "Shekaru 20+ na Kwarewa kan Tace Ruwa",
            "about_desc": "Eco Express Water babban kamfani ne na kare muhalli wanda ya kware kan kayan tace ruwa da kayan aikin tace ruwa don tsabtace ruwa. An kafa shi a shekarar 1998, kayayyakinmu sun hada dukkan matakai tun daga bincike da ci gaba, masana'antu, tallace-tallace zuwa tallafin fasaha. Kamfaninmu yana garin Yuanhua, birnin Haining, lardin Zhejiang, kasar Sin. Muna da ƙwararrun ƙwararrun ƙwararrun ƙwararrun fasaha, da kuma babban cibiyar masana'antu. Mu masu samar da tacewar ruwa ne masu takardar shaidar halal, muna biyan buƙatu na musamman na masu amfani da Musulmi a Malaysia, Indonesia, da sauran ƙasashen musulmi.",
            "why_title": "Abokin Masana'antu Amintacce", "why_desc": "Daga albarkatun kasa zuwa dubawa na karshe, kowane samfuri yana wucewa ta tsarin kula da ingancinmu.",
            "footer_brand_desc": "Jagoran ma'aikatar samar da hanyoyin tace ruwa a Sin tun 1998. Kwararre kan PP Melt Blown, CTO Carbon Block, GAC, da RO membranes don jumla ta duniya da abokan OEM/ODM.",
            "footer_rights": "Duk hakkoki suna kiyaye."
        },
        "categories": {
            "Filter Cartridge": "Kayan Tace Ruwa", "Filter Housing": "Gidan Tace Ruwa", "Flat Cap Filter": "Tacewar Flat Cap",
            "Industrial Filter": "Tacewar Masana'antu", "Inline Filter": "Tacewar Inline", "RO System": "Tsarin RO",
            "Water Dispenser": "Mai Bayar da Ruwa", "Water Purifier": "Mai Tsabtace Ruwa"
        },
        "boilerplate": "An kera shi a cibiyarmu mai takardar shaidar ISO 9001:2015 mai fadin murabba'in m² 20,000+ a garin Yuanhua, birnin Haining, lardin Zhejiang, kasar Sin, wannan samfurin yana daga cikin layinmu na tace ruwa — SGS ta gwada shi da kanta zuwa ma'aunin NSF/ANSI 42 & 53, tare da alamar CE don bin dokokin shigo da kaya na Turai da kuma bayanan kayan matakin FDA akan bukata. Akwai keɓancewar lakabin sirri na OEM/ODM: buga alama, gyare-gyaren ƙarshen ƙira, daidaita launi da marufi. Daidaitaccen MOQ daga guda 1,000; siyarwa ta jumla FOB Shanghai/Ningbo tare da sharuɗɗan biyan kuɗi na T/T 30/70 ko L/C. A halin yanzu muna fitarwa zuwa kasashe 50+ da suka hada da Amurka, Jamus, Rasha, Saudiyya, Malaysia, Indonesia da Brazil, tare da cikakken takardar shaidar halal (JAKIM) a cikin fayil don kasuwannin Musulmi."
    }
}

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
                    if lang in translations:
                        new_p["desc"] = translations[lang]["boilerplate"]
                    new_products.append(new_p)
                new_dict[k] = new_products
            else:
                new_dict[k] = translate_data(v, lang)
        return new_dict
    elif isinstance(data, list):
        return [translate_data(item, lang) for item in data]
    else:
        return data

for lang in ["he", "ur", "fa", "ha"]:
    result = translate_data(en_data, lang)
    with open(os.path.join(base_path, f"{lang}.json"), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

print("Batch 3 completed.")
