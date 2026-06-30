#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add large industrial RO water treatment equipment across all language pages."""

from __future__ import annotations

import html
import json
import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_SLUG = "product-ro-seawater-desalination-machine.html"
AFTER_SLUG = "product-20-inch-commercial-ro-water-purifier-800g-2000g.html"
NEW_SLUG = "product-large-industrial-reverse-osmosis-water-treatment-equipment.html"
PRODUCT_ID = "large-industrial-reverse-osmosis-water-treatment-equipment"
TODAY = "2026-06-14"
MAIN_IMAGE = "large-industrial-reverse-osmosis-water-treatment-equipment-3-100tph-oem.webp"
RTL_LANGS = {"ar", "fa", "he", "ur"}


DATA_ROWS = """
af	Groot industriële omgekeerde-osmose waterbehandelingstoerusting 3-100 t/h	Industriële RO waterbehandeling	Groot industriële omgekeerde-osmose waterbehandelingstoerusting van Yuchen Water is ontwerp vir fabrieke, munisipale projekte, hotelle en B2B kontrakteurs wat stabiele gesuiwerde water teen 3-100 t/h benodig. Die stelsel kombineer drie-stap voorbehandeling met RO skeiding, voloutomatiese intelligente beheer, beskerming teen geen water en oorlading, en aanpasbare prosesmodules vir kraanwater of grondwater.	Groot industriële RO waterbehandelingstelsel met 3-100 t/h vloei, outomatiese beheer, aanpasbare voorbehandeling en UPVC/304 pypopsies vir OEM projekte.	Produksoort|Bedryfsmodus|Behandelingsproses|Skoonwater-vloei|Toevoerwater|Pypmateriaal|Beskermingsfunksies|Beheer|Toepassing|OEM/ODM|MOQ	Voloutomatiese intelligente werking, met handmatige diensmodus volgens projekbehoefte	Drie-stap voorbehandeling plus omgekeerde osmose; prosesvloei word volgens waterontleding aangepas	Kraanwater en grondwater	UPVC of 304 vlekvrye staal volgens projekstandaard	Geen-water beskerming, oorladingsbeskerming en alarmkoppelvlakke	PLC of beheerpaneel kan volgens kliëntvereistes aangepas word	Fabrieke, wateraanlegte, hotelle, voedselverwerking en industriële suiwerwaterprojekte	Vloeitempo, pomp, membraan, tenks, pypmateriaal, spanning, paneeltaal en verpakking kan aangepas word	Bevestig volgens kapasiteit, konfigurasie en OEM vlak
ar	معدات معالجة مياه RO صناعية كبيرة 3-100 طن/ساعة	معالجة مياه RO صناعية	معدات معالجة مياه RO الصناعية الكبيرة من Yuchen Water مخصصة للمصانع ومحطات المياه والفنادق ومقاولي المشاريع الذين يحتاجون إلى مياه نقية مستقرة بتدفق 3-100 طن/ساعة. يجمع النظام بين معالجة أولية من ثلاث مراحل وتقنية التناضح العكسي، مع تشغيل ذكي أوتوماتيكي، وحماية من انقطاع المياه والحمل الزائد، ووحدات عملية قابلة للتخصيص لمياه الصنبور أو المياه الجوفية.	نظام RO صناعي كبير بتدفق 3-100 طن/ساعة، تحكم أوتوماتيكي، معالجة أولية قابلة للتخصيص وخيارات أنابيب UPVC/304 لمشاريع OEM.	نوع المنتج|وضع التشغيل|عملية المعالجة|تدفق المياه النقية|مياه التغذية|مادة الأنابيب|وظائف الحماية|التحكم|الاستخدام|OEM/ODM|MOQ	تشغيل ذكي أوتوماتيكي كامل، مع وضع خدمة يدوي حسب حاجة المشروع	معالجة أولية من ثلاث مراحل بالإضافة إلى التناضح العكسي؛ يتم تخصيص مسار العملية حسب تحليل المياه	مياه الصنبور والمياه الجوفية	UPVC أو فولاذ مقاوم للصدأ 304 حسب معيار المشروع	حماية من انقطاع المياه، حماية من الحمل الزائد وواجهات إنذار	يمكن تخصيص PLC أو لوحة التحكم حسب متطلبات العميل	المصانع، محطات المياه، الفنادق، معالجة الأغذية ومشاريع المياه النقية الصناعية	يمكن تخصيص التدفق، المضخة، الغشاء، الخزانات، مادة الأنابيب، الجهد، لغة اللوحة والتغليف	يتم التأكيد حسب السعة والتكوين ومستوى OEM
az	Böyük sənaye RO su təmizləmə avadanlığı 3-100 t/saat	Sənaye RO su təmizləmə	Yuchen Water böyük sənaye RO su təmizləmə avadanlığı zavodlar, su layihələri, otellər və B2B podratçıları üçün 3-100 t/saat sabit təmiz su istehsalı məqsədi ilə hazırlanır. Sistem üç mərhələli əvvəlcədən təmizləmə, tərs osmos ayrılması, tam avtomatik ağıllı idarəetmə, susuz və həddən artıq yüklənmədən qoruma və kran suyu və ya yeraltı su üçün fərdiləşdirilən proses modullarını birləşdirir.	3-100 t/saat axınlı böyük sənaye RO sistemi, avtomatik idarəetmə, fərdi əvvəlcədən təmizləmə və OEM layihələri üçün UPVC/304 boru variantları.	Məhsul növü|İş rejimi|Təmizləmə prosesi|Təmiz su axını|Giriş suyu|Boru materialı|Qoruma funksiyaları|İdarəetmə|Tətbiq|OEM/ODM|MOQ	Tam avtomatik ağıllı işləmə, layihə ehtiyacına görə əl ilə xidmət rejimi	Üç mərhələli əvvəlcədən təmizləmə və tərs osmos; proses axını su analizinə görə uyğunlaşdırılır	Kran suyu və yeraltı su	UPVC və ya layihə standartına görə 304 paslanmayan polad	Susuz qoruma, həddən artıq yüklənmə qoruması və alarm interfeysləri	PLC və ya idarə paneli müştəri tələbinə görə uyğunlaşdırıla bilər	Zavodlar, su stansiyaları, otellər, qida emalı və sənaye təmiz su layihələri	Axın, nasos, membran, tanklar, boru materialı, gərginlik, panel dili və qablaşdırma fərdiləşdirilə bilər	İstehsal gücü, konfiqurasiya və OEM səviyyəsinə görə təsdiqlənir
bg	Голяма индустриална RO система за пречистване на вода 3-100 т/ч	Индустриално RO пречистване на вода	Голямата индустриална RO система за пречистване на вода на Yuchen Water е предназначена за фабрики, водни станции, хотели и B2B изпълнители, които се нуждаят от стабилна чиста вода с дебит 3-100 т/ч. Системата съчетава тристепенна предварителна обработка с обратна осмоза, напълно автоматично интелигентно управление, защита от липса на вода и претоварване и процесни модули, персонализирани за чешмяна или подземна вода.	Голяма индустриална RO система с дебит 3-100 т/ч, автоматично управление, персонализирана предварителна обработка и UPVC/304 тръбни опции за OEM проекти.	Тип продукт|Режим на работа|Процес на обработка|Дебит чиста вода|Входна вода|Материал на тръбите|Защитни функции|Управление|Приложение|OEM/ODM|MOQ	Напълно автоматична интелигентна работа, с ръчен сервизен режим според проекта	Тристепенна предварителна обработка плюс обратна осмоза; процесът се настройва според анализа на водата	Чешмяна вода и подземна вода	UPVC или неръждаема стомана 304 според стандарта на проекта	Защита от липса на вода, защита от претоварване и алармени интерфейси	PLC или контролен панел може да се персонализира по изискване	Фабрики, водни станции, хотели, хранителна промишленост и индустриални проекти за чиста вода	Дебит, помпа, мембрана, резервоари, тръби, напрежение, език на панела и опаковка могат да се персонализират	Потвърждава се според капацитет, конфигурация и OEM ниво
bn	বড় শিল্প RO পানি শোধন সরঞ্জাম 3-100 টন/ঘণ্টা	শিল্প RO পানি শোধন	Yuchen Water-এর বড় শিল্প RO পানি শোধন সরঞ্জাম কারখানা, পানি প্রকল্প, হোটেল এবং B2B ঠিকাদারদের জন্য তৈরি, যেখানে 3-100 টন/ঘণ্টা স্থিতিশীল বিশুদ্ধ পানি দরকার। সিস্টেমে তিন ধাপ প্রি-ট্রিটমেন্ট, রিভার্স অসমোসিস, পূর্ণ স্বয়ংক্রিয় বুদ্ধিমান নিয়ন্ত্রণ, পানি না থাকলে সুরক্ষা, ওভারলোড সুরক্ষা এবং ট্যাপ পানি বা ভূগর্ভস্থ পানির জন্য কাস্টম প্রক্রিয়া মডিউল রয়েছে।	3-100 টন/ঘণ্টা প্রবাহের বড় শিল্প RO সিস্টেম, স্বয়ংক্রিয় নিয়ন্ত্রণ, কাস্টম প্রি-ট্রিটমেন্ট এবং OEM প্রকল্পের জন্য UPVC/304 পাইপিং বিকল্প।	পণ্যের ধরন|চালনার ধরন|শোধন প্রক্রিয়া|বিশুদ্ধ পানির প্রবাহ|ইনলেট পানি|পাইপ উপাদান|সুরক্ষা ফাংশন|নিয়ন্ত্রণ|ব্যবহার|OEM/ODM|MOQ	পূর্ণ স্বয়ংক্রিয় বুদ্ধিমান চালনা, প্রকল্প অনুযায়ী ম্যানুয়াল সার্ভিস মোড	তিন ধাপ প্রি-ট্রিটমেন্ট এবং রিভার্স অসমোসিস; পানি বিশ্লেষণ অনুযায়ী প্রক্রিয়া কাস্টমাইজড	ট্যাপ পানি ও ভূগর্ভস্থ পানি	UPVC অথবা প্রকল্প মান অনুযায়ী 304 স্টেইনলেস স্টিল	পানি না থাকলে সুরক্ষা, ওভারলোড সুরক্ষা এবং অ্যালার্ম ইন্টারফেস	PLC বা কন্ট্রোল প্যানেল গ্রাহকের চাহিদা অনুযায়ী কাস্টম করা যায়	কারখানা, পানি প্ল্যান্ট, হোটেল, খাদ্য প্রক্রিয়াকরণ এবং শিল্প বিশুদ্ধ পানি প্রকল্প	প্রবাহ, পাম্প, মেমব্রেন, ট্যাংক, পাইপ উপাদান, ভোল্টেজ, প্যানেল ভাষা ও প্যাকেজিং কাস্টম করা যায়	ক্ষমতা, কনফিগারেশন ও OEM স্তর অনুযায়ী নিশ্চিত করা হয়
bs	Velika industrijska RO oprema za tretman vode 3-100 t/h	Industrijski RO tretman vode	Velika industrijska RO oprema za tretman vode Yuchen Water namijenjena je fabrikama, vodnim stanicama, hotelima i B2B izvođačima kojima treba stabilna pročišćena voda od 3-100 t/h. Sistem kombinuje trostepeni predtretman sa reverznom osmozom, potpuno automatski inteligentni rad, zaštitu od rada bez vode i preopterećenja, te procesne module prilagođene vodi iz vodovoda ili podzemnoj vodi.	Veliki industrijski RO sistem 3-100 t/h, automatsko upravljanje, prilagodljiv predtretman i UPVC/304 cijevi za OEM projekte.	Tip proizvoda|Način rada|Proces tretmana|Protok čiste vode|Ulazna voda|Materijal cijevi|Zaštitne funkcije|Upravljanje|Primjena|OEM/ODM|MOQ	Potpuno automatski inteligentni rad, sa ručnim servisnim režimom po potrebi projekta	Trostepeni predtretman plus reverzna osmoza; proces se prilagođava prema analizi vode	Vodovodna voda i podzemna voda	UPVC ili nehrđajući čelik 304 prema standardu projekta	Zaštita bez vode, zaštita od preopterećenja i alarmni interfejsi	PLC ili kontrolni panel može se prilagoditi zahtjevima kupca	Fabrike, vodne stanice, hoteli, prehrambena industrija i industrijski projekti čiste vode	Protok, pumpa, membrana, rezervoari, cijevi, napon, jezik panela i pakovanje mogu se prilagoditi	Potvrđuje se prema kapacitetu, konfiguraciji i OEM nivou
cs	Velké průmyslové RO zařízení pro úpravu vody 3-100 t/h	Průmyslová RO úprava vody	Velké průmyslové RO zařízení Yuchen Water je určeno pro továrny, úpravny vody, hotely a B2B dodavatele, kteří potřebují stabilní produkci čisté vody 3-100 t/h. Systém spojuje třístupňovou předúpravu s reverzní osmózou, plně automatický inteligentní provoz, ochranu proti chodu bez vody a přetížení a procesní moduly přizpůsobené vodovodní nebo podzemní vodě.	Velký průmyslový RO systém s průtokem 3-100 t/h, automatickým řízením, přizpůsobenou předúpravou a potrubím UPVC/304 pro OEM projekty.	Typ produktu|Provozní režim|Proces úpravy|Průtok čisté vody|Vstupní voda|Materiál potrubí|Ochranné funkce|Řízení|Použití|OEM/ODM|MOQ	Plně automatický inteligentní provoz s ručním servisním režimem dle projektu	Třístupňová předúprava plus reverzní osmóza; proces se nastavuje podle analýzy vody	Vodovodní voda a podzemní voda	UPVC nebo nerezová ocel 304 podle standardu projektu	Ochrana proti chodu bez vody, přetížení a alarmové rozhraní	PLC nebo ovládací panel lze upravit dle požadavků zákazníka	Továrny, úpravny vody, hotely, potravinářství a průmyslové projekty čisté vody	Průtok, čerpadlo, membrána, nádrže, potrubí, napětí, jazyk panelu a balení lze přizpůsobit	Potvrzuje se podle kapacity, konfigurace a úrovně OEM
da	Stort industrielt RO-vandbehandlingsanlæg 3-100 t/h	Industriel RO-vandbehandling	Yuchen Water stort industrielt RO-vandbehandlingsanlæg er udviklet til fabrikker, vandværksprojekter, hoteller og B2B-entreprenører, der kræver stabilt rent vand på 3-100 t/h. Systemet kombinerer tretrins forbehandling med omvendt osmose, fuldautomatisk intelligent drift, tørkørsels- og overbelastningsbeskyttelse samt procesmoduler tilpasset ledningsvand eller grundvand.	Stort industrielt RO-system med 3-100 t/h flow, automatisk styring, tilpasset forbehandling og UPVC/304 rørvalg til OEM-projekter.	Produkttype|Driftsform|Behandlingsproces|Rentvandsflow|Fødevand|Rørmateriale|Beskyttelsesfunktioner|Styring|Anvendelse|OEM/ODM|MOQ	Fuldautomatisk intelligent drift med manuel servicefunktion efter projektbehov	Tretrins forbehandling plus omvendt osmose; procesflow tilpasses vandanalysen	Ledningsvand og grundvand	UPVC eller 304 rustfrit stål efter projektstandard	Tørkørselsbeskyttelse, overbelastningsbeskyttelse og alarmgrænseflader	PLC eller kontrolpanel kan tilpasses kundens krav	Fabrikker, vandværker, hoteller, fødevareforarbejdning og industrielle rentvandsprojekter	Flow, pumpe, membran, tanke, rørmateriale, spænding, panelsprog og emballage kan tilpasses	Bekræftes efter kapacitet, konfiguration og OEM-niveau
de	Große industrielle Umkehrosmose-Wasseraufbereitungsanlage 3-100 t/h	Industrielle RO-Wasseraufbereitung	Die große industrielle Umkehrosmose-Wasseraufbereitungsanlage von Yuchen Water ist für Fabriken, Wasserwerke, Hotels und B2B-Projektpartner ausgelegt, die zuverlässig 3-100 t/h Reinwasser benötigen. Das System kombiniert dreistufige Vorbehandlung mit RO-Trennung, vollautomatischer intelligenter Steuerung, Wassermangelschutz, Überlastschutz und anpassbaren Prozessmodulen für Leitungswasser oder Grundwasser.	Große industrielle RO-Anlage mit 3-100 t/h Durchfluss, automatischer Steuerung, kundenspezifischer Vorbehandlung und UPVC/304-Rohrleitungsoptionen für OEM-Projekte.	Produkttyp|Betriebsart|Aufbereitungsprozess|Reinwasser-Durchfluss|Zulaufwasser|Rohrmaterial|Schutzfunktionen|Steuerung|Anwendung|OEM/ODM|MOQ	Vollautomatischer intelligenter Betrieb, mit manuellem Servicemodus nach Projektbedarf	Dreistufige Vorbehandlung plus Umkehrosmose; Prozessablauf wird nach Wasseranalyse angepasst	Leitungswasser und Grundwasser	UPVC oder Edelstahl 304 nach Projektstandard	Wassermangelschutz, Überlastschutz und Alarm-Schnittstellen	PLC oder Schaltschrank kann nach Kundenanforderung angepasst werden	Fabriken, Wasserwerke, Hotels, Lebensmittelverarbeitung und industrielle Reinwasserprojekte	Durchfluss, Pumpe, Membran, Tanks, Rohrmaterial, Spannung, Panelsprache und Verpackung können angepasst werden	Wird nach Kapazität, Konfiguration und OEM-Level bestätigt
el	Μεγάλος βιομηχανικός εξοπλισμός επεξεργασίας νερού RO 3-100 t/h	Βιομηχανική επεξεργασία νερού RO	Ο μεγάλος βιομηχανικός εξοπλισμός επεξεργασίας νερού RO της Yuchen Water προορίζεται για εργοστάσια, έργα νερού, ξενοδοχεία και B2B αναδόχους που χρειάζονται σταθερή παραγωγή καθαρού νερού 3-100 t/h. Το σύστημα συνδυάζει τριών σταδίων προεπεξεργασία με αντίστροφη όσμωση, πλήρως αυτόματη έξυπνη λειτουργία, προστασία από έλλειψη νερού και υπερφόρτωση, καθώς και προσαρμοσμένες μονάδες διεργασίας για νερό δικτύου ή υπόγειο νερό.	Μεγάλο βιομηχανικό σύστημα RO 3-100 t/h με αυτόματο έλεγχο, προσαρμοσμένη προεπεξεργασία και επιλογές σωληνώσεων UPVC/304 για έργα OEM.	Τύπος προϊόντος|Τρόπος λειτουργίας|Διαδικασία επεξεργασίας|Ροή καθαρού νερού|Νερό τροφοδοσίας|Υλικό σωληνώσεων|Λειτουργίες προστασίας|Έλεγχος|Εφαρμογή|OEM/ODM|MOQ	Πλήρως αυτόματη έξυπνη λειτουργία, με χειροκίνητη λειτουργία συντήρησης ανάλογα με το έργο	Τριών σταδίων προεπεξεργασία και αντίστροφη όσμωση· η διεργασία προσαρμόζεται στην ανάλυση νερού	Νερό δικτύου και υπόγειο νερό	UPVC ή ανοξείδωτος χάλυβας 304 σύμφωνα με το πρότυπο έργου	Προστασία έλλειψης νερού, υπερφόρτωσης και διεπαφές συναγερμού	PLC ή πίνακας ελέγχου προσαρμόζεται στις απαιτήσεις πελάτη	Εργοστάσια, μονάδες νερού, ξενοδοχεία, τρόφιμα και βιομηχανικά έργα καθαρού νερού	Ροή, αντλία, μεμβράνη, δεξαμενές, σωληνώσεις, τάση, γλώσσα πάνελ και συσκευασία προσαρμόζονται	Επιβεβαιώνεται κατά χωρητικότητα, διαμόρφωση και επίπεδο OEM
en	Large Industrial Reverse Osmosis Water Treatment Equipment 3-100 TPH	Industrial RO Water Treatment	Yuchen Water large industrial reverse osmosis water treatment equipment is built for factories, water plants, hotels and B2B project contractors that need stable purified water output from 3 to 100 tons per hour. The system combines three-stage pretreatment with RO separation, full automatic intelligent operation, no-water protection, overload protection and customizable process modules for tap water or groundwater.	Large industrial RO water treatment system with 3-100 TPH flow, automatic control, customizable pretreatment and UPVC/304 piping options for OEM projects.	Product Type|Operating Mode|Treatment Process|Pure Water Flow|Feed Water|Piping Material|Protection Functions|Control|Application|OEM/ODM|MOQ	Full automatic intelligent operation, with manual service mode according to project needs	Three-stage pretreatment plus reverse osmosis; purification process is customized according to water analysis	Tap water and groundwater	UPVC or 304 stainless steel according to project standard	No-water protection, overload protection and alarm interfaces	PLC or control panel can be customized according to buyer requirements	Factories, water plants, hotels, food processing and industrial pure water projects	Flow rate, pump, membrane, tanks, piping material, voltage, panel language and packaging can be customized	Confirmed by capacity, configuration and OEM level
es	Equipo industrial grande de tratamiento de agua por ósmosis inversa 3-100 t/h	Tratamiento industrial de agua RO	El equipo industrial grande de tratamiento de agua por ósmosis inversa de Yuchen Water está diseñado para fábricas, plantas de agua, hoteles y contratistas B2B que necesitan agua purificada estable de 3-100 t/h. El sistema combina pretratamiento de tres etapas con separación RO, operación inteligente totalmente automática, protección por falta de agua, protección contra sobrecarga y módulos de proceso personalizables para agua de red o agua subterránea.	Sistema industrial grande RO con flujo de 3-100 t/h, control automático, pretratamiento personalizable y opciones de tubería UPVC/304 para proyectos OEM.	Tipo de producto|Modo de operación|Proceso de tratamiento|Flujo de agua pura|Agua de alimentación|Material de tubería|Funciones de protección|Control|Aplicación|OEM/ODM|MOQ	Operación inteligente totalmente automática, con modo de servicio manual según el proyecto	Pretratamiento de tres etapas más ósmosis inversa; el proceso se personaliza según el análisis del agua	Agua de red y agua subterránea	UPVC o acero inoxidable 304 según el estándar del proyecto	Protección por falta de agua, protección contra sobrecarga e interfaces de alarma	PLC o panel de control personalizado según requisitos del comprador	Fábricas, plantas de agua, hoteles, procesamiento de alimentos y proyectos industriales de agua pura	Flujo, bomba, membrana, tanques, material de tubería, voltaje, idioma del panel y embalaje personalizables	Se confirma según capacidad, configuración y nivel OEM
et	Suur tööstuslik RO veetöötlusseade 3-100 t/h	Tööstuslik RO veetöötlus	Yuchen Water suur tööstuslik RO veetöötlusseade on mõeldud tehastele, veepuhastusprojektidele, hotellidele ja B2B töövõtjatele, kes vajavad stabiilset puhast vett 3-100 t/h. Süsteem ühendab kolmeetapilise eeltöötluse pöördosmoosiga, täisautomaatse intelligentse töö, veepuuduse ja ülekoormuse kaitse ning kraani- või põhjaveele kohandatud protsessimoodulid.	Suur tööstuslik RO süsteem 3-100 t/h vooluga, automaatjuhtimise, kohandatud eeltöötluse ja UPVC/304 torustiku valikutega OEM-projektidele.	Toote tüüp|Töörežiim|Töötlusprotsess|Puhasvee vool|Sisendvesi|Torustiku materjal|Kaitsefunktsioonid|Juhtimine|Kasutus|OEM/ODM|MOQ	Täisautomaatne intelligentne töö, käsitsi hooldusrežiimiga projekti vajaduse järgi	Kolmeetapiline eeltöötlus pluss pöördosmoos; protsess kohandatakse veeanalüüsi järgi	Kraanivesi ja põhjavesi	UPVC või 304 roostevaba teras vastavalt projekti standardile	Veepuuduse kaitse, ülekoormuskaitse ja alarmiliidesed	PLC või juhtpaneel kohandatakse kliendi nõuetele	Tehased, veepuhastusjaamad, hotellid, toiduainetööstus ja tööstusliku puhta vee projektid	Vool, pump, membraan, paagid, torustik, pinge, paneeli keel ja pakend kohandatavad	Kinnitatakse võimsuse, konfiguratsiooni ja OEM taseme järgi
fa	تجهیزات بزرگ تصفیه آب صنعتی RO ظرفیت 3-100 تن در ساعت	تصفیه آب صنعتی RO	تجهیزات بزرگ تصفیه آب صنعتی RO شرکت Yuchen Water برای کارخانه‌ها، پروژه‌های آب، هتل‌ها و پیمانکاران B2B طراحی شده است که به خروجی پایدار آب تصفیه‌شده با ظرفیت 3-100 تن در ساعت نیاز دارند. این سیستم پیش‌تصفیه سه‌مرحله‌ای را با جداسازی اسمز معکوس، عملکرد هوشمند تمام‌خودکار، حفاظت در نبود آب، حفاظت اضافه‌بار و ماژول‌های فرایندی قابل سفارشی‌سازی برای آب شهری یا آب زیرزمینی ترکیب می‌کند.	سیستم بزرگ RO صنعتی با دبی 3-100 تن در ساعت، کنترل خودکار، پیش‌تصفیه سفارشی و گزینه‌های لوله‌کشی UPVC/304 برای پروژه‌های OEM.	نوع محصول|حالت عملکرد|فرایند تصفیه|دبی آب خالص|آب ورودی|جنس لوله‌کشی|عملکردهای حفاظتی|کنترل|کاربرد|OEM/ODM|MOQ	عملکرد هوشمند تمام‌خودکار، همراه با حالت سرویس دستی بر اساس نیاز پروژه	پیش‌تصفیه سه‌مرحله‌ای به‌علاوه اسمز معکوس؛ فرایند طبق آنالیز آب سفارشی می‌شود	آب شهری و آب زیرزمینی	UPVC یا استنلس استیل 304 طبق استاندارد پروژه	حفاظت در نبود آب، حفاظت اضافه‌بار و رابط‌های هشدار	PLC یا پنل کنترل طبق نیاز خریدار قابل سفارشی‌سازی است	کارخانه‌ها، واحدهای آب، هتل‌ها، صنایع غذایی و پروژه‌های آب خالص صنعتی	دبی، پمپ، ممبران، مخازن، جنس لوله، ولتاژ، زبان پنل و بسته‌بندی قابل سفارشی‌سازی است	بر اساس ظرفیت، پیکربندی و سطح OEM تأیید می‌شود
fi	Suuri teollinen RO-vedenkäsittelylaitteisto 3-100 t/h	Teollinen RO-vedenkäsittely	Yuchen Water suuri teollinen RO-vedenkäsittelylaitteisto on tarkoitettu tehtaille, vesilaitoksille, hotelleille ja B2B-projektiurakoitsijoille, jotka tarvitsevat vakaata puhdasta vettä 3-100 t/h. Järjestelmä yhdistää kolmivaiheisen esikäsittelyn käänteisosmoosiin, täysin automaattisen älykkään käytön, kuivakäynti- ja ylikuormitussuojan sekä prosessimoduulit, jotka räätälöidään vesijohto- tai pohjavedelle.	Suuri teollinen RO-järjestelmä 3-100 t/h virtaamalla, automaattiohjauksella, räätälöidyllä esikäsittelyllä ja UPVC/304-putkivaihtoehdoilla OEM-projekteihin.	Tuotetyyppi|Käyttötapa|Käsittelyprosessi|Puhdasvesivirtaus|Syöttövesi|Putkimateriaali|Suojaustoiminnot|Ohjaus|Käyttökohde|OEM/ODM|MOQ	Täysin automaattinen älykäs käyttö ja manuaalinen huoltotila projektin mukaan	Kolmivaiheinen esikäsittely plus käänteisosmoosi; prosessi räätälöidään vesianalyysin mukaan	Vesijohtovesi ja pohjavesi	UPVC tai 304 ruostumaton teräs projektistandardin mukaan	Kuivakäyntisuoja, ylikuormitussuoja ja hälytysliitännät	PLC tai ohjauspaneeli voidaan räätälöidä ostajan vaatimuksiin	Tehtaat, vesilaitokset, hotellit, elintarviketeollisuus ja teolliset puhdasvesiprojektit	Virtaama, pumppu, kalvo, säiliöt, putkimateriaali, jännite, paneelin kieli ja pakkaus räätälöitävissä	Vahvistetaan kapasiteetin, kokoonpanon ja OEM-tason mukaan
fr	Grande installation industrielle de traitement d'eau par osmose inverse 3-100 t/h	Traitement industriel de l'eau RO	La grande installation industrielle de traitement d'eau par osmose inverse de Yuchen Water est conçue pour les usines, stations d'eau, hôtels et contractants B2B qui recherchent une production stable d'eau purifiée de 3-100 t/h. Le système associe un prétraitement en trois étapes à l'osmose inverse, une exploitation intelligente entièrement automatique, une protection manque d'eau, une protection surcharge et des modules de procédé personnalisables pour l'eau de ville ou l'eau souterraine.	Grande installation RO industrielle avec débit 3-100 t/h, contrôle automatique, prétraitement personnalisable et tuyauterie UPVC/304 pour projets OEM.	Type de produit|Mode de fonctionnement|Procédé de traitement|Débit d'eau pure|Eau d'alimentation|Matériau de tuyauterie|Fonctions de protection|Contrôle|Application|OEM/ODM|MOQ	Fonctionnement intelligent entièrement automatique, avec mode service manuel selon le projet	Prétraitement en trois étapes plus osmose inverse; le procédé est personnalisé selon l'analyse d'eau	Eau de ville et eau souterraine	UPVC ou acier inoxydable 304 selon le standard du projet	Protection manque d'eau, protection surcharge et interfaces d'alarme	PLC ou panneau de contrôle personnalisable selon les exigences de l'acheteur	Usines, stations d'eau, hôtels, agroalimentaire et projets industriels d'eau pure	Débit, pompe, membrane, cuves, matériau de tuyauterie, tension, langue du panneau et emballage personnalisables	Confirmé selon capacité, configuration et niveau OEM
ha	Babban kayan aikin RO na masana'antu don tace ruwa 3-100 t/h	Tace ruwan RO na masana'antu	Kayan aikin RO na masana'antu na Yuchen Water an tsara shi ga masana'antu, tashoshin ruwa, otal-otal da masu aikin B2B da ke bukatar tsayayyen ruwan da aka tace 3-100 t/h. Tsarin yana haɗa matakai uku na pretreatment da reverse osmosis, cikakken aiki na atomatik mai hankali, kariya idan babu ruwa, kariya daga nauyi fiye da kima da sassan tsari da za a iya tsara su ga ruwan famfo ko ruwan karkashin kasa.	Babban tsarin RO na masana'antu 3-100 t/h, sarrafa atomatik, pretreatment na musamman da zabin bututun UPVC/304 don ayyukan OEM.	Nau'in samfur|Yanayin aiki|Tsarin tacewa|Gudun ruwan tsabta|Ruwan shigarwa|Kayan bututu|Ayyukan kariya|Sarrafa|Amfani|OEM/ODM|MOQ	Cikakken aiki na atomatik mai hankali, tare da yanayin sabis na hannu bisa bukatar aiki	Matakai uku na pretreatment da reverse osmosis; ana tsara tsarin bisa nazarin ruwa	Ruwan famfo da ruwan karkashin kasa	UPVC ko bakin karfe 304 bisa mizanin aikin	Kariya idan babu ruwa, kariya daga overloading da hanyoyin alarm	PLC ko panel na sarrafawa za a iya tsara shi bisa bukatar abokin ciniki	Masana'antu, tashoshin ruwa, otal-otal, sarrafa abinci da ayyukan ruwan tsabta na masana'antu	Gudu, famfo, membrane, tankuna, bututu, wuta, yaren panel da kunshi za a iya tsara su	A tabbatar bisa karfin aiki, tsarin da matakin OEM
he	ציוד תעשייתי גדול לטיפול במים RO 3-100 טון/שעה	טיפול תעשייתי במים RO	ציוד הטיפול במים RO התעשייתי הגדול של Yuchen Water מיועד למפעלים, תחנות מים, מלונות וקבלני B2B הזקוקים לתפוקת מים מטוהרים יציבה של 3-100 טון/שעה. המערכת משלבת קדם-טיפול בשלושה שלבים עם אוסמוזה הפוכה, הפעלה חכמה אוטומטית מלאה, הגנה מחוסר מים, הגנת עומס יתר ומודולי תהליך מותאמים למי ברז או מי תהום.	מערכת RO תעשייתית גדולה עם ספיקה 3-100 טון/שעה, בקרה אוטומטית, קדם-טיפול מותאם ואפשרויות צנרת UPVC/304 לפרויקטי OEM.	סוג מוצר|מצב פעולה|תהליך טיפול|ספיקת מים טהורים|מי הזנה|חומר צנרת|פונקציות הגנה|בקרה|יישום|OEM/ODM|MOQ	הפעלה חכמה אוטומטית מלאה, עם מצב שירות ידני לפי צורכי הפרויקט	קדם-טיפול בשלושה שלבים בתוספת אוסמוזה הפוכה; התהליך מותאם לפי ניתוח המים	מי ברז ומי תהום	UPVC או נירוסטה 304 לפי תקן הפרויקט	הגנה מחוסר מים, הגנת עומס יתר וממשקי התראה	PLC או לוח בקרה ניתן להתאמה לפי דרישת הלקוח	מפעלים, תחנות מים, מלונות, עיבוד מזון ופרויקטי מים טהורים תעשייתיים	ספיקה, משאבה, ממברנה, מכלים, חומר צנרת, מתח, שפת לוח ואריזה ניתנים להתאמה	מאושר לפי קיבולת, תצורה ורמת OEM
hi	बड़ा औद्योगिक RO जल उपचार उपकरण 3-100 टन/घंटा	औद्योगिक RO जल उपचार	Yuchen Water का बड़ा औद्योगिक RO जल उपचार उपकरण कारखानों, जल संयंत्रों, होटलों और B2B परियोजना ठेकेदारों के लिए बनाया गया है जिन्हें 3-100 टन/घंटा स्थिर शुद्ध जल उत्पादन चाहिए। यह प्रणाली तीन-स्तरीय प्री-ट्रीटमेंट, रिवर्स ऑस्मोसिस, पूर्ण स्वचालित बुद्धिमान संचालन, पानी न होने पर सुरक्षा, ओवरलोड सुरक्षा और नल के पानी या भूजल के लिए अनुकूलित प्रक्रिया मॉड्यूल जोड़ती है।	3-100 टन/घंटा प्रवाह वाला बड़ा औद्योगिक RO सिस्टम, स्वचालित नियंत्रण, अनुकूलित प्री-ट्रीटमेंट और OEM परियोजनाओं के लिए UPVC/304 पाइपिंग विकल्प।	उत्पाद प्रकार|संचालन मोड|उपचार प्रक्रिया|शुद्ध जल प्रवाह|फीड वाटर|पाइप सामग्री|सुरक्षा कार्य|नियंत्रण|अनुप्रयोग|OEM/ODM|MOQ	पूर्ण स्वचालित बुद्धिमान संचालन, परियोजना आवश्यकता के अनुसार मैनुअल सेवा मोड	तीन-स्तरीय प्री-ट्रीटमेंट और रिवर्स ऑस्मोसिस; जल विश्लेषण के अनुसार प्रक्रिया अनुकूलित	नल का पानी और भूजल	UPVC या परियोजना मानक के अनुसार 304 स्टेनलेस स्टील	पानी न होने की सुरक्षा, ओवरलोड सुरक्षा और अलार्म इंटरफेस	PLC या कंट्रोल पैनल ग्राहक की आवश्यकता के अनुसार अनुकूलित	कारखाने, जल संयंत्र, होटल, खाद्य प्रसंस्करण और औद्योगिक शुद्ध जल परियोजनाएँ	प्रवाह, पंप, मेम्ब्रेन, टैंक, पाइप सामग्री, वोल्टेज, पैनल भाषा और पैकिंग अनुकूलित	क्षमता, कॉन्फ़िगरेशन और OEM स्तर के अनुसार पुष्टि
hr	Velika industrijska RO oprema za obradu vode 3-100 t/h	Industrijska RO obrada vode	Velika industrijska RO oprema za obradu vode Yuchen Water namijenjena je tvornicama, vodnim postrojenjima, hotelima i B2B izvođačima kojima treba stabilan izlaz pročišćene vode od 3-100 t/h. Sustav kombinira trostupanjsku predobradu s reverznom osmozom, potpuno automatski inteligentni rad, zaštitu od rada bez vode i preopterećenja te procesne module prilagođene vodovodnoj ili podzemnoj vodi.	Veliki industrijski RO sustav s protokom 3-100 t/h, automatskim upravljanjem, prilagođenom predobradom i UPVC/304 cjevovodom za OEM projekte.	Tip proizvoda|Način rada|Proces obrade|Protok čiste vode|Ulazna voda|Materijal cjevovoda|Zaštitne funkcije|Upravljanje|Primjena|OEM/ODM|MOQ	Potpuno automatski inteligentni rad s ručnim servisnim načinom prema projektu	Trostupanjska predobrada plus reverzna osmoza; proces se prilagođava analizi vode	Vodovodna voda i podzemna voda	UPVC ili nehrđajući čelik 304 prema standardu projekta	Zaštita bez vode, zaštita od preopterećenja i alarmna sučelja	PLC ili upravljačka ploča može se prilagoditi zahtjevu kupca	Tvornice, vodna postrojenja, hoteli, prehrambena industrija i industrijski projekti čiste vode	Protok, pumpa, membrana, spremnici, cjevovod, napon, jezik panela i pakiranje prilagodljivi	Potvrđuje se prema kapacitetu, konfiguraciji i OEM razini
hu	Nagy ipari RO vízkezelő berendezés 3-100 t/h	Ipari RO vízkezelés	A Yuchen Water nagy ipari RO vízkezelő berendezése gyárak, vízkezelő telepek, szállodák és B2B projektkivitelezők számára készült, akiknek 3-100 t/h stabil tisztított vízre van szükségük. A rendszer háromlépcsős előkezelést, fordított ozmózist, teljesen automatikus intelligens működést, vízhiány- és túlterhelésvédelmet, valamint csapvízhez vagy talajvízhez igazítható folyamatmodulokat egyesít.	Nagy ipari RO rendszer 3-100 t/h átfolyással, automatikus vezérléssel, testreszabott előkezeléssel és UPVC/304 csőopciókkal OEM projektekhez.	Terméktípus|Üzemmód|Kezelési folyamat|Tisztavíz átfolyás|Betáplált víz|Csőanyag|Védelmi funkciók|Vezérlés|Alkalmazás|OEM/ODM|MOQ	Teljesen automatikus intelligens működés, kézi szerviz móddal projekt szerint	Háromlépcsős előkezelés plusz fordított ozmózis; a folyamat vízelemzés alapján testreszabott	Csapvíz és talajvíz	UPVC vagy 304 rozsdamentes acél a projekt szabványa szerint	Vízhiány-védelem, túlterhelés-védelem és riasztási interfészek	PLC vagy vezérlőpanel a vevő igénye szerint testreszabható	Gyárak, vízüzemek, szállodák, élelmiszeripar és ipari tisztavíz projektek	Átfolyás, szivattyú, membrán, tartályok, csőanyag, feszültség, panelnyelv és csomagolás testreszabható	Kapacitás, konfiguráció és OEM szint szerint igazoljuk
hy	Մեծ արդյունաբերական RO ջրի մաքրման սարքավորում 3-100 տ/ժ	Արդյունաբերական RO ջրի մաքրում	Yuchen Water-ի մեծ արդյունաբերական RO ջրի մաքրման սարքավորումը նախատեսված է գործարանների, ջրային կայանների, հյուրանոցների և B2B նախագծային կապալառուների համար, որոնք պահանջում են կայուն մաքրված ջուր 3-100 տ/ժ արտադրողականությամբ։ Համակարգը միավորում է եռաստիճան նախամաքրում, հակադարձ օսմոս, լիովին ավտոմատ խելացի աշխատանք, ջրի բացակայության և գերբեռնման պաշտպանություն և ջրի աղբյուրին համապատասխանեցվող գործընթացային մոդուլներ։	Մեծ արդյունաբերական RO համակարգ 3-100 տ/ժ հոսքով, ավտոմատ կառավարումով, հարմարեցվող նախամաքրումով և UPVC/304 խողովակային ընտրանքներով OEM նախագծերի համար։	Ապրանքի տեսակ|Աշխատանքի ռեժիմ|Մշակման գործընթաց|Մաքուր ջրի հոսք|Մուտքային ջուր|Խողովակների նյութ|Պաշտպանական գործառույթներ|Կառավարում|Կիրառություն|OEM/ODM|MOQ	Լիովին ավտոմատ խելացի աշխատանք՝ ձեռքով սպասարկման ռեժիմով ըստ նախագծի	Եռաստիճան նախամաքրում և հակադարձ օսմոս; գործընթացը հարմարեցվում է ջրի վերլուծությանը	Ծորակի ջուր և ստորերկրյա ջուր	UPVC կամ 304 չժանգոտվող պողպատ ըստ նախագծի ստանդարտի	Ջրի բացակայության պաշտպանություն, գերբեռնման պաշտպանություն և ահազանգի ինտերֆեյսներ	PLC կամ կառավարման վահանակը հարմարեցվում է հաճախորդի պահանջին	Գործարաններ, ջրի կայաններ, հյուրանոցներ, սննդի արտադրություն և արդյունաբերական մաքուր ջրի նախագծեր	Հոսք, պոմպ, մեմբրան, բաքեր, խողովակներ, լարում, վահանակի լեզու և փաթեթավորում հնարավոր է հարմարեցնել	Հաստատվում է ըստ արտադրողականության, կոնֆիգուրացիայի և OEM մակարդակի
id	Peralatan pengolahan air RO industri besar 3-100 t/jam	Pengolahan air RO industri	Peralatan pengolahan air RO industri besar Yuchen Water dibuat untuk pabrik, instalasi air, hotel dan kontraktor proyek B2B yang membutuhkan keluaran air murni stabil 3-100 t/jam. Sistem ini menggabungkan pretreatment tiga tahap dengan reverse osmosis, operasi cerdas otomatis penuh, perlindungan tanpa air, perlindungan beban berlebih dan modul proses yang dapat disesuaikan untuk air PDAM atau air tanah.	Sistem RO industri besar dengan aliran 3-100 t/jam, kontrol otomatis, pretreatment khusus dan opsi pipa UPVC/304 untuk proyek OEM.	Jenis produk|Mode operasi|Proses pengolahan|Aliran air murni|Air baku|Material pipa|Fungsi perlindungan|Kontrol|Aplikasi|OEM/ODM|MOQ	Operasi cerdas otomatis penuh, dengan mode servis manual sesuai kebutuhan proyek	Pretreatment tiga tahap plus reverse osmosis; proses disesuaikan berdasarkan analisis air	Air PDAM dan air tanah	UPVC atau stainless steel 304 sesuai standar proyek	Perlindungan tanpa air, perlindungan beban berlebih dan antarmuka alarm	PLC atau panel kontrol dapat disesuaikan dengan kebutuhan pembeli	Pabrik, instalasi air, hotel, pengolahan makanan dan proyek air murni industri	Aliran, pompa, membran, tangki, material pipa, tegangan, bahasa panel dan kemasan dapat disesuaikan	Dikonfirmasi menurut kapasitas, konfigurasi dan level OEM
it	Grande impianto industriale RO per trattamento acqua 3-100 t/h	Trattamento acqua industriale RO	Il grande impianto industriale RO per trattamento acqua di Yuchen Water è progettato per fabbriche, impianti idrici, hotel e appaltatori B2B che richiedono acqua purificata stabile da 3-100 t/h. Il sistema combina pretrattamento a tre stadi con osmosi inversa, funzionamento intelligente completamente automatico, protezione mancanza acqua, protezione sovraccarico e moduli di processo personalizzabili per acqua di rete o di pozzo.	Grande sistema RO industriale con portata 3-100 t/h, controllo automatico, pretrattamento personalizzabile e tubazioni UPVC/304 per progetti OEM.	Tipo di prodotto|Modalità operativa|Processo di trattamento|Portata acqua pura|Acqua in ingresso|Materiale tubazioni|Funzioni di protezione|Controllo|Applicazione|OEM/ODM|MOQ	Funzionamento intelligente completamente automatico, con modalità di servizio manuale secondo il progetto	Pretrattamento a tre stadi più osmosi inversa; processo personalizzato secondo analisi dell'acqua	Acqua di rete e acqua sotterranea	UPVC o acciaio inox 304 secondo standard di progetto	Protezione mancanza acqua, protezione sovraccarico e interfacce allarme	PLC o pannello di controllo personalizzabile secondo richiesta cliente	Fabbriche, impianti idrici, hotel, alimentare e progetti industriali di acqua pura	Portata, pompa, membrana, serbatoi, tubazioni, tensione, lingua pannello e imballo personalizzabili	Confermato secondo capacità, configurazione e livello OEM
ja	大型産業用RO水処理設備 3-100トン/時	産業用RO水処理	Yuchen Waterの大型産業用RO水処理設備は、3-100トン/時の安定した純水供給を必要とする工場、水処理プラント、ホテル、B2Bプロジェクト業者向けに設計されています。三段階前処理と逆浸透膜分離を組み合わせ、全自動インテリジェント運転、無水保護、過負荷保護、水道水または地下水に合わせたカスタムプロセスに対応します。	3-100トン/時対応の大型産業用ROシステム。自動制御、カスタム前処理、UPVC/304配管をOEM案件向けに設定可能。	製品タイプ|運転方式|処理プロセス|純水流量|原水|配管材質|保護機能|制御|用途|OEM/ODM|MOQ	全自動インテリジェント運転、プロジェクトに応じた手動サービスモード	三段階前処理＋逆浸透膜。水質分析に基づき浄化プロセスをカスタム設定	水道水、地下水	UPVC または 304 ステンレス、プロジェクト基準に合わせて選定	無水保護、過負荷保護、アラームインターフェース	PLC または制御盤を購入者仕様に合わせてカスタム可能	工場、水処理プラント、ホテル、食品加工、産業用純水プロジェクト	流量、ポンプ、膜、タンク、配管材質、電圧、パネル言語、梱包をカスタム可能	能力、構成、OEMレベルにより確認
ka	დიდი სამრეწველო RO წყლის დამუშავების მოწყობილობა 3-100 ტ/სთ	სამრეწველო RO წყლის დამუშავება	Yuchen Water-ის დიდი სამრეწველო RO წყლის დამუშავების მოწყობილობა განკუთვნილია ქარხნებისთვის, წყლის სადგურებისთვის, სასტუმროებისა და B2B პროექტის შემსრულებლებისთვის, რომლებსაც სჭირდებათ სტაბილური სუფთა წყლის გამომუშავება 3-100 ტ/სთ. სისტემა აერთიანებს სამსაფეხურიან წინასწარ დამუშავებას, უკუ ოსმოსს, სრულ ავტომატურ ჭკვიან მუშაობას, წყლის არარსებობისა და გადატვირთვის დაცვას და პროცესის მორგებად მოდულებს ონკანის ან მიწისქვეშა წყლისთვის.	დიდი სამრეწველო RO სისტემა 3-100 ტ/სთ ნაკადით, ავტომატური მართვით, მორგებადი წინასწარი დამუშავებით და UPVC/304 მილებით OEM პროექტებისთვის.	პროდუქტის ტიპი|მუშაობის რეჟიმი|დამუშავების პროცესი|სუფთა წყლის ნაკადი|შემავალი წყალი|მილების მასალა|დაცვის ფუნქციები|მართვა|გამოყენება|OEM/ODM|MOQ	სრული ავტომატური ჭკვიანი მუშაობა, ხელით მომსახურების რეჟიმით პროექტის მიხედვით	სამსაფეხურიანი წინასწარი დამუშავება და უკუ ოსმოსი; პროცესი მორგებულია წყლის ანალიზზე	ონკანის წყალი და მიწისქვეშა წყალი	UPVC ან 304 უჟანგავი ფოლადი პროექტის სტანდარტის მიხედვით	წყლის არყოფნის დაცვა, გადატვირთვის დაცვა და განგაშის ინტერფეისები	PLC ან მართვის პანელი მორგებადია მყიდველის მოთხოვნით	ქარხნები, წყლის სადგურები, სასტუმროები, საკვების წარმოება და სამრეწველო სუფთა წყლის პროექტები	ნაკადი, ტუმბო, მემბრანა, ავზები, მილები, ძაბვა, პანელის ენა და შეფუთვა მორგებადია	დადასტურდება სიმძლავრის, კონფიგურაციისა და OEM დონის მიხედვით
kk	3-100 т/сағ ірі өнеркәсіптік RO су тазарту жабдығы	Өнеркәсіптік RO су тазарту	Yuchen Water ірі өнеркәсіптік RO су тазарту жабдығы 3-100 т/сағ тұрақты тазартылған су қажет зауыттар, су станциялары, қонақ үйлер және B2B жобалық мердігерлер үшін жасалған. Жүйе үш сатылы алдын ала өңдеу мен кері осмосты, толық автоматты интеллектуалды жұмысты, сусыз қорғауды, артық жүктемеден қорғауды және су құбыры немесе жер асты суына бейімделетін процесс модульдерін біріктіреді.	3-100 т/сағ ірі өнеркәсіптік RO жүйесі, автоматты басқару, теңшелетін алдын ала өңдеу және OEM жобаларына арналған UPVC/304 құбыр нұсқалары.	Өнім түрі|Жұмыс режимі|Тазарту процесі|Таза су ағыны|Кіріс суы|Құбыр материалы|Қорғау функциялары|Басқару|Қолданылуы|OEM/ODM|MOQ	Толық автоматты интеллектуалды жұмыс, жобаға қарай қолмен қызмет көрсету режимі	Үш сатылы алдын ала өңдеу және кері осмос; процесс су талдауына қарай теңшеледі	Су құбыры суы және жер асты суы	UPVC немесе жоба стандартына қарай 304 тот баспайтын болат	Сусыз қорғау, артық жүктемеден қорғау және дабыл интерфейстері	PLC немесе басқару панелі сатып алушы талабына сай теңшеледі	Зауыттар, су станциялары, қонақ үйлер, тағам өңдеу және өнеркәсіптік таза су жобалары	Ағын, сорғы, мембрана, бактар, құбыр материалы, кернеу, панель тілі және қаптама теңшеледі	Қуаттылық, конфигурация және OEM деңгейі бойынша расталады
ko	대형 산업용 RO 수처리 설비 3-100톤/시간	산업용 RO 수처리	Yuchen Water 대형 산업용 RO 수처리 설비는 3-100톤/시간의 안정적인 정제수 생산이 필요한 공장, 정수 플랜트, 호텔 및 B2B 프로젝트 시공사를 위해 제작됩니다. 이 시스템은 3단계 전처리와 역삼투 분리를 결합하고, 완전 자동 지능 운전, 무수 보호, 과부하 보호, 수돗물 또는 지하수에 맞춘 맞춤 공정 모듈을 제공합니다.	3-100톤/시간 대형 산업용 RO 시스템, 자동 제어, 맞춤 전처리 및 OEM 프로젝트용 UPVC/304 배관 옵션.	제품 유형|운전 방식|처리 공정|순수 유량|원수|배관 재질|보호 기능|제어|용도|OEM/ODM|MOQ	완전 자동 지능 운전, 프로젝트 필요에 따른 수동 서비스 모드	3단계 전처리와 역삼투; 수질 분석에 따라 정화 공정 맞춤	수돗물 및 지하수	UPVC 또는 프로젝트 기준에 따른 304 스테인리스	무수 보호, 과부하 보호 및 알람 인터페이스	PLC 또는 제어 패널은 구매자 요구에 맞게 맞춤 가능	공장, 정수 플랜트, 호텔, 식품 가공 및 산업용 순수 프로젝트	유량, 펌프, 멤브레인, 탱크, 배관 재질, 전압, 패널 언어 및 포장 맞춤 가능	용량, 구성 및 OEM 수준에 따라 확인
ku	Amûra mezin a pîşesazî ya RO ji bo paqijkirina avê 3-100 t/saet	Paqijkirina ava pîşesazî ya RO	Amûra mezin a RO ya Yuchen Water ji bo kargeh, stasyonên avê, otel û peymankarên B2B hatiye çêkirin ku avê paqij a bi derketina 3-100 t/saet dixwazin. Pergal pêşparastina sê-aste, reverse osmosis, xebata aqilmend a tev-otomatik, parastina bê-av, parastina barê zêde û modulên prosesê yên taybet ji bo ava şebekê an ava binerdê digihîne hev.	Pergala RO ya pîşesazî 3-100 t/saet, kontrola otomatik, pêşparastina taybet û hilbijarkên boriyên UPVC/304 ji bo projeyên OEM.	Cureyê hilberê|Moda xebatê|Proseya paqijkirinê|Herikîna ava paqij|Ava têketinê|Materyala boriyan|Fonksiyonên parastinê|Kontrol|Bikaranîn|OEM/ODM|MOQ	Xebata aqilmend a tev-otomatik, bi moda servîsa destan li gor pêdiviya proje	Pêşparastina sê-aste û reverse osmosis; proses li gor analîza avê tê taybetkirin	Ava şebekê û ava binerdê	UPVC an pola nezerav 304 li gor standarda proje	Parastina bê-av, parastina barê zêde û navrûyên alarmê	PLC an panela kontrolê li gor daxwaza kirrûbarê tê taybetkirin	Kargeh, stasyonên avê, otel, xwarinçêkirin û projeyên ava paqij a pîşesazî	Herikîn, pomp, membrane, tank, bori, voltaj, zimanê panelê û pakkirin dikarin taybet bibin	Li gor kapasîte, konfigurasyon û asta OEM tê piştrastkirin
ky	3-100 т/саат ири өнөр жай RO суу тазалоо жабдуусу	Өнөр жай RO суу тазалоо	Yuchen Water ири өнөр жай RO суу тазалоо жабдуусу 3-100 т/саат туруктуу таза суу талап кылган заводдор, суу станциялары, мейманканалар жана B2B долбоор подрядчылары үчүн жасалган. Система үч баскычтуу алдын ала тазалоону, тескери осмосту, толук автоматтык акылдуу иштөөнү, суусуз коргоону, ашыкча жүктөмдөн коргоону жана кран суусу же жер астындагы сууга ылайыкташкан процесс модулдарын бириктирет.	3-100 т/саат ири өнөр жай RO системасы, автоматтык башкаруу, ылайыкташкан алдын ала тазалоо жана OEM долбоорлору үчүн UPVC/304 түтүк варианттары.	Өнүм түрү|Иштөө режими|Тазалоо процесси|Таза суу агымы|Кирүүчү суу|Түтүк материалы|Коргоо функциялары|Башкаруу|Колдонуу|OEM/ODM|MOQ	Толук автоматтык акылдуу иштөө, долбоорго жараша кол менен тейлөө режими	Үч баскычтуу алдын ала тазалоо жана тескери осмос; процесс суу анализине жараша ылайыкташат	Кран суусу жана жер астындагы суу	UPVC же долбоор стандартына ылайык 304 дат баспас болот	Суусуз коргоо, ашыкча жүктөмдөн коргоо жана сигнал интерфейстери	PLC же башкаруу панели сатып алуучу талаптарына ылайыкташат	Заводдор, суу станциялары, мейманканалар, тамак-аш иштетүү жана өнөр жай таза суу долбоорлору	Агым, насос, мембрана, бактар, түтүк материалы, чыңалуу, панель тили жана таңгак ылайыкташат	Кубаттуулук, конфигурация жана OEM деңгээли боюнча такталат
lt	Didelė pramoninė RO vandens valymo įranga 3-100 t/h	Pramoninis RO vandens valymas	Yuchen Water didelė pramoninė RO vandens valymo įranga skirta gamykloms, vandens stotims, viešbučiams ir B2B projektų rangovams, kuriems reikia stabilaus išvalyto vandens 3-100 t/h. Sistema jungia trijų pakopų pirminį valymą su atvirkštiniu osmosu, pilnai automatinį išmanų veikimą, apsaugą nuo vandens trūkumo ir perkrovos bei procesų modulius, pritaikomus vandentiekio ar požeminiam vandeniui.	Didelė pramoninė RO sistema 3-100 t/h srautui, automatiniu valdymu, individualiu pirminiu valymu ir UPVC/304 vamzdžių opcijomis OEM projektams.	Produkto tipas|Veikimo režimas|Valymo procesas|Švaraus vandens srautas|Tiekiamas vanduo|Vamzdžių medžiaga|Apsaugos funkcijos|Valdymas|Pritaikymas|OEM/ODM|MOQ	Pilnai automatinis išmanus veikimas, su rankiniu aptarnavimo režimu pagal projektą	Trijų pakopų pirminis valymas ir atvirkštinis osmosas; procesas pritaikomas pagal vandens analizę	Vandentiekio vanduo ir požeminis vanduo	UPVC arba 304 nerūdijantis plienas pagal projekto standartą	Apsauga nuo vandens trūkumo, perkrovos ir signalizacijos sąsajos	PLC arba valdymo pultas gali būti pritaikytas pagal pirkėjo reikalavimus	Gamyklos, vandens stotys, viešbučiai, maisto perdirbimas ir pramoninio švaraus vandens projektai	Srautas, siurblys, membrana, talpos, vamzdžiai, įtampa, pulto kalba ir pakuotė pritaikomi	Tvirtinama pagal pajėgumą, konfigūraciją ir OEM lygį
lv	Liela rūpnieciska RO ūdens attīrīšanas iekārta 3-100 t/h	Rūpnieciska RO ūdens attīrīšana	Yuchen Water lielā rūpnieciskā RO ūdens attīrīšanas iekārta ir paredzēta rūpnīcām, ūdens stacijām, viesnīcām un B2B projektu darbuzņēmējiem, kam vajadzīga stabila attīrīta ūdens ražība 3-100 t/h. Sistēma apvieno trīspakāpju priekšattīrīšanu ar reverso osmozi, pilnībā automātisku inteliģentu darbību, aizsardzību bez ūdens un pārslodzes gadījumā, kā arī procesus, kas pielāgojami krāna vai pazemes ūdenim.	Liela rūpnieciska RO sistēma ar 3-100 t/h plūsmu, automātisku vadību, pielāgotu priekšattīrīšanu un UPVC/304 cauruļvadu opcijām OEM projektiem.	Produkta tips|Darbības režīms|Attīrīšanas process|Tīrā ūdens plūsma|Ievades ūdens|Cauruļvadu materiāls|Aizsardzības funkcijas|Vadība|Pielietojums|OEM/ODM|MOQ	Pilnībā automātiska inteliģenta darbība, ar manuālu servisa režīmu pēc projekta vajadzības	Trīspakāpju priekšattīrīšana plus reversā osmoze; process pielāgots ūdens analīzei	Krāna ūdens un pazemes ūdens	UPVC vai 304 nerūsējošais tērauds pēc projekta standarta	Aizsardzība bez ūdens, pārslodzes aizsardzība un trauksmes saskarnes	PLC vai vadības paneli var pielāgot pircēja prasībām	Rūpnīcas, ūdens stacijas, viesnīcas, pārtikas pārstrāde un rūpnieciska tīra ūdens projekti	Plūsma, sūknis, membrāna, tvertnes, caurules, spriegums, paneļa valoda un iepakojums pielāgojami	Apstiprina pēc jaudas, konfigurācijas un OEM līmeņa
ms	Peralatan rawatan air RO industri besar 3-100 t/jam	Rawatan air RO industri	Peralatan rawatan air RO industri besar Yuchen Water direka untuk kilang, loji air, hotel dan kontraktor projek B2B yang memerlukan keluaran air tulen stabil 3-100 t/jam. Sistem ini menggabungkan prarawatan tiga tahap dengan osmosis songsang, operasi pintar automatik penuh, perlindungan tiada air, perlindungan beban lampau dan modul proses tersuai untuk air paip atau air bawah tanah.	Sistem RO industri besar dengan aliran 3-100 t/jam, kawalan automatik, prarawatan tersuai dan pilihan paip UPVC/304 untuk projek OEM.	Jenis produk|Mod operasi|Proses rawatan|Aliran air tulen|Air suapan|Bahan paip|Fungsi perlindungan|Kawalan|Aplikasi|OEM/ODM|MOQ	Operasi pintar automatik penuh, dengan mod servis manual mengikut keperluan projek	Prarawatan tiga tahap serta osmosis songsang; proses disesuaikan mengikut analisis air	Air paip dan air bawah tanah	UPVC atau keluli tahan karat 304 mengikut standard projek	Perlindungan tiada air, perlindungan beban lampau dan antara muka penggera	PLC atau panel kawalan boleh disesuaikan mengikut keperluan pembeli	Kilang, loji air, hotel, pemprosesan makanan dan projek air tulen industri	Aliran, pam, membran, tangki, bahan paip, voltan, bahasa panel dan pembungkusan boleh disesuaikan	Disahkan mengikut kapasiti, konfigurasi dan tahap OEM
nl	Grote industriële RO-waterbehandelingsinstallatie 3-100 t/h	Industriële RO-waterbehandeling	De grote industriële RO-waterbehandelingsinstallatie van Yuchen Water is gebouwd voor fabrieken, waterstations, hotels en B2B-projectaannemers die stabiel gezuiverd water van 3-100 t/h nodig hebben. Het systeem combineert drietraps voorbehandeling met omgekeerde osmose, volledig automatische intelligente werking, droogloopbeveiliging, overbelastingsbeveiliging en procesmodules voor leidingwater of grondwater.	Groot industrieel RO-systeem met 3-100 t/h debiet, automatische besturing, aangepaste voorbehandeling en UPVC/304 leidingopties voor OEM-projecten.	Producttype|Bedrijfsmodus|Behandelingsproces|Zuiverwaterdebiet|Voedingswater|Leidingmateriaal|Beveiligingsfuncties|Besturing|Toepassing|OEM/ODM|MOQ	Volledig automatische intelligente werking, met handmatige servicemodus volgens projectbehoefte	Drietraps voorbehandeling plus omgekeerde osmose; proces wordt aangepast volgens wateranalyse	Leidingwater en grondwater	UPVC of 304 roestvast staal volgens projectstandaard	Droogloopbeveiliging, overbelastingsbeveiliging en alarminterfaces	PLC of bedieningspaneel kan worden aangepast aan koperseisen	Fabrieken, waterstations, hotels, voedselverwerking en industriële zuiverwaterprojecten	Debiet, pomp, membraan, tanks, leidingmateriaal, spanning, paneeltaal en verpakking aanpasbaar	Bevestigd volgens capaciteit, configuratie en OEM-niveau
no	Stort industrielt RO-vannbehandlingsanlegg 3-100 t/h	Industriell RO-vannbehandling	Yuchen Water stort industrielt RO-vannbehandlingsanlegg er utviklet for fabrikker, vannverk, hoteller og B2B-prosjektleverandører som trenger stabilt renset vann på 3-100 t/h. Systemet kombinerer tretrinns forbehandling med omvendt osmose, fullautomatisk intelligent drift, beskyttelse mot vannmangel og overbelastning samt prosessmoduler tilpasset springvann eller grunnvann.	Stort industrielt RO-system med 3-100 t/h strømning, automatisk styring, tilpasset forbehandling og UPVC/304 røralternativer for OEM-prosjekter.	Produkttype|Driftsmodus|Behandlingsprosess|Rentvannsstrøm|Fødevann|Rørmateriale|Beskyttelsesfunksjoner|Styring|Bruksområde|OEM/ODM|MOQ	Fullautomatisk intelligent drift, med manuell servicemodus etter prosjektbehov	Tretrinns forbehandling pluss omvendt osmose; prosess tilpasses vannanalyse	Springvann og grunnvann	UPVC eller 304 rustfritt stål etter prosjektstandard	Vannmangelbeskyttelse, overbelastningsvern og alarmgrensesnitt	PLC eller kontrollpanel kan tilpasses kundens krav	Fabrikker, vannverk, hoteller, matbehandling og industrielle rentvannsprosjekter	Strømning, pumpe, membran, tanker, rørmateriale, spenning, panelspråk og emballasje kan tilpasses	Bekreftes etter kapasitet, konfigurasjon og OEM-nivå
pl	Duża przemysłowa instalacja RO do uzdatniania wody 3-100 t/h	Przemysłowe uzdatnianie wody RO	Duża przemysłowa instalacja RO Yuchen Water jest przeznaczona dla fabryk, stacji wody, hoteli i wykonawców projektów B2B, którzy potrzebują stabilnej produkcji wody oczyszczonej 3-100 t/h. System łączy trzystopniowe wstępne uzdatnianie z odwróconą osmozą, w pełni automatyczną inteligentną pracę, zabezpieczenie przed brakiem wody, przeciążeniem oraz moduły procesu dostosowane do wody wodociągowej lub gruntowej.	Duży przemysłowy system RO 3-100 t/h z automatycznym sterowaniem, dostosowanym pretratamentem i opcjami rur UPVC/304 dla projektów OEM.	Typ produktu|Tryb pracy|Proces uzdatniania|Przepływ wody czystej|Woda zasilająca|Materiał rur|Funkcje ochronne|Sterowanie|Zastosowanie|OEM/ODM|MOQ	W pełni automatyczna inteligentna praca z ręcznym trybem serwisowym według projektu	Trzystopniowe wstępne uzdatnianie plus odwrócona osmoza; proces dostosowany do analizy wody	Woda wodociągowa i gruntowa	UPVC lub stal nierdzewna 304 według standardu projektu	Ochrona przed brakiem wody, przeciążeniem i interfejsy alarmowe	PLC lub panel sterowania można dostosować do wymagań kupującego	Fabryki, stacje wody, hotele, przetwórstwo spożywcze i przemysłowe projekty wody czystej	Przepływ, pompa, membrana, zbiorniki, rury, napięcie, język panelu i opakowanie dostosowywane	Potwierdzane według wydajności, konfiguracji i poziomu OEM
pt	Equipamento industrial grande de tratamento de água RO 3-100 t/h	Tratamento industrial de água RO	O equipamento industrial grande de tratamento de água RO da Yuchen Water é desenvolvido para fábricas, estações de água, hotéis e contratantes B2B que precisam de água purificada estável de 3-100 t/h. O sistema combina pré-tratamento de três etapas com osmose reversa, operação inteligente totalmente automática, proteção contra falta de água, proteção contra sobrecarga e módulos de processo personalizáveis para água da rede ou subterrânea.	Sistema RO industrial grande com vazão 3-100 t/h, controle automático, pré-tratamento customizado e opções de tubulação UPVC/304 para projetos OEM.	Tipo de produto|Modo de operação|Processo de tratamento|Vazão de água pura|Água de alimentação|Material da tubulação|Funções de proteção|Controle|Aplicação|OEM/ODM|MOQ	Operação inteligente totalmente automática, com modo de serviço manual conforme o projeto	Pré-tratamento de três etapas mais osmose reversa; processo ajustado conforme análise da água	Água da rede e água subterrânea	UPVC ou aço inoxidável 304 conforme o padrão do projeto	Proteção contra falta de água, sobrecarga e interfaces de alarme	PLC ou painel de controle pode ser customizado conforme requisitos do comprador	Fábricas, estações de água, hotéis, processamento de alimentos e projetos industriais de água pura	Vazão, bomba, membrana, tanques, tubulação, tensão, idioma do painel e embalagem personalizáveis	Confirmado por capacidade, configuração e nível OEM
ro	Echipament industrial mare RO pentru tratarea apei 3-100 t/h	Tratare industrială a apei RO	Echipamentul industrial mare RO pentru tratarea apei de la Yuchen Water este construit pentru fabrici, stații de apă, hoteluri și contractori B2B care au nevoie de apă purificată stabilă la 3-100 t/h. Sistemul combină pretratarea în trei trepte cu osmoza inversă, funcționare inteligentă complet automată, protecție lipsă apă, protecție la suprasarcină și module de proces personalizabile pentru apă de rețea sau apă subterană.	Sistem industrial RO mare cu debit 3-100 t/h, control automat, pretratare personalizată și opțiuni de conducte UPVC/304 pentru proiecte OEM.	Tip produs|Mod de operare|Proces de tratare|Debit apă pură|Apă de alimentare|Material conducte|Funcții de protecție|Control|Aplicație|OEM/ODM|MOQ	Funcționare inteligentă complet automată, cu mod manual de service după proiect	Pretratare în trei trepte plus osmoză inversă; procesul se adaptează analizei apei	Apă de la rețea și apă subterană	UPVC sau oțel inoxidabil 304 conform standardului proiectului	Protecție lipsă apă, protecție la suprasarcină și interfețe de alarmă	PLC sau panou de control personalizabil după cerințele cumpărătorului	Fabrici, stații de apă, hoteluri, procesare alimentară și proiecte industriale de apă pură	Debit, pompă, membrană, rezervoare, conducte, tensiune, limbă panou și ambalare personalizabile	Confirmat după capacitate, configurație și nivel OEM
ru	Крупная промышленная установка обратного осмоса для водоочистки 3-100 т/ч	Промышленная RO водоочистка	Крупная промышленная установка обратного осмоса Yuchen Water предназначена для заводов, водоподготовительных станций, гостиниц и B2B проектных подрядчиков, которым нужен стабильный выпуск очищенной воды 3-100 т/ч. Система сочетает трехступенчатую предварительную подготовку и обратный осмос, полностью автоматический интеллектуальный режим, защиту от отсутствия воды, защиту от перегрузки и настраиваемую технологическую схему для водопроводной или подземной воды.	Крупная промышленная RO-система 3-100 т/ч с автоматическим управлением, настраиваемой предочисткой и трубопроводом UPVC/304 для OEM-проектов.	Тип продукта|Режим работы|Процесс водоочистки|Поток чистой воды|Исходная вода|Материал трубопровода|Функции защиты|Управление|Применение|OEM/ODM|MOQ	Полностью автоматическая интеллектуальная работа, с ручным сервисным режимом по проекту	Трехступенчатая предочистка плюс обратный осмос; технологическая схема настраивается по анализу воды	Водопроводная вода и подземная вода	UPVC или нержавеющая сталь 304 согласно стандарту проекта	Защита от отсутствия воды, защита от перегрузки и интерфейсы сигнализации	PLC или панель управления настраиваются под требования покупателя	Заводы, станции водоподготовки, гостиницы, пищевая промышленность и проекты промышленной чистой воды	Поток, насос, мембрана, баки, материал труб, напряжение, язык панели и упаковка настраиваются	Подтверждается по производительности, конфигурации и уровню OEM
sk	Veľké priemyselné RO zariadenie na úpravu vody 3-100 t/h	Priemyselná RO úprava vody	Veľké priemyselné RO zariadenie Yuchen Water je určené pre fabriky, vodárne, hotely a B2B projektových dodávateľov, ktorí potrebujú stabilný výstup čistej vody 3-100 t/h. Systém spája trojstupňovú predúpravu s reverznou osmózou, plne automatickú inteligentnú prevádzku, ochranu proti chodu bez vody a preťaženiu a procesné moduly prispôsobené vodovodnej alebo podzemnej vode.	Veľký priemyselný RO systém 3-100 t/h s automatickým riadením, prispôsobenou predúpravou a potrubím UPVC/304 pre OEM projekty.	Typ produktu|Prevádzkový režim|Proces úpravy|Prietok čistej vody|Vstupná voda|Materiál potrubia|Ochranné funkcie|Riadenie|Použitie|OEM/ODM|MOQ	Plne automatická inteligentná prevádzka s ručným servisným režimom podľa projektu	Trojstupňová predúprava plus reverzná osmóza; proces sa prispôsobí analýze vody	Vodovodná voda a podzemná voda	UPVC alebo nehrdzavejúca oceľ 304 podľa štandardu projektu	Ochrana bez vody, ochrana proti preťaženiu a alarmové rozhrania	PLC alebo ovládací panel možno upraviť podľa požiadaviek kupujúceho	Fabriky, vodárne, hotely, potravinárstvo a priemyselné projekty čistej vody	Prietok, čerpadlo, membrána, nádrže, potrubie, napätie, jazyk panela a balenie prispôsobiteľné	Potvrdzuje sa podľa kapacity, konfigurácie a úrovne OEM
sl	Velika industrijska RO oprema za obdelavo vode 3-100 t/h	Industrijska RO obdelava vode	Velika industrijska RO oprema za obdelavo vode Yuchen Water je namenjena tovarnam, vodnim postajam, hotelom in B2B projektantskim izvajalcem, ki potrebujejo stabilen izhod prečiščene vode 3-100 t/h. Sistem združuje tristopenjsko predobdelavo z reverzno osmozo, popolnoma avtomatsko inteligentno delovanje, zaščito pred pomanjkanjem vode in preobremenitvijo ter procesne module po meri za vodovodno ali podtalno vodo.	Velik industrijski RO sistem s pretokom 3-100 t/h, avtomatskim nadzorom, prilagojeno predobdelavo in UPVC/304 cevmi za OEM projekte.	Tip izdelka|Način delovanja|Proces obdelave|Pretok čiste vode|Napajalna voda|Material cevi|Zaščitne funkcije|Nadzor|Uporaba|OEM/ODM|MOQ	Popolnoma avtomatsko inteligentno delovanje z ročnim servisnim načinom po projektu	Tristopenjska predobdelava plus reverzna osmoza; proces se prilagodi analizi vode	Vodovodna voda in podtalna voda	UPVC ali nerjavno jeklo 304 po standardu projekta	Zaščita brez vode, zaščita pred preobremenitvijo in alarmni vmesniki	PLC ali nadzorna plošča se prilagodi zahtevam kupca	Tovarne, vodne postaje, hoteli, živilska industrija in industrijski projekti čiste vode	Pretok, črpalka, membrana, rezervoarji, cevi, napetost, jezik plošče in embalaža so prilagodljivi	Potrdi se glede na kapaciteto, konfiguracijo in OEM raven
sq	Pajisje e madhe industriale RO për trajtimin e ujit 3-100 t/orë	Trajtim industrial uji RO	Pajisja e madhe industriale RO e Yuchen Water është projektuar për fabrika, impiante uji, hotele dhe kontraktorë B2B që kërkojnë ujë të pastruar të qëndrueshëm 3-100 t/orë. Sistemi kombinon paratrajtim me tre faza me osmozë të kundërt, funksionim inteligjent plotësisht automatik, mbrojtje pa ujë, mbrojtje nga mbingarkesa dhe module procesi të personalizuara për ujë rubineti ose ujë nëntokësor.	Sistem i madh industrial RO me prurje 3-100 t/orë, kontroll automatik, paratrajtim të personalizuar dhe tuba UPVC/304 për projekte OEM.	Lloji i produktit|Mënyra e punës|Procesi i trajtimit|Prurja e ujit të pastër|Uji hyrës|Materiali i tubave|Funksionet mbrojtëse|Kontrolli|Aplikimi|OEM/ODM|MOQ	Funksionim inteligjent plotësisht automatik, me modalitet shërbimi manual sipas projektit	Paratrajtim me tre faza plus osmozë e kundërt; procesi përshtatet sipas analizës së ujit	Ujë rubineti dhe ujë nëntokësor	UPVC ose çelik inox 304 sipas standardit të projektit	Mbrojtje pa ujë, mbrojtje nga mbingarkesa dhe ndërfaqe alarmi	PLC ose panel kontrolli i personalizuar sipas kërkesës së blerësit	Fabrika, impiante uji, hotele, përpunim ushqimi dhe projekte industriale uji të pastër	Prurja, pompa, membrana, rezervuarët, tubat, tensioni, gjuha e panelit dhe paketimi personalizohen	Konfirmohet sipas kapacitetit, konfigurimit dhe nivelit OEM
sr	Велика индустријска RO опрема за третман воде 3-100 т/ч	Индустријски RO третман воде	Велика индустријска RO опрема Yuchen Water намењена је фабрикама, водним постројењима, хотелима и B2B извођачима којима је потребан стабилан излаз пречишћене воде 3-100 т/ч. Систем комбинује тростепени предтретман са реверзном осмозом, потпуно аутоматски интелигентан рад, заштиту од рада без воде и преоптерећења и процесне модуле прилагођене водоводној или подземној води.	Велики индустријски RO систем 3-100 т/ч са аутоматским управљањем, прилагођеним предтретманом и UPVC/304 цевима за OEM пројекте.	Тип производа|Режим рада|Процес третмана|Проток чисте воде|Улазна вода|Материјал цеви|Заштитне функције|Управљање|Примена|OEM/ODM|MOQ	Потпуно аутоматски интелигентан рад, са ручним сервисним режимом по пројекту	Тростепени предтретман плус реверзна осмоза; процес се прилагођава анализи воде	Водоводна вода и подземна вода	UPVC или нерђајући челик 304 према стандарду пројекта	Заштита без воде, заштита од преоптерећења и алармни интерфејси	PLC или контролна табла може се прилагодити захтеву купца	Фабрике, водна постројења, хотели, прехрамбена индустрија и индустријски пројекти чисте воде	Проток, пумпа, мембрана, резервоари, цеви, напон, језик панела и паковање прилагодљиви	Потврђује се према капацитету, конфигурацији и OEM нивоу
sr-me	Velika industrijska RO oprema za tretman vode 3-100 t/h	Industrijski RO tretman vode	Velika industrijska RO oprema Yuchen Water namijenjena je fabrikama, vodnim postrojenjima, hotelima i B2B izvođačima kojima je potreban stabilan izlaz prečišćene vode 3-100 t/h. Sistem kombinuje trostepeni predtretman sa reverznom osmozom, potpuno automatski inteligentan rad, zaštitu od rada bez vode i preopterećenja i procesne module prilagođene vodovodnoj ili podzemnoj vodi.	Veliki industrijski RO sistem 3-100 t/h sa automatskim upravljanjem, prilagođenim predtretmanom i UPVC/304 cijevima za OEM projekte.	Tip proizvoda|Režim rada|Proces tretmana|Protok čiste vode|Ulazna voda|Materijal cijevi|Zaštitne funkcije|Upravljanje|Primjena|OEM/ODM|MOQ	Potpuno automatski inteligentan rad, sa ručnim servisnim režimom po projektu	Trostepeni predtretman plus reverzna osmoza; proces se prilagođava analizi vode	Vodovodna voda i podzemna voda	UPVC ili nerđajući čelik 304 prema standardu projekta	Zaštita bez vode, zaštita od preopterećenja i alarmni interfejsi	PLC ili kontrolna tabla može se prilagoditi zahtjevu kupca	Fabrike, vodna postrojenja, hoteli, prehrambena industrija i industrijski projekti čiste vode	Protok, pumpa, membrana, rezervoari, cijevi, napon, jezik panela i pakovanje prilagodljivi	Potvrđuje se prema kapacitetu, konfiguraciji i OEM nivou
sv	Stor industriell RO-vattenbehandlingsutrustning 3-100 t/h	Industriell RO-vattenbehandling	Yuchen Water stor industriell RO-vattenbehandlingsutrustning är byggd för fabriker, vattenverk, hotell och B2B-projektentreprenörer som behöver stabilt renat vatten på 3-100 t/h. Systemet kombinerar trestegs förbehandling med omvänd osmos, helautomatisk intelligent drift, skydd mot vattenbrist och överbelastning samt processmoduler anpassade för kranvatten eller grundvatten.	Stor industriell RO-anläggning med 3-100 t/h flöde, automatisk styrning, anpassad förbehandling och UPVC/304 röralternativ för OEM-projekt.	Produkttyp|Driftläge|Behandlingsprocess|Renat vattenflöde|Matarvatten|Rörmaterial|Skyddsfunktioner|Styrning|Användning|OEM/ODM|MOQ	Helautomatisk intelligent drift, med manuell servicemod enligt projektbehov	Trestegs förbehandling plus omvänd osmos; processen anpassas efter vattenanalys	Kranvatten och grundvatten	UPVC eller 304 rostfritt stål enligt projektstandard	Skydd mot vattenbrist, överbelastningsskydd och alarmgränssnitt	PLC eller kontrollpanel kan anpassas efter köparens krav	Fabriker, vattenverk, hotell, livsmedelsindustri och industriella renvattenprojekt	Flöde, pump, membran, tankar, rörmaterial, spänning, panelspråk och emballage kan anpassas	Bekräftas enligt kapacitet, konfiguration och OEM-nivå
sw	Vifaa vikubwa vya viwandani vya RO vya kutibu maji 3-100 t/saa	Matibabu ya maji ya RO viwandani	Vifaa vikubwa vya viwandani vya RO vya Yuchen Water vimeundwa kwa viwanda, mitambo ya maji, hoteli na wakandarasi wa miradi ya B2B wanaohitaji maji safi thabiti 3-100 t/saa. Mfumo huu unaunganisha maandalizi ya awali ya hatua tatu na reverse osmosis, uendeshaji mahiri wa kiotomatiki, ulinzi wa kutokuwa na maji, ulinzi wa mzigo kupita kiasi na moduli za mchakato zinazobadilishwa kwa maji ya bomba au maji ya ardhini.	Mfumo mkubwa wa RO wa viwandani 3-100 t/saa, udhibiti wa kiotomatiki, pretreatment maalum na chaguo za bomba UPVC/304 kwa miradi ya OEM.	Aina ya bidhaa|Hali ya uendeshaji|Mchakato wa matibabu|Mtiririko wa maji safi|Maji ghafi|Nyenzo ya bomba|Kazi za ulinzi|Udhibiti|Matumizi|OEM/ODM|MOQ	Uendeshaji mahiri wa kiotomatiki, na hali ya huduma ya mkono kulingana na mradi	Maandalizi ya awali ya hatua tatu pamoja na reverse osmosis; mchakato hubadilishwa kulingana na uchambuzi wa maji	Maji ya bomba na maji ya ardhini	UPVC au chuma cha pua 304 kulingana na kiwango cha mradi	Ulinzi wa kukosa maji, ulinzi wa mzigo kupita kiasi na violesura vya tahadhari	PLC au paneli ya kudhibiti inaweza kubadilishwa kulingana na mahitaji ya mnunuzi	Viwanda, mitambo ya maji, hoteli, usindikaji wa chakula na miradi ya maji safi viwandani	Mtiririko, pampu, membrane, matangi, bomba, voltage, lugha ya paneli na ufungaji vinaweza kubadilishwa	Huthibitishwa kulingana na uwezo, usanidi na kiwango cha OEM
ta	பெரிய தொழில்துறை RO நீர் சிகிச்சை உபகரணம் 3-100 டன்/மணி	தொழில்துறை RO நீர் சிகிச்சை	Yuchen Water பெரிய தொழில்துறை RO நீர் சிகிச்சை உபகரணம் தொழிற்சாலைகள், நீர் நிலையங்கள், ஹோட்டல்கள் மற்றும் 3-100 டன்/மணி நிலையான சுத்தமான நீர் தேவைப்படும் B2B திட்ட ஒப்பந்தக்காரர்களுக்காக வடிவமைக்கப்பட்டுள்ளது. இது மூன்று நிலை முன் சிகிச்சை, reverse osmosis, முழு தானியங்கி அறிவார்ந்த இயக்கம், நீர் இல்லா பாதுகாப்பு, அதிக சுமை பாதுகாப்பு மற்றும் குழாய் நீர் அல்லது நிலத்தடி நீருக்கான தனிப்பயன் செயல்முறையை இணைக்கிறது.	3-100 டன்/மணி ஓட்டம் கொண்ட பெரிய தொழில்துறை RO அமைப்பு, தானியங்கி கட்டுப்பாடு, தனிப்பயன் முன் சிகிச்சை மற்றும் OEM திட்டங்களுக்கு UPVC/304 குழாய் விருப்பங்கள்.	தயாரிப்பு வகை|இயக்க முறை|சிகிச்சை செயல்முறை|சுத்தமான நீர் ஓட்டம்|உள்வரும் நீர்|குழாய் பொருள்|பாதுகாப்பு செயல்பாடுகள்|கட்டுப்பாடு|பயன்பாடு|OEM/ODM|MOQ	முழு தானியங்கி அறிவார்ந்த இயக்கம், திட்டத் தேவைக்கு ஏற்ப கைமுறை சேவை முறை	மூன்று நிலை முன் சிகிச்சை மற்றும் reverse osmosis; நீர் பகுப்பாய்வு படி செயல்முறை தனிப்பயன்	குழாய் நீர் மற்றும் நிலத்தடி நீர்	UPVC அல்லது திட்டத் தரநிலைக்கு ஏற்ப 304 துருப்பிடிக்காத எஃகு	நீர் இல்லா பாதுகாப்பு, அதிக சுமை பாதுகாப்பு மற்றும் அலாரம் இடைமுகங்கள்	PLC அல்லது கட்டுப்பாட்டு பலகை வாங்குபவர் தேவைக்கு ஏற்ப தனிப்பயன் செய்யலாம்	தொழிற்சாலைகள், நீர் நிலையங்கள், ஹோட்டல்கள், உணவு செயலாக்கம் மற்றும் தொழில்துறை சுத்தநீர் திட்டங்கள்	ஓட்டம், பம்ப், membrane, தொட்டிகள், குழாய் பொருள், மின்னழுத்தம், பலகை மொழி மற்றும் பேக்கிங் தனிப்பயன் செய்யலாம்	திறன், கட்டமைப்பு மற்றும் OEM நிலைப்படி உறுதி செய்யப்படும்
tg	Таҷҳизоти бузурги саноатии RO барои коркарди об 3-100 т/соат	Коркарди саноатии оби RO	Таҷҳизоти бузурги саноатии RO-и Yuchen Water барои корхонаҳо, истгоҳҳои об, меҳмонхонаҳо ва пудратчиёни B2B таҳия шудааст, ки баромади устувори оби тоза 3-100 т/соат талаб мекунанд. Система пешкоркарди се марҳила, осмоси баръакс, кори пурра автоматикии интеллектуалӣ, муҳофизат аз набудани об, муҳофизат аз изофабор ва модулҳои равандро барои оби лӯла ё зеризаминӣ мутобиқ мекунад.	Системаи бузурги саноатии RO 3-100 т/соат бо идоракунии автоматӣ, пешкоркарди фармоишӣ ва қубурҳои UPVC/304 барои лоиҳаҳои OEM.	Навъи маҳсулот|Режими кор|Раванди коркард|Ҷараёни оби тоза|Оби воридшаванда|Маводи қубур|Функсияҳои муҳофизат|Идоракунӣ|Истифода|OEM/ODM|MOQ	Кори пурра автоматикии интеллектуалӣ, бо режими хизматрасонии дастӣ мувофиқи лоиҳа	Пешкоркарди се марҳила ва осмоси баръакс; раванд мувофиқи таҳлили об танзим мешавад	Оби лӯла ва оби зеризаминӣ	UPVC ё пӯлоди зангногир 304 мувофиқи стандарти лоиҳа	Муҳофизат аз набудани об, изофабор ва интерфейсҳои ҳушдор	PLC ё панели идоракунӣ мувофиқи талаботи харидор фармоишӣ мешавад	Корхонаҳо, истгоҳҳои об, меҳмонхонаҳо, коркарди ғизо ва лоиҳаҳои саноатии оби тоза	Ҷараён, насос, мембрана, зарфҳо, қубур, шиддат, забони панел ва бастабандӣ фармоишӣ мешавад	Мувофиқи иқтидор, конфигуратсия ва сатҳи OEM тасдиқ мешавад
th	อุปกรณ์บำบัดน้ำ RO อุตสาหกรรมขนาดใหญ่ 3-100 ตัน/ชั่วโมง	ระบบบำบัดน้ำ RO อุตสาหกรรม	อุปกรณ์บำบัดน้ำ RO อุตสาหกรรมขนาดใหญ่ของ Yuchen Water ออกแบบสำหรับโรงงาน สถานีน้ำ โรงแรม และผู้รับเหมาโครงการ B2B ที่ต้องการน้ำบริสุทธิ์คงที่ 3-100 ตัน/ชั่วโมง ระบบรวมการปรับสภาพเบื้องต้น 3 ขั้นตอนกับรีเวิร์สออสโมซิส การทำงานอัจฉริยะอัตโนมัติเต็มรูปแบบ ระบบป้องกันน้ำขาด ป้องกันโอเวอร์โหลด และโมดูลกระบวนการที่ปรับได้ตามน้ำประปาหรือน้ำบาดาล	ระบบ RO อุตสาหกรรมขนาดใหญ่ 3-100 ตัน/ชั่วโมง ควบคุมอัตโนมัติ ปรับสภาพเบื้องต้นตามโครงการ และเลือกท่อ UPVC/304 สำหรับ OEM.	ประเภทสินค้า|โหมดการทำงาน|กระบวนการบำบัด|อัตราการไหลน้ำบริสุทธิ์|น้ำป้อน|วัสดุท่อ|ฟังก์ชันป้องกัน|การควบคุม|การใช้งาน|OEM/ODM|MOQ	ทำงานอัจฉริยะอัตโนมัติเต็มรูปแบบ พร้อมโหมดบริการแบบแมนนวลตามโครงการ	ปรับสภาพเบื้องต้น 3 ขั้นตอนร่วมกับรีเวิร์สออสโมซิส ปรับกระบวนการตามผลวิเคราะห์น้ำ	น้ำประปาและน้ำบาดาล	UPVC หรือสแตนเลส 304 ตามมาตรฐานโครงการ	ป้องกันน้ำขาด ป้องกันโอเวอร์โหลด และอินเทอร์เฟซแจ้งเตือน	PLC หรือแผงควบคุมปรับได้ตามความต้องการผู้ซื้อ	โรงงาน สถานีน้ำ โรงแรม อาหารแปรรูป และโครงการน้ำบริสุทธิ์อุตสาหกรรม	อัตราการไหล ปั๊ม เมมเบรน ถัง วัสดุท่อ แรงดันไฟ ภาษาแผง และบรรจุภัณฑ์ปรับได้	ยืนยันตามกำลังผลิต การกำหนดค่า และระดับ OEM
tk	Uly senagat RO suw arassalaýyş enjamlary 3-100 t/sagat	Senagat RO suw arassalaýyş	Yuchen Water uly senagat RO suw arassalaýyş enjamlary zawodlar, suw desgalary, myhmanhanalar we B2B taslama potratçylary üçin 3-100 t/sagat durnukly arassa suw öndürmek maksady bilen taýýarlanýar. Sistema üç tapgyrly öňünden arassalaýyş, ters osmos, doly awtomatik akylly iş, suw ýok wagty gorag, artykmaç ýük goragy we kran ýa-da ýerasty suwa laýyk proses modullaryny birleşdirýär.	3-100 t/sagat uly senagat RO ulgamy, awtomatik dolandyryş, ýörite öňünden arassalaýyş we OEM taslamalary üçin UPVC/304 turba görnüşleri.	Önüm görnüşi|Iş tertibi|Arassalaýyş prosesi|Arassa suw akymy|Giriş suwy|Turba materialy|Gorag funksiýalary|Dolandyryş|Ulanylyş|OEM/ODM|MOQ	Doly awtomatik akylly iş, taslama zerurlygyna görä el hyzmat tertibi	Üç tapgyrly öňünden arassalaýyş we ters osmos; proses suw analizine görä sazlanýar	Kran suwy we ýerasty suw	UPVC ýa-da taslama standarty boýunça 304 poslamaýan polat	Suw ýok goragy, artykmaç ýük goragy we duýduryş interfeýsleri	PLC ýa-da dolandyryş paneli alyjynyň talaplaryna görä sazlanýar	Zawodlar, suw desgalary, myhmanhanalar, azyk işläp taýýarlamak we senagat arassa suw taslamalary	Akym, nasos, membrana, baklar, turba, naprýaženiýe, panel dili we gaplama sazlanýar	Kuwwat, konfigurasiýa we OEM derejesi boýunça tassyklanýar
tl	Malaking industriyal na RO water treatment equipment 3-100 t/oras	Industriyal na RO water treatment	Ang malaking industriyal na RO water treatment equipment ng Yuchen Water ay ginawa para sa mga pabrika, water plant, hotel at B2B project contractor na nangangailangan ng matatag na purified water output na 3-100 t/oras. Pinagsasama ng sistema ang three-stage pretreatment at reverse osmosis, full automatic intelligent operation, proteksyon kapag walang tubig, overload protection at process modules na naaangkop sa tap water o groundwater.	Malaking industriyal na RO system na may 3-100 t/oras flow, awtomatikong kontrol, custom pretreatment at UPVC/304 piping options para sa OEM projects.	Uri ng produkto|Paraan ng operasyon|Proseso ng paggamot|Daloy ng purong tubig|Feed water|Materyal ng piping|Mga proteksyon|Kontrol|Aplikasyon|OEM/ODM|MOQ	Full automatic intelligent operation, may manual service mode ayon sa pangangailangan ng proyekto	Three-stage pretreatment plus reverse osmosis; proseso ay inaangkop ayon sa water analysis	Tap water at groundwater	UPVC o 304 stainless steel ayon sa project standard	No-water protection, overload protection at alarm interfaces	PLC o control panel ay maaaring i-customize ayon sa buyer requirements	Mga pabrika, water plants, hotel, food processing at industrial pure water projects	Flow rate, pump, membrane, tanks, piping material, voltage, panel language at packaging ay customizable	Kukumpirmahin ayon sa capacity, configuration at OEM level
tr	Büyük endüstriyel ters ozmoz su arıtma ekipmanı 3-100 t/saat	Endüstriyel RO su arıtma	Yuchen Water büyük endüstriyel ters ozmoz su arıtma ekipmanı; fabrikalar, su tesisleri, oteller ve 3-100 t/saat aralığında stabil saf su çıkışına ihtiyaç duyan B2B proje yüklenicileri için üretilir. Sistem üç aşamalı ön arıtma ile ters ozmozu, tam otomatik akıllı çalışmayı, susuz çalışma korumasını, aşırı yük korumasını ve şebeke suyu veya yeraltı suyuna göre özelleştirilen proses modüllerini birleştirir.	3-100 t/saat debili büyük endüstriyel RO sistemi; otomatik kontrol, özel ön arıtma ve OEM projeleri için UPVC/304 boru seçenekleri.	Ürün tipi|Çalışma modu|Arıtma süreci|Saf su debisi|Besleme suyu|Boru malzemesi|Koruma fonksiyonları|Kontrol|Uygulama|OEM/ODM|MOQ	Tam otomatik akıllı çalışma, proje ihtiyacına göre manuel servis modu	Üç aşamalı ön arıtma ve ters ozmoz; proses su analizine göre özelleştirilir	Şebeke suyu ve yeraltı suyu	UPVC veya proje standardına göre 304 paslanmaz çelik	Susuz çalışma koruması, aşırı yük koruması ve alarm arayüzleri	PLC veya kontrol paneli alıcı gereksinimlerine göre özelleştirilebilir	Fabrikalar, su tesisleri, oteller, gıda işleme ve endüstriyel saf su projeleri	Debi, pompa, membran, tanklar, boru malzemesi, voltaj, panel dili ve ambalaj özelleştirilebilir	Kapasite, konfigürasyon ve OEM seviyesine göre onaylanır
uk	Велика промислова RO установка для очищення води 3-100 т/год	Промислове RO очищення води	Велика промислова RO установка Yuchen Water призначена для заводів, водопідготовчих станцій, готелів і B2B проєктних підрядників, яким потрібна стабільна продуктивність очищеної води 3-100 т/год. Система поєднує триступеневу попередню підготовку зворотним осмосом, повністю автоматичну інтелектуальну роботу, захист від відсутності води, перевантаження і процесні модулі для водопровідної або підземної води.	Велика промислова RO система 3-100 т/год з автоматичним керуванням, налаштованою передочисткою та трубопроводом UPVC/304 для OEM проєктів.	Тип продукту|Режим роботи|Процес очищення|Потік чистої води|Вхідна вода|Матеріал трубопроводу|Функції захисту|Керування|Застосування|OEM/ODM|MOQ	Повністю автоматична інтелектуальна робота, з ручним сервісним режимом за проєктом	Триступенева попередня підготовка плюс зворотний осмос; процес налаштовується за аналізом води	Водопровідна вода і підземна вода	UPVC або нержавіюча сталь 304 згідно зі стандартом проєкту	Захист від відсутності води, перевантаження та інтерфейси сигналізації	PLC або панель керування налаштовується під вимоги покупця	Заводи, водні станції, готелі, харчова промисловість і промислові проєкти чистої води	Потік, насос, мембрана, баки, трубопровід, напруга, мова панелі та пакування налаштовуються	Підтверджується за продуктивністю, конфігурацією та рівнем OEM
ur	بڑا صنعتی RO واٹر ٹریٹمنٹ سامان 3-100 ٹن/گھنٹہ	صنعتی RO واٹر ٹریٹمنٹ	Yuchen Water کا بڑا صنعتی RO واٹر ٹریٹمنٹ سامان فیکٹریوں، واٹر پلانٹس، ہوٹلوں اور B2B پروجیکٹ کنٹریکٹرز کے لیے بنایا گیا ہے جنہیں 3-100 ٹن/گھنٹہ مستحکم صاف پانی درکار ہوتا ہے۔ یہ سسٹم تین مرحلوں کی پری ٹریٹمنٹ، ریورس اوسموسس، مکمل خودکار ذہین آپریشن، پانی نہ ہونے کی حفاظت، اوورلوڈ حفاظت اور نل کے پانی یا زیر زمین پانی کے لیے حسب ضرورت عمل کو یکجا کرتا ہے۔	3-100 ٹن/گھنٹہ بڑا صنعتی RO سسٹم، خودکار کنٹرول، حسب ضرورت پری ٹریٹمنٹ اور OEM پروجیکٹس کے لیے UPVC/304 پائپنگ آپشنز۔	مصنوعات کی قسم|آپریشن موڈ|ٹریٹمنٹ عمل|صاف پانی کا بہاؤ|فیڈ واٹر|پائپنگ مواد|حفاظتی افعال|کنٹرول|استعمال|OEM/ODM|MOQ	مکمل خودکار ذہین آپریشن، پروجیکٹ کی ضرورت کے مطابق دستی سروس موڈ	تین مرحلوں کی پری ٹریٹمنٹ اور ریورس اوسموسس؛ عمل پانی کے تجزیے کے مطابق حسب ضرورت	نل کا پانی اور زیر زمین پانی	UPVC یا پروجیکٹ معیار کے مطابق 304 اسٹین لیس اسٹیل	پانی نہ ہونے کی حفاظت، اوورلوڈ حفاظت اور الارم انٹرفیس	PLC یا کنٹرول پینل خریدار کی ضرورت کے مطابق حسب ضرورت	فیکٹریاں، واٹر پلانٹس، ہوٹل، فوڈ پروسیسنگ اور صنعتی صاف پانی کے منصوبے	بہاؤ، پمپ، میمبرین، ٹینک، پائپنگ، وولٹیج، پینل زبان اور پیکنگ حسب ضرورت	صلاحیت، کنفیگریشن اور OEM سطح کے مطابق تصدیق
uz	3-100 t/soat yirik sanoat RO suv tozalash uskunasi	Sanoat RO suv tozalash	Yuchen Water yirik sanoat RO suv tozalash uskunasi 3-100 t/soat barqaror tozalangan suv chiqishi kerak bo‘lgan zavodlar, suv stansiyalari, mehmonxonalar va B2B loyiha pudratchilari uchun ishlab chiqilgan. Tizim uch bosqichli oldindan tozalash va teskari osmosni, to‘liq avtomatik aqlli ishlashni, suvsiz himoyani, ortiqcha yuklanish himoyasini hamda vodoprovod yoki yerosti suvi uchun moslashtiriladigan jarayon modullarini birlashtiradi.	3-100 t/soat yirik sanoat RO tizimi, avtomatik boshqaruv, moslashtirilgan oldindan tozalash va OEM loyihalari uchun UPVC/304 quvur variantlari.	Mahsulot turi|Ishlash rejimi|Tozalash jarayoni|Toza suv oqimi|Kirish suvi|Quvur materiali|Himoya funksiyalari|Boshqaruv|Qo‘llanish|OEM/ODM|MOQ	To‘liq avtomatik aqlli ishlash, loyiha ehtiyojiga ko‘ra qo‘l bilan servis rejimi	Uch bosqichli oldindan tozalash va teskari osmos; jarayon suv tahliliga qarab moslashtiriladi	Vodoprovod suvi va yerosti suvi	UPVC yoki loyiha standartiga ko‘ra 304 zanglamas po‘lat	Suvsiz himoya, ortiqcha yuklanishdan himoya va signal interfeyslari	PLC yoki boshqaruv paneli xaridor talabiga ko‘ra moslashtiriladi	Zavodlar, suv stansiyalari, mehmonxonalar, oziq-ovqat ishlab chiqarish va sanoat toza suv loyihalari	Oqim, nasos, membrana, baklar, quvur materiali, kuchlanish, panel tili va qadoqlash moslashtiriladi	Quvvat, konfiguratsiya va OEM darajasiga ko‘ra tasdiqlanadi
vi	Thiết bị xử lý nước RO công nghiệp lớn 3-100 tấn/giờ	Xử lý nước RO công nghiệp	Thiết bị xử lý nước RO công nghiệp lớn của Yuchen Water được thiết kế cho nhà máy, trạm nước, khách sạn và nhà thầu dự án B2B cần lưu lượng nước tinh khiết ổn định 3-100 tấn/giờ. Hệ thống kết hợp tiền xử lý ba cấp với thẩm thấu ngược, vận hành thông minh tự động hoàn toàn, bảo vệ thiếu nước, bảo vệ quá tải và các mô-đun quy trình tùy chỉnh cho nước máy hoặc nước ngầm.	Hệ thống RO công nghiệp lớn lưu lượng 3-100 tấn/giờ, điều khiển tự động, tiền xử lý tùy chỉnh và lựa chọn đường ống UPVC/304 cho dự án OEM.	Loại sản phẩm|Chế độ vận hành|Quy trình xử lý|Lưu lượng nước tinh khiết|Nước đầu vào|Vật liệu đường ống|Chức năng bảo vệ|Điều khiển|Ứng dụng|OEM/ODM|MOQ	Vận hành thông minh tự động hoàn toàn, có chế độ bảo trì thủ công theo dự án	Tiền xử lý ba cấp kết hợp thẩm thấu ngược; quy trình được tùy chỉnh theo phân tích nước	Nước máy và nước ngầm	UPVC hoặc inox 304 theo tiêu chuẩn dự án	Bảo vệ thiếu nước, bảo vệ quá tải và giao diện cảnh báo	PLC hoặc tủ điều khiển có thể tùy chỉnh theo yêu cầu người mua	Nhà máy, trạm nước, khách sạn, chế biến thực phẩm và dự án nước tinh khiết công nghiệp	Lưu lượng, bơm, màng, bồn, vật liệu ống, điện áp, ngôn ngữ bảng điều khiển và đóng gói tùy chỉnh	Xác nhận theo công suất, cấu hình và cấp độ OEM
zu	Imishini emikhulu ye-RO yokwelapha amanzi ezimbonini 3-100 t/h	Ukwelashwa kwamanzi e-RO ezimbonini	Imishini emikhulu ye-RO ka Yuchen Water yakhelwe amafekthri, iziteshi zamanzi, amahhotela nabaphathi bephrojekthi be-B2B abadinga amanzi ahlanzekile azinzile angu-3-100 t/h. Uhlelo luhlanganisa ukwelashwa kwangaphambili kwezigaba ezintathu ne-reverse osmosis, ukusebenza okuzenzakalelayo okuhlakaniphile, ukuvikelwa uma kungekho manzi, ukuvikelwa emthwalweni oweqile namamojula enqubo enziwa ngokwezidingo zamanzi ompompi noma angaphansi komhlaba.	Uhlelo olukhulu lwe-RO lwezimboni 3-100 t/h, ukulawula okuzenzakalelayo, pretreatment eyenziwe ngokwezifiso kanye nezinketho zamapayipi UPVC/304 kumaphrojekthi e-OEM.	Uhlobo lomkhiqizo|Indlela yokusebenza|Inqubo yokwelapha|Ukugeleza kwamanzi ahlanzekile|Amanzi angenayo|Impahla yamapayipi|Imisebenzi yokuvikela|Ukulawula|Ukusetshenziswa|OEM/ODM|MOQ	Ukusebenza okuzenzakalelayo okuhlakaniphile, nemodi yesevisi ngesandla ngokwephrojekthi	Ukwelashwa kwangaphambili kwezigaba ezintathu kanye ne-reverse osmosis; inqubo ilungiswa ngokuhlaziywa kwamanzi	Amanzi ompompi namanzi angaphansi komhlaba	UPVC noma insimbi engagqwali 304 ngokwezinga lephrojekthi	Ukuvikelwa kokungabi namanzi, ukuvikelwa komthwalo owedlulele nezixhumi ze-alamu	PLC noma iphaneli yokulawula ingalungiswa ngokwemfuneko yomthengi	Amafekthri, iziteshi zamanzi, amahhotela, ukucubungula ukudla namaphrojekthi amanzi ahlanzekile ezimboni	Ukugeleza, ipompo, membrane, amathangi, amapayipi, voltage, ulimi lwephaneli nokupakisha kuyaguqulwa	Kuqinisekiswa ngokwamandla, ukucushwa nezinga le-OEM
""".strip()


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def load_rows() -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for line in DATA_ROWS.splitlines():
        parts = line.split("\t")
        if len(parts) != 15:
            raise ValueError(f"Bad data row for {parts[0] if parts else 'unknown'}: {len(parts)} fields")
        lang, name, category, intro, card, labels, *values = parts
        rows[lang] = {
            "name": name,
            "category": category,
            "intro": intro,
            "card": card,
            "labels": labels.split("|"),
            "values": [name, values[0], values[1], "3-100 t/h"] + values[2:],
        }
    return rows


