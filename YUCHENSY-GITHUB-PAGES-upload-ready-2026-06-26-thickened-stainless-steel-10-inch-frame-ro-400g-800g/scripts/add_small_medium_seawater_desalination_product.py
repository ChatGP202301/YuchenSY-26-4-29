#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add small and medium seawater desalination RO equipment across all language pages."""

from __future__ import annotations

import html
import json
import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_SLUG = "product-ro-seawater-desalination-machine.html"
AFTER_SLUG = "product-ro-seawater-desalination-machine.html"
NEW_SLUG = "product-small-medium-seawater-desalination-ro-equipment.html"
PRODUCT_ID = "small-medium-seawater-desalination-ro-equipment"
TODAY = "2026-06-21"
MAIN_IMAGE = "small-medium-seawater-desalination-ro-equipment-60l-10000l-oem.webp"
IMAGE_WIDTH = 1190
IMAGE_HEIGHT = 888
RTL_LANGS = {"ar", "fa", "he", "ur"}


ROWS = """
af	Klein en medium seewater-ontsoutings RO-toerusting	Klein en medium seewater-ontsouting	Yuchen Water se klein en medium seewater-ontsoutings RO-toerusting is gebou vir kusprojekte, eilande, vaartuie, hotelle en B2B kontrakteurs wat betroubare drink- of proseswater uit seewater benodig. Die stelsel hanteer rouwater-soutgehalte van 10000-45000 ppm, gebruik voorafbehandeling en omgekeerde osmose, en lewer 60 L/h-10000 L/h met soutverwydering van minstens 99.7%. Beheer, pompe, membraankonfigurasie en beskermingsfunksies word volgens projekwaterontleding aangepas.	Klein en medium seewater-ontsoutings RO-stelsel vir 10000-45000 ppm rouwater, 60 L/h-10000 L/h uitset en OEM-projekkonfigurasie.	Produkmodel|Rouwater-soutgehalte|Nitraatverwyderingskoers|Inlaatwatertemperatuur|Soutverwydering|Produkwater-vloei|Produkwater-soutgehalte|Behandelingsproses|Beheer en beskerming|Toepassing|Aanpassing	Klein en medium seewater-ontsoutings toerusting|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Drie-stap voorbehandeling plus omgekeerde osmose; proses word volgens wateranalise aangepas|Outomatiese werking, beskerming teen geen water en oorladingsbeskerming; funksies volgens projekbehoefte|Seewater- en brakwater-ontsouting vir kus-, eiland-, vaartuig- en projekwatervoorsiening|Membraanhoeveelheid, pomp, spanning, beheerpaneel, raam, pypwerk en verpakking kan gekonfigureer word
ar	معدات تحلية مياه البحر RO صغيرة ومتوسطة	تحلية مياه البحر RO صغيرة ومتوسطة	معدات تحلية مياه البحر RO الصغيرة والمتوسطة من Yuchen Water مخصصة للمشاريع الساحلية والجزر والسفن والفنادق ومقاولي B2B الذين يحتاجون إلى مياه شرب أو مياه عملية موثوقة من مياه البحر. يتعامل النظام مع ملوحة مياه خام 10000-45000 ppm، ويستخدم معالجة أولية وتقنية التناضح العكسي، وينتج 60 لتر/ساعة-10000 لتر/ساعة مع إزالة أملاح لا تقل عن 99.7%. يمكن تخصيص التحكم والمضخات وعدد الأغشية ووظائف الحماية حسب تحليل المياه ومتطلبات المشروع.	نظام تحلية مياه البحر RO صغير ومتوسط لمياه خام 10000-45000 ppm، إنتاج 60-10000 لتر/ساعة وتكوين OEM للمشاريع.	طراز المنتج|ملوحة المياه الخام|معدل إزالة النترات|درجة حرارة مياه الدخول|إزالة الأملاح|تدفق المياه المنتجة|ملوحة المياه المنتجة|عملية المعالجة|التحكم والحماية|الاستخدام|التخصيص	معدات تحلية مياه البحر صغيرة ومتوسطة|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 لتر/ساعة-10000 لتر/ساعة|≤750 ppm|معالجة أولية من ثلاث مراحل بالإضافة إلى التناضح العكسي؛ يتم تخصيص العملية حسب تحليل المياه|تشغيل أوتوماتيكي، حماية من انقطاع المياه وحماية من الحمل الزائد؛ الوظائف حسب حاجة المشروع|تحلية مياه البحر والمياه قليلة الملوحة للمناطق الساحلية والجزر والسفن ومشاريع إمداد المياه|يمكن تكوين عدد الأغشية، المضخة، الجهد، لوحة التحكم، الهيكل، الأنابيب والتغليف
az	Kiçik və orta dəniz suyu duzsuzlaşdırma RO avadanlığı	Kiçik və orta dəniz suyu duzsuzlaşdırma	Yuchen Water kiçik və orta dəniz suyu duzsuzlaşdırma RO avadanlığı sahil layihələri, adalar, gəmilər, otellər və dəniz suyundan etibarlı içməli və ya texnoloji suya ehtiyacı olan B2B podratçıları üçün hazırlanır. Sistem 10000-45000 ppm xam su duzluluğunu emal edir, əvvəlcədən təmizləmə və tərs osmosdan istifadə edir, ən azı 99.7% duzsuzlaşdırma ilə 60 L/saat-10000 L/saat məhsul suyu verir. İdarəetmə, nasoslar, membran sayı və qoruma funksiyaları su analizinə və layihə tələbinə görə uyğunlaşdırılır.	10000-45000 ppm xam su üçün kiçik və orta RO duzsuzlaşdırma sistemi, 60-10000 L/saat çıxış və OEM layihə konfiqurasiyası.	Məhsul modeli|Xam su duzluluğu|Nitrat çıxarılma dərəcəsi|Giriş su temperaturu|Duzsuzlaşdırma dərəcəsi|Məhsul su axını|Məhsul su duzluluğu|Təmizləmə prosesi|İdarə və qoruma|Tətbiq|Fərdiləşdirmə	Kiçik və orta dəniz suyu duzsuzlaşdırma avadanlığı|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/saat-10000 L/saat|≤750 ppm|Üç mərhələli əvvəlcədən təmizləmə və tərs osmos; proses su analizinə görə uyğunlaşdırılır|Avtomatik iş, susuz qoruma və həddindən artıq yüklənmədən qoruma; funksiyalar layihəyə görə seçilir|Sahil, ada, gəmi və layihə su təchizatı üçün dəniz suyu və az duzlu su duzsuzlaşdırma|Membran sayı, nasos, gərginlik, idarə paneli, karkas, borular və qablaşdırma konfiqurasiya edilə bilər
bg	Малка и средна RO система за обезсоляване на морска вода	Малка и средна RO обезсоляваща система	Малката и средна RO система за обезсоляване на морска вода на Yuchen Water е предназначена за крайбрежни проекти, острови, кораби, хотели и B2B изпълнители, които се нуждаят от надеждна питейна или технологична вода от морска вода. Системата обработва сурова вода със соленост 10000-45000 ppm, използва предварителна обработка и обратна осмоза и осигурява 60 L/h-10000 L/h с обезсоляване поне 99.7%. Управлението, помпите, броят мембрани и защитните функции се настройват според анализа на водата и проекта.	Малка и средна RO система за морска вода 10000-45000 ppm, дебит 60-10000 L/h и OEM конфигурация за проекти.	Модел продукт|Соленост на суровата вода|Степен на отстраняване на нитрати|Температура на входната вода|Степен на обезсоляване|Дебит на произведена вода|Соленост на произведена вода|Процес на обработка|Управление и защита|Приложение|Персонализиране	Малко и средно оборудване за обезсоляване на морска вода|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Тристепенна предварителна обработка плюс обратна осмоза; процесът се настройва според анализа на водата|Автоматична работа, защита при липса на вода и защита от претоварване; функции според проекта|Обезсоляване на морска и солена вода за крайбрежни, островни, корабни и проектни водоснабдявания|Брой мембрани, помпа, напрежение, контролен панел, рамка, тръбопровод и опаковка могат да се конфигурират
bn	ছোট ও মাঝারি RO সমুদ্রের পানি লবণমুক্তকরণ সরঞ্জাম	ছোট ও মাঝারি RO সমুদ্রের পানি লবণমুক্তকরণ	Yuchen Water-এর ছোট ও মাঝারি RO সমুদ্রের পানি লবণমুক্তকরণ সরঞ্জাম উপকূলীয় প্রকল্প, দ্বীপ, জাহাজ, হোটেল এবং B2B প্রকল্প ঠিকাদারদের জন্য তৈরি, যেখানে সমুদ্রের পানি থেকে নির্ভরযোগ্য পানীয় বা প্রক্রিয়াজাত পানি দরকার। সিস্টেমটি 10000-45000 ppm কাঁচা পানির লবণাক্ততা গ্রহণ করে, প্রি-ট্রিটমেন্ট ও রিভার্স অসমোসিস ব্যবহার করে, এবং ≥99.7% লবণ অপসারণ সহ 60 L/h-10000 L/h পানি উৎপাদন করে। নিয়ন্ত্রণ, পাম্প, মেমব্রেন সংখ্যা ও সুরক্ষা ফাংশন পানি বিশ্লেষণ অনুযায়ী কাস্টম করা যায়।	10000-45000 ppm কাঁচা পানির জন্য ছোট ও মাঝারি RO সমুদ্রের পানি লবণমুক্তকরণ সিস্টেম, 60-10000 L/h আউটপুট ও OEM প্রকল্প কনফিগারেশন।	পণ্যের মডেল|কাঁচা পানির লবণাক্ততা|নাইট্রেট অপসারণ হার|ইনলেট পানির তাপমাত্রা|লবণ অপসারণ হার|উৎপাদিত পানির প্রবাহ|উৎপাদিত পানির লবণাক্ততা|শোধন প্রক্রিয়া|নিয়ন্ত্রণ ও সুরক্ষা|প্রয়োগ|কাস্টমাইজেশন	ছোট ও মাঝারি সমুদ্রের পানি লবণমুক্তকরণ সরঞ্জাম|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|তিন ধাপ প্রি-ট্রিটমেন্ট ও রিভার্স অসমোসিস; পানি বিশ্লেষণ অনুযায়ী প্রক্রিয়া কাস্টমাইজড|স্বয়ংক্রিয় অপারেশন, পানি না থাকলে সুরক্ষা ও ওভারলোড সুরক্ষা; প্রকল্প অনুযায়ী ফাংশন নির্ধারিত|উপকূল, দ্বীপ, জাহাজ ও প্রকল্প পানি সরবরাহের জন্য সমুদ্রের পানি ও লবণাক্ত পানি লবণমুক্তকরণ|মেমব্রেন সংখ্যা, পাম্প, ভোল্টেজ, কন্ট্রোল প্যানেল, ফ্রেম, পাইপিং ও প্যাকেজিং কনফিগার করা যায়
bs	Mala i srednja RO oprema za desalinizaciju morske vode	Mala i srednja RO desalinizacija morske vode	Yuchen Water mala i srednja RO oprema za desalinizaciju morske vode namijenjena je obalnim projektima, ostrvima, plovilima, hotelima i B2B izvođačima kojima treba pouzdana pitka ili procesna voda iz morske vode. Sistem obrađuje sirovu vodu saliniteta 10000-45000 ppm, koristi predtretman i reverznu osmozu, te daje 60 L/h-10000 L/h uz uklanjanje soli najmanje 99.7%. Upravljanje, pumpe, broj membrana i zaštitne funkcije prilagođavaju se analizi vode i projektu.	Mali i srednji RO sistem za morsku vodu 10000-45000 ppm, izlaz 60-10000 L/h i OEM konfiguracija projekta.	Model proizvoda|Salinitet sirove vode|Stopa uklanjanja nitrata|Temperatura ulazne vode|Uklanjanje soli|Protok proizvedene vode|Salinitet proizvedene vode|Proces tretmana|Upravljanje i zaštita|Primjena|Prilagođavanje	Mala i srednja oprema za desalinizaciju morske vode|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Trostepeni predtretman plus reverzna osmoza; proces se prilagođava prema analizi vode|Automatski rad, zaštita od rada bez vode i preopterećenja; funkcije prema projektu|Desalinizacija morske i slane vode za obalu, ostrva, plovila i projekte vodosnabdijevanja|Broj membrana, pumpa, napon, kontrolni panel, ram, cijevi i pakovanje mogu se konfigurisati
cs	Malé a střední RO zařízení pro odsolování mořské vody	Malé a střední RO odsolování mořské vody	Malé a střední RO zařízení Yuchen Water pro odsolování mořské vody je určeno pro pobřežní projekty, ostrovy, lodě, hotely a B2B dodavatele, kteří potřebují spolehlivou pitnou nebo procesní vodu z mořské vody. Systém zpracuje surovou vodu se salinitou 10000-45000 ppm, využívá předúpravu a reverzní osmózu a dodává 60 L/h-10000 L/h s odsolením nejméně 99.7%. Řízení, čerpadla, počet membrán a ochranné funkce se přizpůsobují analýze vody a projektu.	Malý a střední RO systém pro mořskou vodu 10000-45000 ppm, výkon 60-10000 L/h a OEM projektová konfigurace.	Model produktu|Salinita surové vody|Míra odstranění dusičnanů|Teplota vstupní vody|Odsolení|Průtok vyrobené vody|Salinita vyrobené vody|Proces úpravy|Řízení a ochrana|Použití|Přizpůsobení	Malé a střední zařízení pro odsolování mořské vody|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Třístupňová předúprava plus reverzní osmóza; proces se nastavuje podle analýzy vody|Automatický provoz, ochrana bez vody a proti přetížení; funkce podle projektu|Odsolování mořské a brakické vody pro pobřeží, ostrovy, lodě a projekty zásobování vodou|Počet membrán, čerpadlo, napětí, ovládací panel, rám, potrubí a balení lze konfigurovat
da	Lille og mellemstort RO-anlæg til afsaltning af havvand	Lille og mellemstor RO-afsaltning af havvand	Yuchen Water lille og mellemstore RO-anlæg til afsaltning af havvand er udviklet til kystprojekter, øer, skibe, hoteller og B2B-entreprenører, der har brug for pålideligt drikke- eller procesvand fra havvand. Systemet behandler råvand med salinitet 10000-45000 ppm, bruger forbehandling og omvendt osmose og leverer 60 L/h-10000 L/h med mindst 99.7% saltafvisning. Styring, pumper, membrantal og beskyttelsesfunktioner tilpasses vandanalyse og projektkrav.	Lille og mellemstort RO-afsaltningssystem til 10000-45000 ppm råvand, 60-10000 L/h udbytte og OEM-projektkonfiguration.	Produktmodel|Råvandssalinitet|Nitratfjernelsesgrad|Indløbsvandtemperatur|Saltafvisning|Produktvandsflow|Produktvandssalinitet|Behandlingsproces|Styring og beskyttelse|Anvendelse|Tilpasning	Lille og mellemstort udstyr til afsaltning af havvand|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Tretrins forbehandling plus omvendt osmose; processen tilpasses efter vandanalyse|Automatisk drift, vandmangelsikring og overbelastningsbeskyttelse; funktioner efter projektbehov|Afsaltning af havvand og brakvand til kyst, ø, skib og projektvandforsyning|Membrantal, pumpe, spænding, kontrolpanel, ramme, rørføring og emballage kan konfigureres
de	Kleine und mittlere RO-Anlage zur Meerwasserentsalzung	Kleine und mittlere RO-Meerwasserentsalzung	Die kleine und mittlere RO-Anlage zur Meerwasserentsalzung von Yuchen Water ist für Küstenprojekte, Inseln, Schiffe, Hotels und B2B-Projektpartner ausgelegt, die aus Meerwasser zuverlässig Trink- oder Prozesswasser gewinnen müssen. Die Anlage verarbeitet Rohwasser mit 10000-45000 ppm Salzgehalt, kombiniert Vorbehandlung mit Umkehrosmose und liefert 60 L/h-10000 L/h bei mindestens 99.7% Entsalzungsrate. Steuerung, Pumpen, Membrananzahl und Schutzfunktionen werden nach Wasseranalyse und Projektanforderung angepasst.	Kleine und mittlere RO-Meerwasserentsalzungsanlage für 10000-45000 ppm Rohwasser, 60-10000 L/h Leistung und OEM-Projektkonfiguration.	Produktmodell|Rohwasser-Salzgehalt|Nitratentfernungsrate|Zulauftemperatur|Entsalzungsrate|Produktwasser-Durchfluss|Produktwasser-Salzgehalt|Aufbereitungsprozess|Steuerung und Schutz|Anwendung|Anpassung	Kleine und mittlere Meerwasserentsalzungsanlage|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Dreistufige Vorbehandlung plus Umkehrosmose; Prozess wird nach Wasseranalyse angepasst|Automatischer Betrieb, Wassermangelschutz und Überlastschutz; Funktionen nach Projektbedarf|Meerwasser- und Brackwasserentsalzung für Küsten, Inseln, Schiffe und Projektwasserversorgung|Membrananzahl, Pumpe, Spannung, Schaltschrank, Rahmen, Rohrleitung und Verpackung können konfiguriert werden
el	Μικρός και μεσαίος εξοπλισμός RO αφαλάτωσης θαλασσινού νερού	Μικρή και μεσαία αφαλάτωση θαλασσινού νερού RO	Ο μικρός και μεσαίος εξοπλισμός RO αφαλάτωσης θαλασσινού νερού της Yuchen Water προορίζεται για παράκτια έργα, νησιά, πλοία, ξενοδοχεία και B2B αναδόχους που χρειάζονται αξιόπιστο πόσιμο ή τεχνικό νερό από θαλασσινό νερό. Το σύστημα επεξεργάζεται αλατότητα ακατέργαστου νερού 10000-45000 ppm, χρησιμοποιεί προεπεξεργασία και αντίστροφη όσμωση και αποδίδει 60 L/h-10000 L/h με αφαλάτωση τουλάχιστον 99.7%. Ο έλεγχος, οι αντλίες, ο αριθμός μεμβρανών και οι προστασίες προσαρμόζονται στην ανάλυση νερού και στο έργο.	Μικρό και μεσαίο σύστημα RO αφαλάτωσης για ακατέργαστο νερό 10000-45000 ppm, παροχή 60-10000 L/h και διαμόρφωση έργου OEM.	Μοντέλο προϊόντος|Αλατότητα ακατέργαστου νερού|Ποσοστό απομάκρυνσης νιτρικών|Θερμοκρασία εισόδου νερού|Ποσοστό αφαλάτωσης|Ροή παραγόμενου νερού|Αλατότητα παραγόμενου νερού|Διαδικασία επεξεργασίας|Έλεγχος και προστασία|Εφαρμογή|Προσαρμογή	Μικρός και μεσαίος εξοπλισμός αφαλάτωσης θαλασσινού νερού|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Τριών σταδίων προεπεξεργασία και αντίστροφη όσμωση· η διαδικασία προσαρμόζεται στην ανάλυση νερού|Αυτόματη λειτουργία, προστασία έλλειψης νερού και υπερφόρτωσης· λειτουργίες ανά έργο|Αφαλάτωση θαλασσινού και υφάλμυρου νερού για ακτές, νησιά, πλοία και έργα υδροδότησης|Αριθμός μεμβρανών, αντλία, τάση, πίνακας ελέγχου, πλαίσιο, σωληνώσεις και συσκευασία διαμορφώνονται
en	Small and Medium Seawater Desalination RO Equipment	Small and Medium RO Seawater Desalination	Yuchen Water small and medium seawater desalination RO equipment is built for coastal projects, islands, vessels, hotels and B2B contractors that need reliable drinking or process water from seawater. The system treats 10000-45000 ppm raw water salinity, combines pretreatment with reverse osmosis, and delivers 60 L/h-10000 L/h product water with salt rejection of at least 99.7%. Control, pumps, membrane quantity and protection functions can be customized according to water analysis and project requirements.	Small and medium seawater desalination RO system for 10000-45000 ppm raw water, 60-10000 L/h output and OEM project configuration.	Product model|Raw water salinity|Nitrate removal rate|Inlet water temperature|Salt rejection|Product water flow|Product water salinity|Treatment process|Control and protection|Application|Customization	Small and medium seawater desalination equipment|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Three-stage pretreatment plus reverse osmosis; process customized by water analysis|Automatic operation, no-water protection and overload protection; functions selected by project need|Seawater and brackish water desalination for coastal, island, vessel and project water supply|Membrane quantity, pump, voltage, control panel, frame, piping and packaging can be configured
es	Equipo RO pequeño y mediano para desalinización de agua de mar	Desalinización RO pequeña y mediana de agua de mar	El equipo RO pequeño y mediano para desalinización de agua de mar de Yuchen Water está diseñado para proyectos costeros, islas, embarcaciones, hoteles y contratistas B2B que necesitan agua potable o de proceso fiable a partir de agua de mar. El sistema trata agua bruta con salinidad de 10000-45000 ppm, combina pretratamiento con ósmosis inversa y entrega 60 L/h-10000 L/h con rechazo de sal de al menos 99.7%. El control, las bombas, la cantidad de membranas y las protecciones se ajustan según el análisis del agua y el proyecto.	Sistema RO pequeño y mediano de desalinización para agua bruta 10000-45000 ppm, producción 60-10000 L/h y configuración OEM de proyecto.	Modelo de producto|Salinidad del agua bruta|Tasa de eliminación de nitratos|Temperatura de entrada|Rechazo de sal|Caudal de agua producida|Salinidad del agua producida|Proceso de tratamiento|Control y protección|Aplicación|Personalización	Equipo pequeño y mediano de desalinización de agua de mar|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Pretratamiento de tres etapas más ósmosis inversa; proceso personalizado según análisis del agua|Operación automática, protección sin agua y protección contra sobrecarga; funciones según el proyecto|Desalinización de agua de mar y salobre para costas, islas, embarcaciones y suministro de proyectos|Cantidad de membranas, bomba, voltaje, panel de control, bastidor, tuberías y embalaje configurables
et	Väike ja keskmine RO-seade merevee magestamiseks	Väike ja keskmine RO-merevee magestamine	Yuchen Water väike ja keskmine RO-seade merevee magestamiseks on mõeldud rannikuprojektidele, saartele, laevadele, hotellidele ja B2B töövõtjatele, kes vajavad mereveest usaldusväärset joogi- või protsessivett. Süsteem töötleb 10000-45000 ppm toorvee soolsust, kasutab eeltöötlust ja pöördosmoosi ning toodab 60 L/h-10000 L/h vett vähemalt 99.7% soolaeemaldusega. Juhtimine, pumbad, membraanide arv ja kaitsefunktsioonid kohandatakse veeanalüüsi ja projekti järgi.	Väike ja keskmine RO-merevee magestussüsteem 10000-45000 ppm toorveele, 60-10000 L/h tootlikkus ja OEM-projekti seadistus.	Tootemudel|Toorvee soolsus|Nitraadi eemaldamise määr|Sisendvee temperatuur|Soola eemaldamine|Tootevee vooluhulk|Tootevee soolsus|Töötlusprotsess|Juhtimine ja kaitse|Kasutus|Kohandamine	Väike ja keskmine merevee magestusseade|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Kolmeastmeline eeltöötlus ja pöördosmoos; protsess kohandatakse veeanalüüsi järgi|Automaatne töö, veepuuduse kaitse ja ülekoormuskaitse; funktsioonid projekti järgi|Merevee ja riimvee magestamine ranniku, saarte, laevade ja projektide veevarustuseks|Membraanide arv, pump, pinge, juhtpaneel, raam, torustik ja pakend kohandatavad
fa	تجهیزات کوچک و متوسط RO برای شیرین‌سازی آب دریا	شیرین‌سازی کوچک و متوسط آب دریا با RO	تجهیزات کوچک و متوسط RO برای شیرین‌سازی آب دریا از Yuchen Water برای پروژه‌های ساحلی، جزایر، شناورها، هتل‌ها و پیمانکاران B2B طراحی شده است که به آب آشامیدنی یا آب فرایندی مطمئن از آب دریا نیاز دارند. این سیستم شوری آب خام 10000-45000 ppm را تصفیه می‌کند، پیش‌تصفیه را با اسمز معکوس ترکیب می‌کند و با حذف نمک حداقل 99.7%، ظرفیت 60 L/h-10000 L/h آب تولیدی ارائه می‌دهد. کنترل، پمپ‌ها، تعداد ممبران و حفاظت‌ها بر اساس آنالیز آب و نیاز پروژه قابل تنظیم است.	سامانه کوچک و متوسط RO شیرین‌سازی آب دریا برای آب خام 10000-45000 ppm، خروجی 60-10000 L/h و پیکربندی پروژه OEM.	مدل محصول|شوری آب خام|نرخ حذف نیترات|دمای آب ورودی|نرخ حذف نمک|دبی آب تولیدی|شوری آب تولیدی|فرایند تصفیه|کنترل و حفاظت|کاربرد|سفارشی‌سازی	تجهیزات کوچک و متوسط شیرین‌سازی آب دریا|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|پیش‌تصفیه سه‌مرحله‌ای به همراه اسمز معکوس؛ فرایند بر اساس آنالیز آب تنظیم می‌شود|عملکرد خودکار، حفاظت بی‌آبی و حفاظت اضافه‌بار؛ امکانات بر اساس پروژه انتخاب می‌شود|شیرین‌سازی آب دریا و آب لب‌شور برای مناطق ساحلی، جزایر، شناورها و پروژه‌های تأمین آب|تعداد ممبران، پمپ، ولتاژ، تابلو کنترل، شاسی، لوله‌کشی و بسته‌بندی قابل پیکربندی است
fi	Pieni ja keskisuuri RO-laite meriveden suolanpoistoon	Pieni ja keskisuuri RO-meriveden suolanpoisto	Yuchen Waterin pieni ja keskisuuri RO-laite meriveden suolanpoistoon on tarkoitettu rannikkohankkeisiin, saarille, aluksiin, hotelleihin ja B2B-urakoitsijoille, jotka tarvitsevat luotettavaa juoma- tai prosessivettä merivedestä. Järjestelmä käsittelee 10000-45000 ppm raakaveden suolapitoisuutta, käyttää esikäsittelyä ja käänteisosmoosia sekä tuottaa 60 L/h-10000 L/h vettä vähintään 99.7% suolanpoistolla. Ohjaus, pumput, kalvomäärä ja suojaustoiminnot mukautetaan vesianalyysin ja hankkeen mukaan.	Pieni ja keskisuuri RO-suolanpoistojärjestelmä 10000-45000 ppm raakavedelle, 60-10000 L/h tuotto ja OEM-hankekonfiguraatio.	Tuotemalli|Raakaveden suolapitoisuus|Nitraatinpoistoaste|Tuloveden lämpötila|Suolanpoistoaste|Tuoteveden virtaus|Tuoteveden suolapitoisuus|Käsittelyprosessi|Ohjaus ja suojaus|Käyttö|Mukautus	Pieni ja keskisuuri meriveden suolanpoistolaite|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Kolmivaiheinen esikäsittely ja käänteisosmoosi; prosessi mukautetaan vesianalyysin mukaan|Automaattinen käyttö, vedenpuutteen suoja ja ylikuormitussuoja; toiminnot valitaan hankkeen mukaan|Meriveden ja murtoveden suolanpoisto rannikoille, saarille, aluksiin ja vesihuoltohankkeisiin|Kalvomäärä, pumppu, jännite, ohjauspaneeli, runko, putkisto ja pakkaus voidaan määrittää
fr	Équipement RO petit et moyen de dessalement d'eau de mer	Dessalement RO petit et moyen d'eau de mer	L'équipement RO petit et moyen de dessalement d'eau de mer de Yuchen Water est conçu pour les projets côtiers, îles, navires, hôtels et contractants B2B qui ont besoin d'eau potable ou d'eau de procédé fiable à partir d'eau de mer. Le système traite une salinité d'eau brute de 10000-45000 ppm, associe prétraitement et osmose inverse, et fournit 60 L/h-10000 L/h avec un taux de dessalement d'au moins 99.7%. La commande, les pompes, le nombre de membranes et les protections sont ajustés selon l'analyse de l'eau et le projet.	Système RO petit et moyen de dessalement pour eau brute 10000-45000 ppm, production 60-10000 L/h et configuration OEM de projet.	Modèle du produit|Salinité de l'eau brute|Taux d'élimination des nitrates|Température d'entrée|Taux de dessalement|Débit d'eau produite|Salinité de l'eau produite|Procédé de traitement|Commande et protection|Utilisation|Personnalisation	Équipement petit et moyen de dessalement d'eau de mer|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Prétraitement en trois étapes plus osmose inverse; procédé personnalisé selon l'analyse de l'eau|Fonctionnement automatique, protection manque d'eau et surcharge; fonctions selon le projet|Dessalement d'eau de mer et d'eau saumâtre pour côtes, îles, navires et projets d'alimentation en eau|Nombre de membranes, pompe, tension, panneau de commande, châssis, tuyauterie et emballage configurables
ha	Ƙananan da matsakaicin kayan RO na cire gishirin ruwan teku	Cire gishirin ruwan teku na RO ƙarami da matsakaici	Kayan RO na Yuchen Water don cire gishirin ruwan teku ƙarami da matsakaici an tsara su ne don ayyukan bakin teku, tsibirai, jiragen ruwa, otal-otal da 'yan kwangilar B2B da ke bukatar amintaccen ruwan sha ko ruwan aiki daga ruwan teku. Tsarin yana sarrafa gishirin ruwa na 10000-45000 ppm, yana amfani da pre-treatment da reverse osmosis, sannan yana samar da 60 L/h-10000 L/h tare da cire gishiri akalla 99.7%. Ana daidaita sarrafawa, famfo, yawan membrane da kariya bisa gwajin ruwa da bukatar aiki.	Tsarin RO ƙarami da matsakaici don ruwan teku 10000-45000 ppm, fitarwa 60-10000 L/h da tsarin OEM na aiki.	Samfurin kaya|Gishirin ruwa na farko|Yawan cire nitrate|Zafin ruwan shiga|Yawan cire gishiri|Gudun ruwan da aka samar|Gishirin ruwan da aka samar|Tsarin tacewa|Sarrafa da kariya|Amfani|Keɓancewa	Ƙananan da matsakaicin kayan cire gishirin ruwan teku|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Matakai uku na pre-treatment da reverse osmosis; ana tsara tsari bisa gwajin ruwa|Aiki ta atomatik, kariyar babu ruwa da kariyar nauyi fiye da kima; ayyuka bisa bukatar aiki|Cire gishirin ruwan teku da ruwa mai gishiri ga bakin teku, tsibirai, jirage da samar da ruwa na aiki|Yawan membrane, famfo, wuta, allon sarrafawa, firam, bututu da marufi ana iya daidaitawa
he	ציוד RO קטן ובינוני להתפלת מי ים	התפלת מי ים RO בקנה קטן ובינוני	ציוד RO קטן ובינוני להתפלת מי ים של Yuchen Water מיועד לפרויקטים חופיים, איים, כלי שיט, מלונות וקבלני B2B הזקוקים למי שתייה או מי תהליך אמינים ממי ים. המערכת מטפלת במליחות מים גולמיים של 10000-45000 ppm, משלבת טיפול מקדים עם אוסמוזה הפוכה ומפיקה 60 L/h-10000 L/h עם דחיית מלח של לפחות 99.7%. הבקרה, המשאבות, מספר הממברנות ופונקציות ההגנה מותאמים לפי ניתוח מים ודרישות הפרויקט.	מערכת RO קטנה ובינונית להתפלת מי ים עבור מים גולמיים 10000-45000 ppm, תפוקה 60-10000 L/h ותצורת OEM לפרויקט.	דגם מוצר|מליחות מים גולמיים|שיעור הסרת ניטראט|טמפרטורת מי כניסה|דחיית מלח|ספיקת מים מופקים|מליחות מים מופקים|תהליך טיפול|בקרה והגנה|יישום|התאמה אישית	ציוד קטן ובינוני להתפלת מי ים|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|טיפול מקדים בשלושה שלבים בתוספת אוסמוזה הפוכה; התהליך מותאם לפי ניתוח מים|הפעלה אוטומטית, הגנת חוסר מים והגנת עומס יתר; פונקציות לפי צורך הפרויקט|התפלת מי ים ומים מליחים לחופים, איים, כלי שיט ופרויקטי אספקת מים|מספר ממברנות, משאבה, מתח, לוח בקרה, שלדה, צנרת ואריזה ניתנים להגדרה
hi	छोटे और मध्यम RO समुद्री जल विलवणीकरण उपकरण	छोटा और मध्यम RO समुद्री जल विलवणीकरण	Yuchen Water के छोटे और मध्यम RO समुद्री जल विलवणीकरण उपकरण तटीय परियोजनाओं, द्वीपों, जहाजों, होटलों और B2B ठेकेदारों के लिए बनाए गए हैं जिन्हें समुद्री जल से भरोसेमंद पेय या प्रक्रिया जल चाहिए। सिस्टम 10000-45000 ppm कच्चे पानी की लवणता संभालता है, प्री-ट्रीटमेंट और रिवर्स ऑस्मोसिस को मिलाता है, और कम से कम 99.7% नमक हटाने के साथ 60 L/h-10000 L/h उत्पाद जल देता है। नियंत्रण, पंप, मेम्ब्रेन संख्या और सुरक्षा कार्य जल विश्लेषण और परियोजना के अनुसार अनुकूलित होते हैं।	10000-45000 ppm कच्चे पानी के लिए छोटा और मध्यम RO समुद्री जल विलवणीकरण सिस्टम, 60-10000 L/h उत्पादन और OEM परियोजना कॉन्फ़िगरेशन।	उत्पाद मॉडल|कच्चे पानी की लवणता|नाइट्रेट हटाने की दर|इनलेट पानी तापमान|नमक हटाने की दर|उत्पाद जल प्रवाह|उत्पाद जल लवणता|उपचार प्रक्रिया|नियंत्रण और सुरक्षा|अनुप्रयोग|अनुकूलन	छोटे और मध्यम समुद्री जल विलवणीकरण उपकरण|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|तीन-चरण प्री-ट्रीटमेंट और रिवर्स ऑस्मोसिस; प्रक्रिया जल विश्लेषण के अनुसार अनुकूलित|स्वचालित संचालन, पानी न होने की सुरक्षा और ओवरलोड सुरक्षा; कार्य परियोजना के अनुसार चुने जाते हैं|तटीय, द्वीप, जहाज और परियोजना जल आपूर्ति के लिए समुद्री और खारे पानी का विलवणीकरण|मेम्ब्रेन संख्या, पंप, वोल्टेज, नियंत्रण पैनल, फ्रेम, पाइपिंग और पैकेजिंग कॉन्फ़िगर किए जा सकते हैं
hr	Mala i srednja RO oprema za desalinizaciju morske vode	Mala i srednja RO desalinizacija morske vode	Mala i srednja RO oprema za desalinizaciju morske vode tvrtke Yuchen Water namijenjena je obalnim projektima, otocima, plovilima, hotelima i B2B izvođačima kojima treba pouzdana pitka ili procesna voda iz morske vode. Sustav obrađuje sirovu vodu saliniteta 10000-45000 ppm, koristi predobradu i reverznu osmozu te daje 60 L/h-10000 L/h uz uklanjanje soli najmanje 99.7%. Upravljanje, pumpe, broj membrana i zaštite prilagođavaju se analizi vode i projektu.	Mali i srednji RO sustav za morsku vodu 10000-45000 ppm, izlaz 60-10000 L/h i OEM konfiguracija projekta.	Model proizvoda|Salinitet sirove vode|Stopa uklanjanja nitrata|Temperatura ulazne vode|Uklanjanje soli|Protok proizvedene vode|Salinitet proizvedene vode|Proces obrade|Upravljanje i zaštita|Primjena|Prilagodba	Mala i srednja oprema za desalinizaciju morske vode|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Trostupanjska predobrada plus reverzna osmoza; proces se prilagođava prema analizi vode|Automatski rad, zaštita od rada bez vode i preopterećenja; funkcije prema projektu|Desalinizacija morske i bočate vode za obalu, otoke, plovila i projekte vodoopskrbe|Broj membrana, pumpa, napon, upravljačka ploča, okvir, cjevovod i pakiranje mogu se konfigurirati
hu	Kis és közepes RO tengervíz-sótalanító berendezés	Kis és közepes RO tengervíz-sótalanítás	A Yuchen Water kis és közepes RO tengervíz-sótalanító berendezése part menti projektekhez, szigetekhez, hajókhoz, szállodákhoz és B2B kivitelezőknek készült, akiknek tengervízből megbízható ivó- vagy technológiai vízre van szükségük. A rendszer 10000-45000 ppm nyersvíz-sótartalmat kezel, előkezelést és fordított ozmózist alkalmaz, és legalább 99.7% sóvisszatartással 60 L/h-10000 L/h termelt vizet biztosít. A vezérlés, szivattyúk, membránszám és védelmek vízanalízis és projekt szerint állíthatók.	Kis és közepes RO sótalanító rendszer 10000-45000 ppm nyersvízhez, 60-10000 L/h kapacitással és OEM projektkonfigurációval.	Termékmodell|Nyersvíz sótartalma|Nitráteltávolítási arány|Belépő víz hőmérséklete|Sótalanítási arány|Termelt víz áramlása|Termelt víz sótartalma|Kezelési folyamat|Vezérlés és védelem|Alkalmazás|Testreszabás	Kis és közepes tengervíz-sótalanító berendezés|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Háromlépcsős előkezelés és fordított ozmózis; folyamat vízanalízis alapján testreszabva|Automatikus működés, vízhiány- és túlterhelés-védelem; funkciók projekt szerint|Tengervíz és brakkvíz sótalanítása part menti, szigeti, hajós és projekt vízellátáshoz|Membránszám, szivattyú, feszültség, vezérlőpanel, váz, csővezeték és csomagolás konfigurálható
hy	Փոքր և միջին RO ծովաջրի աղազրկման սարքավորում	Փոքր և միջին RO ծովաջրի աղազրկում	Yuchen Water-ի փոքր և միջին RO ծովաջրի աղազրկման սարքավորումը նախատեսված է ափամերձ նախագծերի, կղզիների, նավերի, հյուրանոցների և B2B կապալառուների համար, որոնք ծովաջրից վստահելի խմելու կամ տեխնոլոգիական ջուր են պահանջում։ Համակարգը մշակում է 10000-45000 ppm հում ջրի աղայնություն, օգտագործում է նախամշակում և հակադարձ օսմոս, և ապահովում է 60 L/h-10000 L/h արտադրական ջուր առնվազն 99.7% աղազրկմամբ։ Կառավարումը, պոմպերը, մեմբրանների քանակը և պաշտպանությունները կարգավորվում են ջրի վերլուծությամբ և նախագծի պահանջով։	Փոքր և միջին RO ծովաջրի աղազրկման համակարգ 10000-45000 ppm հում ջրի, 60-10000 L/h ելքի և OEM նախագծային կազմաձևման համար։	Ապրանքի մոդել|Հում ջրի աղայնություն|Նիտրատի հեռացման տոկոս|Մուտքային ջրի ջերմաստիճան|Աղազրկման տոկոս|Արտադրական ջրի հոսք|Արտադրական ջրի աղայնություն|Մշակման գործընթաց|Կառավարում և պաշտպանություն|Կիրառում|Հարմարեցում	Փոքր և միջին ծովաջրի աղազրկման սարքավորում|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Եռաստիճան նախամշակում և հակադարձ օսմոս; գործընթացը հարմարեցվում է ջրի վերլուծությամբ|Ավտոմատ աշխատանք, անջրության պաշտպանություն և գերբեռնվածության պաշտպանություն; գործառույթները ըստ նախագծի|Ծովաջրի և աղի ջրի աղազրկում ափամերձ, կղզային, նավային և նախագծային ջրամատակարարման համար|Մեմբրանների քանակը, պոմպը, լարումը, կառավարման վահանակը, շրջանակը, խողովակաշարը և փաթեթավորումը կարող են կազմաձևվել
id	Peralatan RO desalinasi air laut kecil dan menengah	Desalinasi air laut RO kecil dan menengah	Peralatan RO desalinasi air laut kecil dan menengah dari Yuchen Water dibuat untuk proyek pesisir, pulau, kapal, hotel dan kontraktor B2B yang membutuhkan air minum atau air proses yang andal dari air laut. Sistem ini mengolah salinitas air baku 10000-45000 ppm, menggabungkan pra-perlakuan dengan reverse osmosis, dan menghasilkan 60 L/h-10000 L/h dengan penolakan garam minimal 99.7%. Kontrol, pompa, jumlah membran dan fungsi perlindungan dapat disesuaikan berdasarkan analisis air dan kebutuhan proyek.	Sistem RO desalinasi air laut kecil dan menengah untuk air baku 10000-45000 ppm, output 60-10000 L/h dan konfigurasi proyek OEM.	Model produk|Salinitas air baku|Tingkat penghilangan nitrat|Suhu air masuk|Penolakan garam|Aliran air produk|Salinitas air produk|Proses pengolahan|Kontrol dan perlindungan|Aplikasi|Kustomisasi	Peralatan desalinasi air laut kecil dan menengah|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Pra-perlakuan tiga tahap ditambah reverse osmosis; proses disesuaikan menurut analisis air|Operasi otomatis, perlindungan tanpa air dan perlindungan beban lebih; fungsi sesuai proyek|Desalinasi air laut dan air payau untuk pesisir, pulau, kapal dan pasokan air proyek|Jumlah membran, pompa, tegangan, panel kontrol, rangka, pipa dan kemasan dapat dikonfigurasi
it	Impianto RO piccolo e medio per dissalazione dell'acqua di mare	Dissalazione RO piccola e media dell'acqua di mare	L'impianto RO piccolo e medio per dissalazione dell'acqua di mare di Yuchen Water è progettato per progetti costieri, isole, imbarcazioni, hotel e appaltatori B2B che necessitano di acqua potabile o di processo affidabile da acqua marina. Il sistema tratta acqua grezza con salinità 10000-45000 ppm, combina pretrattamento e osmosi inversa e produce 60 L/h-10000 L/h con rimozione dei sali di almeno 99.7%. Controllo, pompe, numero di membrane e protezioni sono configurabili secondo analisi dell'acqua e progetto.	Sistema RO piccolo e medio per acqua marina 10000-45000 ppm, produzione 60-10000 L/h e configurazione OEM di progetto.	Modello prodotto|Salinità acqua grezza|Tasso di rimozione nitrati|Temperatura acqua in ingresso|Rimozione sali|Portata acqua prodotta|Salinità acqua prodotta|Processo di trattamento|Controllo e protezione|Applicazione|Personalizzazione	Impianto piccolo e medio per dissalazione dell'acqua di mare|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Pretrattamento a tre stadi più osmosi inversa; processo configurato secondo analisi dell'acqua|Funzionamento automatico, protezione mancanza acqua e sovraccarico; funzioni secondo progetto|Dissalazione di acqua marina e salmastra per coste, isole, imbarcazioni e forniture idriche di progetto|Numero membrane, pompa, tensione, quadro di controllo, telaio, tubazioni e imballo configurabili
ja	小中型海水淡水化RO装置	小中型RO海水淡水化	Yuchen Waterの小中型海水淡水化RO装置は、沿岸プロジェクト、島しょ部、船舶、ホテル、B2B工事会社向けに、海水から安定した飲用水またはプロセス水を得るために設計されています。原水塩分10000-45000 ppmに対応し、前処理と逆浸透膜を組み合わせ、99.7%以上の脱塩率で60 L/h-10000 L/hの処理水を供給します。制御方式、ポンプ、膜本数、保護機能は水質分析と案件条件に合わせて調整できます。	原水10000-45000 ppmに対応する小中型RO海水淡水化システム。処理量60-10000 L/h、OEM案件仕様に対応。	製品モデル|原水塩分|硝酸塩除去率|給水温度|脱塩率|処理水流量|処理水塩分|処理プロセス|制御と保護|用途|カスタム対応	小中型海水淡水化設備|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|三段階前処理と逆浸透膜。水質分析に基づきプロセスを調整|自動運転、無水保護、過負荷保護。機能は案件条件で選定|沿岸、島しょ部、船舶、プロジェクト給水向けの海水・汽水淡水化|膜本数、ポンプ、電圧、制御盤、フレーム、配管、梱包を構成可能
ka	მცირე და საშუალო RO ზღვის წყლის გამტკნარების მოწყობილობა	მცირე და საშუალო RO ზღვის წყლის გამტკნარება	Yuchen Water-ის მცირე და საშუალო RO ზღვის წყლის გამტკნარების მოწყობილობა განკუთვნილია სანაპირო პროექტებისთვის, კუნძულებისთვის, გემებისთვის, სასტუმროებისთვის და B2B კონტრაქტორებისთვის, რომლებსაც სჭირდებათ სანდო სასმელი ან ტექნოლოგიური წყალი ზღვის წყლიდან. სისტემა ამუშავებს 10000-45000 ppm ნედლი წყლის მარილიანობას, იყენებს წინასწარ დამუშავებას და უკუ ოსმოსს და იძლევა 60 L/h-10000 L/h წყალს მინიმუმ 99.7% მარილის მოცილებით. მართვა, ტუმბოები, მემბრანების რაოდენობა და დაცვა ერგება წყლის ანალიზსა და პროექტს.	მცირე და საშუალო RO გამტკნარების სისტემა 10000-45000 ppm ნედლი წყლისთვის, 60-10000 L/h გამოსავლით და OEM პროექტის კონფიგურაციით.	პროდუქტის მოდელი|ნედლი წყლის მარილიანობა|ნიტრატის მოცილების მაჩვენებელი|შემავალი წყლის ტემპერატურა|მარილის მოცილება|წარმოებული წყლის ნაკადი|წარმოებული წყლის მარილიანობა|დამუშავების პროცესი|მართვა და დაცვა|გამოყენება|მორგება	მცირე და საშუალო ზღვის წყლის გამტკნარების მოწყობილობა|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|სამეტაპიანი წინასწარი დამუშავება და უკუ ოსმოსი; პროცესი მორგებულია წყლის ანალიზზე|ავტომატური მუშაობა, უწყლობის დაცვა და გადატვირთვის დაცვა; ფუნქციები პროექტის მიხედვით|ზღვისა და მლაშე წყლის გამტკნარება სანაპიროსთვის, კუნძულებისთვის, გემებისთვის და პროექტებისთვის|მემბრანების რაოდენობა, ტუმბო, ძაბვა, მართვის პანელი, ჩარჩო, მილები და შეფუთვა მორგებადია
kk	Шағын және орта RO теңіз суын тұщыландыру жабдығы	Шағын және орта RO теңіз суын тұщыландыру	Yuchen Water шағын және орта RO теңіз суын тұщыландыру жабдығы жағалау жобалары, аралдар, кемелер, қонақ үйлер және теңіз суынан сенімді ауыз немесе технологиялық су қажет B2B мердігерлеріне арналған. Жүйе 10000-45000 ppm шикі су тұздылығын өңдейді, алдын ала тазарту мен кері осмосты біріктіреді және кемінде 99.7% тұзды ұстап, 60 L/h-10000 L/h өнім суын береді. Басқару, сорғылар, мембрана саны және қорғаныс функциялары су талдауы мен жобаға қарай реттеледі.	10000-45000 ppm шикі суға арналған шағын және орта RO теңіз суын тұщыландыру жүйесі, 60-10000 L/h өнімділік және OEM жоба конфигурациясы.	Өнім моделі|Шикі су тұздылығы|Нитратты жою деңгейі|Кіріс су температурасы|Тұзды ұстау деңгейі|Өнім су ағыны|Өнім су тұздылығы|Тазарту процесі|Басқару және қорғаныс|Қолданылуы|Баптау	Шағын және орта теңіз суын тұщыландыру жабдығы|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Үш сатылы алдын ала тазарту және кері осмос; процесс су талдауына қарай бапталады|Автоматты жұмыс, сусыз қорғаныс және артық жүктемеден қорғаныс; функциялар жобаға сай таңдалады|Жағалау, арал, кеме және жоба сумен жабдықтауына арналған теңіз және тұзды суды тұщыландыру|Мембрана саны, сорғы, кернеу, басқару панелі, рама, құбыр және қаптама конфигурацияланады
ko	소중형 해수 담수화 RO 장비	소중형 RO 해수 담수화	Yuchen Water의 소중형 해수 담수화 RO 장비는 해안 프로젝트, 섬, 선박, 호텔 및 해수에서 안정적인 음용수나 공정수가 필요한 B2B 시공사를 위해 설계되었습니다. 이 시스템은 10000-45000 ppm 원수 염도를 처리하고 전처리와 역삼투를 결합하여 최소 99.7% 탈염률로 60 L/h-10000 L/h의 생산수를 제공합니다. 제어, 펌프, 멤브레인 수량 및 보호 기능은 수질 분석과 프로젝트 조건에 맞게 조정됩니다.	10000-45000 ppm 원수를 위한 소중형 RO 해수 담수화 시스템, 60-10000 L/h 생산량 및 OEM 프로젝트 구성 지원.	제품 모델|원수 염도|질산염 제거율|입수 온도|탈염률|생산수 유량|생산수 염도|처리 공정|제어 및 보호|적용 분야|맞춤 구성	소중형 해수 담수화 장비|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|3단계 전처리와 역삼투; 수질 분석에 따라 공정 맞춤 구성|자동 운전, 무수 보호, 과부하 보호; 기능은 프로젝트 요구에 따라 선택|해안, 섬, 선박 및 프로젝트 급수용 해수와 기수 담수화|멤브레인 수량, 펌프, 전압, 제어반, 프레임, 배관 및 포장 구성 가능
ku	Amûra RO ya piçûk û navîn ji bo şoravkirina ava deryayê	Şoravkirina ava deryayê ya RO piçûk û navîn	Amûra RO ya Yuchen Water ji bo şoravkirina ava deryayê ya piçûk û navîn ji bo projeyên qeraxê deryayê, giravan, keştiyan, otelan û kontraktorên B2B hatiye çêkirin ku ji ava deryayê ava vexwarinê an ava prosesê ya bawer dixwazin. Pergal şorbûna ava xam 10000-45000 ppm dixebitîne, pêş-dermankirin û osmoza berevajî bi hev re bikar tîne, û bi derxistina xwê ya herî kêm 99.7% 60 L/h-10000 L/h ava hilberînê dide. Kontrol, pomp, hejmareya membranan û parastin li gorî analîza avê û projeyê têne sazkirin.	Pergala RO ya piçûk û navîn ji bo ava xam 10000-45000 ppm, derketina 60-10000 L/h û konfigûrasyona projeya OEM.	Modela hilberê|Şorbûna ava xam|Rêjeya rakirina nitratê|Germahiya ava ketinê|Rêjeya rakirina xwê|Herikîna ava hilberînê|Şorbûna ava hilberînê|Pêvajoya dermankirinê|Kontrol û parastin|Bikaranîn|Taybetkirin	Amûra piçûk û navîn ya şoravkirina ava deryayê|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Pêş-dermankirina sê qonaxan û osmoza berevajî; pêvajo li gorî analîza avê tê taybetkirin|Xebata otomatîk, parastina bê av û parastina bargiraniyê; fonksiyon li gorî projeyê|Şoravkirina ava deryayê û ava nîv-şor ji bo qerax, girav, keştî û peydakirina ava projeyê|Hejmareya membran, pomp, voltaj, panela kontrolê, çarçove, borî û pakêt dikarin werin sazkirin
ky	Чакан жана орто RO деңиз суусун тузсуздандыруу жабдуусу	Чакан жана орто RO деңиз суусун тузсуздандыруу	Yuchen Water чакан жана орто RO деңиз суусун тузсуздандыруу жабдуусу жээк долбоорлору, аралдар, кемелер, мейманканалар жана деңиз суусунан ишенимдүү ичүүчү же технологиялык суу талап кылган B2B подрядчылары үчүн жасалган. Система 10000-45000 ppm чийки суу туздуулугун иштетет, алдын ала тазалоо менен тескери осмосту айкалыштырат жана кеминде 99.7% туз кармоо менен 60 L/h-10000 L/h таза суу берет. Башкаруу, насостор, мембрана саны жана коргоо функциялары суу анализине жана долбоорго жараша жөндөлөт.	10000-45000 ppm чийки суу үчүн чакан жана орто RO деңиз суусун тузсуздандыруу системасы, 60-10000 L/h өндүрүм жана OEM долбоор конфигурациясы.	Өнүм модели|Чийки суунун туздуулугу|Нитратты кетирүү деңгээли|Кирүүчү суунун температурасы|Тузду кетирүү деңгээли|Өндүрүлгөн суунун агымы|Өндүрүлгөн суунун туздуулугу|Тазалоо процесси|Башкаруу жана коргоо|Колдонуу|Ыңгайлаштыруу	Чакан жана орто деңиз суусун тузсуздандыруу жабдуусу|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Үч баскычтуу алдын ала тазалоо жана тескери осмос; процесс суу анализине жараша ыңгайлашат|Автоматтык иштөө, суусуз коргоо жана ашыкча жүктөн коргоо; функциялар долбоорго жараша тандалат|Жээк, арал, кеме жана долбоордук суу менен камсыздоо үчүн деңиз жана туздуу сууну тузсуздандыруу|Мембрана саны, насос, чыңалуу, башкаруу панели, рама, түтүк жана таңгак конфигурацияланат
lt	Maža ir vidutinė RO įranga jūros vandens gėlinimui	Mažas ir vidutinis RO jūros vandens gėlinimas	Yuchen Water maža ir vidutinė RO įranga jūros vandens gėlinimui skirta pakrančių projektams, saloms, laivams, viešbučiams ir B2B rangovams, kuriems reikia patikimo geriamojo ar technologinio vandens iš jūros vandens. Sistema apdoroja 10000-45000 ppm žaliavinio vandens druskingumą, naudoja pirminį paruošimą ir atvirkštinį osmosą, tiekia 60 L/h-10000 L/h vandenį su bent 99.7% druskos šalinimu. Valdymas, siurbliai, membranų skaičius ir apsaugos pritaikomos pagal vandens analizę ir projektą.	Maža ir vidutinė RO jūros vandens gėlinimo sistema 10000-45000 ppm vandeniui, 60-10000 L/h našumas ir OEM projekto konfigūracija.	Gaminio modelis|Žaliavinio vandens druskingumas|Nitratų šalinimo norma|Įeinančio vandens temperatūra|Druskos šalinimas|Produkto vandens srautas|Produkto vandens druskingumas|Apdorojimo procesas|Valdymas ir apsauga|Taikymas|Pritaikymas	Maža ir vidutinė jūros vandens gėlinimo įranga|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Trijų etapų pirminis paruošimas ir atvirkštinis osmosas; procesas pritaikomas pagal vandens analizę|Automatinis veikimas, apsauga nuo vandens trūkumo ir perkrovos; funkcijos pagal projektą|Jūros ir sūroko vandens gėlinimas pakrantėms, saloms, laivams ir vandens tiekimo projektams|Membranų skaičius, siurblys, įtampa, valdymo skydas, rėmas, vamzdynas ir pakuotė konfigūruojami
lv	Maza un vidēja RO iekārta jūras ūdens atsāļošanai	Maza un vidēja RO jūras ūdens atsāļošana	Yuchen Water maza un vidēja RO iekārta jūras ūdens atsāļošanai ir paredzēta piekrastes projektiem, salām, kuģiem, viesnīcām un B2B darbuzņēmējiem, kam nepieciešams uzticams dzeramais vai procesa ūdens no jūras ūdens. Sistēma apstrādā 10000-45000 ppm neapstrādāta ūdens sāļumu, izmanto priekšapstrādi un reverso osmozi un nodrošina 60 L/h-10000 L/h ūdens ar vismaz 99.7% sāls atdalīšanu. Vadība, sūkņi, membrānu skaits un aizsardzības funkcijas tiek pielāgotas ūdens analīzei un projektam.	Maza un vidēja RO jūras ūdens atsāļošanas sistēma 10000-45000 ppm neapstrādātam ūdenim, 60-10000 L/h ražība un OEM projekta konfigurācija.	Produkta modelis|Neapstrādāta ūdens sāļums|Nitrātu atdalīšanas pakāpe|Ieplūdes ūdens temperatūra|Sāls atdalīšana|Produkta ūdens plūsma|Produkta ūdens sāļums|Apstrādes process|Vadība un aizsardzība|Pielietojums|Pielāgošana	Maza un vidēja jūras ūdens atsāļošanas iekārta|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Trīspakāpju priekšapstrāde un reversā osmoze; process pielāgots pēc ūdens analīzes|Automātiska darbība, aizsardzība pret ūdens trūkumu un pārslodzi; funkcijas pēc projekta|Jūras un iesāļa ūdens atsāļošana piekrastei, salām, kuģiem un ūdensapgādes projektiem|Membrānu skaits, sūknis, spriegums, vadības panelis, rāmis, cauruļvadi un iepakojums konfigurējami
ms	Peralatan RO penyahgaraman air laut kecil dan sederhana	Penyahgaraman air laut RO kecil dan sederhana	Peralatan RO penyahgaraman air laut kecil dan sederhana Yuchen Water dibina untuk projek pesisir, pulau, kapal, hotel dan kontraktor B2B yang memerlukan air minuman atau air proses yang boleh dipercayai daripada air laut. Sistem ini merawat kemasinan air mentah 10000-45000 ppm, menggabungkan pra-rawatan dengan osmosis songsang dan menghasilkan 60 L/h-10000 L/h dengan penyingkiran garam sekurang-kurangnya 99.7%. Kawalan, pam, bilangan membran dan fungsi perlindungan boleh disesuaikan mengikut analisis air dan projek.	Sistem RO penyahgaraman kecil dan sederhana untuk air mentah 10000-45000 ppm, keluaran 60-10000 L/h dan konfigurasi projek OEM.	Model produk|Kemasinan air mentah|Kadar penyingkiran nitrat|Suhu air masuk|Penyingkiran garam|Aliran air produk|Kemasinan air produk|Proses rawatan|Kawalan dan perlindungan|Aplikasi|Penyesuaian	Peralatan penyahgaraman air laut kecil dan sederhana|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Pra-rawatan tiga peringkat ditambah osmosis songsang; proses disesuaikan mengikut analisis air|Operasi automatik, perlindungan tiada air dan perlindungan beban lebih; fungsi mengikut projek|Penyahgaraman air laut dan air payau untuk pesisir, pulau, kapal dan bekalan air projek|Bilangan membran, pam, voltan, panel kawalan, rangka, paip dan pembungkusan boleh dikonfigurasikan
nl	Kleine en middelgrote RO-installatie voor zeewaterontzilting	Kleine en middelgrote RO-zeewaterontzilting	De kleine en middelgrote RO-installatie voor zeewaterontzilting van Yuchen Water is ontwikkeld voor kustprojecten, eilanden, schepen, hotels en B2B-aannemers die betrouwbaar drink- of proceswater uit zeewater nodig hebben. Het systeem behandelt ruw water met 10000-45000 ppm zoutgehalte, combineert voorbehandeling met omgekeerde osmose en levert 60 L/h-10000 L/h productwater met minstens 99.7% zoutverwijdering. Besturing, pompen, membraanaantal en beveiligingen worden afgestemd op wateranalyse en project.	Klein en middelgroot RO-ontziltingssysteem voor 10000-45000 ppm ruw water, 60-10000 L/h output en OEM-projectconfiguratie.	Productmodel|Zoutgehalte ruw water|Nitraatverwijderingsgraad|Inlaatwatertemperatuur|Zoutverwijdering|Productwaterdebiet|Zoutgehalte productwater|Behandelingsproces|Besturing en bescherming|Toepassing|Maatwerk	Kleine en middelgrote zeewaterontziltingsinstallatie|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Drietraps voorbehandeling plus omgekeerde osmose; proces op basis van wateranalyse aangepast|Automatische werking, droogloopbeveiliging en overbelastingsbeveiliging; functies volgens project|Ontzilting van zeewater en brak water voor kust, eilanden, schepen en projectwatervoorziening|Membraanaantal, pomp, spanning, bedieningspaneel, frame, leidingwerk en verpakking configureerbaar
no	Lite og mellomstort RO-anlegg for avsalting av sjøvann	Liten og mellomstor RO-avsalting av sjøvann	Yuchen Water lite og mellomstort RO-anlegg for avsalting av sjøvann er laget for kystprosjekter, øyer, fartøy, hoteller og B2B-entreprenører som trenger pålitelig drikke- eller prosessvann fra sjøvann. Systemet behandler råvann med salinitet 10000-45000 ppm, bruker forbehandling og omvendt osmose og leverer 60 L/h-10000 L/h med minst 99.7% saltfjerning. Styring, pumper, membrantall og beskyttelse tilpasses vannanalyse og prosjektkrav.	Lite og mellomstort RO-avsaltingssystem for 10000-45000 ppm råvann, 60-10000 L/h produksjon og OEM-prosjektkonfigurasjon.	Produktmodell|Salinitet i råvann|Nitratfjerningsgrad|Innløpsvanntemperatur|Saltfjerning|Produktvannstrøm|Salinitet i produktvann|Behandlingsprosess|Styring og beskyttelse|Bruk|Tilpasning	Lite og mellomstort utstyr for avsalting av sjøvann|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Tretrinns forbehandling pluss omvendt osmose; prosess tilpasses etter vannanalyse|Automatisk drift, beskyttelse mot vannmangel og overbelastning; funksjoner etter prosjekt|Avsalting av sjøvann og brakkvann for kyst, øyer, fartøy og prosjektvannforsyning|Membrantall, pumpe, spenning, kontrollpanel, ramme, rørføring og emballasje kan konfigureres
pl	Małe i średnie urządzenie RO do odsalania wody morskiej	Małe i średnie odsalanie wody morskiej RO	Małe i średnie urządzenie RO do odsalania wody morskiej Yuchen Water jest przeznaczone dla projektów przybrzeżnych, wysp, jednostek pływających, hoteli i wykonawców B2B, którzy potrzebują niezawodnej wody pitnej lub procesowej z wody morskiej. System obsługuje zasolenie wody surowej 10000-45000 ppm, łączy wstępne uzdatnianie z odwróconą osmozą i dostarcza 60 L/h-10000 L/h przy odsalaniu co najmniej 99.7%. Sterowanie, pompy, liczba membran i zabezpieczenia są dobierane według analizy wody i projektu.	Mały i średni system RO do odsalania wody 10000-45000 ppm, wydajność 60-10000 L/h i konfiguracja projektu OEM.	Model produktu|Zasolenie wody surowej|Stopień usuwania azotanów|Temperatura wody zasilającej|Stopień odsalania|Przepływ wody produkcyjnej|Zasolenie wody produkcyjnej|Proces uzdatniania|Sterowanie i ochrona|Zastosowanie|Dostosowanie	Małe i średnie urządzenie do odsalania wody morskiej|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Trzystopniowe wstępne uzdatnianie plus odwrócona osmoza; proces dostosowany do analizy wody|Praca automatyczna, ochrona przed brakiem wody i przeciążeniem; funkcje według projektu|Odsalanie wody morskiej i słonawej dla wybrzeży, wysp, statków i projektów wodnych|Liczba membran, pompa, napięcie, panel sterowania, rama, rurociąg i opakowanie konfigurowalne
pt	Equipamento RO pequeno e médio para dessalinização de água do mar	Dessalinização RO pequena e média de água do mar	O equipamento RO pequeno e médio para dessalinização de água do mar da Yuchen Water é desenvolvido para projetos costeiros, ilhas, embarcações, hotéis e contratantes B2B que precisam de água potável ou de processo confiável a partir de água do mar. O sistema trata água bruta com salinidade de 10000-45000 ppm, combina pré-tratamento com osmose reversa e entrega 60 L/h-10000 L/h com remoção de sal de pelo menos 99.7%. Controle, bombas, número de membranas e proteções são ajustados conforme análise da água e projeto.	Sistema RO pequeno e médio para água bruta 10000-45000 ppm, produção 60-10000 L/h e configuração OEM de projeto.	Modelo do produto|Salinidade da água bruta|Taxa de remoção de nitrato|Temperatura da água de entrada|Remoção de sal|Vazão de água produzida|Salinidade da água produzida|Processo de tratamento|Controle e proteção|Aplicação|Personalização	Equipamento pequeno e médio para dessalinização de água do mar|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Pré-tratamento em três etapas mais osmose reversa; processo personalizado pela análise da água|Operação automática, proteção contra falta de água e sobrecarga; funções conforme projeto|Dessalinização de água do mar e salobra para costa, ilhas, embarcações e projetos de abastecimento|Número de membranas, bomba, tensão, painel de controle, estrutura, tubulação e embalagem configuráveis
ro	Echipament RO mic și mediu pentru desalinizarea apei de mare	Desalinizare RO mică și medie a apei de mare	Echipamentul RO mic și mediu pentru desalinizarea apei de mare de la Yuchen Water este proiectat pentru proiecte de coastă, insule, nave, hoteluri și contractori B2B care au nevoie de apă potabilă sau de proces fiabilă din apă de mare. Sistemul tratează apă brută cu salinitate 10000-45000 ppm, combină pretratarea cu osmoza inversă și livrează 60 L/h-10000 L/h cu eliminare a sării de cel puțin 99.7%. Controlul, pompele, numărul de membrane și protecțiile se adaptează analizei apei și proiectului.	Sistem RO mic și mediu pentru apă brută 10000-45000 ppm, debit 60-10000 L/h și configurație OEM de proiect.	Model produs|Salinitatea apei brute|Rata de eliminare a nitraților|Temperatura apei de intrare|Eliminarea sării|Debit apă produsă|Salinitatea apei produse|Proces de tratare|Control și protecție|Aplicație|Personalizare	Echipament mic și mediu pentru desalinizarea apei de mare|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Pretratare în trei etape plus osmoză inversă; proces personalizat după analiza apei|Funcționare automată, protecție lipsă apă și suprasarcină; funcții după proiect|Desalinizare apă de mare și salmastră pentru coastă, insule, nave și proiecte de alimentare cu apă|Număr membrane, pompă, tensiune, panou de control, cadru, conducte și ambalare configurabile
ru	Малая и средняя RO установка опреснения морской воды	Малое и среднее RO опреснение морской воды	Малая и средняя RO установка опреснения морской воды Yuchen Water предназначена для прибрежных проектов, островов, судов, отелей и B2B подрядчиков, которым нужна надежная питьевая или технологическая вода из морской воды. Система работает с солесодержанием исходной воды 10000-45000 ppm, сочетает предварительную подготовку с обратным осмосом и выдает 60 L/h-10000 L/h при степени опреснения не ниже 99.7%. Управление, насосы, количество мембран и защитные функции подбираются по анализу воды и требованиям проекта.	Малая и средняя RO система опреснения для исходной воды 10000-45000 ppm, производительности 60-10000 L/h и OEM конфигурации проекта.	Модель продукта|Соленость исходной воды|Степень удаления нитратов|Температура входной воды|Степень опреснения|Расход произведенной воды|Соленость произведенной воды|Процесс очистки|Управление и защита|Применение|Настройка	Малое и среднее оборудование опреснения морской воды|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Трехступенчатая предварительная подготовка плюс обратный осмос; процесс настраивается по анализу воды|Автоматическая работа, защита от отсутствия воды и перегрузки; функции выбираются под проект|Опреснение морской и солоноватой воды для побережья, островов, судов и проектного водоснабжения|Количество мембран, насос, напряжение, шкаф управления, рама, трубопровод и упаковка настраиваются
sk	Malé a stredné RO zariadenie na odsoľovanie morskej vody	Malé a stredné RO odsoľovanie morskej vody	Malé a stredné RO zariadenie Yuchen Water na odsoľovanie morskej vody je určené pre pobrežné projekty, ostrovy, lode, hotely a B2B dodávateľov, ktorí potrebujú spoľahlivú pitnú alebo procesnú vodu z morskej vody. Systém spracuje surovú vodu so salinitou 10000-45000 ppm, využíva predúpravu a reverznú osmózu a dodáva 60 L/h-10000 L/h pri odsoľovaní aspoň 99.7%. Riadenie, čerpadlá, počet membrán a ochrany sa prispôsobujú analýze vody a projektu.	Malý a stredný RO systém pre morskú vodu 10000-45000 ppm, výkon 60-10000 L/h a OEM projektová konfigurácia.	Model produktu|Salinita surovej vody|Miera odstránenia dusičnanov|Teplota vstupnej vody|Odsoľovanie|Prietok vyrobenej vody|Salinita vyrobenej vody|Proces úpravy|Riadenie a ochrana|Použitie|Prispôsobenie	Malé a stredné zariadenie na odsoľovanie morskej vody|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Trojstupňová predúprava plus reverzná osmóza; proces sa nastavuje podľa analýzy vody|Automatická prevádzka, ochrana bez vody a proti preťaženiu; funkcie podľa projektu|Odsoľovanie morskej a brakickej vody pre pobrežie, ostrovy, lode a projekty zásobovania vodou|Počet membrán, čerpadlo, napätie, ovládací panel, rám, potrubie a balenie možno konfigurovať
sl	Mala in srednja RO oprema za razsoljevanje morske vode	Malo in srednje RO razsoljevanje morske vode	Mala in srednja RO oprema Yuchen Water za razsoljevanje morske vode je namenjena obalnim projektom, otokom, plovilom, hotelom in B2B izvajalcem, ki potrebujejo zanesljivo pitno ali procesno vodo iz morske vode. Sistem obdeluje surovo vodo s slanostjo 10000-45000 ppm, uporablja predobdelavo in reverzno osmozo ter zagotavlja 60 L/h-10000 L/h z vsaj 99.7% odstranitvijo soli. Krmiljenje, črpalke, število membran in zaščite se prilagodijo analizi vode in projektu.	Mali in srednji RO sistem za morsko vodo 10000-45000 ppm, izhod 60-10000 L/h in OEM projektna konfiguracija.	Model izdelka|Slanost surove vode|Stopnja odstranjevanja nitratov|Temperatura vhodne vode|Odstranjevanje soli|Pretok proizvedene vode|Slanost proizvedene vode|Postopek obdelave|Krmiljenje in zaščita|Uporaba|Prilagoditev	Mala in srednja oprema za razsoljevanje morske vode|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Tristopenjska predobdelava in reverzna osmoza; proces se prilagodi analizi vode|Samodejno delovanje, zaščita brez vode in pred preobremenitvijo; funkcije po projektu|Razsoljevanje morske in somornice za obalo, otoke, plovila in projekte oskrbe z vodo|Število membran, črpalka, napetost, krmilna plošča, okvir, cevovod in embalaža se lahko konfigurirajo
sq	Pajisje RO i vogël dhe i mesëm për shkripëzimin e ujit të detit	Shkripëzim RO i vogël dhe i mesëm i ujit të detit	Pajisja RO e vogël dhe e mesme për shkripëzimin e ujit të detit nga Yuchen Water është ndërtuar për projekte bregdetare, ishuj, anije, hotele dhe kontraktorë B2B që kërkojnë ujë të pijshëm ose procesi të besueshëm nga uji i detit. Sistemi trajton kripësinë e ujit të papërpunuar 10000-45000 ppm, kombinon paratrajtimin me osmozë të kundërt dhe prodhon 60 L/h-10000 L/h me heqje kripe të paktën 99.7%. Kontrolli, pompat, numri i membranave dhe mbrojtjet përshtaten sipas analizës së ujit dhe projektit.	Sistem RO i vogël dhe i mesëm për ujë deti 10000-45000 ppm, prodhim 60-10000 L/h dhe konfigurim projekti OEM.	Modeli i produktit|Kripësia e ujit të papërpunuar|Norma e heqjes së nitrateve|Temperatura e ujit hyrës|Heqja e kripës|Rrjedha e ujit të prodhuar|Kripësia e ujit të prodhuar|Procesi i trajtimit|Kontroll dhe mbrojtje|Aplikimi|Përshtatje	Pajisje e vogël dhe e mesme për shkripëzimin e ujit të detit|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Paratrajtim me tre faza plus osmozë e kundërt; procesi përshtatet sipas analizës së ujit|Punim automatik, mbrojtje pa ujë dhe mbrojtje nga mbingarkesa; funksione sipas projektit|Shkripëzim i ujit të detit dhe ujit të njelmët për bregdet, ishuj, anije dhe furnizim projektesh|Numri i membranave, pompa, tensioni, paneli i kontrollit, korniza, tubacioni dhe paketimi konfigurohen
sr	Мала и средња RO опрема за десалинизацију морске воде	Мала и средња RO десалинизација морске воде	Мала и средња RO опрема за десалинизацију морске воде компаније Yuchen Water намењена је приобалним пројектима, острвима, пловилима, хотелима и B2B извођачима којима је потребна поуздана питка или процесна вода из морске воде. Систем обрађује сирову воду салинитета 10000-45000 ppm, користи предтретман и реверзну осмозу и даје 60 L/h-10000 L/h уз уклањање соли најмање 99.7%. Управљање, пумпе, број мембрана и заштите прилагођавају се анализи воде и пројекту.	Мали и средњи RO систем за морску воду 10000-45000 ppm, излаз 60-10000 L/h и OEM конфигурација пројекта.	Модел производа|Салинитет сирове воде|Стопа уклањања нитрата|Температура улазне воде|Уклањање соли|Проток произведене воде|Салинитет произведене воде|Процес третмана|Управљање и заштита|Примена|Прилагођавање	Мала и средња опрема за десалинизацију морске воде|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Тростепени предтретман плус реверзна осмоза; процес се прилагођава анализи воде|Аутоматски рад, заштита без воде и од преоптерећења; функције према пројекту|Десалинизација морске и слане воде за обалу, острва, пловила и пројектно водоснабдевање|Број мембрана, пумпа, напон, контролни панел, рам, цеви и паковање могу се конфигурисати
sr-me	Mala i srednja RO oprema za desalinizaciju morske vode	Mala i srednja RO desalinizacija morske vode	Mala i srednja RO oprema za desalinizaciju morske vode Yuchen Water namijenjena je obalnim projektima, ostrvima, plovilima, hotelima i B2B izvođačima kojima je potrebna pouzdana pitka ili procesna voda iz morske vode. Sistem obrađuje sirovu vodu saliniteta 10000-45000 ppm, koristi predtretman i reverznu osmozu i daje 60 L/h-10000 L/h uz uklanjanje soli najmanje 99.7%. Upravljanje, pumpe, broj membrana i zaštite prilagođavaju se analizi vode i projektu.	Mali i srednji RO sistem za morsku vodu 10000-45000 ppm, izlaz 60-10000 L/h i OEM konfiguracija projekta.	Model proizvoda|Salinitet sirove vode|Stopa uklanjanja nitrata|Temperatura ulazne vode|Uklanjanje soli|Protok proizvedene vode|Salinitet proizvedene vode|Proces tretmana|Upravljanje i zaštita|Primjena|Prilagođavanje	Mala i srednja oprema za desalinizaciju morske vode|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Trostepeni predtretman plus reverzna osmoza; proces se prilagođava prema analizi vode|Automatski rad, zaštita bez vode i od preopterećenja; funkcije prema projektu|Desalinizacija morske i slane vode za obalu, ostrva, plovila i projektno vodosnabdijevanje|Broj membrana, pumpa, napon, kontrolni panel, ram, cijevi i pakovanje mogu se konfigurisati
sv	Liten och medelstor RO-utrustning för avsaltning av havsvatten	Liten och medelstor RO-avsaltning av havsvatten	Yuchen Waters lilla och medelstora RO-utrustning för avsaltning av havsvatten är byggd för kustprojekt, öar, fartyg, hotell och B2B-entreprenörer som behöver tillförlitligt dricks- eller processvatten från havsvatten. Systemet behandlar råvatten med salthalt 10000-45000 ppm, kombinerar förbehandling med omvänd osmos och levererar 60 L/h-10000 L/h med minst 99.7% saltavskiljning. Styrning, pumpar, membranantal och skyddsfunktioner anpassas efter vattenanalys och projekt.	Litet och medelstort RO-avsaltningssystem för 10000-45000 ppm råvatten, 60-10000 L/h kapacitet och OEM-projektkonfiguration.	Produktmodell|Råvattnets salthalt|Nitratavskiljningsgrad|Inloppsvattentemperatur|Saltavskiljning|Produktvattenflöde|Produktvattnets salthalt|Behandlingsprocess|Styrning och skydd|Användning|Anpassning	Liten och medelstor utrustning för avsaltning av havsvatten|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Trestegs förbehandling plus omvänd osmos; process anpassas efter vattenanalys|Automatisk drift, skydd mot vattenbrist och överbelastning; funktioner efter projekt|Avsaltning av havsvatten och brackvatten för kust, öar, fartyg och projektvattenförsörjning|Membranantal, pump, spänning, kontrollpanel, ram, rördragning och förpackning kan konfigureras
sw	Vifaa vidogo na vya kati vya RO vya kuondoa chumvi kwenye maji ya bahari	Uondoaji chumvi wa maji ya bahari kwa RO ndogo na ya kati	Vifaa vidogo na vya kati vya RO vya Yuchen Water vya kuondoa chumvi kwenye maji ya bahari vimeundwa kwa miradi ya pwani, visiwa, vyombo vya baharini, hoteli na wakandarasi wa B2B wanaohitaji maji ya kunywa au ya mchakato kutoka maji ya bahari. Mfumo hushughulikia chumvi ya maji ghafi 10000-45000 ppm, hutumia matibabu ya awali na osmosis ya kurudi nyuma, na hutoa 60 L/h-10000 L/h kwa uondoaji wa chumvi angalau 99.7%. Udhibiti, pampu, idadi ya membrane na ulinzi hubadilishwa kulingana na uchambuzi wa maji na mradi.	Mfumo mdogo na wa kati wa RO kwa maji ghafi 10000-45000 ppm, uzalishaji 60-10000 L/h na usanidi wa mradi wa OEM.	Mfano wa bidhaa|Chumvi ya maji ghafi|Kiwango cha kuondoa nitrati|Joto la maji yanayoingia|Uondoaji chumvi|Mtiririko wa maji yaliyotengenezwa|Chumvi ya maji yaliyotengenezwa|Mchakato wa matibabu|Udhibiti na ulinzi|Matumizi|Ubinafsishaji	Vifaa vidogo na vya kati vya kuondoa chumvi kwenye maji ya bahari|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Matibabu ya awali hatua tatu pamoja na osmosis ya kurudi nyuma; mchakato hubadilishwa kwa uchambuzi wa maji|Uendeshaji wa kiotomatiki, ulinzi wa kukosa maji na ulinzi wa mzigo kupita kiasi; kazi kulingana na mradi|Kuondoa chumvi kwenye maji ya bahari na maji yenye chumvi kidogo kwa pwani, visiwa, vyombo na miradi ya maji|Idadi ya membrane, pampu, voltage, paneli ya udhibiti, fremu, mabomba na ufungaji vinaweza kusanidiwa
ta	சிறிய மற்றும் நடுத்தர RO கடல் நீர் உப்பு நீக்கி உபகரணம்	சிறிய மற்றும் நடுத்தர RO கடல் நீர் உப்பு நீக்கம்	Yuchen Water இன் சிறிய மற்றும் நடுத்தர RO கடல் நீர் உப்பு நீக்கி உபகரணம் கடற்கரை திட்டங்கள், தீவுகள், கப்பல்கள், ஹோட்டல்கள் மற்றும் கடல் நீரிலிருந்து நம்பகமான குடிநீர் அல்லது செயல்முறை நீர் தேவைப்படும் B2B ஒப்பந்ததாரர்களுக்காக உருவாக்கப்பட்டுள்ளது. அமைப்பு 10000-45000 ppm மூல நீர் உப்புத்தன்மையை கையாள்கிறது, முன் சிகிச்சை மற்றும் ரிவர்ஸ் ஆஸ்மோசிஸை இணைக்கிறது, மேலும் குறைந்தது 99.7% உப்பு நீக்கத்துடன் 60 L/h-10000 L/h நீரை வழங்குகிறது. கட்டுப்பாடு, பம்புகள், மெம்பிரேன் எண்ணிக்கை மற்றும் பாதுகாப்புகள் நீர் பகுப்பாய்வு மற்றும் திட்டத்துக்கு ஏற்ப அமைக்கப்படுகின்றன.	10000-45000 ppm மூல நீருக்கான சிறிய மற்றும் நடுத்தர RO கடல் நீர் உப்பு நீக்கி அமைப்பு, 60-10000 L/h வெளியீடு மற்றும் OEM திட்ட அமைப்பு.	தயாரிப்பு மாதிரி|மூல நீர் உப்புத்தன்மை|நைட்ரேட் அகற்றும் விகிதம்|உள்வரும் நீர் வெப்பநிலை|உப்பு நீக்கும் விகிதம்|உற்பத்தி நீர் ஓட்டம்|உற்பத்தி நீர் உப்புத்தன்மை|சிகிச்சை செயல்முறை|கட்டுப்பாடு மற்றும் பாதுகாப்பு|பயன்பாடு|தனிப்பயன்	சிறிய மற்றும் நடுத்தர கடல் நீர் உப்பு நீக்கி உபகரணம்|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|மூன்று நிலை முன் சிகிச்சை மற்றும் ரிவர்ஸ் ஆஸ்மோசிஸ்; நீர் பகுப்பாய்வு அடிப்படையில் செயல்முறை தனிப்பயன்|தானியங்கி இயக்கம், நீர் இல்லா பாதுகாப்பு மற்றும் அதிக சுமை பாதுகாப்பு; செயல்பாடுகள் திட்டத்திற்கு ஏற்ப|கடற்கரை, தீவு, கப்பல் மற்றும் திட்ட நீர் விநியோகத்திற்கான கடல் நீர் மற்றும் உப்புக் கலந்த நீர் உப்பு நீக்கம்|மெம்பிரேன் எண்ணிக்கை, பம்ப், மின்னழுத்தம், கட்டுப்பாட்டு பலகை, சட்டகம், குழாய் மற்றும் பேக்கிங் அமைக்கலாம்
tg	Таҷҳизоти хурд ва миёнаи RO барои ширинсозии оби баҳр	Ширинсозии хурд ва миёнаи оби баҳр бо RO	Таҷҳизоти хурд ва миёнаи RO барои ширинсозии оби баҳри Yuchen Water барои лоиҳаҳои соҳилӣ, ҷазираҳо, киштиҳо, меҳмонхонаҳо ва пудратчиёни B2B сохта шудааст, ки аз оби баҳр оби нӯшокӣ ё технологӣ боэътимод мехоҳанд. Система шӯрии оби хоми 10000-45000 ppm-ро коркард мекунад, пештозакуниро бо осмоси баръакс муттаҳид мекунад ва бо бартарафсозии намак на камтар аз 99.7% 60 L/h-10000 L/h об медиҳад. Идоракунӣ, насосҳо, шумораи мембрана ва ҳимояҳо мувофиқи таҳлили об ва лоиҳа танзим мешаванд.	Системаи хурд ва миёнаи RO барои оби хоми 10000-45000 ppm, ҳосилнокии 60-10000 L/h ва конфигуратсияи OEM.	Модели маҳсулот|Шӯрии оби хом|Сатҳи бартарафсозии нитрат|Ҳарорати оби воридшаванда|Сатҳи бартарафсозии намак|Ҷараёни оби истеҳсолшуда|Шӯрии оби истеҳсолшуда|Раванди тозакунӣ|Идоракунӣ ва ҳимоя|Истифода|Мутобиқсозӣ	Таҷҳизоти хурд ва миёнаи ширинсозии оби баҳр|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Пештозакунии сеқадам ва осмоси баръакс; раванд тибқи таҳлили об мутобиқ мешавад|Кори автоматӣ, ҳимоя аз набудани об ва аз изофабор; функсияҳо тибқи лоиҳа|Ширинсозии оби баҳр ва оби нимшӯр барои соҳил, ҷазира, киштӣ ва таъминоти оби лоиҳа|Шумораи мембрана, насос, шиддат, панели идоракунӣ, чорчӯба, қубур ва бастабандӣ танзимшавандаанд
th	อุปกรณ์ RO กลั่นน้ำทะเลขนาดเล็กและกลาง	ระบบ RO กลั่นน้ำทะเลขนาดเล็กและกลาง	อุปกรณ์ RO กลั่นน้ำทะเลขนาดเล็กและกลางของ Yuchen Water ออกแบบสำหรับโครงการชายฝั่ง เกาะ เรือ โรงแรม และผู้รับเหมางาน B2B ที่ต้องการน้ำดื่มหรือน้ำใช้ในกระบวนการจากน้ำทะเลอย่างเชื่อถือได้ ระบบรองรับความเค็มน้ำดิบ 10000-45000 ppm ใช้การปรับสภาพก่อนเข้าร่วมกับรีเวิร์สออสโมซิส และให้น้ำผลิต 60 L/h-10000 L/h พร้อมอัตราขจัดเกลือไม่น้อยกว่า 99.7% การควบคุม ปั๊ม จำนวนเมมเบรน และระบบป้องกันปรับได้ตามผลวิเคราะห์น้ำและโครงการ	ระบบ RO กลั่นน้ำทะเลขนาดเล็กและกลางสำหรับน้ำดิบ 10000-45000 ppm ผลิต 60-10000 L/h และปรับแต่งโครงการ OEM ได้	รุ่นสินค้า|ความเค็มน้ำดิบ|อัตรากำจัดไนเตรต|อุณหภูมิน้ำเข้า|อัตราขจัดเกลือ|อัตราการผลิตน้ำ|ความเค็มน้ำผลิต|กระบวนการบำบัด|การควบคุมและการป้องกัน|การใช้งาน|การปรับแต่ง	อุปกรณ์กลั่นน้ำทะเลขนาดเล็กและกลาง|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|การปรับสภาพก่อนเข้า 3 ขั้นตอนร่วมกับรีเวิร์สออสโมซิส ปรับกระบวนการตามผลวิเคราะห์น้ำ|ทำงานอัตโนมัติ ป้องกันน้ำขาด และป้องกันโหลดเกิน เลือกฟังก์ชันตามโครงการ|กลั่นน้ำทะเลและน้ำกร่อยสำหรับชายฝั่ง เกาะ เรือ และโครงการจัดหาน้ำ|จำนวนเมมเบรน ปั๊ม แรงดันไฟ ตู้ควบคุม โครง ท่อ และบรรจุภัณฑ์ปรับได้
tk	Kiçi we orta RO deňiz suwuny süýjüleşdiriji enjam	Kiçi we orta RO deňiz suwuny süýjüleşdirmek	Yuchen Water kiçi we orta RO deňiz suwuny süýjüleşdiriji enjamy kenarýaka taslamalary, adalar, gämiler, myhmanhanalar we deňiz suwundan ygtybarly içimlik ýa-da proses suwuny talap edýän B2B potratçylary üçin taýýarlanýar. Ulgam 10000-45000 ppm çig suw duzlulygyny işleýär, öňünden arassalamany we ters osmosy birleşdirýär hem-de azyndan 99.7% duz aýyrma bilen 60 L/h-10000 L/h suw öndürýär. Dolandyryş, nasoslar, membrana sany we gorag funksiýalary suw derňewine we taslama görä sazlanýar.	10000-45000 ppm çig suw üçin kiçi we orta RO deňiz suwy süýjüleşdiriji ulgam, 60-10000 L/h çykyş we OEM taslama konfigurasiýasy.	Önüm modeli|Çig suw duzlulygy|Nitrat aýyrmak derejesi|Giriş suw temperaturasy|Duz aýyrmak derejesi|Öndürilen suw akymy|Öndürilen suw duzlulygy|Arassalama prosesi|Dolandyryş we gorag|Ulanylyş|Ýöriteleşdirme	Kiçi we orta deňiz suwuny süýjüleşdiriji enjam|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Üç tapgyrly öňünden arassalama we ters osmos; proses suw derňewine görä sazlanýar|Awtomatiki iş, suwsuz gorag we artykmaç ýük goragy; funksiýalar taslama görä saýlanýar|Kenarýaka, ada, gämi we taslama suw üpjünçiligi üçin deňiz we şor suw süýjüleşdirmek|Membrana sany, nasos, naprýaženiýe, dolandyryş paneli, rama, turbalar we gaplama sazlanýar
tl	Maliit at katamtamang RO kagamitan para sa desalination ng tubig-dagat	Maliit at katamtamang RO desalination ng tubig-dagat	Ang maliit at katamtamang RO kagamitan ng Yuchen Water para sa desalination ng tubig-dagat ay ginawa para sa mga proyektong baybayin, isla, sasakyang-dagat, hotel at B2B contractor na nangangailangan ng maaasahang inuming tubig o process water mula sa tubig-dagat. Pinoproseso ng sistema ang 10000-45000 ppm na alat ng raw water, pinagsasama ang pretreatment at reverse osmosis, at nagbibigay ng 60 L/h-10000 L/h na tubig na may hindi bababa sa 99.7% pagtanggal ng asin. Ang kontrol, pump, bilang ng membrane at proteksyon ay inaangkop ayon sa pagsusuri ng tubig at proyekto.	Maliit at katamtamang RO seawater desalination system para sa 10000-45000 ppm raw water, 60-10000 L/h output at OEM project configuration.	Modelo ng produkto|Alat ng raw water|Rate ng pagtanggal ng nitrate|Temperatura ng inlet water|Pagtanggal ng asin|Daloy ng produced water|Alat ng produced water|Proseso ng paggamot|Kontrol at proteksyon|Gamit|Pag-customize	Maliit at katamtamang kagamitan sa desalination ng tubig-dagat|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Tatlong yugto ng pretreatment at reverse osmosis; proseso ayon sa pagsusuri ng tubig|Awtomatikong operasyon, proteksyon kapag walang tubig at proteksyon sa overload; function ayon sa proyekto|Desalination ng tubig-dagat at brackish water para sa baybayin, isla, sasakyang-dagat at proyekto ng supply ng tubig|Bilang ng membrane, pump, boltahe, control panel, frame, piping at packaging ay maaaring i-configure
tr	Küçük ve orta ölçekli RO deniz suyu arıtma ekipmanı	Küçük ve orta ölçekli RO deniz suyu tuz giderme	Yuchen Water küçük ve orta ölçekli RO deniz suyu arıtma ekipmanı; kıyı projeleri, adalar, gemiler, oteller ve deniz suyundan güvenilir içme suyu veya proses suyu isteyen B2B yükleniciler için üretilir. Sistem 10000-45000 ppm ham su tuzluluğunu işler, ön arıtma ile ters ozmozu birleştirir ve en az 99.7% tuz giderimiyle 60 L/h-10000 L/h ürün suyu sağlar. Kontrol, pompalar, membran sayısı ve koruma fonksiyonları su analizine ve projeye göre özelleştirilir.	10000-45000 ppm ham su için küçük ve orta RO deniz suyu tuz giderme sistemi, 60-10000 L/h çıkış ve OEM proje konfigürasyonu.	Ürün modeli|Ham su tuzluluğu|Nitrat giderim oranı|Giriş suyu sıcaklığı|Tuz giderim oranı|Ürün suyu debisi|Ürün suyu tuzluluğu|Arıtma süreci|Kontrol ve koruma|Uygulama|Özelleştirme	Küçük ve orta deniz suyu tuz giderme ekipmanı|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Üç aşamalı ön arıtma ve ters ozmoz; süreç su analizine göre özelleştirilir|Otomatik çalışma, susuz çalışma koruması ve aşırı yük koruması; fonksiyonlar projeye göre seçilir|Kıyı, ada, gemi ve proje su temini için deniz suyu ve acı su tuz giderme|Membran sayısı, pompa, voltaj, kontrol paneli, şase, borulama ve ambalaj yapılandırılabilir
uk	Мала і середня RO установка опріснення морської води	Мале і середнє RO опріснення морської води	Мала і середня RO установка опріснення морської води Yuchen Water призначена для прибережних проєктів, островів, суден, готелів і B2B підрядників, яким потрібна надійна питна або технологічна вода з морської води. Система працює з солоністю сирої води 10000-45000 ppm, поєднує попередню підготовку зі зворотним осмосом і видає 60 L/h-10000 L/h при опрісненні не нижче 99.7%. Керування, насоси, кількість мембран і захисти налаштовуються за аналізом води та проєктом.	Мала і середня RO система опріснення для сирої води 10000-45000 ppm, продуктивності 60-10000 L/h і OEM конфігурації проєкту.	Модель продукту|Солоність сирої води|Ступінь видалення нітратів|Температура вхідної води|Ступінь опріснення|Потік виробленої води|Солоність виробленої води|Процес очищення|Керування і захист|Застосування|Налаштування	Мале і середнє обладнання опріснення морської води|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Триступенева попередня підготовка плюс зворотний осмос; процес налаштовується за аналізом води|Автоматична робота, захист від відсутності води та перевантаження; функції за проєктом|Опріснення морської і солонуватої води для узбережжя, островів, суден і проєктного водопостачання|Кількість мембран, насос, напруга, шафа керування, рама, трубопровід і пакування налаштовуються
ur	چھوٹا اور درمیانہ RO سمندری پانی ڈی سیلینیشن سامان	چھوٹا اور درمیانہ RO سمندری پانی ڈی سیلینیشن	Yuchen Water کا چھوٹا اور درمیانہ RO سمندری پانی ڈی سیلینیشن سامان ساحلی منصوبوں، جزائر، جہازوں، ہوٹلوں اور B2B کنٹریکٹرز کے لیے بنایا گیا ہے جنہیں سمندری پانی سے قابل اعتماد پینے کا یا پراسیس پانی درکار ہے۔ یہ سسٹم 10000-45000 ppm خام پانی کی نمکیات کو سنبھالتا ہے، پری ٹریٹمنٹ اور ریورس اوسموسس کو ملاتا ہے، اور کم از کم 99.7% نمک ہٹانے کے ساتھ 60 L/h-10000 L/h پانی فراہم کرتا ہے۔ کنٹرول، پمپ، میمبرین کی تعداد اور حفاظتی افعال پانی کے تجزیے اور منصوبے کے مطابق ترتیب دیے جاتے ہیں۔	10000-45000 ppm خام پانی کے لیے چھوٹا اور درمیانہ RO ڈی سیلینیشن سسٹم، 60-10000 L/h پیداوار اور OEM منصوبہ ترتیب۔	مصنوعات کا ماڈل|خام پانی کی نمکیات|نائٹریٹ ہٹانے کی شرح|انلیٹ پانی کا درجہ حرارت|نمک ہٹانے کی شرح|پیدا شدہ پانی کا بہاؤ|پیدا شدہ پانی کی نمکیات|ٹریٹمنٹ عمل|کنٹرول اور حفاظت|استعمال|حسب ضرورت	چھوٹا اور درمیانہ سمندری پانی ڈی سیلینیشن سامان|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|تین مرحلوں کی پری ٹریٹمنٹ اور ریورس اوسموسس؛ عمل پانی کے تجزیے کے مطابق|خودکار آپریشن، پانی نہ ہونے کی حفاظت اور اوورلوڈ حفاظت؛ افعال منصوبے کے مطابق|ساحل، جزائر، جہازوں اور منصوبہ جاتی پانی کی فراہمی کے لیے سمندری اور نیم نمکین پانی کی ڈی سیلینیشن|میمبرین تعداد، پمپ، وولٹیج، کنٹرول پینل، فریم، پائپنگ اور پیکنگ ترتیب دی جا سکتی ہے
uz	Kichik va o‘rta RO dengiz suvini chuchuklashtirish uskunasi	Kichik va o‘rta RO dengiz suvini chuchuklashtirish	Yuchen Water kichik va o‘rta RO dengiz suvini chuchuklashtirish uskunasi qirg‘oq loyihalari, orollar, kemalar, mehmonxonalar va dengiz suvidan ishonchli ichimlik yoki texnologik suv kerak bo‘lgan B2B pudratchilar uchun ishlab chiqilgan. Tizim 10000-45000 ppm xom suv sho‘rligini qayta ishlaydi, oldindan tozalash va teskari osmosni birlashtiradi hamda kamida 99.7% tuz ushlash bilan 60 L/h-10000 L/h mahsulot suv beradi. Boshqaruv, nasoslar, membrana soni va himoya funksiyalari suv tahlili va loyiha talabiga ko‘ra moslashtiriladi.	10000-45000 ppm xom suv uchun kichik va o‘rta RO dengiz suvini chuchuklashtirish tizimi, 60-10000 L/h chiqish va OEM loyiha konfiguratsiyasi.	Mahsulot modeli|Xom suv sho‘rligi|Nitratni olib tashlash darajasi|Kirish suvi harorati|Tuzni ushlash darajasi|Mahsulot suvi oqimi|Mahsulot suvi sho‘rligi|Tozalash jarayoni|Boshqaruv va himoya|Qo‘llanish|Moslashtirish	Kichik va o‘rta dengiz suvini chuchuklashtirish uskunasi|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Uch bosqichli oldindan tozalash va teskari osmos; jarayon suv tahliliga ko‘ra moslashtiriladi|Avtomatik ishlash, suvsiz himoya va ortiqcha yuklanishdan himoya; funksiyalar loyiha bo‘yicha tanlanadi|Qirg‘oq, orol, kema va loyiha suv ta’minoti uchun dengiz va sho‘r suvni chuchuklashtirish|Membrana soni, nasos, kuchlanish, boshqaruv paneli, rama, quvur va qadoqlash sozlanadi
vi	Thiết bị RO khử mặn nước biển cỡ nhỏ và trung bình	Khử mặn nước biển RO cỡ nhỏ và trung bình	Thiết bị RO khử mặn nước biển cỡ nhỏ và trung bình của Yuchen Water được thiết kế cho dự án ven biển, đảo, tàu thuyền, khách sạn và nhà thầu B2B cần nước uống hoặc nước quy trình ổn định từ nước biển. Hệ thống xử lý độ mặn nước thô 10000-45000 ppm, kết hợp tiền xử lý với thẩm thấu ngược và tạo nước 60 L/h-10000 L/h với tỷ lệ khử muối tối thiểu 99.7%. Điều khiển, bơm, số lượng màng và chức năng bảo vệ có thể tùy chỉnh theo phân tích nước và yêu cầu dự án.	Hệ thống RO khử mặn nước biển cỡ nhỏ và trung bình cho nước thô 10000-45000 ppm, lưu lượng 60-10000 L/h và cấu hình dự án OEM.	Model sản phẩm|Độ mặn nước thô|Tỷ lệ loại bỏ nitrat|Nhiệt độ nước đầu vào|Tỷ lệ khử muối|Lưu lượng nước sản xuất|Độ mặn nước sản xuất|Quy trình xử lý|Điều khiển và bảo vệ|Ứng dụng|Tùy chỉnh	Thiết bị khử mặn nước biển cỡ nhỏ và trung bình|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Tiền xử lý ba cấp kết hợp thẩm thấu ngược; quy trình tùy chỉnh theo phân tích nước|Vận hành tự động, bảo vệ thiếu nước và bảo vệ quá tải; chức năng theo dự án|Khử mặn nước biển và nước lợ cho ven biển, đảo, tàu thuyền và dự án cấp nước|Số lượng màng, bơm, điện áp, tủ điều khiển, khung, đường ống và đóng gói có thể cấu hình
zu	Imishini emincane naphakathi ye-RO yokususa usawoti emanzini olwandle	Ukususa usawoti emanzini olwandle nge-RO encane naphakathi	Imishini emincane naphakathi ye-RO ka Yuchen Water yokususa usawoti emanzini olwandle yakhelwe amaphrojekthi asogwini, iziqhingi, imikhumbi, amahhotela nabaphathi be-B2B abadinga amanzi okuphuza noma awenqubo athembekile aphuma olwandle. Uhlelo luphatha usawoti wamanzi angakahlanzwa 10000-45000 ppm, luhlanganisa ukwelashwa kwangaphambili ne-reverse osmosis, futhi lunikeza 60 L/h-10000 L/h ngokususa usawoti okungenani 99.7%. Ukulawula, amaphampu, inani lama-membrane nemisebenzi yokuvikela kulungiswa ngokuhlaziywa kwamanzi nephrojekthi.	Uhlelo oluncane naphakathi lwe-RO lokususa usawoti emanzini olwandle 10000-45000 ppm, 60-10000 L/h nokucushwa kwephrojekthi ye-OEM.	Imodeli yomkhiqizo|Usawoti wamanzi aluhlaza|Izinga lokususa i-nitrate|Izinga lokushisa lamanzi angenayo|Ukususwa kosawoti|Ukugeleza kwamanzi akhiqiziwe|Usawoti wamanzi akhiqiziwe|Inqubo yokwelapha|Ukulawula nokuvikela|Ukusetshenziswa|Ukwenza ngokwezifiso	Imishini emincane naphakathi yokususa usawoti emanzini olwandle|10000-45000 ppm|≥90%|2-40°C|≥99.7%|60 L/h-10000 L/h|≤750 ppm|Ukwelashwa kwangaphambili kwezigaba ezintathu kanye ne-reverse osmosis; inqubo ilungiswa ngokuhlaziywa kwamanzi|Ukusebenza okuzenzakalelayo, ukuvikelwa kokungabi namanzi nokuvikelwa komthwalo oweqile; imisebenzi ngokwephrojekthi|Ukususa usawoti emanzini olwandle namanzi anosawoti omncane ogwini, eziqhingini, emikhunjini nasekuphakeleni amanzi kwephrojekthi|Inani lama-membrane, iphampu, voltage, iphaneli yokulawula, uhlaka, amapayipi nokupakisha kuyacushwa
""".strip()


