#!/usr/bin/env python3
"""Fix visible mixed-English copy in priority language pages.

This script intentionally keeps the layout untouched. It replaces product intro
paragraphs, product-card blurbs and product FAQ blocks in selected language
folders where earlier static generation left English template text visible.
"""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANGS = ["ru", "es", "de", "fr", "vi", "ja", "uz", "kk", "ky"]


COPY = {
    "ru": {
        "intro": "{name} поставляется Yuchen Water для B2B-дистрибьюторов, импортеров и OEM/ODM брендов. Конфигурация подбирается по размеру, материалу, микронности, расходу, рабочему давлению и условиям применения. Поддерживаются собственная торговая марка, печать этикеток, экспортная упаковка и документы качества по запросу.",
        "card": "{name} для оптовых проектов водоочистки: параметры, упаковка и маркировка могут быть согласованы под OEM/ODM заказ, а качество контролируется перед экспортной поставкой.",
        "quality": "Документы ISO 9001, CE, SGS и Halal, а также испытания по требованиям NSF/ANSI 42, 53 и 58 для выбранных изделий предоставляются по запросу.",
        "faq_title": "Частые вопросы для B2B покупателей",
        "q": [
            ("Какая информация нужна для расчета цены?", "Укажите модель продукта, количество, размер или производительность, требования к логотипу и упаковке, страну назначения и порт прибытия. Это помогает инженеру быстро подтвердить OEM/ODM конфигурацию."),
            ("Можно ли заказать OEM/ODM брендирование?", "Да. Yuchen Water поддерживает печать логотипа, этикетки фильтра, цвет корпуса, инструкцию, коробку и экспортную маркировку по требованиям дистрибьютора."),
            ("Какой MOQ для заказа?", "MOQ зависит от продукта и степени кастомизации. Для стандартных фильтров возможны пробные партии, а для индивидуальной печати, цвета или формы количество подтверждается по спецификации."),
            ("Какие документы качества доступны?", "Выбранные продукты могут поставляться или тестироваться согласно требованиям NSF/ANSI 42, 53 и 58. Документы ISO 9001, CE, SGS и Halal предоставляются по запросу."),
            ("Какой срок поставки?", "Стандартные образцы и складские позиции обычно готовятся быстрее. OEM печать обычно занимает около 20-25 дней после утверждения макета, а сложные системы и оборудование около 30-45 дней."),
            ("Какие условия доставки поддерживаются?", "Доступны FOB Shanghai/Ningbo, а также CIF, CFR и DDP по согласованию. Экспортная упаковка подбирается по типу продукта и маршруту доставки."),
        ],
        "cta": {"View Product Catalog": "Каталог продукции", "Send Inquiry": "Отправить запрос", "Contact Engineer": "Связаться с инженером", "Request OEM Quote": "Запросить OEM цену"},
    },
    "es": {
        "intro": "{name} se suministra por Yuchen Water para distribuidores B2B, importadores y marcas OEM/ODM. La configuración puede ajustarse por tamaño, material, micraje, caudal, presión de trabajo y aplicación. Se admiten marca privada, etiqueta del filtro, embalaje de exportación y documentos de calidad bajo solicitud.",
        "card": "{name} para proyectos mayoristas de filtración de agua, con especificación, embalaje y marca adaptables a pedidos OEM/ODM y control de calidad antes del envío.",
        "quality": "Los documentos ISO 9001, CE, SGS y relacionados con Halal, así como ensayos según NSF/ANSI 42, 53 y 58 para productos seleccionados, están disponibles bajo solicitud.",
        "faq_title": "Preguntas frecuentes para compradores B2B",
        "q": [
            ("¿Qué información se necesita para cotizar?", "Indique modelo, cantidad, tamaño o capacidad, requisitos de logotipo y embalaje, país de destino y puerto. Así el ingeniero puede confirmar rápidamente la configuración OEM/ODM."),
            ("¿Pueden hacer marca OEM/ODM?", "Sí. Yuchen Water ofrece impresión de logotipo, etiqueta del filtro, color del producto, manual, caja y marcas de exportación según la solicitud del distribuidor."),
            ("¿Cuál es el MOQ?", "El MOQ depende del producto y del nivel de personalización. Para filtros estándar se pueden revisar pedidos de prueba; para impresión, color o molde personalizado se confirma según especificación."),
            ("¿Qué documentos de calidad ofrecen?", "Algunos productos pueden suministrarse o ensayarse conforme a NSF/ANSI 42, 53 y 58. Documentos ISO 9001, CE, SGS y relacionados con Halal disponibles bajo solicitud."),
            ("¿Cuál es el plazo de entrega?", "Las muestras y productos estándar suelen prepararse más rápido. La impresión OEM suele requerir 20-25 días tras aprobar el diseño; equipos y sistemas complejos, 30-45 días."),
            ("¿Qué términos de envío aceptan?", "FOB Shanghai/Ningbo está disponible; CIF, CFR y DDP se pueden discutir. El embalaje de exportación se ajusta al producto y a la ruta logística."),
        ],
        "cta": {"View Product Catalog": "Catálogo de productos", "Send Inquiry": "Enviar consulta", "Contact Engineer": "Contactar ingeniero", "Request OEM Quote": "Solicitar cotización OEM"},
    },
    "de": {
        "intro": "{name} wird von Yuchen Water für B2B-Händler, Importeure und OEM/ODM-Marken geliefert. Die Ausführung wird nach Größe, Material, Mikronrate, Durchfluss, Arbeitsdruck und Anwendung abgestimmt. Eigenmarke, Filteretikett, Exportverpackung und Qualitätsunterlagen sind auf Anfrage verfügbar.",
        "card": "{name} für Großhandelsprojekte in der Wasserfiltration, mit anpassbarer Spezifikation, Verpackung und Markenkennzeichnung für OEM/ODM-Aufträge sowie Qualitätskontrolle vor dem Export.",
        "quality": "ISO 9001, CE, SGS und Halal-bezogene Unterlagen sowie Prüfungen nach NSF/ANSI 42, 53 und 58 für ausgewählte Produkte sind auf Anfrage verfügbar.",
        "faq_title": "Häufige Fragen von B2B-Käufern",
        "q": [
            ("Welche Angaben werden für ein Angebot benötigt?", "Bitte nennen Sie Modell, Menge, Größe oder Leistung, Logo- und Verpackungsanforderungen, Zielland und Hafen. So kann der Ingenieur die OEM/ODM-Konfiguration schnell bestätigen."),
            ("Ist OEM/ODM-Branding möglich?", "Ja. Yuchen Water unterstützt Logodruck, Filteretiketten, Gehäusefarbe, Anleitung, Karton und Exportmarkierungen nach Vorgabe des Distributors."),
            ("Wie hoch ist die MOQ?", "Die MOQ hängt vom Produkt und der Anpassung ab. Für Standardfilter sind Testbestellungen möglich; bei Druck, Farbe oder eigenem Werkzeug wird die Menge nach Spezifikation bestätigt."),
            ("Welche Qualitätsdokumente sind verfügbar?", "Ausgewählte Produkte können nach NSF/ANSI 42, 53 und 58 geliefert oder geprüft werden. ISO 9001, CE, SGS und Halal-bezogene Unterlagen sind auf Anfrage verfügbar."),
            ("Welche Lieferzeit ist realistisch?", "Muster und Standardware sind meist schneller verfügbar. OEM-Druck benötigt in der Regel 20-25 Tage nach Freigabe der Druckdaten; komplexe Systeme und Geräte etwa 30-45 Tage."),
            ("Welche Versandbedingungen bieten Sie an?", "FOB Shanghai/Ningbo ist verfügbar; CIF, CFR und DDP können besprochen werden. Die Exportverpackung wird an Produkt und Transportweg angepasst."),
        ],
        "cta": {"View Product Catalog": "Produktkatalog", "Send Inquiry": "Anfrage senden", "Contact Engineer": "Ingenieur kontaktieren", "Request OEM Quote": "OEM-Angebot anfordern"},
    },
    "fr": {
        "intro": "{name} est fourni par Yuchen Water pour les distributeurs B2B, importateurs et marques OEM/ODM. La configuration peut être adaptée selon la taille, le matériau, le seuil de filtration, le débit, la pression de service et l'application. Marque privée, étiquette de filtre, emballage export et documents qualité sont disponibles sur demande.",
        "card": "{name} pour projets de filtration d'eau en gros, avec spécifications, emballage et marquage personnalisables pour les commandes OEM/ODM et contrôle qualité avant exportation.",
        "quality": "Les documents ISO 9001, CE, SGS et liés au Halal, ainsi que les essais selon NSF/ANSI 42, 53 et 58 pour certains produits, sont disponibles sur demande.",
        "faq_title": "Questions fréquentes des acheteurs B2B",
        "q": [
            ("Quelles informations fournir pour un devis ?", "Indiquez le modèle, la quantité, la taille ou capacité, les exigences de logo et d'emballage, le pays de destination et le port. L'ingénieur pourra confirmer rapidement la configuration OEM/ODM."),
            ("Proposez-vous le branding OEM/ODM ?", "Oui. Yuchen Water prend en charge l'impression du logo, l'étiquette du filtre, la couleur du produit, le manuel, le carton et les marquages export selon la demande du distributeur."),
            ("Quel est le MOQ ?", "Le MOQ dépend du produit et du niveau de personnalisation. Les commandes d'essai peuvent être étudiées pour les filtres standard; l'impression, la couleur ou le moule personnalisé sont confirmés selon la spécification."),
            ("Quels documents qualité sont disponibles ?", "Certains produits peuvent être fournis ou testés selon les exigences NSF/ANSI 42, 53 et 58. Les documents ISO 9001, CE, SGS et liés au Halal sont disponibles sur demande."),
            ("Quel délai de production prévoir ?", "Les échantillons et produits standard sont généralement plus rapides. L'impression OEM demande environ 20-25 jours après validation du visuel; les systèmes et équipements complexes environ 30-45 jours."),
            ("Quelles conditions d'expédition proposez-vous ?", "FOB Shanghai/Ningbo est disponible; CIF, CFR et DDP peuvent être discutés. L'emballage export est choisi selon le produit et l'itinéraire logistique."),
        ],
        "cta": {"View Product Catalog": "Catalogue produits", "Send Inquiry": "Envoyer une demande", "Contact Engineer": "Contacter un ingénieur", "Request OEM Quote": "Demander un devis OEM"},
    },
    "vi": {
        "intro": "{name} được Yuchen Water cung cấp cho nhà phân phối B2B, nhà nhập khẩu và thương hiệu OEM/ODM. Cấu hình có thể điều chỉnh theo kích thước, vật liệu, cấp micron, lưu lượng, áp suất làm việc và ứng dụng. Hỗ trợ nhãn riêng, nhãn lõi lọc, bao bì xuất khẩu và hồ sơ chất lượng theo yêu cầu.",
        "card": "{name} dành cho dự án lọc nước bán buôn, có thể tùy chỉnh thông số, bao bì và nhận diện thương hiệu cho đơn hàng OEM/ODM, kèm kiểm soát chất lượng trước khi xuất khẩu.",
        "quality": "Hồ sơ ISO 9001, CE, SGS, tài liệu liên quan Halal và thử nghiệm theo NSF/ANSI 42, 53, 58 cho một số sản phẩm có thể cung cấp theo yêu cầu.",
        "faq_title": "Câu hỏi thường gặp cho khách hàng B2B",
        "q": [
            ("Cần thông tin gì để báo giá?", "Vui lòng cung cấp mẫu sản phẩm, số lượng, kích thước hoặc công suất, yêu cầu logo và bao bì, quốc gia và cảng đến. Kỹ sư sẽ xác nhận nhanh cấu hình OEM/ODM."),
            ("Có hỗ trợ thương hiệu OEM/ODM không?", "Có. Yuchen Water hỗ trợ in logo, nhãn lõi lọc, màu sản phẩm, hướng dẫn sử dụng, thùng carton và ký hiệu xuất khẩu theo yêu cầu nhà phân phối."),
            ("MOQ là bao nhiêu?", "MOQ phụ thuộc vào sản phẩm và mức độ tùy chỉnh. Đơn thử có thể xem xét cho lõi lọc tiêu chuẩn; in ấn, màu sắc hoặc khuôn riêng sẽ xác nhận theo thông số."),
            ("Có hồ sơ chất lượng nào?", "Một số sản phẩm có thể được cung cấp hoặc thử nghiệm theo NSF/ANSI 42, 53 và 58. Hồ sơ ISO 9001, CE, SGS và Halal có thể cung cấp theo yêu cầu."),
            ("Thời gian giao hàng thế nào?", "Mẫu và hàng tiêu chuẩn thường nhanh hơn. In OEM thường khoảng 20-25 ngày sau khi duyệt thiết kế; hệ thống và thiết bị phức tạp khoảng 30-45 ngày."),
            ("Điều kiện vận chuyển?", "Có FOB Shanghai/Ningbo; CIF, CFR và DDP có thể trao đổi. Bao bì xuất khẩu được chọn theo sản phẩm và tuyến vận chuyển."),
        ],
        "cta": {"View Product Catalog": "Danh mục sản phẩm", "Send Inquiry": "Gửi yêu cầu", "Contact Engineer": "Liên hệ kỹ sư", "Request OEM Quote": "Yêu cầu báo giá OEM"},
    },
    "ja": {
        "intro": "{name} は、B2B販売代理店、輸入業者、OEM/ODMブランド向けに Yuchen Water が供給する製品です。サイズ、材質、ろ過精度、流量、使用圧力、用途に合わせて仕様を確認できます。プライベートラベル、フィルターラベル、輸出梱包、品質書類はご要望に応じて対応します。",
        "card": "{name} は卸売向け水処理プロジェクト用です。OEM/ODM注文に合わせて仕様、梱包、ブランド表示を調整でき、出荷前の品質確認に対応します。",
        "quality": "ISO 9001、CE、SGS、Halal関連書類、および一部製品の NSF/ANSI 42、53、58 要求に基づく試験はご要望に応じて対応可能です。",
        "faq_title": "B2Bバイヤー向けFAQ",
        "q": [
            ("見積にはどの情報が必要ですか？", "製品モデル、数量、サイズまたは能力、ロゴと梱包の要求、仕向国、到着港をお知らせください。担当エンジニアが OEM/ODM 仕様を確認します。"),
            ("OEM/ODMブランド対応は可能ですか？", "はい。Yuchen Water はロゴ印刷、フィルターラベル、製品カラー、取扱説明書、外箱、輸出マークに対応します。"),
            ("MOQはどのくらいですか？", "MOQは製品とカスタマイズ内容により異なります。標準フィルターは試作注文を相談でき、印刷、色、専用金型は仕様により確認します。"),
            ("品質書類はありますか？", "一部製品は NSF/ANSI 42、53、58 の要求に基づく供給または試験が可能です。ISO 9001、CE、SGS、Halal関連書類はご要望に応じて提供します。"),
            ("納期はどれくらいですか？", "サンプルと標準品は比較的短納期です。OEM印刷はデザイン承認後約20-25日、複雑なシステムや設備は約30-45日が目安です。"),
            ("出荷条件は何に対応しますか？", "FOB Shanghai/Ningbo に対応し、CIF、CFR、DDP も相談可能です。輸出梱包は製品と輸送ルートに合わせて選定します。"),
        ],
        "cta": {"View Product Catalog": "製品カタログ", "Send Inquiry": "問い合わせを送信", "Contact Engineer": "技術担当に相談", "Request OEM Quote": "OEM見積を依頼"},
    },
    "uz": {
        "intro": "{name} Yuchen Water tomonidan B2B distribyutorlar, importyorlar va OEM/ODM brendlari uchun yetkazib beriladi. Konfiguratsiya o‘lcham, material, mikron darajasi, oqim, ish bosimi va qo‘llanilishiga ko‘ra moslashtiriladi. Shaxsiy brend, filtr yorlig‘i, eksport qadoqlash va sifat hujjatlari so‘rov bo‘yicha qo‘llab-quvvatlanadi.",
        "card": "{name} ulgurji suv filtrlash loyihalari uchun mo‘ljallangan; spetsifikatsiya, qadoqlash va brendlash OEM/ODM buyurtmasiga moslanadi, eksportdan oldin sifat nazorati bajariladi.",
        "quality": "ISO 9001, CE, SGS va Halal bilan bog‘liq hujjatlar, shuningdek tanlangan mahsulotlar uchun NSF/ANSI 42, 53 va 58 talablari bo‘yicha sinovlar so‘rov bo‘yicha taqdim etiladi.",
        "faq_title": "B2B xaridorlar uchun savollar",
        "q": [
            ("Narx olish uchun qanday ma'lumot kerak?", "Mahsulot modeli, miqdori, o‘lcham yoki quvvat, logo va qadoqlash talablari, boradigan mamlakat va portni yuboring. Muhandis OEM/ODM konfiguratsiyasini tez tasdiqlaydi."),
            ("OEM/ODM brendlash mumkinmi?", "Ha. Yuchen Water logo bosish, filtr yorlig‘i, mahsulot rangi, qo‘llanma, karton va eksport belgilari bo‘yicha distribyutor talabini qo‘llab-quvvatlaydi."),
            ("MOQ qancha?", "MOQ mahsulot va moslashtirish darajasiga bog‘liq. Standart filtrlar uchun sinov buyurtmalari muhokama qilinadi; bosma, rang yoki maxsus qolip bo‘yicha miqdor spetsifikatsiyaga ko‘ra tasdiqlanadi."),
            ("Qanday sifat hujjatlari bor?", "Tanlangan mahsulotlar NSF/ANSI 42, 53 va 58 talablari bo‘yicha yetkazilishi yoki sinovdan o‘tkazilishi mumkin. ISO 9001, CE, SGS va Halal hujjatlari so‘rov bo‘yicha beriladi."),
            ("Yetkazib berish muddati qanday?", "Namunalar va standart mahsulotlar odatda tezroq tayyorlanadi. OEM bosma ishlari dizayn tasdig‘idan keyin taxminan 20-25 kun, murakkab tizim va uskunalar 30-45 kun atrofida."),
            ("Qaysi yetkazib berish shartlari bor?", "FOB Shanghai/Ningbo mavjud; CIF, CFR va DDP muhokama qilinadi. Eksport qadoqlash mahsulot va logistika yo‘nalishiga qarab tanlanadi."),
        ],
        "cta": {"View Product Catalog": "Mahsulot katalogi", "Send Inquiry": "So‘rov yuborish", "Contact Engineer": "Muhandis bilan bog‘lanish", "Request OEM Quote": "OEM narx so‘rash"},
    },
    "kk": {
        "intro": "{name} өнімін Yuchen Water B2B дистрибьюторларына, импорттаушыларға және OEM/ODM брендтеріне жеткізеді. Конфигурация өлшемі, материалы, микрон рейтингі, ағын көлемі, жұмыс қысымы және қолданылуына қарай бейімделеді. Жеке бренд, сүзгі жапсырмасы, экспорттық қаптама және сапа құжаттары сұраныс бойынша қолжетімді.",
        "card": "{name} көтерме су сүзу жобаларына арналған; сипаттама, қаптама және бренд белгісі OEM/ODM тапсырысына сай бейімделеді, экспорт алдында сапа бақылауы жүргізіледі.",
        "quality": "ISO 9001, CE, SGS және Halal құжаттары, сондай-ақ таңдалған өнімдер үшін NSF/ANSI 42, 53 және 58 талаптарына сәйкес сынақтар сұраныс бойынша беріледі.",
        "faq_title": "B2B сатып алушыларға арналған сұрақтар",
        "q": [
            ("Баға есептеу үшін қандай ақпарат керек?", "Өнім моделі, саны, өлшемі немесе қуаты, логотип пен қаптама талаптары, жеткізу елі және порты қажет. Инженер OEM/ODM конфигурациясын жылдам растайды."),
            ("OEM/ODM брендтеу жасайсыздар ма?", "Иә. Yuchen Water логотип басу, сүзгі жапсырмасы, өнім түсі, нұсқаулық, картон қорап және экспорт белгілерін дистрибьютор талабына сай қолдайды."),
            ("MOQ қандай?", "MOQ өнімге және бейімдеу деңгейіне байланысты. Стандартты сүзгілерге сынақ тапсырысы қаралады; баспа, түс немесе жеке қалып көлемі сипаттама бойынша расталады."),
            ("Қандай сапа құжаттары бар?", "Таңдалған өнімдер NSF/ANSI 42, 53 және 58 талаптарына сай жеткізілуі немесе сыналуы мүмкін. ISO 9001, CE, SGS және Halal құжаттары сұраныс бойынша беріледі."),
            ("Жеткізу мерзімі қандай?", "Үлгілер мен стандартты өнімдер әдетте тезірек дайындалады. OEM баспа дизайн бекітілгеннен кейін шамамен 20-25 күн, күрделі жүйелер мен жабдық 30-45 күн шамасында."),
            ("Қандай жеткізу шарттары бар?", "FOB Shanghai/Ningbo қолжетімді; CIF, CFR және DDP талқыланады. Экспорттық қаптама өнімге және логистика бағытына қарай таңдалады."),
        ],
        "cta": {"View Product Catalog": "Өнім каталогы", "Send Inquiry": "Сұрау жіберу", "Contact Engineer": "Инженермен байланысу", "Request OEM Quote": "OEM баға сұрау"},
    },
    "ky": {
        "intro": "{name} Yuchen Water тарабынан B2B дистрибьюторлор, импорттоочулар жана OEM/ODM бренддери үчүн жеткирилет. Конфигурация өлчөмү, материалы, микрон деңгээли, агымы, иш басымы жана колдонулушуна жараша ыңгайлаштырылат. Жеке бренд, чыпка этикеткасы, экспорттук таңгак жана сапат документтери суроо боюнча берилет.",
        "card": "{name} дүң суу чыпкалоо долбоорлору үчүн; спецификация, таңгак жана бренд белгилери OEM/ODM буйрутмасына ылайыкташат, экспорт алдында сапат көзөмөлү жүргүзүлөт.",
        "quality": "ISO 9001, CE, SGS жана Halal боюнча документтер, ошондой эле тандалган продукциялар үчүн NSF/ANSI 42, 53 жана 58 талаптарына ылайык сыноолор суроо боюнча берилет.",
        "faq_title": "B2B сатып алуучулар үчүн суроолор",
        "q": [
            ("Бааны эсептөө үчүн кандай маалымат керек?", "Өнүм модели, саны, өлчөмү же кубаттуулугу, логотип жана таңгак талаптары, баруучу өлкө жана порт керек. Инженер OEM/ODM конфигурациясын тез тактайт."),
            ("OEM/ODM бренддөө мүмкүнбү?", "Ооба. Yuchen Water логотип басуу, чыпка этикеткасы, өнүм түсү, нускама, картон жана экспорт белгилерин дистрибьютор талабына ылайык колдойт."),
            ("MOQ канча?", "MOQ өнүмгө жана ыңгайлаштыруу деңгээлине жараша болот. Стандарттуу чыпкалар үчүн сынамык буйрутма каралат; басма, түс же жеке калып көлөмү спецификация боюнча такталат."),
            ("Кандай сапат документтери бар?", "Тандалган өнүмдөр NSF/ANSI 42, 53 жана 58 талаптарына ылайык жеткирилиши же сыналышы мүмкүн. ISO 9001, CE, SGS жана Halal документтери суроо боюнча берилет."),
            ("Жеткирүү мөөнөтү кандай?", "Үлгүлөр жана стандарттуу продукциялар адатта тезирээк даярдалат. OEM басма дизайн бекитилгенден кийин болжол менен 20-25 күн, татаал системалар жана жабдуулар 30-45 күн."),
            ("Кандай жеткирүү шарттары бар?", "FOB Shanghai/Ningbo бар; CIF, CFR жана DDP сүйлөшүлөт. Экспорттук таңгак өнүмгө жана логистика багытына жараша тандалат."),
        ],
        "cta": {"View Product Catalog": "Өнүм каталогу", "Send Inquiry": "Суроо жөнөтүү", "Contact Engineer": "Инженер менен байланышуу", "Request OEM Quote": "OEM баа суроо"},
    },
}