DATA = load_rows()
BASE_COPY = runpy.run_path(str(ROOT / "scripts" / "add_20inch_commercial_ro_product.py"))
BASE_LOCAL_TERMS = BASE_COPY.get("LOCAL_TERMS", {})
BASE_UI = BASE_COPY.get("UI", {})


UI = {
    "en": {"home": "Home", "products": "Products", "specs": "Technical Specifications", "process": "System Configuration", "faq": "FAQ", "related": "Related Products", "request": "Request OEM Quote", "whatsapp": "WhatsApp Sales", "send": "Send Inquiry", "item": "Item", "spec": "Specification"},
    "ru": {"home": "Главная", "products": "Продукция", "specs": "Технические характеристики", "process": "Конфигурация системы", "faq": "FAQ", "related": "Похожие продукты", "request": "Запросить OEM-предложение", "whatsapp": "Продажи WhatsApp", "send": "Отправить запрос", "item": "Параметр", "spec": "Спецификация"},
    "es": {"home": "Inicio", "products": "Productos", "specs": "Especificaciones técnicas", "process": "Configuración del sistema", "faq": "FAQ", "related": "Productos relacionados", "request": "Solicitar cotización OEM", "whatsapp": "Ventas por WhatsApp", "send": "Enviar consulta", "item": "Ítem", "spec": "Especificación"},
    "de": {"home": "Startseite", "products": "Produkte", "specs": "Technische Daten", "process": "Systemkonfiguration", "faq": "FAQ", "related": "Ähnliche Produkte", "request": "OEM-Angebot anfordern", "whatsapp": "WhatsApp-Vertrieb", "send": "Anfrage senden", "item": "Punkt", "spec": "Spezifikation"},
    "fr": {"home": "Accueil", "products": "Produits", "specs": "Spécifications techniques", "process": "Configuration du système", "faq": "FAQ", "related": "Produits associés", "request": "Demander un devis OEM", "whatsapp": "Ventes WhatsApp", "send": "Envoyer une demande", "item": "Élément", "spec": "Spécification"},
    "vi": {"home": "Trang chủ", "products": "Sản phẩm", "specs": "Thông số kỹ thuật", "process": "Cấu hình hệ thống", "faq": "FAQ", "related": "Sản phẩm liên quan", "request": "Yêu cầu báo giá OEM", "whatsapp": "Bán hàng WhatsApp", "send": "Gửi yêu cầu", "item": "Hạng mục", "spec": "Thông số"},
    "ja": {"home": "ホーム", "products": "製品", "specs": "技術仕様", "process": "システム構成", "faq": "FAQ", "related": "関連製品", "request": "OEM見積を依頼", "whatsapp": "WhatsApp営業", "send": "問い合わせを送信", "item": "項目", "spec": "仕様"},
    "uz": {"home": "Bosh sahifa", "products": "Mahsulotlar", "specs": "Texnik xususiyatlar", "process": "Tizim konfiguratsiyasi", "faq": "FAQ", "related": "Tegishli mahsulotlar", "request": "OEM narx so‘rash", "whatsapp": "WhatsApp savdo", "send": "So‘rov yuborish", "item": "Band", "spec": "Spetsifikatsiya"},
    "kk": {"home": "Басты бет", "products": "Өнімдер", "specs": "Техникалық сипаттамалар", "process": "Жүйе конфигурациясы", "faq": "FAQ", "related": "Ұқсас өнімдер", "request": "OEM ұсынысын сұрау", "whatsapp": "WhatsApp сату", "send": "Сұрау жіберу", "item": "Параметр", "spec": "Сипаттама"},
    "ky": {"home": "Башкы бет", "products": "Өнүмдөр", "specs": "Техникалык мүнөздөмөлөр", "process": "Система конфигурациясы", "faq": "FAQ", "related": "Окшош өнүмдөр", "request": "OEM баасын суроо", "whatsapp": "WhatsApp сатуу", "send": "Суроо жөнөтүү", "item": "Параметр", "spec": "Спецификация"},
}