BASE = runpy.run_path(str(ROOT / "scripts" / "add_large_industrial_ro_equipment.py"))
BASE_UI_FOR = BASE["ui_for"]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def load_rows() -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for line in ROWS.splitlines():
        parts = line.split("\t")
        if len(parts) != 7:
            raise ValueError(f"Bad data row for {parts[0] if parts else 'unknown'}: {len(parts)} fields")
        lang, name, category, intro, card, labels, values = parts
        label_list = labels.split("|")
        value_list = values.split("|")
        if len(label_list) != len(value_list):
            raise ValueError(f"Label/value mismatch for {lang}: {len(label_list)} != {len(value_list)}")
        rows[lang] = {
            "name": name,
            "category": category,
            "intro": intro,
            "card": card,
            "labels": label_list,
            "values": value_list,
        }
    return rows


DATA = load_rows()


def dirs() -> list[str]:
    return sorted(p.name for p in ROOT.iterdir() if p.is_dir() and (p / "index.html").exists())


def ui_for(lang: str) -> dict:
    ui = BASE_UI_FOR(lang)
    return {
        "home": ui.get("home", "Home"),
        "products": ui.get("products", "Products"),
        "specs": ui.get("specs", "Technical Specifications"),
        "process": ui.get("process", ui.get("options", "System Configuration")),
        "faq": ui.get("faq", "FAQ"),
        "related": ui.get("related", "Related Products"),
        "request": ui.get("request", "Request OEM Quote"),
        "whatsapp": ui.get("whatsapp", "WhatsApp"),
        "send": ui.get("send", "Send Inquiry"),
        "item": ui.get("item", "Item"),
        "spec": ui.get("spec", "Specification"),
    }