EXTRA = {
    "ru": {
        "thanks": "Спасибо. Ваш запрос успешно отправлен в Yuchen Water на expresswater025@gmail.com. Наш инженер по продажам свяжется с вами как можно скорее. Вы также можете связаться с нами через WhatsApp или email.",
        "rights": "Все права защищены.",
        "privacy": "Политика конфиденциальности",
        "privacy_desc": "Политика конфиденциальности Yuchen Water для форм запросов, данных покупателей, email-доставки и контактной информации.",
        "halal": "Документы, связанные с Halal, доступны по запросу для подходящих заказов.",
    },
    "es": {
        "thanks": "Gracias. Su consulta se ha enviado correctamente a Yuchen Water en expresswater025@gmail.com. Nuestro ingeniero de ventas se pondrá en contacto con usted lo antes posible. También puede escribirnos por WhatsApp o email.",
        "rights": "Todos los derechos reservados.",
        "privacy": "Política de privacidad",
        "privacy_desc": "Política de privacidad de Yuchen Water para formularios de consulta, datos de compradores, envío por email e información de contacto.",
        "halal": "Los documentos relacionados con Halal están disponibles bajo solicitud para pedidos cualificados.",
    },
    "de": {
        "thanks": "Vielen Dank. Ihre Anfrage wurde erfolgreich an Yuchen Water unter expresswater025@gmail.com gesendet. Unser Vertriebsingenieur meldet sich so schnell wie möglich. Sie können uns auch per WhatsApp oder E-Mail kontaktieren.",
        "rights": "Alle Rechte vorbehalten.",
        "privacy": "Datenschutzerklärung",
        "privacy_desc": "Datenschutzerklärung von Yuchen Water für Anfrageformulare, Käuferdaten, E-Mail-Zustellung und Kontaktinformationen.",
        "halal": "Halal-bezogene Unterlagen sind für qualifizierte Bestellungen auf Anfrage verfügbar.",
    },
    "fr": {
        "thanks": "Merci. Votre demande a bien été envoyée à Yuchen Water à expresswater025@gmail.com. Notre ingénieur commercial vous contactera dès que possible. Vous pouvez aussi nous joindre par WhatsApp ou email.",
        "rights": "Tous droits réservés.",
        "privacy": "Politique de confidentialité",
        "privacy_desc": "Politique de confidentialité de Yuchen Water pour les formulaires de demande, les données acheteurs, l'envoi par email et les coordonnées.",
        "halal": "Les documents liés au Halal sont disponibles sur demande pour les commandes qualifiées.",
    },
    "vi": {
        "thanks": "Cảm ơn. Yêu cầu của bạn đã được gửi thành công đến Yuchen Water tại expresswater025@gmail.com. Kỹ sư kinh doanh của chúng tôi sẽ liên hệ sớm nhất có thể. Bạn cũng có thể liên hệ qua WhatsApp hoặc email.",
        "rights": "Đã bảo lưu mọi quyền.",
        "privacy": "Chính sách bảo mật",
        "privacy_desc": "Chính sách bảo mật của Yuchen Water cho biểu mẫu yêu cầu, dữ liệu người mua, gửi email và thông tin liên hệ.",
        "halal": "Tài liệu liên quan Halal có thể cung cấp theo yêu cầu cho đơn hàng phù hợp.",
    },
    "ja": {
        "thanks": "ありがとうございます。お問い合わせは Yuchen Water（expresswater025@gmail.com）へ正常に送信されました。営業エンジニアができるだけ早くご連絡します。WhatsApp またはメールでもお問い合わせいただけます。",
        "rights": "すべての権利を保有します。",
        "privacy": "プライバシーポリシー",
        "privacy_desc": "Yuchen Water の問い合わせフォーム、購入者データ、メール送信、連絡先情報に関するプライバシーポリシー。",
        "halal": "対象注文については、Halal 関連書類をリクエストに応じて提供できます。",
    },
    "uz": {
        "thanks": "Rahmat. So‘rovingiz Yuchen Water kompaniyasiga expresswater025@gmail.com manzili orqali muvaffaqiyatli yuborildi. Savdo muhandisimiz imkon qadar tez bog‘lanadi. WhatsApp yoki email orqali ham murojaat qilishingiz mumkin.",
        "rights": "Barcha huquqlar himoyalangan.",
        "privacy": "Maxfiylik siyosati",
        "privacy_desc": "Yuchen Water so‘rov shakllari, xaridor ma'lumotlari, email yuborish va aloqa ma'lumotlari bo‘yicha maxfiylik siyosati.",
        "halal": "Halal bilan bog‘liq hujjatlar mos buyurtmalar uchun so‘rov bo‘yicha taqdim etiladi.",
    },
    "kk": {
        "thanks": "Рақмет. Сұрауыңыз Yuchen Water компаниясына expresswater025@gmail.com арқылы сәтті жіберілді. Сату инженері мүмкіндігінше тез хабарласады. WhatsApp немесе email арқылы да байланыса аласыз.",
        "rights": "Барлық құқықтар қорғалған.",
        "privacy": "Құпиялылық саясаты",
        "privacy_desc": "Yuchen Water сұрау формалары, сатып алушы деректері, email жеткізу және байланыс ақпараты бойынша құпиялылық саясаты.",
        "halal": "Halal бойынша құжаттар тиісті тапсырыстар үшін сұраныс бойынша беріледі.",
    },
    "ky": {
        "thanks": "Рахмат. Сурооңуз Yuchen Water компаниясына expresswater025@gmail.com дареги аркылуу ийгиликтүү жөнөтүлдү. Сатуу инженери мүмкүн болушунча тез байланышат. WhatsApp же email аркылуу да кайрыла аласыз.",
        "rights": "Бардык укуктар корголгон.",
        "privacy": "Купуялык саясаты",
        "privacy_desc": "Yuchen Water суроо формалары, сатып алуучу маалыматтары, email жеткирүү жана байланыш маалыматы боюнча купуялык саясаты.",
        "halal": "Halal боюнча документтер ылайыктуу буйрутмалар үчүн суроо боюнча берилет.",
    },
}