def dirs() -> list[str]:
    return sorted(p.name for p in ROOT.iterdir() if p.is_dir() and (p / "index.html").exists())


def ui_for(lang: str) -> dict:
    if lang in UI:
        return UI[lang].copy()
    if lang in BASE_LOCAL_TERMS:
        t = BASE_LOCAL_TERMS[lang]
        return {
            "home": t["home"],
            "products": t["products"],
            "specs": t["specs"],
            "process": t["options"],
            "faq": "FAQ",
            "related": t["related"],
            "request": t["request"],
            "whatsapp": "WhatsApp",
            "send": t["send"],
            "item": t["item"],
            "spec": t["spec"],
        }
    if lang in BASE_UI:
        b = BASE_UI[lang]
        return {
            "home": b.get("home", UI["en"]["home"]),
            "products": b.get("products", UI["en"]["products"]),
            "specs": b.get("specs", UI["en"]["specs"]),
            "process": b.get("options", UI["en"]["process"]),
            "faq": b.get("faq", "FAQ"),
            "related": b.get("related", UI["en"]["related"]),
            "request": b.get("request", UI["en"]["request"]),
            "whatsapp": b.get("whatsapp", "WhatsApp"),
            "send": b.get("send", UI["en"]["send"]),
            "item": b.get("item", UI["en"]["item"]),
            "spec": b.get("spec", UI["en"]["spec"]),
        }
    return UI["en"].copy()


