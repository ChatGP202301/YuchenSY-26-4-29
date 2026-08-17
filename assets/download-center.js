/* Yuchen Water unified download center: one accessible surface, existing secure delivery. */
(() => {
  'use strict';

  const I18N = {
    af:{title:'Aflaaie en tegniese hulpbronne',intro:'Kies een hulpbron. Die veilige versoekvorm maak in hierdie venster oop.',select:'Kies',close:'Sluit',back:'Alle hulpbronne',full:'Maak volledige bladsy oop',loading:'Veilige versoek word gelaai…',english:'Versoekvorm beskikbaar in Engels',pdf:'Beskermde PDF',manual:'Beskermde aanlyn handleiding',names:['OEM-produkkatalogus','Katalogus vir kommersiële RO-stelsels','Filterpatroonkatalogus','Gebruikershandleiding vir kommersiële RO']},
    ar:{title:'التنزيلات والموارد الفنية',intro:'اختر موردًا واحدًا. سيفتح نموذج الطلب الآمن في هذه النافذة.',select:'اختيار',close:'إغلاق',back:'كل الموارد',full:'فتح الصفحة الكاملة',loading:'جارٍ تحميل الطلب الآمن…',english:'نموذج الطلب متاح بالإنجليزية',pdf:'PDF محمي',manual:'دليل محمي عبر الإنترنت',names:['كتالوج منتجات OEM','كتالوج أنظمة RO التجارية','كتالوج خراطيش الفلاتر','دليل مستخدم RO التجاري']},
    az:{title:'Yükləmələr və texniki resurslar',intro:'Bir resurs seçin. Təhlükəsiz sorğu forması bu pəncərədə açılacaq.',select:'Seçin',close:'Bağla',back:'Bütün resurslar',full:'Tam səhifəni aç',loading:'Təhlükəsiz sorğu yüklənir…',english:'Sorğu forması ingilis dilindədir',pdf:'Qorunan PDF',manual:'Qorunan onlayn təlimat',names:['OEM məhsul kataloqu','Kommersiya RO sistemləri kataloqu','Filtr kartricləri kataloqu','Kommersiya RO istifadəçi təlimatı']},
    be:{title:'Спампоўкі і тэхнічныя матэрыялы',intro:'Выберыце адзін матэрыял. Бяспечная форма запыту адкрыецца ў гэтым акне.',select:'Выбраць',close:'Закрыць',back:'Усе матэрыялы',full:'Адкрыць поўную старонку',loading:'Загрузка бяспечнага запыту…',english:'Форма запыту даступная па-англійску',pdf:'Абаронены PDF',manual:'Абароненая анлайн-інструкцыя',names:['Каталог прадукцыі OEM','Каталог камерцыйных RO-сістэм','Каталог фільтруючых картрыджаў','Інструкцыя карыстальніка камерцыйнай RO-сістэмы']},
    bg:{title:'Изтегляния и технически ресурси',intro:'Изберете един ресурс. Защитеният формуляр ще се отвори в този прозорец.',select:'Избери',close:'Затвори',back:'Всички ресурси',full:'Отвори цялата страница',loading:'Зареждане на защитения формуляр…',english:'Формулярът е наличен на английски',pdf:'Защитен PDF',manual:'Защитено онлайн ръководство',names:['Каталог на OEM продукти','Каталог на търговски RO системи','Каталог на филтърни патрони','Ръководство за търговски RO системи']},
    bn:{title:'ডাউনলোড ও প্রযুক্তিগত রিসোর্স',intro:'একটি রিসোর্স নির্বাচন করুন। নিরাপদ অনুরোধ ফর্মটি এই উইন্ডোতেই খুলবে।',select:'নির্বাচন করুন',close:'বন্ধ করুন',back:'সব রিসোর্স',full:'সম্পূর্ণ পৃষ্ঠা খুলুন',loading:'নিরাপদ অনুরোধ লোড হচ্ছে…',english:'অনুরোধ ফর্মটি ইংরেজিতে উপলভ্য',pdf:'সুরক্ষিত PDF',manual:'সুরক্ষিত অনলাইন ম্যানুয়াল',names:['OEM পণ্য ক্যাটালগ','বাণিজ্যিক RO সিস্টেম ক্যাটালগ','ফিল্টার কার্টিজ ক্যাটালগ','বাণিজ্যিক RO ব্যবহারকারী ম্যানুয়াল']},
    bs:{title:'Preuzimanja i tehnički resursi',intro:'Odaberite jedan resurs. Sigurni obrazac otvara se u ovom prozoru.',select:'Odaberi',close:'Zatvori',back:'Svi resursi',full:'Otvori cijelu stranicu',loading:'Učitavanje sigurnog zahtjeva…',english:'Obrazac je dostupan na engleskom',pdf:'Zaštićeni PDF',manual:'Zaštićeni online priručnik',names:['Katalog OEM proizvoda','Katalog komercijalnih RO sistema','Katalog filterskih uložaka','Korisnički priručnik za komercijalni RO']},
    cnr:{title:'Preuzimanja i tehnički resursi',intro:'Izaberite jedan resurs. Sigurni obrazac otvara se u ovom prozoru.',select:'Izaberi',close:'Zatvori',back:'Svi resursi',full:'Otvori cijelu stranicu',loading:'Učitavanje sigurnog zahtjeva…',english:'Obrazac je dostupan na engleskom',pdf:'Zaštićeni PDF',manual:'Zaštićeni onlajn priručnik',names:['Katalog OEM proizvoda','Katalog komercijalnih RO sistema','Katalog filterskih uložaka','Korisnički priručnik za komercijalni RO']},
    cs:{title:'Soubory ke stažení a technické materiály',intro:'Vyberte jeden materiál. Zabezpečený formulář se otevře v tomto okně.',select:'Vybrat',close:'Zavřít',back:'Všechny materiály',full:'Otevřít celou stránku',loading:'Načítání zabezpečeného formuláře…',english:'Formulář je dostupný v angličtině',pdf:'Chráněný PDF',manual:'Chráněný online návod',names:['Katalog OEM produktů','Katalog komerčních RO systémů','Katalog filtračních vložek','Návod pro komerční RO systém']},
    da:{title:'Downloads og tekniske ressourcer',intro:'Vælg én ressource. Den sikre formular åbnes i dette vindue.',select:'Vælg',close:'Luk',back:'Alle ressourcer',full:'Åbn hele siden',loading:'Indlæser sikker formular…',english:'Formularen findes på engelsk',pdf:'Beskyttet PDF',manual:'Beskyttet onlinevejledning',names:['OEM-produktkatalog','Katalog over kommercielle RO-systemer','Katalog over filterpatroner','Brugervejledning til kommercielt RO']},
    de:{title:'Downloads und technische Unterlagen',intro:'Wählen Sie eine Unterlage aus. Das geschützte Anfrageformular öffnet sich in diesem Fenster.',select:'Auswählen',close:'Schließen',back:'Alle Unterlagen',full:'Vollständige Seite öffnen',loading:'Geschützte Anfrage wird geladen…',english:'Anfrageformular auf Englisch verfügbar',pdf:'Geschütztes PDF',manual:'Geschütztes Online-Handbuch',names:['OEM-Produktkatalog','Katalog für gewerbliche RO-Systeme','Filterpatronen-Katalog','Benutzerhandbuch für gewerbliche RO-Systeme']},
    el:{title:'Λήψεις και τεχνικό υλικό',intro:'Επιλέξτε ένα αρχείο. Η ασφαλής φόρμα αιτήματος ανοίγει σε αυτό το παράθυρο.',select:'Επιλογή',close:'Κλείσιμο',back:'Όλο το υλικό',full:'Άνοιγμα πλήρους σελίδας',loading:'Φόρτωση ασφαλούς αιτήματος…',english:'Η φόρμα είναι διαθέσιμη στα αγγλικά',pdf:'Προστατευμένο PDF',manual:'Προστατευμένο ηλεκτρονικό εγχειρίδιο',names:['Κατάλογος προϊόντων OEM','Κατάλογος επαγγελματικών συστημάτων RO','Κατάλογος φυσιγγίων φίλτρου','Εγχειρίδιο επαγγελματικού συστήματος RO']},
    en:{title:'Downloads & Technical Resources',intro:'Choose one resource. The secure request form opens in this window.',select:'Select',close:'Close',back:'All resources',full:'Open full page',loading:'Loading secure request…',english:'Request form available in English',pdf:'Protected PDF',manual:'Protected online manual',names:['OEM Product Catalog','Commercial RO Systems Catalog','Filter Cartridge Catalog','Commercial RO User Manual']},
    es:{title:'Descargas y recursos técnicos',intro:'Seleccione un recurso. El formulario seguro se abrirá en esta ventana.',select:'Seleccionar',close:'Cerrar',back:'Todos los recursos',full:'Abrir página completa',loading:'Cargando solicitud segura…',english:'Formulario disponible en inglés',pdf:'PDF protegido',manual:'Manual en línea protegido',names:['Catálogo de productos OEM','Catálogo de sistemas RO comerciales','Catálogo de cartuchos filtrantes','Manual de usuario de RO comercial']},
    et:{title:'Allalaadimised ja tehnilised materjalid',intro:'Valige üks materjal. Turvaline päringuvorm avaneb selles aknas.',select:'Vali',close:'Sulge',back:'Kõik materjalid',full:'Ava terve leht',loading:'Turvalise vormi laadimine…',english:'Päringuvorm on inglise keeles',pdf:'Kaitstud PDF',manual:'Kaitstud veebijuhend',names:['OEM-tootekataloog','Kaubanduslike RO-süsteemide kataloog','Filtrikassettide kataloog','Kaubandusliku RO kasutusjuhend']},
    fa:{title:'دانلودها و منابع فنی',intro:'یک منبع را انتخاب کنید. فرم درخواست امن در همین پنجره باز می‌شود.',select:'انتخاب',close:'بستن',back:'همه منابع',full:'باز کردن صفحه کامل',loading:'در حال بارگذاری درخواست امن…',english:'فرم درخواست به زبان انگلیسی موجود است',pdf:'PDF محافظت‌شده',manual:'راهنمای آنلاین محافظت‌شده',names:['کاتالوگ محصولات OEM','کاتالوگ سیستم‌های RO تجاری','کاتالوگ کارتریج‌های فیلتر','راهنمای کاربر RO تجاری']},
    fi:{title:'Ladattavat aineistot ja tekniset materiaalit',intro:'Valitse yksi aineisto. Suojattu pyyntölomake avautuu tähän ikkunaan.',select:'Valitse',close:'Sulje',back:'Kaikki aineistot',full:'Avaa koko sivu',loading:'Suojattua lomaketta ladataan…',english:'Pyyntölomake on saatavana englanniksi',pdf:'Suojattu PDF',manual:'Suojattu verkko-ohje',names:['OEM-tuoteluettelo','Kaupallisten RO-järjestelmien luettelo','Suodatinpatruunaluettelo','Kaupallisen RO-järjestelmän käyttöohje']},
    fr:{title:'Téléchargements et ressources techniques',intro:'Choisissez une ressource. Le formulaire sécurisé s’ouvre dans cette fenêtre.',select:'Sélectionner',close:'Fermer',back:'Toutes les ressources',full:'Ouvrir la page complète',loading:'Chargement de la demande sécurisée…',english:'Formulaire disponible en anglais',pdf:'PDF protégé',manual:'Manuel en ligne protégé',names:['Catalogue de produits OEM','Catalogue des systèmes RO commerciaux','Catalogue de cartouches filtrantes','Manuel utilisateur RO commercial']},
    ga:{title:'Íoslódálacha agus acmhainní teicniúla',intro:'Roghnaigh acmhainn amháin. Osclófar an fhoirm shlán san fhuinneog seo.',select:'Roghnaigh',close:'Dún',back:'Gach acmhainn',full:'Oscail an leathanach iomlán',loading:'Iarratas slán á lódáil…',english:'Foirm iarratais ar fáil i mBéarla',pdf:'PDF cosanta',manual:'Lámhleabhar cosanta ar líne',names:['Catalóg táirgí OEM','Catalóg córas RO tráchtála','Catalóg cartús scagaire','Lámhleabhar úsáideora RO tráchtála']},
    ha:{title:'Abubuwan saukewa da bayanan fasaha',intro:'Zaɓi abu guda. Fom ɗin neman izini mai tsaro zai buɗe a wannan taga.',select:'Zaɓa',close:'Rufe',back:'Duk bayanai',full:'Buɗe cikakken shafi',loading:'Ana loda fom mai tsaro…',english:'Ana samun fom ɗin da Turanci',pdf:'PDF mai kariya',manual:'Littafin umarni na yanar gizo mai kariya',names:['Kundin kayayyakin OEM','Kundin tsarin RO na kasuwanci','Kundin katun tacewa','Littafin amfani da RO na kasuwanci']},
    he:{title:'הורדות ומשאבים טכניים',intro:'בחרו משאב אחד. טופס הבקשה המאובטח ייפתח בחלון זה.',select:'בחירה',close:'סגירה',back:'כל המשאבים',full:'פתיחת העמוד המלא',loading:'הבקשה המאובטחת נטענת…',english:'טופס הבקשה זמין באנגלית',pdf:'PDF מוגן',manual:'מדריך מקוון מוגן',names:['קטלוג מוצרי OEM','קטלוג מערכות RO מסחריות','קטלוג מחסניות סינון','מדריך למשתמש במערכת RO מסחרית']},
    hi:{title:'डाउनलोड और तकनीकी संसाधन',intro:'एक संसाधन चुनें। सुरक्षित अनुरोध फ़ॉर्म इसी विंडो में खुलेगा।',select:'चुनें',close:'बंद करें',back:'सभी संसाधन',full:'पूरा पृष्ठ खोलें',loading:'सुरक्षित अनुरोध लोड हो रहा है…',english:'अनुरोध फ़ॉर्म अंग्रेज़ी में उपलब्ध है',pdf:'सुरक्षित PDF',manual:'सुरक्षित ऑनलाइन मैनुअल',names:['OEM उत्पाद कैटलॉग','वाणिज्यिक RO सिस्टम कैटलॉग','फ़िल्टर कार्ट्रिज कैटलॉग','वाणिज्यिक RO उपयोगकर्ता मैनुअल']},
    hr:{title:'Preuzimanja i tehnički resursi',intro:'Odaberite jedan resurs. Sigurni obrazac otvorit će se u ovom prozoru.',select:'Odaberi',close:'Zatvori',back:'Svi resursi',full:'Otvori cijelu stranicu',loading:'Učitavanje sigurnog zahtjeva…',english:'Obrazac je dostupan na engleskom',pdf:'Zaštićeni PDF',manual:'Zaštićeni mrežni priručnik',names:['Katalog OEM proizvoda','Katalog komercijalnih RO sustava','Katalog filtarskih uložaka','Korisnički priručnik za komercijalni RO']},
    hu:{title:'Letöltések és műszaki anyagok',intro:'Válasszon egy anyagot. A biztonságos igénylőlap ebben az ablakban nyílik meg.',select:'Kiválasztás',close:'Bezárás',back:'Minden anyag',full:'Teljes oldal megnyitása',loading:'Biztonságos űrlap betöltése…',english:'Az igénylőlap angol nyelven érhető el',pdf:'Védett PDF',manual:'Védett online kézikönyv',names:['OEM termékkatalógus','Kereskedelmi RO rendszerek katalógusa','Szűrőbetét-katalógus','Kereskedelmi RO felhasználói kézikönyv']},
    hy:{title:'Ներբեռնումներ և տեխնիկական նյութեր',intro:'Ընտրեք մեկ նյութ։ Անվտանգ հարցման ձևը կբացվի այս պատուհանում։',select:'Ընտրել',close:'Փակել',back:'Բոլոր նյութերը',full:'Բացել ամբողջ էջը',loading:'Անվտանգ հարցումը բեռնվում է…',english:'Հարցման ձևը հասանելի է անգլերեն',pdf:'Պաշտպանված PDF',manual:'Պաշտպանված առցանց ձեռնարկ',names:['OEM արտադրանքի կատալոգ','Առևտրային RO համակարգերի կատալոգ','Ֆիլտրի քարթրիջների կատալոգ','Առևտրային RO օգտագործողի ձեռնարկ']},
    id:{title:'Unduhan dan sumber teknis',intro:'Pilih satu sumber. Formulir permintaan aman akan terbuka di jendela ini.',select:'Pilih',close:'Tutup',back:'Semua sumber',full:'Buka halaman lengkap',loading:'Memuat permintaan aman…',english:'Formulir tersedia dalam bahasa Inggris',pdf:'PDF terlindungi',manual:'Manual daring terlindungi',names:['Katalog Produk OEM','Katalog Sistem RO Komersial','Katalog Kartrid Filter','Manual Pengguna RO Komersial']},
    it:{title:'Download e risorse tecniche',intro:'Seleziona una risorsa. Il modulo protetto si aprirà in questa finestra.',select:'Seleziona',close:'Chiudi',back:'Tutte le risorse',full:'Apri la pagina completa',loading:'Caricamento della richiesta protetta…',english:'Modulo disponibile in inglese',pdf:'PDF protetto',manual:'Manuale online protetto',names:['Catalogo prodotti OEM','Catalogo sistemi RO commerciali','Catalogo cartucce filtranti','Manuale utente RO commerciale']},
    ja:{title:'ダウンロード・技術資料',intro:'資料を1つ選択してください。安全な申請フォームがこの画面に開きます。',select:'選択',close:'閉じる',back:'すべての資料',full:'ページ全体を開く',loading:'安全な申請フォームを読み込んでいます…',english:'申請フォームは英語で提供されます',pdf:'保護されたPDF',manual:'保護されたオンラインマニュアル',names:['OEM製品カタログ','業務用ROシステムカタログ','フィルターカートリッジカタログ','業務用ROユーザーマニュアル']},
    ka:{title:'ჩამოსატვირთი და ტექნიკური მასალები',intro:'აირჩიეთ ერთი მასალა. დაცული მოთხოვნის ფორმა ამ ფანჯარაში გაიხსნება.',select:'არჩევა',close:'დახურვა',back:'ყველა მასალა',full:'სრული გვერდის გახსნა',loading:'დაცული მოთხოვნა იტვირთება…',english:'ფორმა ხელმისაწვდომია ინგლისურად',pdf:'დაცული PDF',manual:'დაცული ონლაინ სახელმძღვანელო',names:['OEM პროდუქციის კატალოგი','კომერციული RO სისტემების კატალოგი','ფილტრის კარტრიჯების კატალოგი','კომერციული RO მომხმარებლის სახელმძღვანელო']},
    kk:{title:'Жүктеулер және техникалық материалдар',intro:'Бір материалды таңдаңыз. Қауіпсіз сұрау нысаны осы терезеде ашылады.',select:'Таңдау',close:'Жабу',back:'Барлық материалдар',full:'Толық бетті ашу',loading:'Қауіпсіз сұрау жүктелуде…',english:'Сұрау нысаны ағылшын тілінде',pdf:'Қорғалған PDF',manual:'Қорғалған онлайн нұсқаулық',names:['OEM өнімдер каталогы','Коммерциялық RO жүйелер каталогы','Сүзгі картридждері каталогы','Коммерциялық RO пайдаланушы нұсқаулығы']},
    ko:{title:'다운로드 및 기술 자료',intro:'자료 하나를 선택하세요. 보안 요청 양식이 이 창에서 열립니다.',select:'선택',close:'닫기',back:'모든 자료',full:'전체 페이지 열기',loading:'보안 요청을 불러오는 중…',english:'요청 양식은 영어로 제공됩니다',pdf:'보호된 PDF',manual:'보호된 온라인 매뉴얼',names:['OEM 제품 카탈로그','상업용 RO 시스템 카탈로그','필터 카트리지 카탈로그','상업용 RO 사용자 매뉴얼']},
    ku:{title:'Daxistin û çavkaniyên teknîkî',intro:'Çavkaniyekê hilbijêrin. Forma daxwazê ya ewle di vê paceyê de vedibe.',select:'Hilbijêre',close:'Bigire',back:'Hemû çavkanî',full:'Rûpela tevahî veke',loading:'Daxwaza ewle tê barkirin…',english:'Forma daxwazê bi Îngilîzî heye',pdf:'PDF-a parastî',manual:'Rêbera serhêl a parastî',names:['Kataloga hilberên OEM','Kataloga pergalên RO yên bazirganî','Kataloga kartûşên fîlterê','Rêbera bikarhêner a RO ya bazirganî']},
    ky:{title:'Жүктөөлөр жана техникалык материалдар',intro:'Бир материалды тандаңыз. Коопсуз суроо формасы ушул терезеде ачылат.',select:'Тандоо',close:'Жабуу',back:'Бардык материалдар',full:'Толук баракты ачуу',loading:'Коопсуз форма жүктөлүүдө…',english:'Суроо формасы англис тилинде',pdf:'Корголгон PDF',manual:'Корголгон онлайн колдонмо',names:['OEM өнүмдөр каталогу','Коммерциялык RO системалар каталогу','Чыпка картридждер каталогу','Коммерциялык RO колдонмосу']},
    lb:{title:'Downloads an technesch Dokumenter',intro:'Wielt eng Ressource. De gesécherten Ufroformulaire mécht an dëser Fënster op.',select:'Auswielen',close:'Zoumaachen',back:'All Dokumenter',full:'Ganz Säit opmaachen',loading:'Geséchert Ufro gëtt gelueden…',english:'Ufroformulaire op Englesch verfügbar',pdf:'Geschützte PDF',manual:'Geschützten Online-Handbuch',names:['OEM-Produktkatalog','Katalog fir kommerziell RO-Systemer','Filterpatrounekatalog','Benotzerhandbuch fir kommerziell RO']},
    lt:{title:'Atsisiuntimai ir techninė medžiaga',intro:'Pasirinkite vieną medžiagą. Saugi užklausos forma bus atidaryta šiame lange.',select:'Pasirinkti',close:'Uždaryti',back:'Visa medžiaga',full:'Atidaryti visą puslapį',loading:'Įkeliama saugi užklausa…',english:'Užklausos forma pateikta anglų kalba',pdf:'Apsaugotas PDF',manual:'Apsaugotas internetinis vadovas',names:['OEM gaminių katalogas','Komercinių RO sistemų katalogas','Filtrų kasečių katalogas','Komercinės RO sistemos naudotojo vadovas']},
    lv:{title:'Lejupielādes un tehniskie materiāli',intro:'Izvēlieties vienu materiālu. Drošā pieprasījuma veidlapa tiks atvērta šajā logā.',select:'Izvēlēties',close:'Aizvērt',back:'Visi materiāli',full:'Atvērt pilno lapu',loading:'Notiek drošā pieprasījuma ielāde…',english:'Pieprasījuma veidlapa ir angļu valodā',pdf:'Aizsargāts PDF',manual:'Aizsargāta tiešsaistes rokasgrāmata',names:['OEM produktu katalogs','Komerciālo RO sistēmu katalogs','Filtru kasetņu katalogs','Komerciālās RO sistēmas lietotāja rokasgrāmata']},
    mk:{title:'Преземања и технички материјали',intro:'Изберете еден материјал. Безбедниот формулар ќе се отвори во овој прозорец.',select:'Избери',close:'Затвори',back:'Сите материјали',full:'Отвори ја целата страница',loading:'Се вчитува безбедниот формулар…',english:'Формуларот е достапен на англиски',pdf:'Заштитен PDF',manual:'Заштитено онлајн упатство',names:['Каталог на OEM производи','Каталог на комерцијални RO системи','Каталог на филтерски патрони','Упатство за комерцијален RO систем']},
    ms:{title:'Muat turun dan sumber teknikal',intro:'Pilih satu sumber. Borang permintaan selamat akan dibuka dalam tetingkap ini.',select:'Pilih',close:'Tutup',back:'Semua sumber',full:'Buka halaman penuh',loading:'Memuatkan permintaan selamat…',english:'Borang tersedia dalam bahasa Inggeris',pdf:'PDF terlindung',manual:'Manual dalam talian terlindung',names:['Katalog Produk OEM','Katalog Sistem RO Komersial','Katalog Kartrij Penapis','Manual Pengguna RO Komersial']},
    mt:{title:'Tniżżil u riżorsi tekniċi',intro:'Agħżel riżorsa waħda. Il-formola sigura tinfetaħ f’din it-tieqa.',select:'Agħżel',close:'Agħlaq',back:'Ir-riżorsi kollha',full:'Iftaħ il-paġna sħiħa',loading:'Qed tittella’ t-talba sigura…',english:'Il-formola hija disponibbli bl-Ingliż',pdf:'PDF protett',manual:'Manwal online protett',names:['Katalgu tal-prodotti OEM','Katalgu tas-sistemi RO kummerċjali','Katalgu tal-iskrataċ tal-filtri','Manwal tal-utent RO kummerċjali']},
    nl:{title:'Downloads en technische documentatie',intro:'Kies één document. Het beveiligde aanvraagformulier opent in dit venster.',select:'Selecteren',close:'Sluiten',back:'Alle documenten',full:'Volledige pagina openen',loading:'Beveiligde aanvraag wordt geladen…',english:'Aanvraagformulier beschikbaar in het Engels',pdf:'Beveiligde PDF',manual:'Beveiligde online handleiding',names:['OEM-productcatalogus','Catalogus voor commerciële RO-systemen','Filterpatronencatalogus','Gebruikershandleiding voor commerciële RO']},
    no:{title:'Nedlastinger og tekniske ressurser',intro:'Velg én ressurs. Det sikre skjemaet åpnes i dette vinduet.',select:'Velg',close:'Lukk',back:'Alle ressurser',full:'Åpne hele siden',loading:'Laster sikkert skjema…',english:'Skjemaet er tilgjengelig på engelsk',pdf:'Beskyttet PDF',manual:'Beskyttet nettmanual',names:['OEM-produktkatalog','Katalog for kommersielle RO-systemer','Filterpatronkatalog','Brukerhåndbok for kommersiell RO']},
    pl:{title:'Pliki do pobrania i materiały techniczne',intro:'Wybierz jeden materiał. Bezpieczny formularz otworzy się w tym oknie.',select:'Wybierz',close:'Zamknij',back:'Wszystkie materiały',full:'Otwórz pełną stronę',loading:'Wczytywanie bezpiecznego formularza…',english:'Formularz dostępny w języku angielskim',pdf:'Chroniony PDF',manual:'Chroniona instrukcja online',names:['Katalog produktów OEM','Katalog komercyjnych systemów RO','Katalog wkładów filtracyjnych','Instrukcja użytkownika komercyjnego RO']},
    pt:{title:'Downloads e recursos técnicos',intro:'Selecione um recurso. O formulário seguro será aberto nesta janela.',select:'Selecionar',close:'Fechar',back:'Todos os recursos',full:'Abrir página completa',loading:'A carregar o pedido seguro…',english:'Formulário disponível em inglês',pdf:'PDF protegido',manual:'Manual online protegido',names:['Catálogo de produtos OEM','Catálogo de sistemas RO comerciais','Catálogo de cartuchos filtrantes','Manual do utilizador de RO comercial']},
    ro:{title:'Descărcări și resurse tehnice',intro:'Selectați o resursă. Formularul securizat se va deschide în această fereastră.',select:'Selectați',close:'Închideți',back:'Toate resursele',full:'Deschide pagina completă',loading:'Se încarcă solicitarea securizată…',english:'Formular disponibil în limba engleză',pdf:'PDF protejat',manual:'Manual online protejat',names:['Catalog de produse OEM','Catalog de sisteme RO comerciale','Catalog de cartușe filtrante','Manual de utilizare RO comercial']},
    ru:{title:'Загрузки и технические материалы',intro:'Выберите один материал. Защищённая форма запроса откроется в этом окне.',select:'Выбрать',close:'Закрыть',back:'Все материалы',full:'Открыть полную страницу',loading:'Загрузка защищённой формы…',english:'Форма запроса доступна на английском',pdf:'Защищённый PDF',manual:'Защищённое онлайн-руководство',names:['Каталог OEM-продукции','Каталог коммерческих RO-систем','Каталог фильтрующих картриджей','Руководство пользователя коммерческой RO-системы']},
    sk:{title:'Súbory na stiahnutie a technické materiály',intro:'Vyberte jeden materiál. Zabezpečený formulár sa otvorí v tomto okne.',select:'Vybrať',close:'Zavrieť',back:'Všetky materiály',full:'Otvoriť celú stránku',loading:'Načítava sa zabezpečený formulár…',english:'Formulár je dostupný v angličtine',pdf:'Chránený PDF',manual:'Chránený online návod',names:['Katalóg OEM produktov','Katalóg komerčných RO systémov','Katalóg filtračných vložiek','Návod pre komerčný RO systém']},
    sl:{title:'Prenosi in tehnično gradivo',intro:'Izberite eno gradivo. Varen obrazec se odpre v tem oknu.',select:'Izberi',close:'Zapri',back:'Vsa gradiva',full:'Odpri celotno stran',loading:'Nalaganje varnega obrazca…',english:'Obrazec je na voljo v angleščini',pdf:'Zaščiten PDF',manual:'Zaščiten spletni priročnik',names:['Katalog izdelkov OEM','Katalog komercialnih sistemov RO','Katalog filtrskih vložkov','Uporabniški priročnik za komercialni RO']},
    sq:{title:'Shkarkime dhe burime teknike',intro:'Zgjidhni një burim. Formulari i sigurt do të hapet në këtë dritare.',select:'Zgjidh',close:'Mbyll',back:'Të gjitha burimet',full:'Hap faqen e plotë',loading:'Po ngarkohet kërkesa e sigurt…',english:'Formulari është në anglisht',pdf:'PDF i mbrojtur',manual:'Manual online i mbrojtur',names:['Katalogu i produkteve OEM','Katalogu i sistemeve komerciale RO','Katalogu i fishekëve të filtrit','Manuali i përdoruesit për RO komerciale']},
    sr:{title:'Преузимања и технички материјали',intro:'Изаберите један материјал. Безбедан образац ће се отворити у овом прозору.',select:'Изабери',close:'Затвори',back:'Сви материјали',full:'Отвори целу страницу',loading:'Учитавање безбедног обрасца…',english:'Образац је доступан на енглеском',pdf:'Заштићени PDF',manual:'Заштићено онлајн упутство',names:['Каталог OEM производа','Каталог комерцијалних RO система','Каталог филтерских уложака','Упутство за комерцијални RO систем']},
    'sr-me':{title:'Preuzimanja i tehnički resursi',intro:'Izaberite jedan resurs. Sigurni obrazac otvara se u ovom prozoru.',select:'Izaberi',close:'Zatvori',back:'Svi resursi',full:'Otvori cijelu stranicu',loading:'Učitavanje sigurnog zahtjeva…',english:'Obrazac je dostupan na engleskom',pdf:'Zaštićeni PDF',manual:'Zaštićeni onlajn priručnik',names:['Katalog OEM proizvoda','Katalog komercijalnih RO sistema','Katalog filterskih uložaka','Korisnički priručnik za komercijalni RO']},
    sv:{title:'Nedladdningar och tekniskt material',intro:'Välj ett material. Det säkra formuläret öppnas i det här fönstret.',select:'Välj',close:'Stäng',back:'Allt material',full:'Öppna hela sidan',loading:'Läser in säkert formulär…',english:'Formuläret finns på engelska',pdf:'Skyddad PDF',manual:'Skyddad onlinehandbok',names:['OEM-produktkatalog','Katalog för kommersiella RO-system','Filterpatronkatalog','Användarhandbok för kommersiell RO']},
    sw:{title:'Vipakuliwa na nyenzo za kiufundi',intro:'Chagua nyenzo moja. Fomu salama itafunguka katika dirisha hili.',select:'Chagua',close:'Funga',back:'Nyenzo zote',full:'Fungua ukurasa kamili',loading:'Inapakia ombi salama…',english:'Fomu inapatikana kwa Kiingereza',pdf:'PDF iliyolindwa',manual:'Mwongozo wa mtandaoni uliolindwa',names:['Katalogi ya bidhaa za OEM','Katalogi ya mifumo ya RO ya kibiashara','Katalogi ya katriji za kichujio','Mwongozo wa mtumiaji wa RO ya kibiashara']},
    ta:{title:'பதிவிறக்கங்கள் மற்றும் தொழில்நுட்ப வளங்கள்',intro:'ஒரு வளத்தைத் தேர்ந்தெடுக்கவும். பாதுகாப்பான கோரிக்கைப் படிவம் இந்தச் சாளரத்தில் திறக்கும்.',select:'தேர்ந்தெடு',close:'மூடு',back:'அனைத்து வளங்களும்',full:'முழுப் பக்கத்தைத் திற',loading:'பாதுகாப்பான கோரிக்கை ஏற்றப்படுகிறது…',english:'கோரிக்கைப் படிவம் ஆங்கிலத்தில் உள்ளது',pdf:'பாதுகாக்கப்பட்ட PDF',manual:'பாதுகாக்கப்பட்ட இணையக் கையேடு',names:['OEM தயாரிப்புப் பட்டியல்','வணிக RO அமைப்புகள் பட்டியல்','வடிகட்டி கார்ட்ரிட்ஜ் பட்டியல்','வணிக RO பயனர் கையேடு']},
    tg:{title:'Боргириҳо ва маводи техникӣ',intro:'Як маводро интихоб кунед. Шакли бехатари дархост дар ҳамин равзана кушода мешавад.',select:'Интихоб',close:'Пӯшидан',back:'Ҳамаи мавод',full:'Кушодани саҳифаи пурра',loading:'Шакли бехатар бор мешавад…',english:'Шакл ба забони англисӣ дастрас аст',pdf:'PDF-и ҳифзшуда',manual:'Дастури онлайнии ҳифзшуда',names:['Каталоги маҳсулоти OEM','Каталоги системаҳои тиҷоратии RO','Каталоги картриджҳои филтр','Дастури корбари RO-и тиҷоратӣ']},
    th:{title:'ดาวน์โหลดและเอกสารทางเทคนิค',intro:'เลือกเอกสารหนึ่งรายการ แบบฟอร์มคำขอที่ปลอดภัยจะเปิดในหน้าต่างนี้',select:'เลือก',close:'ปิด',back:'เอกสารทั้งหมด',full:'เปิดหน้าเต็ม',loading:'กำลังโหลดคำขอที่ปลอดภัย…',english:'แบบฟอร์มคำขอมีเป็นภาษาอังกฤษ',pdf:'PDF ที่มีการป้องกัน',manual:'คู่มือออนไลน์ที่มีการป้องกัน',names:['แคตตาล็อกผลิตภัณฑ์ OEM','แคตตาล็อกระบบ RO เชิงพาณิชย์','แคตตาล็อกไส้กรอง','คู่มือผู้ใช้ RO เชิงพาณิชย์']},
    tk:{title:'Ýüklemeler we tehniki maglumatlar',intro:'Bir maglumaty saýlaň. Howpsuz haýyş formasy şu penjirede açylar.',select:'Saýla',close:'Ýap',back:'Ähli maglumatlar',full:'Doly sahypany aç',loading:'Howpsuz forma ýüklenýär…',english:'Haýyş formasy iňlis dilinde',pdf:'Goralan PDF',manual:'Goralan onlaýn gollanma',names:['OEM önümler katalogy','Söwda RO ulgamlary katalogy','Filtr kartrijleri katalogy','Söwda RO ulanyjy gollanmasy']},
    tl:{title:'Mga download at teknikal na sanggunian',intro:'Pumili ng isang sanggunian. Magbubukas sa window na ito ang ligtas na request form.',select:'Piliin',close:'Isara',back:'Lahat ng sanggunian',full:'Buksan ang buong pahina',loading:'Nilo-load ang ligtas na request…',english:'Available sa English ang request form',pdf:'Protektadong PDF',manual:'Protektadong online manual',names:['Katalogo ng mga produktong OEM','Katalogo ng komersyal na RO system','Katalogo ng filter cartridge','Manwal ng gumagamit para sa komersyal na RO']},
    tr:{title:'İndirmeler ve teknik kaynaklar',intro:'Bir kaynak seçin. Güvenli talep formu bu pencerede açılır.',select:'Seç',close:'Kapat',back:'Tüm kaynaklar',full:'Tam sayfayı aç',loading:'Güvenli talep yükleniyor…',english:'Talep formu İngilizce sunulmaktadır',pdf:'Korumalı PDF',manual:'Korumalı çevrimiçi kılavuz',names:['OEM Ürün Kataloğu','Ticari RO Sistemleri Kataloğu','Filtre Kartuşu Kataloğu','Ticari RO Kullanım Kılavuzu']},
    uk:{title:'Завантаження й технічні матеріали',intro:'Виберіть один матеріал. Захищена форма запиту відкриється в цьому вікні.',select:'Вибрати',close:'Закрити',back:'Усі матеріали',full:'Відкрити повну сторінку',loading:'Завантаження захищеної форми…',english:'Форма запиту доступна англійською',pdf:'Захищений PDF',manual:'Захищений онлайн-посібник',names:['Каталог OEM-продукції','Каталог комерційних RO-систем','Каталог фільтрувальних картриджів','Посібник користувача комерційної RO-системи']},
    ur:{title:'ڈاؤن لوڈز اور تکنیکی وسائل',intro:'ایک وسیلہ منتخب کریں۔ محفوظ درخواست فارم اسی ونڈو میں کھلے گا۔',select:'منتخب کریں',close:'بند کریں',back:'تمام وسائل',full:'مکمل صفحہ کھولیں',loading:'محفوظ درخواست لوڈ ہو رہی ہے…',english:'درخواست فارم انگریزی میں دستیاب ہے',pdf:'محفوظ PDF',manual:'محفوظ آن لائن رہنما',names:['OEM مصنوعات کا کیٹلاگ','تجارتی RO سسٹمز کا کیٹلاگ','فلٹر کارٹریج کیٹلاگ','تجارتی RO صارف رہنما']},
    uz:{title:'Yuklamalar va texnik materiallar',intro:'Bitta materialni tanlang. Xavfsiz so‘rov shakli shu oynada ochiladi.',select:'Tanlash',close:'Yopish',back:'Barcha materiallar',full:'To‘liq sahifani ochish',loading:'Xavfsiz so‘rov yuklanmoqda…',english:'So‘rov shakli ingliz tilida',pdf:'Himoyalangan PDF',manual:'Himoyalangan onlayn qo‘llanma',names:['OEM mahsulotlar katalogi','Tijoriy RO tizimlari katalogi','Filtr kartrijlari katalogi','Tijoriy RO foydalanuvchi qo‘llanmasi']},
    vi:{title:'Tải xuống và tài liệu kỹ thuật',intro:'Chọn một tài liệu. Biểu mẫu yêu cầu bảo mật sẽ mở trong cửa sổ này.',select:'Chọn',close:'Đóng',back:'Tất cả tài liệu',full:'Mở trang đầy đủ',loading:'Đang tải yêu cầu bảo mật…',english:'Biểu mẫu có sẵn bằng tiếng Anh',pdf:'PDF được bảo vệ',manual:'Hướng dẫn trực tuyến được bảo vệ',names:['Danh mục sản phẩm OEM','Danh mục hệ thống RO thương mại','Danh mục lõi lọc','Hướng dẫn sử dụng RO thương mại']},
    zu:{title:'Okulandwayo nezinsiza zobuchwepheshe',intro:'Khetha insiza eyodwa. Ifomu lesicelo elivikelekile lizovuleka kuleli windi.',select:'Khetha',close:'Vala',back:'Zonke izinsiza',full:'Vula ikhasi eligcwele',loading:'Kulayishwa isicelo esivikelekile…',english:'Ifomu litholakala ngesiNgisi',pdf:'I-PDF evikelekile',manual:'Imanuwali eku-inthanethi evikelekile',names:['Ikhathalogi yemikhiqizo ye-OEM','Ikhathalogi yezinhlelo ze-RO zezentengiselwano','Ikhathalogi yama-cartridge esihlungi','Imanuwali yomsebenzisi ye-RO yezentengiselwano']}
  };

  const FILTER_LOCALES = new Set(['en', 'es', 'ar', 'fr', 'de', 'ru']);
  const MANUAL_FALLBACK_LOCALES = new Set(['be', 'cnr', 'ga', 'lb', 'mk', 'mt']);
  const RESOURCES = Object.freeze({
    oem: { slug:'sanyishui-catalog.html', image:'/assets/catalog/yuchen-water-oem-catalog-cover-480.webp', width:480, height:678, index:0, kind:'pdf' },
    commercial: { slug:'commercial-ro-water-systems-catalog.html', image:'/assets/catalog/commercial-ro-catalog-cover-480.webp', width:480, height:679, index:1, kind:'pdf' },
    filter: { slug:'filter-cartridge-catalog.html', image:'/assets/catalog/filter-cartridge-catalog-cover-480.webp', width:480, height:720, index:2, kind:'pdf' },
    manual: { slug:'commercial-ro-water-purifier-manual-request.html', image:'/assets/manuals/commercial-ro-water-purifier-manual/commercial-ro-water-purifier-manual-page-01.webp', width:1191, height:1786, index:3, kind:'manual' }
  });
  const SLUG_TO_RESOURCE = Object.fromEntries(Object.entries(RESOURCES).map(([id, item]) => [item.slug, id]));
  const rtlLocales = new Set(['ar', 'fa', 'he', 'ur']);
  let modal;
  let lastFocus;
  let activeResource = '';
  let activeSource = '';

  const safeSource = value => String(value || 'page_link').toLowerCase().replace(/[^a-z0-9_-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 80) || 'page_link';
  const pathParts = () => location.pathname.split('/').filter(Boolean);
  const locale = () => {
    const pathLocale = (pathParts()[0] || '').toLowerCase();
    if (I18N[pathLocale]) return pathLocale;
    const htmlLocale = String(document.documentElement.lang || '').toLowerCase();
    if (I18N[htmlLocale]) return htmlLocale;
    const base = htmlLocale.split('-')[0];
    return I18N[base] ? base : 'en';
  };
  const copy = () => I18N[locale()] || I18N.en;
  const resourceLocale = id => {
    const current = locale();
    if (id === 'filter' && !FILTER_LOCALES.has(current)) return 'en';
    if (id === 'manual' && MANUAL_FALLBACK_LOCALES.has(current)) return 'en';
    return current;
  };
  const resourcePath = id => `/${resourceLocale(id)}/${RESOURCES[id].slug}`;
  const currentSlug = () => pathParts().at(-1) || '';
  const currentResource = () => SLUG_TO_RESOURCE[currentSlug()] || '';
  const isLanguageLink = link => Boolean(link.closest('.lang-menu, .lang-switcher, [data-language-menu], .language-menu') || link.hasAttribute('lang'));
  const ctaSource = link => safeSource(
    link.dataset.source || link.dataset.ctaLocation || link.closest('[data-cta-location]')?.dataset.ctaLocation
      || (link.closest('header, .header') ? 'header' : '')
      || (link.closest('footer, .footer') ? 'footer' : '')
      || (link.closest('.product-actions') ? 'product_actions' : '')
      || (link.closest('.hero-actions, .catalog-hero, .sy-download-hero') ? 'hero' : '')
      || 'page_link'
  );
  const dispatch = (name, detail = {}) => document.dispatchEvent(new CustomEvent(name, { detail }));

  function resourceForLink(link) {
    if (!link || link.dataset.ywDownloadBypass === 'true' || isLanguageLink(link)) return '';
    const href = link.getAttribute('href') || '';
    if (href.startsWith('#catalog-request') && currentResource()) return currentResource();
    let url;
    try { url = new URL(href, location.href); } catch (error) { return ''; }
    if (url.origin !== location.origin) return '';
    return SLUG_TO_RESOURCE[url.pathname.split('/').pop() || ''] || '';
  }

  function annotateLinks(root = document) {
    root.querySelectorAll('a[href]').forEach(link => {
      const id = resourceForLink(link);
      if (!id) return;
      link.dataset.ywDownload = 'true';
      link.setAttribute('data-resource-id', id);
      if (!link.dataset.source) link.dataset.source = ctaSource(link);
    });
  }

  function modalMarkup() {
    const t = copy();
    return `<section class="yw-download-center" data-yw-download-center hidden aria-hidden="true">
      <button type="button" class="yw-download-center__backdrop" data-yw-close tabindex="-1" aria-label="${escapeHtml(t.close)}"></button>
      <div class="yw-download-center__dialog" role="dialog" aria-modal="true" aria-labelledby="yw-download-title" aria-describedby="yw-download-intro">
        <header class="yw-download-center__header">
          <button type="button" class="yw-download-center__back" data-yw-back hidden>${escapeHtml(t.back)}</button>
          <div class="yw-download-center__header-copy"><span class="yw-download-center__eyebrow">Yuchen Water</span><h2 class="yw-download-center__title" id="yw-download-title">${escapeHtml(t.title)}</h2><p class="yw-download-center__intro" id="yw-download-intro">${escapeHtml(t.intro)}</p></div>
          <button type="button" class="yw-download-center__close" data-yw-close aria-label="${escapeHtml(t.close)}">×</button>
        </header>
        <div class="yw-download-center__body" data-yw-resource-list><div class="yw-download-center__grid">${Object.entries(RESOURCES).map(([id, item]) => resourceCard(id, item, t)).join('')}</div></div>
        <div class="yw-download-center__resource" data-yw-resource-view hidden>
          <div class="yw-download-center__resource-meta"><strong class="yw-download-center__resource-name" data-yw-resource-name></strong><a class="yw-download-center__full-page" data-yw-full-page data-yw-download-bypass="true">${escapeHtml(t.full)}</a></div>
          <div class="yw-download-center__frame-wrap"><div class="yw-download-center__loading" data-yw-loading role="status">${escapeHtml(t.loading)}</div><iframe class="yw-download-center__frame" data-yw-frame title="${escapeHtml(t.title)}" referrerpolicy="strict-origin-when-cross-origin"></iframe></div>
        </div>
      </div>
    </section>`;
  }

  function resourceCard(id, item, t) {
    const fallback = resourceLocale(id) === 'en' && locale() !== 'en';
    return `<article class="yw-download-center__card" data-yw-card="${id}"><div class="yw-download-center__media"><img src="${item.image}" width="${item.width}" height="${item.height}" loading="lazy" alt=""></div><div class="yw-download-center__card-copy"><p class="yw-download-center__type">${escapeHtml(item.kind === 'manual' ? t.manual : t.pdf)}</p><h3>${escapeHtml(t.names[item.index])}</h3>${fallback ? `<p class="yw-download-center__availability">${escapeHtml(t.english)}</p>` : '<p class="yw-download-center__availability" aria-hidden="true">&nbsp;</p>'}<button type="button" class="yw-download-center__select" data-yw-select="${id}">${escapeHtml(t.select)}</button></div></article>`;
  }

  function escapeHtml(value) {
    return String(value || '').replace(/[&<>"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[char]));
  }

  function ensureModal() {
    if (modal) return modal;
    document.body.insertAdjacentHTML('beforeend', modalMarkup());
    modal = document.querySelector('[data-yw-download-center]');
    modal.querySelectorAll('[data-yw-close]').forEach(button => button.addEventListener('click', close));
    modal.querySelector('[data-yw-back]').addEventListener('click', showList);
    modal.querySelectorAll('[data-yw-select]').forEach(button => button.addEventListener('click', () => showResource(button.dataset.ywSelect, activeSource || 'download_center')));
    modal.addEventListener('keydown', trapFocus);
    return modal;
  }

  function open(options = {}) {
    const selected = RESOURCES[options.resourceId] ? options.resourceId : '';
    activeSource = safeSource(options.source || 'page_link');
    lastFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const center = ensureModal();
    center.hidden = false;
    center.setAttribute('aria-hidden', 'false');
    document.body.classList.add('yw-download-center-open');
    dispatch('yuchen:download-center-open', { resourceId: selected, ctaLocation: activeSource });
    if (selected) showResource(selected, activeSource);
    else showList();
    requestAnimationFrame(() => center.querySelector(selected ? '[data-yw-back]' : '[data-yw-select]')?.focus({ preventScroll: true }));
  }

  function close() {
    if (!modal || modal.hidden) return;
    modal.hidden = true;
    modal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('yw-download-center-open');
    const frame = modal.querySelector('[data-yw-frame]');
    frame.removeAttribute('src');
    activeResource = '';
    if (lastFocus && document.contains(lastFocus)) lastFocus.focus({ preventScroll: true });
  }

  function showList() {
    const center = ensureModal();
    activeResource = '';
    center.querySelector('[data-yw-resource-list]').hidden = false;
    center.querySelector('[data-yw-resource-view]').hidden = true;
    center.querySelector('[data-yw-back]').hidden = true;
    center.querySelector('[data-yw-frame]').removeAttribute('src');
    center.querySelector('[data-yw-select]')?.focus({ preventScroll: true });
  }

  function showResource(id, source) {
    if (!RESOURCES[id]) return showList();
    const center = ensureModal();
    const t = copy();
    const path = resourcePath(id);
    const url = new URL(path, location.origin);
    url.searchParams.set('yw_download_embed', '1');
    url.searchParams.set('yw_resource', id);
    url.searchParams.set('yw_source_page', location.pathname);
    url.searchParams.set('yw_source', safeSource(source));
    const currentQuery = new URLSearchParams(location.search);
    ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','product_slug','product_family'].forEach(key => {
      if (currentQuery.get(key)) url.searchParams.set(key, currentQuery.get(key).slice(0, 160));
    });
    url.hash = '';
    activeResource = id;
    activeSource = safeSource(source);
    center.querySelector('[data-yw-resource-list]').hidden = true;
    center.querySelector('[data-yw-resource-view]').hidden = false;
    center.querySelector('[data-yw-back]').hidden = false;
    center.querySelector('[data-yw-resource-name]').textContent = t.names[RESOURCES[id].index];
    const full = center.querySelector('[data-yw-full-page]');
    full.href = path;
    const loading = center.querySelector('[data-yw-loading]');
    loading.hidden = false;
    const frame = center.querySelector('[data-yw-frame]');
    frame.title = t.names[RESOURCES[id].index];
    frame.onload = () => { loading.hidden = true; };
    frame.src = url.href;
    dispatch('yuchen:download-resource-select', { resourceId: id, ctaLocation: activeSource });
  }

  function trapFocus(event) {
    if (event.key === 'Escape') {
      event.preventDefault();
      close();
      return;
    }
    if (event.key !== 'Tab') return;
    const focusable = Array.from(modal.querySelectorAll('button:not([hidden]):not([disabled]), a[href]:not([hidden]), iframe:not([hidden])')).filter(node => node.offsetParent !== null);
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable.at(-1);
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  }

  function onClick(event) {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest('a[href]');
    const id = resourceForLink(link);
    if (!id) return;
    event.preventDefault();
    open({ resourceId: id, source: ctaSource(link) });
  }

  function prepareEmbed() {
    const params = new URLSearchParams(location.search);
    if (params.get('yw_download_embed') !== '1') return false;
    document.documentElement.classList.add('yw-download-embed');
    const setup = () => {
      const form = document.querySelector('[data-sanyishui-catalog-form], [data-catalog-form], #manualRequestForm');
      if (!form) return;
      const shell = document.createElement('main');
      shell.className = 'yw-download-embed-shell';
      shell.appendChild(form);
      document.body.appendChild(shell);
      let started = false;
      form.addEventListener('input', () => {
        if (started) return;
        started = true;
        postToParent('form_start', { resourceId: params.get('yw_resource') || currentResource() });
      }, true);
      document.addEventListener('yuchen:catalog-submit-success', event => postToParent('catalog_submit_success', event.detail || {}));
      document.addEventListener('yuchen:catalog-download-complete', event => postToParent('catalog_download_complete', event.detail || {}));
      document.addEventListener('yuchen:quote-submit-success', event => {
        if (currentResource() !== 'manual') return;
        try { sessionStorage.setItem(form.dataset.accessKey || 'commercial-ro-manual-access', 'granted'); } catch (error) { /* Access can still redirect. */ }
        postToParent('manual_access_granted', { ...(event.detail || {}), redirectPath: `/${resourceLocale('manual')}/commercial-ro-water-purifier-manual.html` });
      });
    };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup, { once:true });
    else setup();
    return true;
  }

  function postToParent(type, detail) {
    if (window.parent === window) return;
    window.parent.postMessage({ source:'yuchen-download-center', type, detail:{ ...detail, resourceId: detail.resourceId || new URLSearchParams(location.search).get('yw_resource') || currentResource(), ctaLocation: safeSource(new URLSearchParams(location.search).get('yw_source') || 'download_center') } }, location.origin);
  }

  function onMessage(event) {
    if (!modal || event.origin !== location.origin || event.source !== modal.querySelector('[data-yw-frame]')?.contentWindow) return;
    const message = event.data;
    if (!message || message.source !== 'yuchen-download-center' || !message.detail) return;
    const detail = { ...message.detail, resourceId: activeResource || message.detail.resourceId, ctaLocation: activeSource || message.detail.ctaLocation };
    if (message.type === 'form_start') dispatch('yuchen:download-form-start', detail);
    if (message.type === 'catalog_submit_success') dispatch('yuchen:catalog-submit-success', detail);
    if (message.type === 'catalog_download_complete') dispatch('yuchen:catalog-download-complete', detail);
    if (message.type === 'manual_access_granted') {
      dispatch('yuchen:manual-access-granted', detail);
      if (detail.redirectPath) window.setTimeout(() => { location.href = detail.redirectPath; }, 700);
    }
  }

  const RECEIPT_KEY = 'yuchen_pending_download_receipts_v1';
  const readReceipts = () => { try { return JSON.parse(localStorage.getItem(RECEIPT_KEY) || '[]'); } catch (error) { return []; } };
  const writeReceipts = rows => { try { localStorage.setItem(RECEIPT_KEY, JSON.stringify(rows.slice(-10))); } catch (error) { /* Server delivery remains authoritative. */ } };
  async function sendReceipt(entry, attempt = 0) {
    try {
      const response = await fetch(`${entry.apiBase}/v1/catalog/download-events`, { method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify(entry.payload), cache:'no-store', keepalive:true });
      if (!response.ok) throw new Error('receipt_rejected');
      writeReceipts(readReceipts().filter(row => row.id !== entry.id));
      return true;
    } catch (error) {
      if (attempt < 2) {
        window.setTimeout(() => sendReceipt(entry, attempt + 1), [1500, 5000][attempt]);
      } else {
        const pending = readReceipts().filter(row => row.id !== entry.id);
        pending.push(entry);
        writeReceipts(pending);
      }
      return false;
    }
  }
  function reportReceipt({ apiBase, payload }) {
    if (!apiBase || !payload?.submissionId || !payload?.receipt) return Promise.resolve(false);
    return sendReceipt({ id:`${payload.submissionId}:${payload.catalogId || ''}`, apiBase, payload }, 0);
  }
  function flushReceipts() { readReceipts().forEach(entry => sendReceipt(entry, 0)); }

  if (prepareEmbed()) {
    window.YuchenDownloadReceipts = Object.freeze({ report: reportReceipt, flush: flushReceipts });
    flushReceipts();
    return;
  }

  annotateLinks();
  document.addEventListener('click', onClick, true);
  window.addEventListener('message', onMessage);
  document.addEventListener('yuchen:quote-submit-success', event => {
    if (currentResource() !== 'manual') return;
    const form = document.querySelector('#manualRequestForm');
    try { sessionStorage.setItem(form?.dataset.accessKey || 'commercial-ro-manual-access', 'granted'); } catch (error) { /* Redirect remains available. */ }
    dispatch('yuchen:manual-access-granted', { ...(event.detail || {}), resourceId:'manual', ctaLocation:'manual_request_page' });
    if (form?.dataset.successRedirect) window.setTimeout(() => { location.href = form.dataset.successRedirect; }, 700);
  });
  window.YUCHEN_DOWNLOAD_CENTER = Object.freeze({ open, close });
  window.YuchenDownloadReceipts = Object.freeze({ report: reportReceipt, flush: flushReceipts });
  flushReceipts();
})();