QUALITY_LABEL = {
    "ru": "Документы качества",
    "es": "Documentos de calidad",
    "de": "Qualitätsunterlagen",
    "fr": "Documents qualité",
    "vi": "Hồ sơ chất lượng",
    "ja": "品質書類",
    "uz": "Sifat hujjatlari",
    "kk": "Сапа құжаттары",
    "ky": "Сапат документтери",
}

FOOD_GRADE_DECLARATIONS = {
    "ru": "декларации материалов пищевого класса",
    "es": "declaraciones de materiales aptos para contacto alimentario",
    "de": "Konformitätserklärungen für lebensmittelechte Materialien",
    "fr": "déclarations de matériaux aptes au contact alimentaire",
    "vi": "tuyên bố vật liệu cấp thực phẩm",
    "ja": "食品接触材料に関する宣言",
    "uz": "oziq-ovqat bilan aloqa qiluvchi materiallar deklaratsiyalari",
    "kk": "тағамдық материалдар декларациялары",
    "ky": "тамак-ашка ылайыктуу материалдар декларациялары",
}

PRODUCT_NAME_OVERRIDES = {
    "ru": {
        "product-alkaline-inline.html": "Щелочной линейный фильтрующий картридж",
        "product-cto-cartridge.html": "Фильтрующий картридж CTO с угольным блоком",
        "product-pp-melt-blown.html": "Осадочный фильтрующий картридж PP расплавного выдува",
        "product-quick-connect-inline.html": "Линейный фильтр с быстросъемным соединением",
        "product-uf-inline-filter.html": "Линейный UF фильтрующий картридж",
    },
    "es": {
        "product-alkaline-inline.html": "Cartucho filtrante alcalino en línea",
        "product-cto-cartridge.html": "Cartucho filtrante CTO de bloque de carbón",
        "product-pp-melt-blown.html": "Cartucho sedimentario PP soplado por fusión",
        "product-quick-connect-inline.html": "Filtro en línea de conexión rápida",
        "product-uf-inline-filter.html": "Cartucho filtrante UF en línea",
    },
    "de": {
        "product-alkaline-inline.html": "Alkalische Filterkartusche für Leitungsinstallation",
        "product-cto-cartridge.html": "CTO-Kohlenstoffblock-Filterkartusche",
        "product-pp-melt-blown.html": "PP-Sedimentfilterkartusche aus schmelzgeblasenem Vlies",
        "product-quick-connect-inline.html": "Wasserfilter mit Schnellanschluss",
        "product-uf-inline-filter.html": "UF-Filterkartusche für Leitungsinstallation",
    },
    "fr": {
        "product-alkaline-inline.html": "Cartouche filtrante alcaline en ligne",
        "product-cto-cartridge.html": "Cartouche filtrante CTO en bloc de charbon",
        "product-pp-melt-blown.html": "Cartouche sédiments PP soufflée par fusion",
        "product-quick-connect-inline.html": "Filtre en ligne à raccord rapide",
        "product-uf-inline-filter.html": "Cartouche filtrante UF en ligne",
    },
}