def copy_for(lang: str) -> dict:
    if lang not in DATA:
        raise KeyError(f"No translation data for {lang}")
    c = DATA[lang].copy()
    c.update(ui_for(lang))
    c["title"] = f"{c['name']} | Yuchen Water OEM"
    c["meta"] = re.sub(r"\s+", " ", c["intro"]).strip()
    if len(c["meta"]) > 260:
        c["meta"] = c["meta"][:257].rsplit(" ", 1)[0] + "..."
    c["quote"] = f"{c['request']}: {c['name']}"
    c["quote_desc"] = c["intro"]
    c["faq_pairs"] = [
        (f"{c['labels'][3]}?", c["values"][3]),
        (f"{c['labels'][4]}?", c["values"][4]),
        (f"{c['labels'][8]}?", c["values"][8]),
        (f"{c['labels'][9]}?", c["values"][9]),
    ]
    return c


def page_h1(lang: str, href: str, fallback: str) -> str:
    path = ROOT / lang / href
    if not path.exists():
        return fallback
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"<h1[^>]*>(.*?)</h1>", text, flags=re.S)
    if not match:
        return fallback
    title = re.sub(r"<.*?>", "", match.group(1)).strip()
    return title or fallback


def product_graph(lang: str, c: dict) -> str:
    props = [
        {"@type": "PropertyValue", "name": label, "value": value}
        for label, value in zip(c["labels"], c["values"])
    ]
    faq_entities = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in c["faq_pairs"]
    ]
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@context": "https://schema.org",
                "@type": "Organization",
                "@id": "https://www.yuchensy.com/#organization",
                "name": "Yuchen Water",
                "url": "https://www.yuchensy.com/",
                "logo": "https://www.yuchensy.com/assets/logo.png",
                "telephone": "+86-19908311885",
                "email": "expresswater025@gmail.com",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "Yuanhua Town",
                    "addressLocality": "Haining City",
                    "addressRegion": "Zhejiang Province",
                    "addressCountry": "CN",
                },
            },
            {"@context": "https://schema.org", "@type": "WebSite", "@id": "https://www.yuchensy.com/#website", "name": "Yuchen Water", "url": "https://www.yuchensy.com/", "publisher": {"@id": "https://www.yuchensy.com/#organization"}, "inLanguage": lang},
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": c["home"], "item": f"https://www.yuchensy.com/{lang}/index.html"},
                    {"@type": "ListItem", "position": 2, "name": c["products"], "item": f"https://www.yuchensy.com/{lang}/products.html"},
                    {"@type": "ListItem", "position": 3, "name": c["name"], "item": f"https://www.yuchensy.com/{lang}/{NEW_SLUG}"},
                ],
            },
            {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_entities},
            {
                "@context": "https://schema.org",
                "@type": "Product",
                "@id": f"https://www.yuchensy.com/{lang}/{NEW_SLUG}#product",
                "name": c["name"],
                "description": c["intro"],
                "image": [f"https://www.yuchensy.com/assets/products/{MAIN_IMAGE}"],
                "brand": {"@type": "Brand", "name": "Yuchen Water"},
                "manufacturer": {"@id": "https://www.yuchensy.com/#organization"},
                "category": c["category"],
                "additionalProperty": props,
                "offers": {
                    "@type": "Offer",
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock",
                    "url": f"https://www.yuchensy.com/{lang}/{NEW_SLUG}",
                    "priceValidUntil": "2027-12-31",
                },
            },
        ],
    }
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def build_main(lang: str, c: dict) -> str:
    rows = "\n".join(
        f"      <tr><th>{esc(label)}</th><td>{esc(value)}</td></tr>"
        for label, value in zip(c["labels"], c["values"])
    )
    faq = "\n".join(
        f'      <div class="faq-item"><button class="faq-q">{esc(q)}</button><div class="faq-a"><p>{esc(a)}</p></div></div>'
        for q, a in c["faq_pairs"]
    )
    related = [
        ("product-ro-seawater-desalination-machine.html", page_h1(lang, "product-ro-seawater-desalination-machine.html", "RO Seawater Desalination Equipment"), "ro-seawater-desalination-equipment-complete-system-oem.jpg", "RO System"),
        ("product-20-inch-commercial-ro-water-purifier-800g-2000g.html", page_h1(lang, "product-20-inch-commercial-ro-water-purifier-800g-2000g.html", "20-inch Commercial RO Water Purifier 800G/1200G/1600G/2000G"), "20-inch-commercial-ro-water-purifier-800g-2000g-front-full-frame-oem.webp", "RO System"),
        ("product-ss-jumbo-housing.html", page_h1(lang, "product-ss-jumbo-housing.html", "304/316L Stainless Steel Filter Housing"), "ss-jumbo-filter-housing-304-316l-stainless-steel-oem.webp", "Filter Housing"),
    ]
    related_html = "\n".join(
        f'''      <article class="product-card" data-cat="{esc(cat)}">
        <a href="{href}" class="product-img-wrap">
          <span class="product-cat-badge">{esc(cat)}</span>
          <img src="../assets/products/{img}" alt="{esc(title)}" loading="lazy" decoding="async" width="640" height="480" />
        </a>
        <div class="product-body">
          <h3>{esc(title)}</h3>
          <p>{esc(c["card"])}</p>
          <a href="{href}" class="product-link">{esc(c["send"])}</a>
        </div>
      </article>'''
        for href, title, img, cat in related
    )
    return f'''<main>
<section class="section section-cream product-hero">
  <div class="container product-detail">
    <div class="product-detail-img">
      <img src="../assets/products/{MAIN_IMAGE}" alt="{esc(c["name"])}" loading="eager" fetchpriority="high" decoding="async" width="1140" height="618" class="product-main-image" />
    </div>
    <div class="product-detail-info">
      <nav class="breadcrumb"><a href="index.html">{esc(c["home"])}</a><span>·</span><a href="products.html">{esc(c["products"])}</a><span>·</span><span>{esc(c["name"])}</span></nav>
      <h1>{esc(c["name"])}</h1>
      <span class="cat-badge">{esc(c["category"])}</span>
      <p class="desc">{esc(c["intro"])}</p>
      <div class="product-actions"><a href="contact.html" class="btn btn-gold">{esc(c["request"])}</a><a href="https://wa.me/8619908311885?text=Inquiry%20about%20Large%20Industrial%20RO%20Water%20Treatment%20Equipment" class="btn" target="_blank" rel="noopener">{esc(c["whatsapp"])}</a></div>
    </div>
  </div>
</section>
<section class="section section-cream">
  <div class="container">
    <div class="section-head"><span class="eyebrow">{esc(c["specs"])}</span><h2>{esc(c["name"])}</h2></div>
    <table class="spec-table">
      <tr><th>{esc(c["item"])}</th><td>{esc(c["spec"])}</td></tr>
{rows}
    </table>
  </div>
</section>
<section class="section section-cream">
  <div class="container">
    <div class="section-head"><span class="eyebrow">{esc(c["process"])}</span><h2>{esc(c["category"])}</h2></div>
    <p class="section-lead">{esc(c["card"])}</p>
    <table class="spec-table">
      <tr><th>{esc(c["labels"][1])}</th><td>{esc(c["values"][1])}</td></tr>
      <tr><th>{esc(c["labels"][2])}</th><td>{esc(c["values"][2])}</td></tr>
      <tr><th>{esc(c["labels"][6])}</th><td>{esc(c["values"][6])}</td></tr>
      <tr><th>{esc(c["labels"][9])}</th><td>{esc(c["values"][9])}</td></tr>
    </table>
  </div>
</section>
<section class="section section-light">
  <div class="container">
    <div class="section-head"><span class="eyebrow">{esc(c["faq"])}</span><h2>{esc(c["name"])}</h2></div>
    <div class="faq-wrap">
{faq}
    </div>
  </div>
</section>
<section class="section section-cream">
  <div class="container">
    <div class="section-head"><span class="eyebrow">{esc(c["related"])}</span><h2>{esc(c["related"])}</h2></div>
    <div class="product-grid">
{related_html}
    </div>
  </div>
</section>
<section class="section section-dark quote-strip">
  <div class="container">
    <h2>{esc(c["quote"])}</h2>
    <p>{esc(c["quote_desc"])}</p>
    <div class="hero-actions"><a href="contact.html" class="btn btn-gold">{esc(c["request"])}</a><a href="https://wa.me/8619908311885?text=Inquiry%20about%20Large%20Industrial%20RO%20Water%20Treatment%20Equipment" class="btn" target="_blank" rel="noopener">{esc(c["whatsapp"])}</a></div>
  </div>
</section>
</main>'''