def copy_for(lang: str) -> dict:
    c = DATA[lang].copy()
    c.update(ui_for(lang))
    c["title"] = f"{c['name']} | Yuchen Water"
    c["meta"] = re.sub(r"\s+", " ", c["intro"]).strip()
    if len(c["meta"]) > 260:
        c["meta"] = c["meta"][:257].rsplit(" ", 1)[0] + "..."
    c["quote"] = f"{c['request']}: {c['name']}"
    c["quote_desc"] = c["intro"]
    c["faq_pairs"] = [
        (f"{c['labels'][1]}?", c["values"][1]),
        (f"{c['labels'][4]}?", c["values"][4]),
        (f"{c['labels'][5]}?", c["values"][5]),
        (f"{c['labels'][10]}?", c["values"][10]),
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
        ("product-ro-seawater-desalination-machine.html", page_h1(lang, "product-ro-seawater-desalination-machine.html", "RO Seawater Desalination Equipment"), "ro-seawater-desalination-equipment-complete-system-oem.jpg", c["category"]),
        ("product-large-industrial-reverse-osmosis-water-treatment-equipment.html", page_h1(lang, "product-large-industrial-reverse-osmosis-water-treatment-equipment.html", "Large Industrial Reverse Osmosis Water Treatment Equipment"), "large-industrial-reverse-osmosis-water-treatment-equipment-3-100tph-oem.webp", c["category"]),
        ("product-20-inch-commercial-ro-water-purifier-800g-2000g.html", page_h1(lang, "product-20-inch-commercial-ro-water-purifier-800g-2000g.html", "20-inch Commercial RO Water Purifier"), "20-inch-commercial-ro-water-purifier-800g-2000g-front-full-frame-oem.webp", c["category"]),
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
      <img src="../assets/products/{MAIN_IMAGE}" alt="{esc(c["name"])}" loading="eager" fetchpriority="high" decoding="async" width="{IMAGE_WIDTH}" height="{IMAGE_HEIGHT}" class="product-main-image" />
    </div>
    <div class="product-detail-info">
      <nav class="breadcrumb"><a href="index.html">{esc(c["home"])}</a><span>·</span><a href="products.html">{esc(c["products"])}</a><span>·</span><span>{esc(c["name"])}</span></nav>
      <h1>{esc(c["name"])}</h1>
      <span class="cat-badge">{esc(c["category"])}</span>
      <p class="desc">{esc(c["intro"])}</p>
      <div class="product-actions"><a href="contact.html" class="btn btn-gold">{esc(c["request"])}</a><a href="https://wa.me/8619908311885?text=Inquiry%20about%20Small%20Medium%20Seawater%20Desalination%20RO%20Equipment" class="btn" target="_blank" rel="noopener">{esc(c["whatsapp"])}</a></div>
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
      <tr><th>{esc(c["labels"][7])}</th><td>{esc(c["values"][7])}</td></tr>
      <tr><th>{esc(c["labels"][8])}</th><td>{esc(c["values"][8])}</td></tr>
      <tr><th>{esc(c["labels"][9])}</th><td>{esc(c["values"][9])}</td></tr>
      <tr><th>{esc(c["labels"][10])}</th><td>{esc(c["values"][10])}</td></tr>
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
    <div class="hero-actions"><a href="contact.html" class="btn btn-gold">{esc(c["request"])}</a><a href="https://wa.me/8619908311885?text=Inquiry%20about%20Small%20Medium%20Seawater%20Desalination%20RO%20Equipment" class="btn" target="_blank" rel="noopener">{esc(c["whatsapp"])}</a></div>
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
    text = re.sub(r'\n<section class="section section-cream product-faq">.*?</section>', "", text, count=1, flags=re.S)
    (ROOT / lang / NEW_SLUG).write_text(text, encoding="utf-8")


def product_card(lang: str) -> str:
    c = copy_for(lang)
    return f'''<article class="product-card" data-cat="RO System">
  <a href="{NEW_SLUG}" class="product-img-wrap">
    <span class="product-cat-badge">{esc(c["category"])}</span>
    <img src="../assets/products/{MAIN_IMAGE}" alt="{esc(c["name"])}" loading="lazy" decoding="async" width="{IMAGE_WIDTH}" height="{IMAGE_HEIGHT}" />
  </a>
  <div class="product-body">
    <h3>{esc(c["name"])}</h3>
    <p>{esc(c["card"])}</p>
    <a href="{NEW_SLUG}" class="product-link">{esc(c["send"])}</a>
  </div>
</article>
'''


def home_product_card(lang: str) -> str:
    c = copy_for(lang)
    return f'''<article class="product-card" data-cat="{esc(c["category"])}">
  <a href="{NEW_SLUG}" class="product-img-wrap">
    <span class="product-cat-badge">{esc(c["category"])}</span>
    <img src="../assets/products/{MAIN_IMAGE}" alt="{esc(c["name"])}" loading="lazy" decoding="async" width="{IMAGE_WIDTH}" height="{IMAGE_HEIGHT}" />
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
        match = re.search(r'(<article class="[^"]*\bproduct-card\b[^"]*"[^>]*>.*?' + re.escape(AFTER_SLUG) + r'.*?</article>\s*)', text, flags=re.S)
        if not match:
            raise RuntimeError(f"Could not find insertion point in {path}")
        text = text[:match.end()] + "\n" + product_card(lang) + text[match.end():]
    text = update_item_list_json(text, lang)
    path.write_text(text, encoding="utf-8")


def update_home_page(lang: str) -> None:
    path = ROOT / lang / "index.html"
    text = path.read_text(encoding="utf-8")
    if NEW_SLUG in text:
        return
    match = re.search(r'(<article class="[^"]*\bproduct-card\b[^"]*"[^>]*>.*?' + re.escape(AFTER_SLUG) + r'.*?</article>\s*)', text, flags=re.S)
    if not match:
        return
    text = text[:match.end()] + "\n" + home_product_card(lang) + text[match.end():]
    path.write_text(text, encoding="utf-8")


def update_products_json() -> None:
    path = ROOT / "scripts" / "products.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    products = data.setdefault("products", [])
    if any(item.get("id") == PRODUCT_ID for item in products):
        return
    insert_at = next((i + 1 for i, item in enumerate(products) if item.get("id") == "ro-seawater-desalination-machine"), 4)
    products.insert(insert_at, {
        "id": PRODUCT_ID,
        "name": DATA["en"]["name"],
        "category": "RO System",
        "desc": DATA["en"]["card"],
        "specs": dict(zip(DATA["en"]["labels"], DATA["en"]["values"])),
        "image": f"../assets/products/{MAIN_IMAGE}",
        "image_local": f"assets/products/{MAIN_IMAGE}",
        "image_orig": f"../assets/products/{MAIN_IMAGE}",
        "summary": DATA["en"]["intro"],
        "features": ["10000-45000 ppm feed water", "≥99.7% salt rejection", "60-10000 L/h product water", "Automatic operation with no-water and overload protection", "Project-based membrane and pump configuration"],
        "applications": "Coastal projects, islands, vessels, hotels and seawater or brackish water supply projects.",
        "related": ["ro-seawater-desalination-machine", "large-industrial-reverse-osmosis-water-treatment-equipment", "20-inch-commercial-ro-water-purifier-800g-2000g"],
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
    line = f"- Small and Medium Seawater Desalination RO Equipment: https://www.yuchensy.com/en/{NEW_SLUG}\n"
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
        update_home_page(lang)
        update_products_page(lang)
    update_products_json()
    update_sitemap(languages)
    update_ai_files()
    print(f"generated_pages={len(languages)}")


if __name__ == "__main__":
    main()