LOCALIZED_ADDRESS = {
    "ru": "Юаньхуа, г. Хайнин, провинция Чжэцзян, Китай",
    "es": "Yuanhua, Haining, provincia de Zhejiang, China",
    "de": "Yuanhua, Haining, Provinz Zhejiang, China",
    "fr": "Yuanhua, Haining, province du Zhejiang, Chine",
    "vi": "Yuanhua, Haining, tỉnh Chiết Giang, Trung Quốc",
    "ja": "中国浙江省海寧市袁花鎮",
    "uz": "Yuanhua shaharchasi, Haining shahri, Zhejiang viloyati, Xitoy",
    "kk": "Юаньхуа кенті, Хайнин қаласы, Чжэцзян провинциясы, Қытай",
    "ky": "Юаньхуа шаарчасы, Хайнин шаары, Чжэцзян провинциясы, Кытай",
}

VISIBLE_LABELS = {
    "ru": {
        "Big Blue Water Filter": "Фильтр Big Blue",
        "PP Melt Blown Filter": "PP фильтр расплавного выдува",
        "PP Melt Blown Line": "Линия PP фильтров расплавного выдува",
        "Household RO Machine": "Бытовая RO-система",
        "RO Seawater Machine": "RO машина для опреснения морской воды",
        "Factory & ISO 9001": "Завод и ISO 9001",
        "Product Big Blue 3Stage": "Трехступенчатый фильтр Big Blue",
    },
    "es": {
        "Big Blue Water Filter": "Filtro Big Blue",
        "PP Melt Blown Filter": "Filtro PP soplado por fusión",
        "PP Melt Blown Line": "Línea PP soplada por fusión",
        "Household RO Machine": "Sistema RO doméstico",
        "RO Seawater Machine": "Máquina RO para agua de mar",
        "Factory & ISO 9001": "Fábrica e ISO 9001",
    },
    "de": {
        "Big Blue Water Filter": "Big-Blue-Wasserfilter",
        "PP Melt Blown Filter": "PP-Filter aus schmelzgeblasenem Vlies",
        "PP Melt Blown Line": "PP-Schmelzblaslinie",
        "Household RO Machine": "RO-System für Haushalt",
        "RO Seawater Machine": "RO-Anlage für Meerwasser",
        "Factory & ISO 9001": "Werk und ISO 9001",
    },
    "fr": {
        "Big Blue Water Filter": "Filtre Big Blue",
        "PP Melt Blown Filter": "Filtre PP soufflé par fusion",
        "PP Melt Blown Line": "Ligne PP soufflée par fusion",
        "Household RO Machine": "Système RO domestique",
        "RO Seawater Machine": "Machine RO pour eau de mer",
        "Factory & ISO 9001": "Usine et ISO 9001",
    },
    "vi": {
        "Big Blue Water Filter": "Bộ lọc nước Big Blue",
        "PP Melt Blown Filter": "Lõi lọc PP thổi nóng chảy",
        "PP Melt Blown Line": "Dây chuyền PP thổi nóng chảy",
        "Household RO Machine": "Máy RO gia đình",
        "RO Seawater Machine": "Máy RO khử mặn nước biển",
        "Factory & ISO 9001": "Nhà máy và ISO 9001",
    },
    "ja": {
        "Big Blue Water Filter": "Big Blue浄水フィルター",
        "PP Melt Blown Filter": "PPメルトブローンフィルター",
        "PP Melt Blown Line": "PPメルトブローン生産ライン",
        "Household RO Machine": "家庭用RO浄水器",
        "RO Seawater Machine": "海水淡水化RO装置",
        "Factory & ISO 9001": "工場とISO 9001",
    },
    "uz": {
        "Big Blue Water Filter": "Big Blue suv filtri",
        "PP Melt Blown Filter": "PP eritma-purkash filtri",
        "PP Melt Blown Line": "PP eritma-purkash ishlab chiqarish liniyasi",
        "PP melt-blown ishlab chiqarish liniyasi": "PP eritma-purkash ishlab chiqarish liniyasi",
        "Household RO Machine": "Uy uchun RO suv tozalagich",
        "RO Seawater Machine": "Dengiz suvi uchun RO uskunasi",
        "Factory & ISO 9001": "Zavod va ISO 9001",
        "27+ Years Producing Premium Water Filtration": "27+ yillik yuqori sifatli suv filtrlash mahsulotlari ishlab chiqarish",
        "How We Use The Information": "Ma'lumotlardan qanday foydalanamiz",
        "R&D & Testing": "Tadqiqot va sinov",
        "Container-Ready": "Konteynerga tayyor",
        "1×20'GP ≈ 80,000 cartridges. FOB SHA/NGB · CIF · DDP terms.": "1×20'GP konteyneri uchun taxminan 80 000 kartrij. FOB Shanghai/Ningbo, CIF va DDP shartlari muhokama qilinadi.",
        "Tooling & R&D": "Qolip va tadqiqot",
        "injection-mold tooling — refundable on volume orders.": "Inyeksion qolip xarajati katta hajmli buyurtmalarda kelishuv asosida qaytarilishi mumkin.",
        "Built for Global B2B Distributors": "Global B2B distribyutorlar uchun ishlab chiqilgan",
        "Certifications & Compliance": "Sertifikatlar va muvofiqlik",
        "Globally Recognized Quality Standards": "Xalqaro tan olingan sifat standartlari",
        "Aesthetic, health and reverse osmosis water treatment.": "Estetik, sog‘liq va teskari osmos suv tozalash talablariga oid sinovlar.",
        "Quality management documents available upon request.": "Sifat menejmenti hujjatlari so‘rov bo‘yicha taqdim etiladi.",
        "CE Marking": "CE belgisi",
        "European import compliance.": "Yevropa import talablari uchun muvofiqlik.",
        "SGS Test Reports": "SGS sinov hisobotlari",
        "Heavy-metal & VOC removal validated.": "Og‘ir metallar va VOC kamaytirish ko‘rsatkichlari tekshiruvdan o‘tgan.",
        "Compulsory certification for dispensers.": "Dispenserlar uchun majburiy sertifikatlash hujjatlari.",
        "PP melt blown filter cartridge production line": "PP eritma-purkash filtr kartriji ishlab chiqarish liniyasi",
        "CTO carbon block filter production line with coconut shell activated carbon media": "Kokos qobig‘i faollashtirilgan ko‘mirli CTO karbon blok filtri ishlab chiqarish liniyasi",
        "Inline water filter cartridge quick connect assembly line": "Tez ulanuvchi liniyali suv filtri kartriji yig‘ish liniyasi",
        "Water filter pressure and leakage quality control test before shipment": "Jo‘natishdan oldingi suv filtri bosim va sizib chiqish QC sinovi",
        "Gradient-density sediment cartridge production.": "Gradient zichlikdagi cho‘kindi kartrijlarini ishlab chiqarish.",
        "Coconut shell CTO carbon block processing.": "Kokos qobig‘i asosidagi CTO karbon bloklarini qayta ishlash.",
        "Inline filtr Assembly": "Liniyali filtr yig‘ish",
        "T33, mineral and quick-connect filter assembly.": "T33, mineral va tez ulanuvchi filtrlarni yig‘ish.",
        "Dimension, flow, pressure drop and assembly inspection": "O‘lcham, oqim, bosim yo‘qotilishi va yig‘ishni tekshirish",
        "Appearance, leakage, labeling, carton and random sampling": "Tashqi ko‘rinish, sizib chiqish, yorliq, karton va tasodifiy namuna tekshiruvi",
    },
    "kk": {
        "Big Blue Water Filter": "Big Blue су сүзгісі",
        "PP Melt Blown Filter": "PP балқыма үрлеу сүзгісі",
        "PP Melt Blown Line": "PP балқыма үрлеу өндіріс желісі",
        "Household RO Machine": "Тұрмыстық RO су тазартқыш",
        "RO Seawater Machine": "Теңіз суын тұщыландыратын RO жабдығы",
        "Factory & ISO 9001": "Зауыт және ISO 9001",
        "27+ Years Producing Premium Water Filtration": "27 жылдан астам жоғары сапалы су сүзу өнімдерін өндіру",
        "R&D & Testing": "Зерттеу және сынақ",
        "Container-Ready": "Контейнерге дайын",
        "1×20'GP ≈ 80,000 cartridges. FOB SHA/NGB · CIF · DDP terms.": "1×20'GP контейнеріне шамамен 80 000 картридж. FOB Shanghai/Ningbo, CIF және DDP шарттары талқыланады.",
        "Tooling & R&D": "Қалып және зерттеу",
        "injection-mold tooling — refundable on volume orders.": "Инъекциялық қалып шығыны көлемді тапсырыстарда келісім бойынша қайтарылуы мүмкін.",
        "Built for Global B2B Distributors": "Жаһандық B2B дистрибьюторларына арналған",
        "Certifications & Compliance": "Сертификаттар және сәйкестік",
        "Globally Recognized Quality Standards": "Халықаралық танылған сапа стандарттары",
        "Aesthetic, health and reverse osmosis water treatment.": "Эстетикалық, денсаулық және кері осмос су тазарту талаптарына қатысты сынақтар.",
        "Quality management documents available upon request.": "Сапа менеджменті құжаттары сұраныс бойынша беріледі.",
        "CE Marking": "CE белгісі",
        "European import compliance.": "Еуропалық импорт талаптарына сәйкестік.",
        "SGS Test Reports": "SGS сынақ есептері",
        "Heavy-metal & VOC removal validated.": "Ауыр металдар мен VOC азайту көрсеткіштері тексерілген.",
        "Compulsory certification for dispensers.": "Диспенсерлер үшін міндетті сертификаттау құжаттары.",
    },
    "ky": {
        "Big Blue Water Filter": "Big Blue суу сүзгүсү",
        "PP Melt Blown Filter": "PP эритип үйлөө сүзгүсү",
        "PP Melt Blown Line": "PP эритип үйлөө өндүрүш линиясы",
        "Household RO Machine": "Үй-тиричилик RO суу тазалагычы",
        "RO Seawater Machine": "Деңиз суусун тузсуздандыруучу RO жабдыгы",
        "Factory & ISO 9001": "Завод жана ISO 9001",
        "27+ Years Producing Premium Water Filtration": "27 жылдан ашык жогорку сапаттагы суу чыпкалоо продукциясын өндүрүү",
        "OEM/ODM Manufacturing OEM/ODM": "OEM/ODM өндүрүшү",
        "R&D & Testing": "Изилдөө жана сыноо",
        "Container-Ready": "Контейнерге даяр",
        "1×20'GP ≈ 80,000 cartridges. FOB SHA/NGB · CIF · DDP terms.": "1×20'GP контейнерине болжол менен 80 000 картридж. FOB Shanghai/Ningbo, CIF жана DDP шарттары сүйлөшүлөт.",
        "Tooling & R&D": "Калып жана изилдөө",
        "injection-mold tooling — refundable on volume orders.": "Инжекциялык калып чыгымы көлөмдүү буйрутмаларда келишим боюнча кайтарылышы мүмкүн.",
        "Built for Global B2B Distributors": "Дүйнөлүк B2B дистрибьюторлор үчүн ылайыкталган",
        "Certifications & Compliance": "Сертификаттар жана шайкештик",
        "Globally Recognized Quality Standards": "Эл аралык таанылган сапат стандарттары",
        "Aesthetic, health and reverse osmosis water treatment.": "Эстетика, ден соолук жана тескери осмос суу тазалоо талаптарына тиешелүү сыноолор.",
        "Quality management documents available upon request.": "Сапат менеджменти документтери суроо боюнча берилет.",
        "CE Marking": "CE белгиси",
        "European import compliance.": "Европалык импорт талаптарына шайкештик.",
        "SGS Test Reports": "SGS сыноо отчеттору",
        "Heavy-metal & VOC removal validated.": "Оор металлдар жана VOC азайтуу көрсөткүчтөрү текшерилген.",
        "Compulsory certification for dispensers.": "Диспенсерлер үчүн милдеттүү сертификаттоо документтери.",
        "Gradient-density sediment cartridge production.": "Градиенттик тыгыздыктагы чөкмө картридждерди өндүрүү.",
        "Coconut shell CTO carbon block processing.": "Кокос кабыгынан жасалган CTO көмүр блогун иштетүү.",
        "Inline сүзгү Assembly": "Линиялык сүзгү жыйноо",
        "T33, mineral and quick-connect filter assembly.": "T33, минералдык жана тез туташтыргыч фильтрлерди жыйноо.",
        "Dimension, flow, pressure drop and assembly inspection": "Өлчөм, агым, басымдын төмөндөшү жана жыйноо текшерүүсү",
        "Appearance, leakage, labeling, carton and random sampling": "Көрүнүш, агып кетүү, этикеткалоо, картон жана тандалма текшерүү",
        "How We Use The Information": "Маалыматты кантип колдонобуз",
        "Documents": "Документтер",
    },
}