def update_head(text: str, lang: str, c: dict) -> str:
    direction = "rtl" if lang in RTL_LANGS else "ltr"
    text = text.replace(TEMPLATE_SLUG, NEW_SLUG)
    text = re.sub(r'<html lang="[^"]+" dir="[^"]+">', f'<html lang="{lang}" dir="{direction}">', text, count=1)
    text = re.sub(r"<title>.*?</title>", f"<title>{esc(c['title'])}</title>", text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description" content="[^"]*" />', f'<meta name="description" content="{esc(c["meta"])}" />', text, count=1)
    text = re.sub(r'<link rel="canonical" href="[^"]+" />', f'<link rel="canonical" href="https://www.yuchensy.com/{lang}/{NEW_SLUG}" />', text, count=1)
    text = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]+" />', f'<link rel="alternate" hreflang="x-default" href="https://www.yuchensy.com/en/{NEW_SLUG}" />', text, count=1)
    text = re.sub(r'<link rel="preload" as="image" href="[^"]+" fetchpriority="high" />', f'<link rel="preload" as="image" href="../assets/products/{MAIN_IMAGE}" fetchpriority="high" />', text, count=1)
    text = re.sub(r'<meta property="og:title" content="[^"]*" />', f'<meta property="og:title" content="{esc(c["title"])}" />', text, count=1)
    text = re.sub(r'<meta property="og:description" content="[^"]*" />', f'<meta property="og:description" content="{esc(c["meta"])}" />', text, count=1)
    text = re.sub(r'<meta property="og:url" content="[^"]*" />', f'<meta property="og:url" content="https://www.yuchensy.com/{lang}/{NEW_SLUG}" />', text, count=1)
    text = re.sub(r'<meta property="og:image" content="[^"]*" />', f'<meta property="og:image" content="https://www.yuchensy.com/assets/products/{MAIN_IMAGE}" />', text, count=1)
    text = re.sub(r'<script type="application/ld\+json">.*?</script>', f'<script type="application/ld+json">{product_graph(lang, c)}</script>', text, count=1, flags=re.S)
    return text


def make_page(lang: str) -> None:
    template = (ROOT / lang / TEMPLATE_SLUG).read_text(encoding="utf-8")
    c = copy_for(lang)
    text = update_head(template, lang, c)
    text = re.sub(r"<main>.*?</main>", build_main(lang, c), text, count=1, flags=re.S)
    (ROOT / lang / NEW_SLUG).write_text(text, encoding="utf-8")


def product_card(lang: str) -> str:
    c = copy_for(lang)
    return f'''<article class="product-card" data-cat="RO System">
  <a href="{NEW_SLUG}" class="product-img-wrap">
    <span class="product-cat-badge">{esc(c["category"])}</span>
    <img src="../assets/products/{MAIN_IMAGE}" alt="{esc(c["name"])}" loading="lazy" decoding="async" width="1140" height="618" />
  </a>
  <div class="product-body">
    <h3>{esc(c["name"])}</h3>
    <p>{esc(c["card"])}</p>
    <a href="{NEW_SLUG}" class="product-link">{esc(c["send"])}</a>
  </div>
</article>
'''


def update_item_list_json(text: str, lang: str) -> str:
    c = copy_for(lang)
    for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', text, flags=re.S):
        try:
            data = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        graph = data.get("@graph") if isinstance(data, dict) else None
        if not isinstance(graph, list):
            continue
        for node in graph:
            if node.get("@type") != "ItemList":
                continue
            elements = node.setdefault("itemListElement", [])
            if any(NEW_SLUG in item.get("url", "") for item in elements if isinstance(item, dict)):
                return text
            insert_at = len(elements)
            for i, item in enumerate(elements):
                if AFTER_SLUG in item.get("url", ""):
                    insert_at = i + 1
                    break
            elements.insert(insert_at, {
                "@type": "ListItem",
                "position": insert_at + 1,
                "url": f"https://www.yuchensy.com/{lang}/{NEW_SLUG}",
                "name": c["name"],
                "description": c["card"],
            })
            for pos, item in enumerate(elements, 1):
                if isinstance(item, dict):
                    item["position"] = pos
            node["numberOfItems"] = len(elements)
            new_script = f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>'
            return text[:match.start()] + new_script + text[match.end():]
    return text


def update_products_page(lang: str) -> None:
    path = ROOT / lang / "products.html"
    text = path.read_text(encoding="utf-8")
    if NEW_SLUG not in text:
        anchor = AFTER_SLUG if AFTER_SLUG in text else TEMPLATE_SLUG
        match = re.search(r'(<article class="[^"]*\bproduct-card\b[^"]*"[^>]*>.*?' + re.escape(anchor) + r'.*?</article>\s*)', text, flags=re.S)
        if not match:
            raise RuntimeError(f"Could not find insertion point in {path}")
        text = text[:match.end()] + "\n" + product_card(lang) + text[match.end():]
    text = update_item_list_json(text, lang)
    path.write_text(text, encoding="utf-8")


def update_products_json() -> None:
    path = ROOT / "scripts" / "products.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    products = data.setdefault("products", [])
    if any(item.get("id") == PRODUCT_ID for item in products):
        return
    insert_at = next((i + 1 for i, item in enumerate(products) if item.get("id") == "20-inch-commercial-ro-water-purifier-800g-2000g"), 4)
    products.insert(insert_at, {
        "id": PRODUCT_ID,
        "name": DATA["en"]["name"],
        "category": "RO System",
        "desc": DATA["en"]["card"],
        "specs": {
            "Product Type": DATA["en"]["name"],
            "Operating Mode": DATA["en"]["values"][1],
            "Treatment Process": DATA["en"]["values"][2],
            "Pure Water Flow": DATA["en"]["values"][3],
            "Feed Water": DATA["en"]["values"][4],
            "Piping Material": DATA["en"]["values"][5],
            "Protection Functions": DATA["en"]["values"][6],
            "OEM/ODM": DATA["en"]["values"][9],
        },
        "image": f"../assets/products/{MAIN_IMAGE}",
        "image_local": f"assets/products/{MAIN_IMAGE}",
        "image_orig": f"../assets/products/{MAIN_IMAGE}",
        "summary": DATA["en"]["intro"],
        "features": ["3-100 TPH pure water flow", "Full automatic intelligent operation", "No-water and overload protection", "Three-stage pretreatment plus reverse osmosis", "UPVC or 304 piping options"],
        "applications": "Factories, water plants, hotels, food processing and industrial pure water projects.",
        "related": ["ro-seawater-desalination-machine", "20-inch-commercial-ro-water-purifier-800g-2000g", "ss-jumbo-housing"],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_sitemap(langs: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    if NEW_SLUG in text:
        return
    urls = []
    for lang in langs:
        urls.append(
            f"  <url>\n"
            f"    <loc>https://www.yuchensy.com/{lang}/{NEW_SLUG}</loc>\n"
            f"    <lastmod>{TODAY}</lastmod>\n"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>0.8</priority>\n"
            f"  </url>\n"
        )
    text = text.replace("</urlset>", "".join(urls) + "</urlset>")
    path.write_text(text, encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Large Industrial Reverse Osmosis Water Treatment Equipment 3-100 TPH: https://www.yuchensy.com/en/{NEW_SLUG}\n"
    for name in ["llms.txt", "llms-full.txt"]:
        path = ROOT / name
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if NEW_SLUG not in text:
                path.write_text(text.rstrip() + "\n" + line, encoding="utf-8")


def main() -> None:
    languages = dirs()
    missing = [lang for lang in languages if lang not in DATA]
    if missing:
        raise RuntimeError(f"Missing translations: {', '.join(missing)}")
    for lang in languages:
        make_page(lang)
        update_products_page(lang)
    update_products_json()
    update_sitemap(languages)
    update_ai_files()
    print(f"generated_pages={len(languages)}")


if __name__ == "__main__":
    main()
