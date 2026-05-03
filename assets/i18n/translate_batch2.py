
import json
import os

languages = ["bn", "tl", "ta", "kk"]
base_path = "/Users/jet/.accio/accounts/1661502182/agents/DID-F456DA-2B0D4C/project/assets/i18n/"
en_file = os.path.join(base_path, "en.json")

with open(en_file, 'r', encoding='utf-8') as f:
    en_data = json.load(f)

translations = {
    "bn": {
        "ui": {
            "nav_home": "হোম", "nav_products": "পণ্যসমূহ", "nav_about": "আমাদের সম্পর্কে", "nav_workshop": "ওয়ার্কশপ",
            "nav_exhibition": "প্রদর্শনী", "nav_contact": "যোগাযোগ", "cta_whatsapp": "হোয়াটসঅ্যাপ করুন",
            "topbar_tag": "গ্লোবাল বাল্ক হোলসেল · OEM/ODM বিশেষজ্ঞ · ১৯৯৮ থেকে",
            "hero_eyebrow": "✦ শীর্ষস্থানীয় চীন ওয়াটার ফিল্টার প্রস্তুতকারক | NSF এবং ISO প্রত্যয়িত কারখানা",
            "hero_title": "ইন্ডাস্ট্রিয়াল-গ্রেড ওয়াটার পিউরিফিকেশন এবং OEM সমাধান",
            "hero_desc": "উচ্চ-ক্ষমতাসম্পন্ন PP Melt Blown, CTO, GAC ফিল্টার এবং RO মেমব্রেনের গ্লোবাল বাল্ক হোলসেল সরবরাহকারী। ১৯৯৮ থেকে আমরা ৫০+ দেশের জন্য NSF/ISO প্রত্যয়িত OEM/ODM প্রযুক্তিগত সহায়তা প্রদান করছি।",
            "hero_btn_explore": "ফ্যাক্টরি পোর্টফোলিও দেখুন", "hero_btn_quote": "বাল্ক কোটেশন অনুরোধ করুন",
            "stats_years": "বছরের অভিজ্ঞতা", "stats_models": "পণ্য মডেল", "stats_countries": "সেবা প্রদানকারী দেশ", "stats_area": "উৎপাদন এলাকা",
            "about_eyebrow": "আমাদের সম্পর্কে", "about_title": "২০+ বছরের ওয়াটার ফিল্ট্রেশন শ্রেষ্ঠত্ব",
            "about_desc": "ইকো এক্সপ্রেস ওয়াটার একটি উচ্চ-প্রযুক্তি পরিবেশ সুরক্ষা এন্টারপ্রাইজ যা জল পরিশোধনের জন্য ফিল্টার উপাদান এবং ফিল্টার সরঞ্জামগুলিতে বিশেষজ্ঞ। ১৯৯৮ সালে প্রতিষ্ঠিত, আমাদের পণ্যগুলি গবেষণা এবং উন্নয়ন, উৎপাদন, বিপণন থেকে শুরু করে প্রযুক্তিগত সহায়তা পর্যন্ত সম্পূর্ণ প্রবাহকে একীভূত করে। আমাদের কোম্পানি চীনের ঝেজিয়াং প্রদেশের হাইনিং সিটির ইউয়ানহুয়া টাউনে অবস্থিত। আমাদের একটি প্রথম-শ্রেণীর প্রযুক্তিগত বিশেষজ্ঞ দল এবং একটি বড় আকারের উৎপাদন কেন্দ্র রয়েছে। আমরা হালাল প্রত্যয়িত ওয়াটার ফিল্টার সরবরাহকারী, যা মালয়েশিয়া, ইন্দোনেশিয়া এবং অন্যান্য মুসলিম দেশগুলির মুসলিম গ্রাহকদের অনন্য প্রয়োজন মেটায়।",
            "why_title": "বিশ্বস্ত উৎপাদন অংশীদার", "why_desc": "কাঁচামাল থেকে চূড়ান্ত পরিদর্শন পর্যন্ত, প্রতিটি পণ্য আমাদের কঠোর মান নিয়ন্ত্রণ ব্যবস্থার মধ্য দিয়ে যায়।",
            "footer_brand_desc": "১৯৯৮ থেকে জল পরিস্রাবণ সমাধানের শীর্ষস্থানীয় চীন প্রস্তুতকারক। গ্লোবাল বাল্ক হোলসেল এবং OEM/ODM অংশীদারদের জন্য PP Melt Blown, CTO Carbon Block, GAC এবং RO মেমব্রেনে বিশেষজ্ঞ।",
            "footer_rights": "সর্বস্বত্ব সংরক্ষিত।"
        },
        "categories": {
            "Filter Cartridge": "ফিল্টার কার্তুজ", "Filter Housing": "ফিল্টার হাউজিং", "Flat Cap Filter": "ফ্ল্যাট ক্যাপ ফিল্টার",
            "Industrial Filter": "ইন্ডাস্ট্রিয়াল ফিল্টার", "Inline Filter": "ইনলাইন ফিল্টার", "RO System": "RO সিস্টেম",
            "Water Dispenser": "ওয়াটার ডিস্পেনসার", "Water Purifier": "ওয়াটার পিউরিফায়ার"
        },
        "boilerplate": "চীনের ঝেজিয়াং প্রদেশের হাইনিং সিটির ইউয়ানহুয়া টাউনে আমাদের ২০,০০০+ বর্গমিটার ISO 9001:2015 প্রত্যয়িত সুবিধায় উৎপাদিত, এই পণ্যটি আমাদের ফুল-স্ট্যাক ওয়াটার ফিল্ট্রেশন লাইনের অংশ — যা SGS দ্বারা NSF/ANSI 42 এবং 53 স্ট্যান্ডার্ডে স্বাধীনভাবে পরীক্ষিত, ইউরোপীয় আমদানির জন্য CE মার্কিং এবং অনুরোধে FDA-গ্রেড উপাদান ঘোষণা সহ। OEM/ODM প্রাইভেট-লেবেল কাস্টমাইজেশন উপলব্ধ: ব্র্যান্ড প্রিন্টিং, কাস্টম এন্ড-ক্যাপ মোল্ডিং, কালার ম্যাচিং এবং প্যাকেজিং। ১,০০০ পিস থেকে স্ট্যান্ডার্ড MOQ; T/T 30/70 বা L/C অ্যাট সাইট পেমেন্ট শর্তে FOB সাংহাই/নিংবো বাল্ক হোলসেল। আমরা বর্তমানে মার্কিন যুক্তরাষ্ট্র, জার্মানি, রাশিয়া, সৌদি আরব, মালয়েশিয়া, ইন্দোনেশিয়া এবং ব্রাজিল সহ ৫০+ দেশে রপ্তানি করছি, মুসলিম বাজারের জন্য ফাইলে সম্পূর্ণ হালাল (JAKIM) সার্টিফিকেশন সহ।"
    },
    "tl": {
        "ui": {
            "nav_home": "Home", "nav_products": "Mga Produkto", "nav_about": "Tungkol sa Amin", "nav_workshop": "Workshop",
            "nav_exhibition": "Mga Eksibisyon", "nav_contact": "Kontak", "cta_whatsapp": "I-WhatsApp Kami",
            "topbar_tag": "Global Bulk Wholesale · Eksperto sa OEM/ODM · Mula noong 1998",
            "hero_eyebrow": "✦ Nangungunang Manufacturer ng Water Filter sa China | NSF at ISO Certified Factory",
            "hero_title": "Industrial-Grade na Paglilinis ng Tubig at mga Solusyong OEM",
            "hero_desc": "Global bulk wholesale supplier ng high-performance na PP Melt Blown, CTO, GAC filter, at RO membranes. Mula noong 1998, nagbibigay kami ng NSF/ISO certified OEM/ODM technical support para sa 50+ bansa.",
            "hero_btn_explore": "Tingnan ang Portfolio ng Pabrika", "hero_btn_quote": "Humingi ng Bulk Quote",
            "stats_years": "Taon ng Karanasan", "stats_models": "Mga Modelo ng Produkto", "stats_countries": "Mga Bansang Pinagsisilbihan", "stats_area": "Lugar ng Paggawa",
            "about_eyebrow": "Tungkol sa Amin", "about_title": "20+ Taon ng Kahusayan sa Pag-filter ng Tubig",
            "about_desc": "Ang Eco Express Water ay isang high-tech na enterprise para sa proteksyon ng kapaligiran na dalubhasa sa mga materyales sa filter at kagamitan sa filter para sa paglilinis ng tubig. Itinatag noong 1998, ang aming mga produkto ay nagsasama ng buong stream mula sa pananaliksik at pagpapaunlad, paggawa, marketing hanggang sa teknikal na suporta. Ang aming kumpanya ay matatagpuan sa Yuanhua Town, Haining City, Zhejiang Province, China. Mayroon kaming first-class na technical expert team at isang malaking sentro ng pagmamanupaktura. Kami ay isang sertipikadong supplier ng mga halal water filter, na tumutugon sa mga natatanging pangangailangan ng mga Muslim na mamimili sa Malaysia, Indonesia, at iba pang mga bansang Muslim.",
            "why_title": "Pinagkakatiwalaang Kasosyo sa Paggawa", "why_desc": "Mula sa mga hilaw na materyales hanggang sa huling inspeksyon, ang bawat produkto ay dumadaan sa aming mahigpit na sistema ng kontrol sa kalidad.",
            "footer_brand_desc": "Nangungunang manufacturer ng mga solusyon sa pag-filter ng tubig sa China mula noong 1998. Dalubhasa sa PP Melt Blown, CTO Carbon Block, GAC, at RO membranes para sa global bulk wholesale at mga kasosyo sa OEM/ODM.",
            "footer_rights": "Lahat ng karapatan ay nakareserba."
        },
        "categories": {
            "Filter Cartridge": "Filter Cartridge", "Filter Housing": "Filter Housing", "Flat Cap Filter": "Flat Cap Filter",
            "Industrial Filter": "Pang-industriyang Filter", "Inline Filter": "Inline Filter", "RO System": "Sistemang RO",
            "Water Dispenser": "Dispenser ng Tubig", "Water Purifier": "Water Purifier"
        },
        "boilerplate": "Ginawa sa aming 20,000+ m² ISO 9001:2015 certified facility sa Yuanhua Town, Haining City, Zhejiang Province, China, ang produktong ito ay bahagi ng aming full-stack water filtration line — independiyenteng sinubukan sa mga pamantayan ng NSF/ANSI 42 at 53 ng SGS, na may CE marking para sa pagsunod sa pag-import sa Europa at mga deklarasyon ng materyal na FDA-grade kapag hiniling. Available ang OEM/ODM private-label customization: pag-print ng brand, custom na end-cap molding, pagtutugma ng kulay at packaging. Standard MOQ mula 1,000 pcs; bulk wholesale FOB Shanghai/Ningbo na may T/T 30/70 o L/C at sight na mga tuntunin sa pagbabayad. Kasalukuyan kaming nag-e-export sa 50+ bansa kabilang ang Estados Unidos, Alemanya, Rusya, Saudi Arabia, Malaysia, Indonesia at Brazil, na may kumpletong halal (JAKIM) certification para sa mga merkado ng Muslim."
    },
    "ta": {
        "ui": {
            "nav_home": "முகப்பு", "nav_products": "தயாரிப்புகள்", "nav_about": "எங்களைப் பற்றி", "nav_workshop": "பணிமனை",
            "nav_exhibition": "கண்காட்சிகள்", "nav_contact": "தொடர்பு", "cta_whatsapp": "வாட்ஸ்அப் மூலம் தொடர்பு கொள்ளவும்",
            "topbar_tag": "உலகளாவிய மொத்த விற்பனை · OEM/ODM நிபுணர் · 1998 முதல்",
            "hero_eyebrow": "✦ முன்னணி சீனா நீர் வடிகட்டி உற்பத்தியாளர் | NSF & ISO சான்றளிக்கப்பட்ட தொழிற்சாலை",
            "hero_title": "தொழில்துறை தர நீர் சுத்திகரிப்பு & OEM தீர்வுகள்",
            "hero_desc": "உயர் செயல்திறன் கொண்ட PP Melt Blown, CTO, GAC வடிகட்டிகள் மற்றும் RO சவ்வுகளின் உலகளாவிய மொத்த விற்பனை சப்ளையர். 1998 முதல், 50+ நாடுகளுக்கு NSF/ISO சான்றளிக்கப்பட்ட OEM/ODM தொழில்நுட்ப ஆதரவை வழங்குகிறோம்.",
            "hero_btn_explore": "தொழிற்சாலை போர்ட்ஃபோலியோவைப் பார்க்கவும்", "hero_btn_quote": "மொத்த விற்பனை மேற்கோளைக் கோரவும்",
            "stats_years": "ஆண்டு அனுபவம்", "stats_models": "தயாரிப்பு மாதிரிகள்", "stats_countries": "சேவையளிக்கப்பட்ட நாடுகள்", "stats_area": "உற்பத்திப் பகுதி",
            "about_eyebrow": "எங்களைப் பற்றி", "about_title": "20+ வருட நீர் வடிகட்டுதல் மேன்மை",
            "about_desc": "Eco Express Water என்பது நீர் சுத்திகரிப்புக்கான வடிகட்டி பொருட்கள் மற்றும் வடிகட்டி உபகரணங்களில் நிபுணத்துவம் பெற்ற ஒரு உயர் தொழில்நுட்ப சுற்றுச்சூழல் பாதுகாப்பு நிறுவனமாகும். 1998 இல் நிறுவப்பட்டது, எங்கள் தயாரிப்புகள் ஆராய்ச்சி மற்றும் மேம்பாடு, உற்பத்தி, சந்தைப்படுத்தல் முதல் தொழில்நுட்ப ஆதரவு வரை முழு ஓட்டத்தையும் ஒருங்கிணைக்கின்றன. எங்கள் நிறுவனம் சீனாவின் ஜெஜியாங் மாகாணத்தின் ஹைனிங் நகரில் உள்ள யுவான்ஹுவா நகரில் அமைந்துள்ளது. எங்களிடம் முதல் தர தொழில்நுட்ப நிபுணர் குழு மற்றும் பெரிய அளவிலான உற்பத்தி மையம் உள்ளது. நாங்கள் ஹலால் சான்றளிக்கப்பட்ட நீர் வடிகட்டிகளின் அங்கீகரிக்கப்பட்ட சப்ளையர், மலேசியா, இந்தோனேசியா மற்றும் பிற முஸ்லீம் நாடுகளில் உள்ள முஸ்லீம் நுகர்வோரின் தனித்துவமான தேவைகளைப் பூர்த்தி செய்கிறோம்.",
            "why_title": "நம்பகமான உற்பத்தி பங்குதாரர்", "why_desc": "மூலப்பொருட்கள் முதல் இறுதி ஆய்வு வரை, ஒவ்வொரு தயாரிப்பும் எங்களது கடுமையான தரக் கட்டுப்பாட்டு முறையைக் கடந்து செல்கின்றன.",
            "footer_brand_desc": "1998 முதல் நீர் வடிகட்டுதல் தீர்வுகளில் முன்னணி சீனா உற்பத்தியாளர். உலகளாவிய மொத்த விற்பனை மற்றும் OEM/ODM கூட்டாளர்களுக்கு PP Melt Blown, CTO Carbon Block, GAC மற்றும் RO சவ்வுகளில் நிபுணத்துவம் பெற்றவர்.",
            "footer_rights": "அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை."
        },
        "categories": {
            "Filter Cartridge": "வடிகட்டி கார்ட்ரிட்ஜ்", "Filter Housing": "வடிகட்டி வீடுகள்", "Flat Cap Filter": "பிளாட் கேப் வடிகட்டி",
            "Industrial Filter": "தொழில்துறை வடிகட்டி", "Inline Filter": "இன்லைன் வடிகட்டி", "RO System": "RO அமைப்பு",
            "Water Dispenser": "வாட்டர் டிஸ்பென்சர்", "Water Purifier": "நீர் சுத்திகரிப்பு இயந்திரம்"
        },
        "boilerplate": "சீனாவின் ஜெஜியாங் மாகாணத்தின் ஹைனிங் நகரில் உள்ள யுவான்ஹுவா நகரில் அமைந்துள்ள எங்களது 20,000+ m² ISO 9001:2015 சான்றளிக்கப்பட்ட வசதியில் தயாரிக்கப்பட்ட இந்தத் தயாரிப்பு, எங்களது முழு-அடுக்கு நீர் வடிகட்டுதல் வரிசையின் ஒரு பகுதியாகும் — SGS ஆல் NSF/ANSI 42 & 53 தரநிலைகளுக்கு சுயாதீனமாக சோதிக்கப்பட்டது, ஐரோப்பிய இறக்குமதி இணக்கத்திற்கான CE குறி மற்றும் கோரிக்கையின் பேரில் FDA-தர பொருள் அறிவிப்புகளுடன். OEM/ODM பிரைவேட்-லேபிள் தனிப்பயனாக்கம் கிடைக்கிறது: பிராண்ட் பிரிண்டிங், தனிப்பயன் எண்ட்-கேப் மோல்டிங், வண்ணப் பொருத்தம் மற்றும் பேக்கேஜிங். 1,000 பிசிக்களில் இருந்து நிலையான MOQ; T/T 30/70 அல்லது L/C பார்வைக் கட்டண விதிமுறைகளுடன் FOB ஷாங்காய்/நிங்போ மொத்த விற்பனை. நாங்கள் தற்போது அமெரிக்கா, ஜெர்மனி, ரஷ்யா, சவுதி அரேபியா, மலேசியா, இந்தோனேசியா மற்றும் பிரேசில் உள்ளிட்ட 50+ நாடுகளுக்கு ஏற்றுமதி செய்கிறோம், முஸ்லீம் சந்தைகளுக்கான முழு ஹலால் (JAKIM) சான்றிதழுடன்."
    },
    "kk": {
        "ui": {
            "nav_home": "Басты бет", "nav_products": "Өнімдер", "nav_about": "Біз туралы", "nav_workshop": "Шеберхана",
            "nav_exhibition": "Көрмелер", "nav_contact": "Байланыс", "cta_whatsapp": "WhatsApp арқылы хабарласу",
            "topbar_tag": "Жаһандық жаппай көтерме сауда · OEM/ODM маманы · 1998 жылдан бастап",
            "hero_eyebrow": "✦ Қытайдың жетекші су сүзгілерін өндірушісі | NSF және ISO сертификатталған зауыт",
            "hero_title": "Өнеркәсіптік деңгейдегі суды тазарту және OEM шешімдері",
            "hero_desc": "Жоғары өнімді PP Melt Blown, CTO, GAC сүзгілерінің және RO мембраналарының жаһандық жаппай көтерме жеткізушісі. 1998 жылдан бастап біз 50-ден астам елге NSF/ISO сертификатталған OEM/ODM техникалық қолдауын көрсетеміз.",
            "hero_btn_explore": "Зауыт портфолиосын қарау", "hero_btn_quote": "Көтерме бағаны сұрау",
            "stats_years": "Жылдық тәжірибе", "stats_models": "Өнім модельдері", "stats_countries": "Қызмет көрсетілетін елдер", "stats_area": "Өндірістік аймақ",
            "about_eyebrow": "Біз туралы", "about_title": "Суды сүзу саласындағы 20 жылдан астам кемелдік",
            "about_desc": "Eco Express Water - суды тазартуға арналған сүзгі материалдары мен сүзгі жабдықтарына мамандандырылған жоғары технологиялық қоршаған ортаны қорғау кәсіпорны. 1998 жылы негізі қаланған біздің өнімдер ғылыми-зерттеу және тәжірибелік-конструкторлық жұмыстардан, өндірістен, маркетингтен техникалық қолдауға дейінгі толық циклді қамтиды. Біздің компания Қытайдың Чжэцзян провинциясы, Хайнин қаласы, Юаньхуа қалашығында орналасқан. Бізде бірінші дәрежелі техникалық сарапшылар тобы және ірі өндірістік орталық бар. Біз Малайзиядағы, Индонезиядағы және басқа да мұсылман елдеріндегі мұсылман тұтынушыларының бірегей қажеттіліктерін қанағаттандыратын халал сертификатталған су сүзгілерінің сенімді жеткізушісіміз.",
            "why_title": "Сенімді өндірістік серіктес", "why_desc": "Шикізаттан бастап соңғы тексеруге дейін әрбір өнім біздің қатаң сапаны бақылау жүйесінен өтеді.",
            "footer_brand_desc": "1998 жылдан бастап суды сүзу шешімдерінің Қытайдағы жетекші өндірушісі. Жаһандық жаппай көтерме және OEM/ODM серіктестері үшін PP Melt Blown, CTO Carbon Block, GAC және RO мембраналарына мамандандырылған.",
            "footer_rights": "Барлық құқықтар қорғалған."
        },
        "categories": {
            "Filter Cartridge": "Сүзгі картриджі", "Filter Housing": "Сүзгі корпусы", "Flat Cap Filter": "Жалпақ қақпақты сүзгі",
            "Industrial Filter": "Өнеркәсіптік сүзгі", "Inline Filter": "Инлайн сүзгі", "RO System": "RO жүйесі",
            "Water Dispenser": "Су диспенсері", "Water Purifier": "Су тазартқыш"
        },
        "boilerplate": "Қытайдың Чжэцзян провинциясы, Хайнин қаласы, Юаньхуа қалашығында орналасқан біздің 20 000 м²-ден астам ISO 9001:2015 сертификатталған кәсіпорнымызда өндірілген бұл өнім суды сүзудің толық спектрінің бөлігі болып табылады — SGS тарапынан NSF/ANSI 42 және 53 стандарттары бойынша тәуелсіз сынақтан өткен, еуропалық импорттық сәйкестік үшін CE таңбасы бар және сұраныс бойынша FDA деңгейіндегі материал декларациялары беріледі. OEM/ODM жеке брендін теңшеу мүмкіндігі бар: брендті басып шығару, тапсырыс бойынша қақпақтарды құю, түстерді таңдау және қаптау. Стандартты MOQ 1000 данадан басталады; T/T 30/70 немесе аккредитив бойынша төлем шарттарымен Шанхай/Нинбо FOB жаппай көтерме сауда. Біз қазіргі уақытта АҚШ, Германия, Ресей, Сауд Арабиясы, Малайзия, Индонезия және Бразилияны қоса алғанда 50-ден астам елге экспорттаймыз, мұсылман нарықтары үшін толық халал (JAKIM) сертификаты бар."
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

for lang in ["bn", "tl", "ta", "kk"]:
    result = translate_data(en_data, lang)
    with open(os.path.join(base_path, f"{lang}.json"), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

print("Batch 2 completed.")