TITLE_SLUG_RE = re.compile(
    r"\b(product [a-z]|pp melt blown|cto carbon block|gac udf|ro membrane|uf membrane|"
    r"filter housing|t33 inline)\b",
    re.I,
)


def clean_name(text: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    text = re.sub(r"\([^)]*[A-Za-z][^)]*\)", "", text)
    text = re.sub(r"（[^）]*[A-Za-z][^）]*）", "", text)
    text = re.sub(r"\s+", " ", text).strip(" ·-")
    return text or "Yuchen Water"


def product_name(page: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", page, flags=re.S)
    if match:
        return clean_name(match.group(1))
    return "Yuchen Water"


def replace_h1_and_titles(page: str, lang: str, path: Path) -> str:
    override = PRODUCT_NAME_OVERRIDES.get(lang, {}).get(path.name)
    if override:
        page = re.sub(
            r"(<h1[^>]*>)(.*?)(</h1>)",
            lambda m: f"{m.group(1)}{html.escape(override)}{m.group(3)}",
            page,
            count=1,
            flags=re.S,
        )

    title_match = re.search(r"<title>(.*?)</title>", page, flags=re.S)
    if not title_match:
        return page
    current_title = html.unescape(re.sub(r"\s+", " ", title_match.group(1))).strip()
    if not (override or TITLE_SLUG_RE.search(current_title)):
        return page

    h1 = product_name(page)
    if not h1 or h1 == "Yuchen Water":
        return page
    new_title = f"{h1} | Yuchen Water"
    page = re.sub(
        r"<title>.*?</title>",
        f"<title>{html.escape(new_title)}</title>",
        page,
        count=1,
        flags=re.S,
    )
    page = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        lambda m: f'{m.group(1)}{html.escape(new_title, quote=True)}{m.group(2)}',
        page,
        count=1,
        flags=re.S,
    )
    page = re.sub(
        r'(<meta\s+name="twitter:title"\s+content=")[^"]*(")',
        lambda m: f'{m.group(1)}{html.escape(new_title, quote=True)}{m.group(2)}',
        page,
        count=1,
        flags=re.S,
    )
    return page


def card_name(card: str) -> str:
    match = re.search(r"<h3[^>]*>(.*?)</h3>", card, flags=re.S)
    if match:
        return clean_name(match.group(1))
    alt = re.search(r'alt="([^"]*)"', card)
    if alt:
        return clean_name(alt.group(1).split(" - ")[0])
    return "Yuchen Water"


def faq_html(lang: str) -> str:
    c = COPY[lang]
    items = []
    for question, answer in c["q"]:
        items.append(
            '<div class="faq-item">'
            f'<button class="faq-q">{html.escape(question)}</button>'
            f'<div class="faq-a"><p>{html.escape(answer)}</p></div>'
            '</div>'
        )
    return (
        '<section class="section section-cream product-faq">\n'
        '  <div class="container">\n'
        f'    <div class="section-head"><span class="eyebrow">FAQ</span><h2>{html.escape(c["faq_title"])}</h2></div>\n'
        f'    <div class="faq-wrap">{"".join(items)}</div>\n'
        '  </div>\n'
        '</section>'
    )


def replace_product_cards(page: str, lang: str) -> str:
    c = COPY[lang]

    def rewrite(match: re.Match[str]) -> str:
        card = match.group(0)
        name = card_name(card)
        desc = c["card"].format(name=name)
        card = re.sub(
            r"(<div class=\"product-body\">\s*<h3>.*?</h3>\s*<p>)(.*?)(</p>)",
            lambda m: f"{m.group(1)}{html.escape(desc)}{m.group(3)}",
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


def replace_product_intro(page: str, lang: str, path: Path) -> str:
    if not path.name.startswith("product-"):
        return page
    c = COPY[lang]
    name = product_name(page)
    intro = c["intro"].format(name=name)
    page = re.sub(
        r'(<p class="desc">)(.*?)(</p>)',
        lambda m: f"{m.group(1)}{html.escape(intro)}{m.group(3)}",
        page,
        count=1,
        flags=re.S,
    )
    page = re.sub(
        r'(<meta\s+name="description"\s+content=")[^"]*(")',
        lambda m: f'{m.group(1)}{html.escape(intro, quote=True)}{m.group(2)}',
        page,
        count=1,
        flags=re.S,
    )
    page = re.sub(
        r'(<meta\s+property="og:description"\s+content=")[^"]*(")',
        lambda m: f'{m.group(1)}{html.escape(intro, quote=True)}{m.group(2)}',
        page,
        count=1,
        flags=re.S,
    )
    page = re.sub(
        r'<section class="section section-cream product-faq">.*?</section>',
        faq_html(lang),
        page,
        count=1,
        flags=re.S,
    )
    return page


def replace_quality_and_ctas(page: str, lang: str) -> str:
    c = COPY[lang]
    e = EXTRA[lang]
    q_label = QUALITY_LABEL[lang]
    food_grade = FOOD_GRADE_DECLARATIONS[lang]
    page = page.replace("Quality documents available upon request", c["quality"])
    page = page.replace("Selected products can be supplied or tested according to NSF/ANSI 42, 53 and 58 requirements. ISO 9001, CE, SGS and Halal-related documents are available upon request.", c["quality"])
    page = page.replace("Selected products can be supplied or tested according to NSF/ANSI 42, 53 and 58 requirements. ISO 9001, CE, SGS and Halal-related documents are available upon request by product model and market requirement.", c["quality"])
    page = page.replace("food-grade material declarations", food_grade)
    page = page.replace("食品グレード 食品接触材料に関する宣言承認", "食品接触対応")
    page = page.replace("Thank you. Your inquiry has been submitted successfully and sent to Yuchen Water at expresswater025@gmail.com. Our sales engineer will contact you as soon as possible. You can also contact WhatsApp or email expresswater025@gmail.com anytime.", e["thanks"])
    page = re.sub(
        r'(<p id="formSuccess" class="form-success" hidden>).*?(</p>)',
        lambda m: f"{m.group(1)}{html.escape(e['thanks'])}{m.group(2)}",
        page,
        flags=re.S,
    )
    page = page.replace(
        'Privacy policy for Yuchen Water inquiry forms, buyer data, email delivery and contact information.',
        e["privacy_desc"],
    )
    page = page.replace("All Rights Reserved", e["rights"])
    page = page.replace("All rights reserved.", e["rights"])
    page = page.replace("Privacy Policy", e["privacy"])
    page = page.replace("selected NSF/ANSI and Halal-related documents available on request", c["quality"])
    page = page.replace("NSF/ANSI options · Сапат документтери суроо боюнча берилет · Halal documents on request", c["quality"])
    page = page.replace("Halal documents on request", e["halal"])
    page = page.replace("Halal-related documents are available upon request for qualified orders.", e["halal"])
    page = page.replace("Halal-related documents available upon request", e["halal"])
    page = page.replace("For Muslim-market distribution.", e["halal"])
    page = page.replace(f"{e['halal']} where applicable", e["halal"])
    page = page.replace("Quality documents", q_label)
    for source, target in c["cta"].items():
        page = page.replace(f">{source}<", f">{target}<")
        page = page.replace(f">{source} →<", f">{target} →<")
    return page


def replace_visible_labels(page: str, lang: str) -> str:
    page = page.replace("Yuanhua Town, Haining City, Zhejiang Province, China", LOCALIZED_ADDRESS[lang])
    page = page.replace("Factory:", {
        "ru": "Завод:",
        "es": "Fábrica:",
        "de": "Werk:",
        "fr": "Usine :",
        "vi": "Nhà máy:",
        "ja": "工場:",
        "uz": "Zavod:",
        "kk": "Зауыт:",
        "ky": "Завод:",
    }[lang])
    for source, target in VISIBLE_LABELS.get(lang, {}).items():
        page = page.replace(source, target)
    halal_title = {
        "ru": "Документы Halal",
        "es": "Documentos Halal",
        "de": "Halal-Unterlagen",
        "fr": "Documents Halal",
        "vi": "Hồ sơ Halal",
        "ja": "Halal関連書類",
        "uz": "Halal hujjatlari",
        "kk": "Halal құжаттары",
        "ky": "Halal документтери",
    }[lang]
    page = re.sub(
        r'(<h3([^>]*)>)' + re.escape(EXTRA[lang]["halal"]) + r"(</h3>)",
        lambda m: f"{m.group(1)}{html.escape(halal_title)}{m.group(3)}",
        page,
    )
    return page


def replace_general_faq_page(page: str, lang: str, path: Path) -> str:
    if path.name != "faq.html":
        return page
    c = COPY[lang]
    items = []
    for question, answer in c["q"]:
        items.append(
            '<div class="faq-item">'
            f'<button class="faq-q">{html.escape(question)}</button>'
            f'<div class="faq-a"><p>{html.escape(answer)}</p></div>'
            '</div>'
        )
    page = re.sub(
        r'(<div class="faq-wrap">).*?(</div>\s*</section>)',
        lambda m: f'{m.group(1)}{"".join(items)}{m.group(2)}',
        page,
        count=1,
        flags=re.S,
    )
    return page


def fix_file(path: Path, lang: str) -> bool:
    original = path.read_text(encoding="utf-8", errors="ignore")
    page = original
    page = replace_h1_and_titles(page, lang, path)
    page = replace_product_intro(page, lang, path)
    if path.name in {"products.html", "index.html"} or path.name.startswith("product-"):
        page = replace_product_cards(page, lang)
    page = replace_quality_and_ctas(page, lang)
    page = replace_visible_labels(page, lang)
    page = replace_general_faq_page(page, lang, path)
    if page != original:
        path.write_text(page, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    scanned = 0
    for lang in LANGS:
        lang_dir = ROOT / lang
        if not lang_dir.exists():
            continue
        for path in lang_dir.glob("*.html"):
            scanned += 1
            if fix_file(path, lang):
                changed += 1
    print(f"Scanned {scanned} HTML files; changed {changed} files.")


if __name__ == "__main__":
    main()
