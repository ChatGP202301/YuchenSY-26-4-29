#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add dual-tank pretreatment integrated skid RO equipment across all language pages."""

from __future__ import annotations

import html
import json
import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_SLUG = "product-large-industrial-reverse-osmosis-water-treatment-equipment.html"
AFTER_SLUG = "product-large-industrial-reverse-osmosis-water-treatment-equipment.html"
NEW_SLUG = "product-dual-tank-pretreatment-integrated-skid-ro-equipment.html"
PRODUCT_ID = "dual-tank-pretreatment-integrated-skid-ro-equipment"
TODAY = "2026-06-21"
MAIN_IMAGE = "dual-tank-pretreatment-integrated-skid-ro-equipment-1000l-3000l-oem.webp"
IMAGE_WIDTH = 960
IMAGE_HEIGHT = 668
RTL_LANGS = {"ar", "fa", "he", "ur"}


BASE = runpy.run_path(str(ROOT / "scripts" / "add_large_industrial_ro_equipment.py"))
BASE_DATA = BASE["DATA"]
BASE_UI_FOR = BASE["ui_for"]
SMALL = runpy.run_path(str(ROOT / "scripts" / "add_small_medium_seawater_desalination_product.py"))
SMALL_DATA = SMALL["DATA"]
COMMERCIAL = runpy.run_path(str(ROOT / "scripts" / "add_20inch_commercial_ro_product.py"))
COMMERCIAL_RELATED = COMMERCIAL.get("RELATED_TITLES", {})


TERMS_ROWS = """
af	Dubbeltenk-voorbehandeling geïntegreerde raam-RO-toerusting 1000-3000 L/h	Geïntegreerde raam-RO met dubbeltenk-voorbehandeling	Yuchen Water se dubbeltenk-voorbehandeling geïntegreerde raam-RO-toerusting is gebou vir kommersiële en ligte industriële B2B projekte wat kraanwater of grondwater moet suiwer. Die stelsel kombineer 'n outomatiese sandtenk, outomatiese koolstoftenk, presisiefilter en omgekeerde osmose op een kompakte raam, met 1000-3000 L/h skoonwater-vloei en 0.1-0.4 MPa inlaatdruk. Voorkoms, prosesvloei, konfigurasie en funksies word volgens waterontleding en kliëntvereistes aangepas.	Geïntegreerde raam-RO-stelsel met outomatiese sand- en koolstoftenks, presisiefiltrasie en 1000-3000 L/h suiwer water vir OEM-projekte.	Outomatiese sandtenk + outomatiese koolstoftenk + presisiefilter + omgekeerde osmose	Inlaatdruk	Projekaanpassing	Voorkoms, prosesvloei, toerustingkonfigurasie, beheerpaneel en beskermingsfunksies kan volgens bronwater en projekruimte aangepas word	Hotelle, fabrieke, skole, gemeenskappe, kommersiële kombuise en projekwaterbehandeling
ar	معدات RO مدمجة على هيكل واحد مع معالجة أولية بخزانين 1000-3000 لتر/ساعة	نظام RO على هيكل واحد مع معالجة أولية بخزانين	معدات RO المدمجة على هيكل واحد مع معالجة أولية بخزانين من Yuchen Water مصممة لمشاريع B2B التجارية والصناعية الخفيفة التي تعالج مياه الصنبور أو المياه الجوفية. يجمع النظام بين خزان رمل أوتوماتيكي وخزان كربون أوتوماتيكي وفلتر دقيق ووحدة تناضح عكسي على إطار واحد، مع تدفق مياه نقية 1000-3000 لتر/ساعة وضغط دخول 0.1-0.4 MPa. يمكن تخصيص الشكل ومسار العملية والتكوين والوظائف حسب تحليل المياه ومتطلبات العميل.	نظام RO مدمج بخزاني رمل وكربون أوتوماتيكيين، فلترة دقيقة وتدفق 1000-3000 لتر/ساعة لمشاريع OEM.	خزان رمل أوتوماتيكي + خزان كربون أوتوماتيكي + فلتر دقيق + تناضح عكسي	ضغط الدخول	تخصيص المشروع	يمكن تخصيص الشكل ومسار العملية وتكوين المعدات ولوحة التحكم ووظائف الحماية حسب مصدر المياه ومساحة المشروع	الفنادق والمصانع والمدارس والمجمعات والمطابخ التجارية ومشاريع معالجة المياه
az	İki çənli əvvəlcədən təmizləməli inteqrə skid RO avadanlığı 1000-3000 L/saat	İki çənli əvvəlcədən təmizləməli skid RO sistemi	Yuchen Water iki çənli əvvəlcədən təmizləməli inteqrə skid RO avadanlığı kran suyu və ya yeraltı suyu təmizləyən kommersiya və yüngül sənaye B2B layihələri üçün hazırlanır. Sistem avtomatik qum çəni, avtomatik karbon çəni, dəqiq filtr və tərs osmos qurğusunu bir karkasda birləşdirir, 1000-3000 L/saat təmiz su axını və 0.1-0.4 MPa giriş təzyiqi ilə işləyir. Görünüş, proses axını, konfiqurasiya və funksiyalar su analizinə və müştəri tələbinə görə uyğunlaşdırılır.	Avtomatik qum və karbon çənləri, dəqiq filtrasiya və OEM layihələri üçün 1000-3000 L/saat təmiz su verən inteqrə skid RO sistemi.	Avtomatik qum çəni + avtomatik karbon çəni + dəqiq filtr + tərs osmos	Giriş təzyiqi	Layihə üzrə uyğunlaşdırma	Görünüş, proses axını, avadanlıq konfiqurasiyası, idarə paneli və qoruma funksiyaları mənbə suyuna və layihə sahəsinə görə uyğunlaşdırıla bilər	Otellər, zavodlar, məktəblər, yaşayış kompleksləri, kommersiya mətbəxləri və su təmizləmə layihələri
bg	Интегрирана скидна RO система с двуколонна предварителна обработка 1000-3000 L/h	Скидна RO система с двуколонна предварителна обработка	Интегрираната скидна RO система с двуколонна предварителна обработка на Yuchen Water е разработена за търговски и леки индустриални B2B проекти, които пречистват чешмяна или подземна вода. Системата комбинира автоматичен пясъчен съд, автоматичен въглероден съд, фин филтър и обратна осмоза върху една рама, с дебит чиста вода 1000-3000 L/h и входно налягане 0.1-0.4 MPa. Външен вид, процес, конфигурация и функции се настройват според анализа на водата и изискванията на клиента.	Интегрирана скидна RO система с автоматични пясъчен и въглероден съд, фин филтър и 1000-3000 L/h чиста вода за OEM проекти.	Автоматичен пясъчен съд + автоматичен въглероден съд + фин филтър + обратна осмоза	Входно налягане	Настройка по проект	Външният вид, процесът, конфигурацията, контролният панел и защитните функции могат да се адаптират към водоизточника и проектното пространство	Хотели, фабрики, училища, жилищни комплекси, търговски кухни и проекти за пречистване на вода
bn	দুই ট্যাংক প্রি-ট্রিটমেন্ট ইন্টিগ্রেটেড স্কিড RO সরঞ্জাম 1000-3000 L/h	দুই ট্যাংক প্রি-ট্রিটমেন্ট স্কিড RO সিস্টেম	Yuchen Water-এর দুই ট্যাংক প্রি-ট্রিটমেন্ট ইন্টিগ্রেটেড স্কিড RO সরঞ্জাম ট্যাপ পানি বা ভূগর্ভস্থ পানি বিশুদ্ধ করার বাণিজ্যিক ও হালকা শিল্প B2B প্রকল্পের জন্য তৈরি। সিস্টেমে এক ফ্রেমে স্বয়ংক্রিয় বালু ট্যাংক, স্বয়ংক্রিয় কার্বন ট্যাংক, প্রিসিশন ফিল্টার ও রিভার্স অসমোসিস ইউনিট থাকে, যা 1000-3000 L/h বিশুদ্ধ পানি এবং 0.1-0.4 MPa ইনলেট চাপের জন্য উপযোগী। বাহ্যিক নকশা, প্রক্রিয়া, কনফিগারেশন ও ফাংশন পানি বিশ্লেষণ এবং গ্রাহকের প্রয়োজন অনুযায়ী কাস্টম করা যায়।	স্বয়ংক্রিয় বালু ও কার্বন ট্যাংক, প্রিসিশন ফিল্টার এবং OEM প্রকল্পের জন্য 1000-3000 L/h বিশুদ্ধ পানি সহ ইন্টিগ্রেটেড স্কিড RO সিস্টেম।	স্বয়ংক্রিয় বালু ট্যাংক + স্বয়ংক্রিয় কার্বন ট্যাংক + প্রিসিশন ফিল্টার + রিভার্স অসমোসিস	ইনলেট চাপ	প্রকল্প অনুযায়ী কাস্টমাইজেশন	বাহ্যিক নকশা, প্রক্রিয়া, সরঞ্জাম কনফিগারেশন, কন্ট্রোল প্যানেল এবং সুরক্ষা ফাংশন উৎস পানি ও প্রকল্প স্থানের ভিত্তিতে কাস্টম করা যায়	হোটেল, কারখানা, স্কুল, কমিউনিটি, বাণিজ্যিক রান্নাঘর এবং পানি শোধন প্রকল্প
bs	Integrisana skid RO oprema s dvotankovskim predtretmanom 1000-3000 L/h	Skid RO sistem s dvotankovskim predtretmanom	Yuchen Water integrisana skid RO oprema s dvotankovskim predtretmanom namijenjena je komercijalnim i lakim industrijskim B2B projektima koji pročišćavaju vodovodnu ili podzemnu vodu. Sistem objedinjuje automatski pješčani tank, automatski karbonski tank, precizni filter i reverznu osmozu na jednom ramu, uz protok čiste vode 1000-3000 L/h i ulazni pritisak 0.1-0.4 MPa. Izgled, proces, konfiguracija i funkcije prilagođavaju se analizi vode i zahtjevima kupca.	Integrisani skid RO sistem s automatskim pješčanim i karbonskim tankom, preciznom filtracijom i 1000-3000 L/h čiste vode za OEM projekte.	Automatski pješčani tank + automatski karbonski tank + precizni filter + reverzna osmoza	Ulazni pritisak	Prilagođavanje projektu	Izgled, procesni tok, konfiguracija opreme, kontrolni panel i zaštitne funkcije mogu se prilagoditi izvoru vode i prostoru projekta	Hoteli, fabrike, škole, naselja, komercijalne kuhinje i projekti tretmana vode
cs	Integrované skidové RO zařízení s dvounádobovou předúpravou 1000-3000 L/h	Skidový RO systém s dvounádobovou předúpravou	Integrované skidové RO zařízení Yuchen Water s dvounádobovou předúpravou je určeno pro komerční a lehké průmyslové B2B projekty, které upravují vodovodní nebo podzemní vodu. Systém spojuje automatickou pískovou nádobu, automatickou uhlíkovou nádobu, jemný filtr a reverzní osmózu na jednom rámu, s průtokem čisté vody 1000-3000 L/h a vstupním tlakem 0.1-0.4 MPa. Vzhled, proces, konfigurace a funkce se upravují podle analýzy vody a požadavků zákazníka.	Integrovaný skidový RO systém s automatickou pískovou a uhlíkovou nádobou, jemnou filtrací a 1000-3000 L/h čisté vody pro OEM projekty.	Automatická písková nádoba + automatická uhlíková nádoba + jemný filtr + reverzní osmóza	Vstupní tlak	Přizpůsobení projektu	Vzhled, procesní tok, konfigurace zařízení, ovládací panel a ochranné funkce lze přizpůsobit zdrojové vodě a prostoru projektu	Hotely, továrny, školy, obytné areály, komerční kuchyně a projekty úpravy vody
da	Integreret skid-RO-anlæg med to-tanks forbehandling 1000-3000 L/h	Skid-RO med to-tanks forbehandling	Yuchen Water integreret skid-RO-anlæg med to-tanks forbehandling er udviklet til kommercielle og lettere industrielle B2B-projekter, der renser ledningsvand eller grundvand. Systemet samler automatisk sandtank, automatisk kultank, finfilter og omvendt osmose på én ramme, med 1000-3000 L/h rentvandsflow og 0.1-0.4 MPa indløbstryk. Udseende, procesflow, konfiguration og funktioner tilpasses vandanalyse og kundens krav.	Integreret skid-RO-system med automatiske sand- og kultanke, finfiltrering og 1000-3000 L/h rent vand til OEM-projekter.	Automatisk sandtank + automatisk kultank + finfilter + omvendt osmose	Indløbstryk	Projekttilpasning	Udseende, procesflow, udstyrskonfiguration, kontrolpanel og beskyttelsesfunktioner kan tilpasses kildevand og projektplads	Hoteller, fabrikker, skoler, boligområder, storkøkkener og vandbehandlingsprojekter
de	Integrierte Skid-RO-Anlage mit Zweitank-Vorbehandlung 1000-3000 L/h	Skid-RO-System mit Zweitank-Vorbehandlung	Die integrierte Skid-RO-Anlage mit Zweitank-Vorbehandlung von Yuchen Water ist für gewerbliche und leichte industrielle B2B-Projekte ausgelegt, die Leitungswasser oder Grundwasser aufbereiten. Das System kombiniert automatischen Sandbehälter, automatischen Aktivkohlebehälter, Feinfilter und Umkehrosmose auf einem Rahmen, mit 1000-3000 L/h Reinwasserleistung und 0.1-0.4 MPa Zulaufdruck. Ausführung, Prozessablauf, Konfiguration und Funktionen werden nach Wasseranalyse und Kundenanforderung angepasst.	Integriertes Skid-RO-System mit automatischem Sand- und Aktivkohlebehälter, Feinfiltration und 1000-3000 L/h Reinwasser für OEM-Projekte.	Automatischer Sandbehälter + automatischer Aktivkohlebehälter + Feinfilter + Umkehrosmose	Zulaufdruck	Projektanpassung	Ausführung, Prozessablauf, Anlagenkonfiguration, Schaltschrank und Schutzfunktionen können an Rohwasser und Projektfläche angepasst werden	Hotels, Fabriken, Schulen, Wohnanlagen, Großküchen und Wasseraufbereitungsprojekte
el	Ενσωματωμένος εξοπλισμός RO σε skid με προεπεξεργασία δύο δεξαμενών 1000-3000 L/h	Σύστημα RO skid με προεπεξεργασία δύο δεξαμενών	Ο ενσωματωμένος εξοπλισμός RO σε skid με προεπεξεργασία δύο δεξαμενών της Yuchen Water προορίζεται για εμπορικά και ελαφρά βιομηχανικά B2B έργα που επεξεργάζονται νερό δικτύου ή υπόγειο νερό. Το σύστημα ενώνει αυτόματη δεξαμενή άμμου, αυτόματη δεξαμενή ενεργού άνθρακα, φίλτρο ακριβείας και αντίστροφη όσμωση σε ένα πλαίσιο, με παροχή καθαρού νερού 1000-3000 L/h και πίεση εισόδου 0.1-0.4 MPa. Εμφάνιση, ροή διαδικασίας, διαμόρφωση και λειτουργίες προσαρμόζονται στην ανάλυση νερού και στις απαιτήσεις πελάτη.	Ενσωματωμένο σύστημα RO skid με αυτόματες δεξαμενές άμμου και άνθρακα, φίλτρο ακριβείας και 1000-3000 L/h καθαρού νερού για έργα OEM.	Αυτόματη δεξαμενή άμμου + αυτόματη δεξαμενή άνθρακα + φίλτρο ακριβείας + αντίστροφη όσμωση	Πίεση εισόδου	Προσαρμογή έργου	Η εμφάνιση, η ροή διαδικασίας, η διαμόρφωση εξοπλισμού, ο πίνακας ελέγχου και οι προστασίες προσαρμόζονται στο νερό πηγής και στον χώρο έργου	Ξενοδοχεία, εργοστάσια, σχολεία, κοινότητες, επαγγελματικές κουζίνες και έργα επεξεργασίας νερού
en	Dual-Tank Pretreatment Integrated Skid RO Equipment 1000-3000 L/h	Dual-tank pretreatment skid RO system	Yuchen Water dual-tank pretreatment integrated skid RO equipment is designed for commercial and light industrial B2B projects using tap water or groundwater. The system integrates an automatic sand tank, automatic carbon tank, precision filter and reverse osmosis unit on one frame, producing 1000-3000 L/h purified water with 0.1-0.4 MPa feed pressure. Appearance, process flow, configuration and functions can be customized according to source-water analysis and buyer requirements.	Integrated skid RO system with automatic sand and carbon tanks, precision filtration and 1000-3000 L/h purified water output for OEM projects.	Automatic sand tank + automatic carbon tank + precision filter + reverse osmosis	Feed pressure	Project customization	Appearance, process flow, equipment configuration, control panel and protection functions can be customized according to source water and project space	Hotels, factories, schools, communities, commercial kitchens and water treatment projects
es	Equipo RO integrado en bastidor con pretratamiento de dos tanques 1000-3000 L/h	Sistema RO en bastidor con pretratamiento de dos tanques	El equipo RO integrado en bastidor con pretratamiento de dos tanques de Yuchen Water está diseñado para proyectos B2B comerciales e industriales ligeros que purifican agua de red o agua subterránea. El sistema combina un tanque automático de arena, un tanque automático de carbón, un filtro de precisión y ósmosis inversa en un solo bastidor, con 1000-3000 L/h de agua purificada y presión de entrada de 0.1-0.4 MPa. La apariencia, el flujo del proceso, la configuración y las funciones se personalizan según el análisis del agua y los requisitos del comprador.	Sistema RO integrado en bastidor con tanques automáticos de arena y carbón, filtración de precisión y 1000-3000 L/h de agua purificada para proyectos OEM.	Tanque automático de arena + tanque automático de carbón + filtro de precisión + ósmosis inversa	Presión de entrada	Personalización del proyecto	Apariencia, flujo del proceso, configuración del equipo, panel de control y funciones de protección se adaptan al agua de origen y al espacio del proyecto	Hoteles, fábricas, escuelas, comunidades, cocinas comerciales y proyectos de tratamiento de agua
et	Kahe paagiga eeltöötlusega integreeritud skid-RO seade 1000-3000 L/h	Kahe paagiga eeltöötluse skid-RO süsteem	Yuchen Water kahe paagiga eeltöötlusega integreeritud skid-RO seade on mõeldud äri- ja kergtööstuse B2B projektidele, kus puhastatakse kraanivett või põhjavett. Süsteem ühendab automaatse liivapaagi, automaatse söepaagi, peenfiltri ja pöördosmoosi ühe raamiga, andes 1000-3000 L/h puhast vett ning töötades 0.1-0.4 MPa sisendrõhul. Välimus, protsessivoog, konfiguratsioon ja funktsioonid kohandatakse veeanalüüsi ning kliendi nõuete järgi.	Integreeritud skid-RO süsteem automaatsete liiva- ja söepaakidega, peenfiltriga ning 1000-3000 L/h puhta veega OEM-projektidele.	Automaatne liivapaak + automaatne söepaak + peenfilter + pöördosmoos	Sisendrõhk	Projekti kohandamine	Välimus, protsessivoog, seadmete konfiguratsioon, juhtpaneel ja kaitsefunktsioonid saab kohandada lähteveele ja projektiruumile	Hotellid, tehased, koolid, kogukonnad, suurköögid ja veetöötlusprojektid
fa	دستگاه RO یکپارچه روی شاسی با پیش‌تصفیه دو مخزن 1000-3000 لیتر/ساعت	سامانه RO شاسی‌دار با پیش‌تصفیه دو مخزن	دستگاه RO یکپارچه روی شاسی با پیش‌تصفیه دو مخزن Yuchen Water برای پروژه‌های B2B تجاری و صنعتی سبک که آب شهری یا آب زیرزمینی را تصفیه می‌کنند طراحی شده است. این سامانه مخزن شنی خودکار، مخزن کربن خودکار، فیلتر دقیق و واحد اسمز معکوس را روی یک فریم ترکیب می‌کند و با فشار ورودی 0.1-0.4 MPa، دبی آب تصفیه‌شده 1000-3000 لیتر/ساعت ارائه می‌دهد. ظاهر، مسیر فرایند، پیکربندی و عملکردها بر اساس تحلیل آب و نیاز خریدار قابل سفارشی‌سازی است.	سامانه RO شاسی‌دار با مخازن شنی و کربنی خودکار، فیلتراسیون دقیق و خروجی 1000-3000 لیتر/ساعت برای پروژه‌های OEM.	مخزن شنی خودکار + مخزن کربن خودکار + فیلتر دقیق + اسمز معکوس	فشار ورودی	سفارشی‌سازی پروژه	ظاهر، مسیر فرایند، پیکربندی تجهیزات، تابلو کنترل و عملکردهای حفاظتی بر اساس آب ورودی و فضای پروژه قابل تنظیم است	هتل‌ها، کارخانه‌ها، مدارس، مجتمع‌ها، آشپزخانه‌های تجاری و پروژه‌های تصفیه آب
fi	Kahden säiliön esikäsittelyllä varustettu integroitu skid-RO-laite 1000-3000 L/h	Kahden säiliön esikäsittelyn skid-RO-järjestelmä	Yuchen Waterin kahden säiliön esikäsittelyllä varustettu integroitu skid-RO-laite on suunniteltu kaupallisiin ja kevyen teollisuuden B2B-hankkeisiin, joissa puhdistetaan vesijohtovettä tai pohjavettä. Järjestelmä yhdistää automaattisen hiekkasäiliön, automaattisen hiilisäiliön, tarkkuussuodattimen ja käänteisosmoosin yhdelle rungolle, tuottaen 1000-3000 L/h puhdasta vettä 0.1-0.4 MPa tulopaineella. Ulkoasu, prosessivirtaus, kokoonpano ja toiminnot mukautetaan vesianalyysin ja ostajan vaatimusten mukaan.	Integroitu skid-RO-järjestelmä automaattisilla hiekka- ja hiilisäiliöillä, tarkkuussuodatuksella ja 1000-3000 L/h puhdasvesituotolla OEM-hankkeisiin.	Automaattinen hiekkasäiliö + automaattinen hiilisäiliö + tarkkuussuodatin + käänteisosmoosi	Tulopaine	Projektikohtainen mukautus	Ulkoasu, prosessivirtaus, laitekokoonpano, ohjauspaneeli ja suojaustoiminnot voidaan mukauttaa lähdeveden ja projektitilan mukaan	Hotellit, tehtaat, koulut, yhteisöt, suurkeittiöt ja vedenkäsittelyhankkeet
fr	Équipement RO intégré sur châssis avec prétraitement à deux cuves 1000-3000 L/h	Système RO sur châssis avec prétraitement à deux cuves	L’équipement RO intégré sur châssis avec prétraitement à deux cuves de Yuchen Water est conçu pour les projets B2B commerciaux et industriels légers traitant l’eau du réseau ou l’eau souterraine. Le système réunit une cuve à sable automatique, une cuve à charbon automatique, un filtre de précision et l’osmose inverse sur un seul châssis, avec un débit d’eau purifiée de 1000-3000 L/h et une pression d’entrée de 0.1-0.4 MPa. L’apparence, le procédé, la configuration et les fonctions sont adaptés à l’analyse de l’eau et aux exigences de l’acheteur.	Système RO intégré sur châssis avec cuves automatiques à sable et à charbon, filtration de précision et 1000-3000 L/h d’eau purifiée pour projets OEM.	Cuve à sable automatique + cuve à charbon automatique + filtre de précision + osmose inverse	Pression d’entrée	Personnalisation du projet	L’apparence, le procédé, la configuration, l’armoire de commande et les fonctions de protection peuvent être adaptés à l’eau source et à l’espace du projet	Hôtels, usines, écoles, résidences, cuisines professionnelles et projets de traitement de l’eau
ha	Na'urar RO ta skid mai matatar farko ta tankuna biyu 1000-3000 L/h	Tsarin RO na skid mai tankuna biyu	Na'urar RO ta skid mai matatar farko ta tankuna biyu ta Yuchen Water an yi ta ne don ayyukan B2B na kasuwanci da ƙananan masana'antu da ke tace ruwan famfo ko ruwan ƙasa. Tsarin yana haɗa tankin yashi na atomatik, tankin carbon na atomatik, matatar daidaito da reverse osmosis a kan firam ɗaya, yana bada ruwan da aka tsarkake 1000-3000 L/h da matsin shigar ruwa 0.1-0.4 MPa. Siffa, tsarin aiki, kayan haɗi da ayyuka ana iya daidaita su bisa gwajin ruwa da bukatar abokin ciniki.	Tsarin RO na skid tare da tankin yashi da carbon na atomatik, matatar daidaito da 1000-3000 L/h ruwan tsabta don ayyukan OEM.	Tankin yashi na atomatik + tankin carbon na atomatik + matatar daidaito + reverse osmosis	Matsin shigar ruwa	Daidaitawar aikin	Siffa, tsarin aiki, kayan aiki, allon sarrafawa da ayyukan kariya ana iya daidaita su bisa tushen ruwa da sararin aikin	Otelu, masana'antu, makarantu, unguwanni, manyan girki na kasuwanci da ayyukan tace ruwa
he	מערכת RO משולבת על שלדה עם קדם־טיפול בשני מכלים 1000-3000 ליטר/שעה	מערכת RO על שלדה עם קדם־טיפול בשני מכלים	מערכת RO משולבת על שלדה עם קדם־טיפול בשני מכלים של Yuchen Water מיועדת לפרויקטי B2B מסחריים ותעשייה קלה המטפלים במי רשת או במי תהום. המערכת משלבת מכל חול אוטומטי, מכל פחם אוטומטי, מסנן עדין ויחידת אוסמוזה הפוכה על מסגרת אחת, עם תפוקת מים מטוהרים 1000-3000 ליטר/שעה ולחץ כניסה 0.1-0.4 MPa. המראה, זרימת התהליך, התצורה והפונקציות ניתנים להתאמה לפי ניתוח המים ודרישות הרוכש.	מערכת RO משולבת על שלדה עם מכלי חול ופחם אוטומטיים, סינון עדין ותפוקת 1000-3000 ליטר/שעה לפרויקטי OEM.	מכל חול אוטומטי + מכל פחם אוטומטי + מסנן עדין + אוסמוזה הפוכה	לחץ כניסה	התאמה לפרויקט	המראה, זרימת התהליך, תצורת הציוד, לוח הבקרה ופונקציות ההגנה ניתנים להתאמה למקור המים ולשטח הפרויקט	בתי מלון, מפעלים, בתי ספר, קהילות, מטבחים מסחריים ופרויקטים לטיפול במים
hi	दो टैंक प्री-ट्रीटमेंट इंटीग्रेटेड स्किड RO उपकरण 1000-3000 L/h	दो टैंक प्री-ट्रीटमेंट स्किड RO सिस्टम	Yuchen Water का दो टैंक प्री-ट्रीटमेंट इंटीग्रेटेड स्किड RO उपकरण उन वाणिज्यिक और हल्के औद्योगिक B2B परियोजनाओं के लिए है जो नल के पानी या भूजल को शुद्ध करती हैं। यह सिस्टम एक ही फ्रेम पर ऑटोमैटिक सैंड टैंक, ऑटोमैटिक कार्बन टैंक, प्रिसिजन फिल्टर और रिवर्स ऑस्मोसिस यूनिट को जोड़ता है, 0.1-0.4 MPa इनलेट दबाव पर 1000-3000 L/h शुद्ध पानी देता है। बाहरी रूप, प्रक्रिया, कॉन्फिगरेशन और कार्य पानी के विश्लेषण तथा खरीदार की आवश्यकता के अनुसार अनुकूलित किए जा सकते हैं।	OEM परियोजनाओं के लिए ऑटोमैटिक सैंड और कार्बन टैंक, प्रिसिजन फिल्ट्रेशन और 1000-3000 L/h शुद्ध पानी वाला इंटीग्रेटेड स्किड RO सिस्टम।	ऑटोमैटिक सैंड टैंक + ऑटोमैटिक कार्बन टैंक + प्रिसिजन फिल्टर + रिवर्स ऑस्मोसिस	इनलेट दबाव	परियोजना अनुकूलन	बाहरी रूप, प्रक्रिया प्रवाह, उपकरण कॉन्फिगरेशन, कंट्रोल पैनल और सुरक्षा कार्य स्रोत पानी और परियोजना स्थान के अनुसार अनुकूलित किए जा सकते हैं	होटल, कारखाने, स्कूल, समुदाय, वाणिज्यिक रसोई और जल उपचार परियोजनाएँ
hr	Integrirana skid RO oprema s dvospremničkom predobradom 1000-3000 L/h	Skid RO sustav s dvospremničkom predobradom	Yuchen Water integrirana skid RO oprema s dvospremničkom predobradom namijenjena je komercijalnim i lakim industrijskim B2B projektima koji pročišćavaju vodovodnu ili podzemnu vodu. Sustav objedinjuje automatski pješčani spremnik, automatski ugljeni spremnik, fini filtar i reverznu osmozu na jednom okviru, uz protok čiste vode 1000-3000 L/h i ulazni tlak 0.1-0.4 MPa. Izgled, proces, konfiguracija i funkcije prilagođavaju se analizi vode i zahtjevima kupca.	Integrirani skid RO sustav s automatskim pješčanim i ugljenim spremnikom, finom filtracijom i 1000-3000 L/h čiste vode za OEM projekte.	Automatski pješčani spremnik + automatski ugljeni spremnik + fini filtar + reverzna osmoza	Ulazni tlak	Prilagodba projektu	Izgled, procesni tok, konfiguracija opreme, upravljačka ploča i zaštitne funkcije mogu se prilagoditi izvornoj vodi i prostoru projekta	Hoteli, tvornice, škole, naselja, komercijalne kuhinje i projekti obrade vode
hu	Két tartályos előkezelésű integrált skid RO berendezés 1000-3000 L/h	Két tartályos előkezelésű skid RO rendszer	A Yuchen Water két tartályos előkezelésű integrált skid RO berendezése kereskedelmi és könnyűipari B2B projektekhez készült, ahol vezetékes vizet vagy talajvizet kell tisztítani. A rendszer automatikus homoktartályt, automatikus aktívszén-tartályt, finomszűrőt és fordított ozmózist egy keretre épít, 1000-3000 L/h tisztítottvíz-hozammal és 0.1-0.4 MPa belépő nyomással. A megjelenés, a folyamat, a konfiguráció és a funkciók a vízelemzéshez és a vevő igényeihez igazíthatók.	Integrált skid RO rendszer automatikus homok- és aktívszén-tartállyal, finomszűréssel és 1000-3000 L/h tisztított vízzel OEM projektekhez.	Automatikus homoktartály + automatikus aktívszén-tartály + finomszűrő + fordított ozmózis	Belépő nyomás	Projekt szerinti testreszabás	A megjelenés, a folyamat, a berendezés-konfiguráció, a vezérlőpanel és a védelmi funkciók a forrásvízhez és a projektterülethez igazíthatók	Szállodák, gyárak, iskolák, lakóközösségek, ipari konyhák és vízkezelési projektek
hy	Երկու տարայով նախամշակմամբ ինտեգրված skid RO սարքավորում 1000-3000 L/h	Երկու տարայով նախամշակման skid RO համակարգ	Yuchen Water-ի երկու տարայով նախամշակմամբ ինտեգրված skid RO սարքավորումը նախատեսված է առևտրային և թեթև արդյունաբերական B2B նախագծերի համար, որոնք մաքրում են ծորակի կամ ստորգետնյա ջուր։ Համակարգը մեկ շրջանակի վրա միավորում է ավտոմատ ավազային տարա, ավտոմատ ածխային տարա, ճշգրիտ ֆիլտր և հակադարձ օսմոս, ապահովելով 1000-3000 L/h մաքրված ջուր և 0.1-0.4 MPa մուտքային ճնշում։ Տեսքը, գործընթացը, կազմաձևումը և գործառույթները հարմարեցվում են ջրի վերլուծությանն ու գնորդի պահանջներին։	Ինտեգրված skid RO համակարգ՝ ավտոմատ ավազային և ածխային տարաներով, ճշգրիտ ֆիլտրացմամբ և 1000-3000 L/h մաքուր ջրի ելքով OEM նախագծերի համար։	Ավտոմատ ավազային տարա + ավտոմատ ածխային տարա + ճշգրիտ ֆիլտր + հակադարձ օսմոս	Մուտքային ճնշում	Նախագծային հարմարեցում	Տեսքը, գործընթացի հոսքը, սարքավորման կազմաձևումը, կառավարման վահանակը և պաշտպանական գործառույթները հարմարեցվում են սկզբնաղբյուր ջրին և նախագծի տարածքին	Հյուրանոցներ, գործարաններ, դպրոցներ, համայնքներ, առևտրային խոհանոցներ և ջրի մաքրման նախագծեր
id	Peralatan RO skid terintegrasi dengan praperlakuan dua tangki 1000-3000 L/jam	Sistem RO skid dengan praperlakuan dua tangki	Peralatan RO skid terintegrasi dengan praperlakuan dua tangki dari Yuchen Water dirancang untuk proyek B2B komersial dan industri ringan yang mengolah air ledeng atau air tanah. Sistem ini menggabungkan tangki pasir otomatis, tangki karbon otomatis, filter presisi dan reverse osmosis dalam satu rangka, menghasilkan air murni 1000-3000 L/jam dengan tekanan masuk 0.1-0.4 MPa. Tampilan, alur proses, konfigurasi dan fungsi dapat disesuaikan menurut analisis air serta kebutuhan pembeli.	Sistem RO skid terintegrasi dengan tangki pasir dan karbon otomatis, filtrasi presisi dan keluaran air murni 1000-3000 L/jam untuk proyek OEM.	Tangki pasir otomatis + tangki karbon otomatis + filter presisi + reverse osmosis	Tekanan masuk	Penyesuaian proyek	Tampilan, alur proses, konfigurasi peralatan, panel kontrol dan fungsi perlindungan dapat disesuaikan dengan sumber air dan ruang proyek	Hotel, pabrik, sekolah, komunitas, dapur komersial dan proyek pengolahan air
it	Impianto RO integrato su skid con pretrattamento a due serbatoi 1000-3000 L/h	Sistema RO su skid con pretrattamento a due serbatoi	L’impianto RO integrato su skid con pretrattamento a due serbatoi di Yuchen Water è progettato per progetti B2B commerciali e industriali leggeri che trattano acqua di rete o acqua di falda. Il sistema combina serbatoio automatico a sabbia, serbatoio automatico a carbone, filtro di precisione e osmosi inversa su un unico telaio, con 1000-3000 L/h di acqua purificata e pressione in ingresso 0.1-0.4 MPa. Aspetto, flusso di processo, configurazione e funzioni sono personalizzabili in base all’analisi dell’acqua e alle richieste dell’acquirente.	Sistema RO integrato su skid con serbatoi automatici a sabbia e carbone, filtrazione di precisione e 1000-3000 L/h di acqua purificata per progetti OEM.	Serbatoio automatico a sabbia + serbatoio automatico a carbone + filtro di precisione + osmosi inversa	Pressione in ingresso	Personalizzazione del progetto	Aspetto, flusso di processo, configurazione dell’impianto, quadro di controllo e funzioni di protezione possono essere adattati all’acqua di origine e allo spazio del progetto	Hotel, fabbriche, scuole, comunità, cucine commerciali e progetti di trattamento acqua
ja	二槽式前処理一体型スキッドRO装置 1000-3000 L/h	二槽式前処理スキッドROシステム	Yuchen Waterの二槽式前処理一体型スキッドRO装置は、水道水または地下水を処理する商業施設・軽工業向けB2B案件に適した設計です。自動砂ろ過槽、自動活性炭槽、精密フィルター、逆浸透膜ユニットを一体フレームにまとめ、0.1-0.4 MPaの給水圧で1000-3000 L/hの浄水を供給します。外観、処理フロー、構成、保護機能は原水分析と購入者の要件に合わせて調整できます。	OEM案件向けに、自動砂ろ過槽と活性炭槽、精密ろ過、1000-3000 L/hの浄水能力を備えた一体型スキッドROシステム。	自動砂ろ過槽 + 自動活性炭槽 + 精密フィルター + 逆浸透膜	給水圧	案件別カスタマイズ	外観、処理フロー、機器構成、制御盤、保護機能は原水条件と設置スペースに合わせて調整できます	ホテル、工場、学校、集合施設、業務用厨房、水処理案件
ka	ორი ავზის წინასწარი დამუშავებით ინტეგრირებული skid RO მოწყობილობა 1000-3000 L/h	ორი ავზის წინასწარი დამუშავების skid RO სისტემა	Yuchen Water-ის ორი ავზის წინასწარი დამუშავებით ინტეგრირებული skid RO მოწყობილობა განკუთვნილია კომერციული და მსუბუქი ინდუსტრიული B2B პროექტებისთვის, სადაც მუშავდება ონკანის ან მიწისქვეშა წყალი. სისტემა ერთ ჩარჩოზე აერთიანებს ავტომატურ ქვიშის ავზს, ავტომატურ ნახშირის ავზს, ზუსტ ფილტრს და უკუ ოსმოსს, აწარმოებს 1000-3000 L/h გასუფთავებულ წყალს 0.1-0.4 MPa შესასვლელი წნევით. გარეგნობა, პროცესის სქემა, კონფიგურაცია და ფუნქციები მორგებულია წყლის ანალიზსა და მყიდველის მოთხოვნებზე.	ინტეგრირებული skid RO სისტემა ავტომატური ქვიშისა და ნახშირის ავზებით, ზუსტი ფილტრაციით და 1000-3000 L/h სუფთა წყლით OEM პროექტებისთვის.	ავტომატური ქვიშის ავზი + ავტომატური ნახშირის ავზი + ზუსტი ფილტრი + უკუ ოსმოსი	შესასვლელი წნევა	პროექტზე მორგება	გარეგნობა, პროცესის სქემა, მოწყობილობის კონფიგურაცია, მართვის პანელი და დაცვის ფუნქციები წყლის წყაროსა და პროექტის სივრცეზე მორგდება	სასტუმროები, ქარხნები, სკოლები, საცხოვრებელი კომპლექსები, კომერციული სამზარეულოები და წყლის დამუშავების პროექტები
kk	Екі бакты алдын ала тазарту біріктірілген skid RO жабдығы 1000-3000 L/h	Екі бакты алдын ала тазарту skid RO жүйесі	Yuchen Water екі бакты алдын ала тазарту біріктірілген skid RO жабдығы құбыр суын немесе жер асты суын тазартатын коммерциялық және жеңіл өнеркәсіптік B2B жобаларға арналған. Жүйе бір раманың үстінде автоматты құм багын, автоматты көмір багын, дәл сүзгіні және кері осмос блогын біріктіреді, 0.1-0.4 MPa кіріс қысымында 1000-3000 L/h тазартылған су береді. Сыртқы түрі, процесс сызбасы, конфигурациясы және функциялары су талдауы мен сатып алушы талабына қарай бейімделеді.	OEM жобалары үшін автоматты құм және көмір бактары, дәл сүзгілеу және 1000-3000 L/h тазартылған су шығаратын біріктірілген skid RO жүйесі.	Автоматты құм багы + автоматты көмір багы + дәл сүзгі + кері осмос	Кіріс қысымы	Жобаға бейімдеу	Сыртқы түрі, процесс ағыны, жабдық конфигурациясы, басқару панелі және қорғаныс функциялары су көзі мен жоба алаңына қарай бейімделеді	Қонақүйлер, зауыттар, мектептер, тұрғын кешендер, коммерциялық асүйлер және су тазарту жобалары
ko	이중 탱크 전처리 일체형 스키드 RO 설비 1000-3000 L/h	이중 탱크 전처리 스키드 RO 시스템	Yuchen Water의 이중 탱크 전처리 일체형 스키드 RO 설비는 수돗물 또는 지하수를 정수하는 상업 및 경공업 B2B 프로젝트용으로 설계되었습니다. 자동 모래 탱크, 자동 활성탄 탱크, 정밀 필터와 역삼투 장치를 하나의 프레임에 통합하여 0.1-0.4 MPa 급수 압력에서 1000-3000 L/h의 정제수를 생산합니다. 외관, 공정 흐름, 구성과 기능은 원수 분석 및 구매자 요구에 맞추어 조정할 수 있습니다.	OEM 프로젝트용 자동 모래 및 활성탄 탱크, 정밀 여과와 1000-3000 L/h 정수 생산 능력을 갖춘 일체형 스키드 RO 시스템.	자동 모래 탱크 + 자동 활성탄 탱크 + 정밀 필터 + 역삼투	급수 압력	프로젝트 맞춤	외관, 공정 흐름, 설비 구성, 제어반과 보호 기능은 원수 조건과 설치 공간에 맞게 조정할 수 있습니다	호텔, 공장, 학교, 단지, 상업용 주방 및 수처리 프로젝트
ku	Amûra RO ya skidê ya yekpare bi pêşpaqijkirina du tankan 1000-3000 L/h	Sîstema RO ya skidê bi pêşpaqijkirina du tankan	Amûra RO ya skidê ya yekpare bi pêşpaqijkirina du tankan a Yuchen Water ji bo projeyên B2B yên bazirganî û pîşesaziya sivik tê çêkirin ku ava torê an ava binerdê paqij dikin. Sîstem tankê x砂ê otomatîk, tankê karbonê otomatîk, fîltreyê hûr û osmoza berevajî li ser yek çarçoveyê digihîne hev, bi herikîna ava paqij 1000-3000 L/h û zexta têketinê 0.1-0.4 MPa. Dîmen, rêça pêvajoyê, konfîgûrasyon û fonksiyon li gorî analîza avê û daxwaza kiryar têne eyarkirin.	Sîstema RO ya skidê ya yekpare bi tankên x砂 û karbonê otomatîk, fîltrasyona hûr û 1000-3000 L/h ava paqij ji bo projeyên OEM.	Tankê x砂ê otomatîk + tankê karbonê otomatîk + fîltreyê hûr + osmoza berevajî	Zexta têketinê	Eyarkirina projeyê	Dîmen, rêça pêvajoyê, konfîgûrasyona amûrê, panela kontrolê û fonksiyonên parastinê li gorî çavkaniya avê û cihê projeyê têne eyarkirin	Otel, fabrîqe, dibistan, civak, metbexên bazirganî û projeyên paqijkirina avê
ky	Эки бактуу алдын ала тазалоосу бар интеграцияланган skid RO жабдыгы 1000-3000 L/h	Эки бактуу алдын ала тазалоочу skid RO системасы	Yuchen Water эки бактуу алдын ала тазалоосу бар интеграцияланган skid RO жабдыгы кран суусун же жер астындагы сууну тазалаган коммерциялык жана жеңил өнөр жай B2B долбоорлору үчүн жасалган. Система бир рамада автоматтык кум багын, автоматтык көмүр багын, так фильтрди жана тескери осмосту бириктирет, 0.1-0.4 MPa кирүү басымында 1000-3000 L/h таза суу берет. Сырткы көрүнүшү, процесс агымы, конфигурациясы жана функциялары суу анализине жана сатып алуучунун талабына жараша ылайыкташат.	OEM долбоорлору үчүн автоматтык кум жана көмүр бактары, так фильтрация жана 1000-3000 L/h таза суу чыгаруучу интеграцияланган skid RO системасы.	Автоматтык кум багы + автоматтык көмүр багы + так фильтр + тескери осмос	Кирүү басымы	Долбоорго ылайыкташтыруу	Сырткы көрүнүш, процесс агымы, жабдык конфигурациясы, башкаруу панели жана коргоо функциялары суу булагына жана долбоор мейкиндигине жараша ылайыкталат	Мейманканалар, заводдор, мектептер, турак жай комплекстери, коммерциялык ашканалар жана суу тазалоо долбоорлору
lt	Integruota skid RO įranga su dviejų talpų pirminiu valymu 1000-3000 L/h	Skid RO sistema su dviejų talpų pirminiu valymu	Yuchen Water integruota skid RO įranga su dviejų talpų pirminiu valymu skirta komerciniams ir lengvosios pramonės B2B projektams, kuriuose valomas vandentiekio arba požeminis vanduo. Sistema viename rėme sujungia automatinę smėlio talpą, automatinę anglies talpą, tikslų filtrą ir atvirkštinį osmosą, tiekdama 1000-3000 L/h išvalyto vandens esant 0.1-0.4 MPa įėjimo slėgiui. Išvaizda, proceso eiga, konfigūracija ir funkcijos pritaikomos pagal vandens analizę ir pirkėjo reikalavimus.	Integruota skid RO sistema su automatinėmis smėlio ir anglies talpomis, tikslia filtracija ir 1000-3000 L/h švaraus vandens našumu OEM projektams.	Automatinė smėlio talpa + automatinė anglies talpa + tikslus filtras + atvirkštinis osmosas	Įėjimo slėgis	Projekto pritaikymas	Išvaizda, proceso eiga, įrangos konfigūracija, valdymo skydas ir apsaugos funkcijos gali būti pritaikytos vandens šaltiniui ir projekto erdvei	Viešbučiai, gamyklos, mokyklos, gyvenvietės, komercinės virtuvės ir vandens valymo projektai
lv	Integrēta skid RO iekārta ar divu tvertņu priekšattīrīšanu 1000-3000 L/h	Skid RO sistēma ar divu tvertņu priekšattīrīšanu	Yuchen Water integrētā skid RO iekārta ar divu tvertņu priekšattīrīšanu ir paredzēta komerciāliem un vieglās rūpniecības B2B projektiem, kuros attīra krāna ūdeni vai pazemes ūdeni. Sistēma vienā rāmī apvieno automātisku smilšu tvertni, automātisku ogles tvertni, precīzo filtru un reverso osmozi, nodrošinot 1000-3000 L/h attīrīta ūdens un 0.1-0.4 MPa ieplūdes spiedienu. Izskats, procesa plūsma, konfigurācija un funkcijas tiek pielāgotas ūdens analīzei un pircēja prasībām.	Integrēta skid RO sistēma ar automātiskām smilšu un ogles tvertnēm, precīzo filtrāciju un 1000-3000 L/h tīra ūdens izlaidi OEM projektiem.	Automātiska smilšu tvertne + automātiska ogles tvertne + precīzais filtrs + reversā osmoze	Ieplūdes spiediens	Projekta pielāgošana	Izskatu, procesa plūsmu, iekārtas konfigurāciju, vadības paneli un aizsardzības funkcijas var pielāgot ūdens avotam un projekta telpai	Viesnīcas, rūpnīcas, skolas, kopienas, komerciālās virtuves un ūdens attīrīšanas projekti
ms	Peralatan RO skid bersepadu dengan prarawatan dua tangki 1000-3000 L/jam	Sistem RO skid dengan prarawatan dua tangki	Peralatan RO skid bersepadu dengan prarawatan dua tangki daripada Yuchen Water direka untuk projek B2B komersial dan industri ringan yang menulenkan air paip atau air bawah tanah. Sistem ini menggabungkan tangki pasir automatik, tangki karbon automatik, penapis ketepatan dan osmosis songsang pada satu rangka, menghasilkan air tulen 1000-3000 L/jam pada tekanan masuk 0.1-0.4 MPa. Rupa, aliran proses, konfigurasi dan fungsi boleh disesuaikan mengikut analisis air serta keperluan pembeli.	Sistem RO skid bersepadu dengan tangki pasir dan karbon automatik, penapisan ketepatan dan keluaran air tulen 1000-3000 L/jam untuk projek OEM.	Tangki pasir automatik + tangki karbon automatik + penapis ketepatan + osmosis songsang	Tekanan masuk	Penyesuaian projek	Rupa, aliran proses, konfigurasi peralatan, panel kawalan dan fungsi perlindungan boleh disesuaikan mengikut sumber air dan ruang projek	Hotel, kilang, sekolah, komuniti, dapur komersial dan projek rawatan air
nl	Geïntegreerde skid-RO-installatie met tweetanks voorbehandeling 1000-3000 L/h	Skid-RO-systeem met tweetanks voorbehandeling	De geïntegreerde skid-RO-installatie met tweetanks voorbehandeling van Yuchen Water is ontwikkeld voor commerciële en lichte industriële B2B-projecten die leidingwater of grondwater zuiveren. Het systeem combineert een automatische zandtank, automatische koolstoftank, fijnfilter en omgekeerde osmose op één frame, met 1000-3000 L/h gezuiverd water en 0.1-0.4 MPa inlaatdruk. Uiterlijk, processtroom, configuratie en functies worden aangepast op basis van wateranalyse en eisen van de koper.	Geïntegreerd skid-RO-systeem met automatische zand- en koolstoftanks, fijnfiltratie en 1000-3000 L/h gezuiverd water voor OEM-projecten.	Automatische zandtank + automatische koolstoftank + fijnfilter + omgekeerde osmose	Inlaatdruk	Projectaanpassing	Uiterlijk, processtroom, apparatuurconfiguratie, bedieningspaneel en beschermingsfuncties kunnen worden aangepast aan bronwater en projectruimte	Hotels, fabrieken, scholen, gemeenschappen, grootkeukens en waterbehandelingsprojecten
no	Integrert skid-RO-anlegg med to-tanks forbehandling 1000-3000 L/h	Skid-RO-system med to-tanks forbehandling	Yuchen Water integrert skid-RO-anlegg med to-tanks forbehandling er laget for kommersielle og lette industrielle B2B-prosjekter som renser springvann eller grunnvann. Systemet samler automatisk sandtank, automatisk karbontank, presisjonsfilter og omvendt osmose på én ramme, med 1000-3000 L/h renset vann og 0.1-0.4 MPa innløpstrykk. Utseende, prosessflyt, konfigurasjon og funksjoner tilpasses vannanalyse og kjøperens krav.	Integrert skid-RO-system med automatiske sand- og karbontanker, presisjonsfiltrering og 1000-3000 L/h rent vann for OEM-prosjekter.	Automatisk sandtank + automatisk karbontank + presisjonsfilter + omvendt osmose	Innløpstrykk	Prosjekttilpasning	Utseende, prosessflyt, utstyrskonfigurasjon, kontrollpanel og beskyttelsesfunksjoner kan tilpasses kildevann og prosjektplass	Hoteller, fabrikker, skoler, boligområder, storkjøkken og vannbehandlingsprosjekter
pl	Zintegrowana stacja RO na ramie z dwuzbiornikowym przygotowaniem wody 1000-3000 L/h	Skid RO z dwuzbiornikowym przygotowaniem wody	Zintegrowana stacja RO na ramie z dwuzbiornikowym przygotowaniem wody Yuchen Water jest przeznaczona do komercyjnych i lekkich przemysłowych projektów B2B uzdatniających wodę wodociągową lub podziemną. System łączy automatyczny zbiornik piaskowy, automatyczny zbiornik węglowy, filtr dokładny i odwróconą osmozę na jednej ramie, zapewniając 1000-3000 L/h wody oczyszczonej przy ciśnieniu wejściowym 0.1-0.4 MPa. Wygląd, przebieg procesu, konfiguracja i funkcje dostosowuje się do analizy wody oraz wymagań kupującego.	Zintegrowany skid RO z automatycznymi zbiornikami piaskowym i węglowym, filtracją dokładną oraz 1000-3000 L/h wody oczyszczonej dla projektów OEM.	Automatyczny zbiornik piaskowy + automatyczny zbiornik węglowy + filtr dokładny + odwrócona osmoza	Ciśnienie wejściowe	Dostosowanie projektu	Wygląd, przebieg procesu, konfigurację urządzenia, panel sterowania i funkcje ochronne można dostosować do źródła wody i przestrzeni projektu	Hotele, zakłady, szkoły, osiedla, kuchnie komercyjne i projekty uzdatniania wody
pt	Equipamento RO integrado em skid com pré-tratamento de dois tanques 1000-3000 L/h	Sistema RO em skid com pré-tratamento de dois tanques	O equipamento RO integrado em skid com pré-tratamento de dois tanques da Yuchen Water foi desenvolvido para projetos B2B comerciais e industriais leves que purificam água da rede ou água subterrânea. O sistema combina tanque automático de areia, tanque automático de carvão, filtro de precisão e osmose reversa em uma única estrutura, fornecendo 1000-3000 L/h de água purificada com pressão de entrada de 0.1-0.4 MPa. Aparência, fluxo de processo, configuração e funções podem ser personalizados conforme a análise da água e os requisitos do comprador.	Sistema RO integrado em skid com tanques automáticos de areia e carvão, filtragem de precisão e 1000-3000 L/h de água purificada para projetos OEM.	Tanque automático de areia + tanque automático de carvão + filtro de precisão + osmose reversa	Pressão de entrada	Personalização do projeto	Aparência, fluxo de processo, configuração do equipamento, painel de controle e funções de proteção podem ser ajustados à água de origem e ao espaço do projeto	Hotéis, fábricas, escolas, comunidades, cozinhas comerciais e projetos de tratamento de água
ro	Echipament RO integrat pe skid cu pretratare în două tancuri 1000-3000 L/h	Sistem RO pe skid cu pretratare în două tancuri	Echipamentul RO integrat pe skid cu pretratare în două tancuri de la Yuchen Water este proiectat pentru proiecte B2B comerciale și industriale ușoare care purifică apă de la rețea sau apă subterană. Sistemul combină un tanc automat cu nisip, un tanc automat cu carbon, filtru de precizie și osmoză inversă pe un singur cadru, cu debit de apă purificată 1000-3000 L/h și presiune de intrare 0.1-0.4 MPa. Aspectul, fluxul de proces, configurația și funcțiile se personalizează conform analizei apei și cerințelor cumpărătorului.	Sistem RO integrat pe skid cu tancuri automate de nisip și carbon, filtrare de precizie și 1000-3000 L/h apă purificată pentru proiecte OEM.	Tanc automat cu nisip + tanc automat cu carbon + filtru de precizie + osmoză inversă	Presiune de intrare	Personalizare proiect	Aspectul, fluxul de proces, configurația echipamentului, panoul de control și funcțiile de protecție pot fi adaptate la sursa de apă și spațiul proiectului	Hoteluri, fabrici, școli, comunități, bucătării comerciale și proiecte de tratare a apei
ru	Двухколонная интегрированная рамная RO установка предварительной очистки 1000-3000 л/ч	Рамная RO система с двухколонной предварительной очисткой	Двухколонная интегрированная рамная RO установка предварительной очистки Yuchen Water предназначена для коммерческих и легких промышленных B2B проектов, где требуется очистка водопроводной или подземной воды. Система объединяет автоматическую песчаную колонну, автоматическую угольную колонну, фильтр тонкой очистки и обратный осмос на одной раме, обеспечивая 1000-3000 л/ч очищенной воды при входном давлении 0.1-0.4 MPa. Внешний вид, технологическая схема, комплектация и функции настраиваются по анализу воды и требованиям покупателя.	Интегрированная рамная RO система с автоматическими песчаной и угольной колоннами, тонкой фильтрацией и 1000-3000 л/ч очищенной воды для OEM проектов.	Автоматическая песчаная колонна + автоматическая угольная колонна + фильтр тонкой очистки + обратный осмос	Входное давление	Настройка под проект	Внешний вид, технологическая схема, комплектация оборудования, панель управления и защитные функции настраиваются по источнику воды и площади проекта	Отели, заводы, школы, жилые комплексы, коммерческие кухни и проекты водоочистки
sk	Integrované skidové RO zariadenie s dvojtankovou predúpravou 1000-3000 L/h	Skidový RO systém s dvojtankovou predúpravou	Integrované skidové RO zariadenie Yuchen Water s dvojtankovou predúpravou je určené pre komerčné a ľahké priemyselné B2B projekty, ktoré upravujú vodovodnú alebo podzemnú vodu. Systém spája automatickú pieskovú nádobu, automatickú uhlíkovú nádobu, jemný filter a reverznú osmózu na jednom ráme, s prietokom čistej vody 1000-3000 L/h a vstupným tlakom 0.1-0.4 MPa. Vzhľad, proces, konfigurácia a funkcie sa prispôsobujú analýze vody a požiadavkám kupujúceho.	Integrovaný skidový RO systém s automatickými pieskovými a uhlíkovými nádobami, jemnou filtráciou a 1000-3000 L/h čistej vody pre OEM projekty.	Automatická piesková nádoba + automatická uhlíková nádoba + jemný filter + reverzná osmóza	Vstupný tlak	Prispôsobenie projektu	Vzhľad, procesný tok, konfiguráciu zariadenia, ovládací panel a ochranné funkcie možno prispôsobiť zdrojovej vode a priestoru projektu	Hotely, továrne, školy, komunity, komerčné kuchyne a projekty úpravy vody
sl	Integrirana skid RO oprema z dvorezervoarsko predobdelavo 1000-3000 L/h	Skid RO sistem z dvorezervoarsko predobdelavo	Integrirana skid RO oprema Yuchen Water z dvorezervoarsko predobdelavo je namenjena komercialnim in lahkim industrijskim B2B projektom, ki čistijo vodovodno ali podtalno vodo. Sistem združuje avtomatski peščeni rezervoar, avtomatski ogljikov rezervoar, fini filter in reverzno osmozo na enem okvirju, s pretokom čiste vode 1000-3000 L/h in vstopnim tlakom 0.1-0.4 MPa. Videz, proces, konfiguracija in funkcije se prilagodijo analizi vode ter zahtevam kupca.	Integriran skid RO sistem z avtomatskim peščenim in ogljikovim rezervoarjem, fino filtracijo ter 1000-3000 L/h čiste vode za OEM projekte.	Avtomatski peščeni rezervoar + avtomatski ogljikov rezervoar + fini filter + reverzna osmoza	Vstopni tlak	Prilagoditev projektu	Videz, procesni tok, konfiguracijo opreme, krmilno ploščo in zaščitne funkcije je mogoče prilagoditi viru vode in prostoru projekta	Hoteli, tovarne, šole, skupnosti, komercialne kuhinje in projekti obdelave vode
sq	Pajisje RO e integruar në skid me paratrajtim me dy depozita 1000-3000 L/h	Sistem RO skid me paratrajtim me dy depozita	Pajisja RO e integruar në skid me paratrajtim me dy depozita nga Yuchen Water është projektuar për projekte B2B tregtare dhe industriale të lehta që pastrojnë ujë rrjeti ose ujë nëntokësor. Sistemi bashkon depozitë automatike rëre, depozitë automatike karboni, filtër preciz dhe osmozë të kundërt në një kornizë, me 1000-3000 L/h ujë të pastruar dhe presion hyrës 0.1-0.4 MPa. Pamja, rrjedha e procesit, konfigurimi dhe funksionet përshtaten sipas analizës së ujit dhe kërkesave të blerësit.	Sistem RO i integruar në skid me depozita automatike rëre dhe karboni, filtrimi preciz dhe 1000-3000 L/h ujë i pastruar për projekte OEM.	Depozitë automatike rëre + depozitë automatike karboni + filtër preciz + osmozë e kundërt	Presioni hyrës	Përshtatje projekti	Pamja, rrjedha e procesit, konfigurimi i pajisjes, paneli i kontrollit dhe funksionet mbrojtëse mund të përshtaten me burimin e ujit dhe hapësirën e projektit	Hotele, fabrika, shkolla, komunitete, kuzhina tregtare dhe projekte trajtimi uji
sr	Интегрисана skid RO опрема са двотанковским предтретманом 1000-3000 L/h	Skid RO систем са двотанковским предтретманом	Интегрисана skid RO опрема са двотанковским предтретманом компаније Yuchen Water намењена је комерцијалним и лаким индустријским B2B пројектима који пречишћавају водоводну или подземну воду. Систем обједињује аутоматски пешчани танк, аутоматски карбонски танк, прецизни филтер и реверзну осмозу на једном раму, са протоком чисте воде 1000-3000 L/h и улазним притиском 0.1-0.4 MPa. Изглед, процес, конфигурација и функције прилагођавају се анализи воде и захтевима купца.	Интегрисани skid RO систем са аутоматским пешчаним и карбонским танком, прецизном филтрацијом и 1000-3000 L/h чисте воде за OEM пројекте.	Аутоматски пешчани танк + аутоматски карбонски танк + прецизни филтер + реверзна осмоза	Улазни притисак	Прилагођавање пројекту	Изглед, ток процеса, конфигурација опреме, контролни панел и заштитне функције могу се прилагодити извору воде и простору пројекта	Хотели, фабрике, школе, насеља, комерцијалне кухиње и пројекти третмана воде
sr-me	Integrisana skid RO oprema sa dvotankovskim predtretmanom 1000-3000 L/h	Skid RO sistem sa dvotankovskim predtretmanom	Integrisana skid RO oprema sa dvotankovskim predtretmanom kompanije Yuchen Water namijenjena je komercijalnim i lakim industrijskim B2B projektima koji prečišćavaju vodovodnu ili podzemnu vodu. Sistem objedinjuje automatski pješčani tank, automatski karbonski tank, precizni filter i reverznu osmozu na jednom ramu, sa protokom čiste vode 1000-3000 L/h i ulaznim pritiskom 0.1-0.4 MPa. Izgled, proces, konfiguracija i funkcije prilagođavaju se analizi vode i zahtjevima kupca.	Integrisani skid RO sistem sa automatskim pješčanim i karbonskim tankom, preciznom filtracijom i 1000-3000 L/h čiste vode za OEM projekte.	Automatski pješčani tank + automatski karbonski tank + precizni filter + reverzna osmoza	Ulazni pritisak	Prilagođavanje projektu	Izgled, tok procesa, konfiguracija opreme, kontrolni panel i zaštitne funkcije mogu se prilagoditi izvoru vode i prostoru projekta	Hoteli, fabrike, škole, naselja, komercijalne kuhinje i projekti tretmana vode
sv	Integrerad skid-RO-utrustning med tvåtanks förbehandling 1000-3000 L/h	Skid-RO-system med tvåtanks förbehandling	Yuchen Water integrerad skid-RO-utrustning med tvåtanks förbehandling är framtagen för kommersiella och lätt industriella B2B-projekt som renar kranvatten eller grundvatten. Systemet förenar automatisk sandtank, automatisk koltank, finfilter och omvänd osmos på en ram, med 1000-3000 L/h renat vatten och 0.1-0.4 MPa inloppstryck. Utseende, processflöde, konfiguration och funktioner anpassas efter vattenanalys och köparens krav.	Integrerat skid-RO-system med automatiska sand- och koltankar, finfiltrering och 1000-3000 L/h renat vatten för OEM-projekt.	Automatisk sandtank + automatisk koltank + finfilter + omvänd osmos	Inloppstryck	Projektanpassning	Utseende, processflöde, utrustningskonfiguration, kontrollpanel och skyddsfunktioner kan anpassas efter källvatten och projektutrymme	Hotell, fabriker, skolor, bostadsområden, storkök och vattenbehandlingsprojekt
sw	Kifaa cha RO cha skid kilichounganishwa na matayarisho ya matenki mawili 1000-3000 L/h	Mfumo wa RO skid wenye matayarisho ya matenki mawili	Kifaa cha RO cha skid kilichounganishwa na matayarisho ya matenki mawili cha Yuchen Water kimetengenezwa kwa miradi ya B2B ya biashara na viwanda vyepesi inayosafisha maji ya bomba au maji ya ardhini. Mfumo unaunganisha tenki la mchanga la moja kwa moja, tenki la kaboni la moja kwa moja, kichujio sahihi na reverse osmosis kwenye fremu moja, ukitoa maji safi 1000-3000 L/h kwa shinikizo la kuingia 0.1-0.4 MPa. Mwonekano, mtiririko wa mchakato, usanidi na kazi zinaweza kubadilishwa kulingana na uchambuzi wa maji na mahitaji ya mnunuzi.	Mfumo wa RO skid uliounganishwa wenye matenki ya mchanga na kaboni ya moja kwa moja, uchujaji sahihi na 1000-3000 L/h maji safi kwa miradi ya OEM.	Tenki la mchanga la moja kwa moja + tenki la kaboni la moja kwa moja + kichujio sahihi + reverse osmosis	Shinikizo la kuingia	Ubinafsishaji wa mradi	Mwonekano, mtiririko wa mchakato, usanidi wa kifaa, paneli ya udhibiti na kazi za ulinzi zinaweza kubadilishwa kulingana na chanzo cha maji na nafasi ya mradi	Hoteli, viwanda, shule, jamii, majiko ya biashara na miradi ya kutibu maji
ta	இரண்டு தொட்டி முன்சிகிச்சையுடன் ஒருங்கிணைந்த skid RO உபகரணம் 1000-3000 L/h	இரண்டு தொட்டி முன்சிகிச்சை skid RO அமைப்பு	Yuchen Water இரண்டு தொட்டி முன்சிகிச்சையுடன் ஒருங்கிணைந்த skid RO உபகரணம் குழாய் நீர் அல்லது நிலத்தடி நீரை சுத்திகரிக்கும் வணிக மற்றும் இலகு தொழில்துறை B2B திட்டங்களுக்கு வடிவமைக்கப்பட்டது. இந்த அமைப்பு தானியங்கி மணல் தொட்டி, தானியங்கி கார்பன் தொட்டி, துல்லிய வடிகட்டி மற்றும் எதிர்மறை ஒஸ்மோசிஸை ஒரே சட்டத்தில் இணைத்து, 0.1-0.4 MPa நுழைவு அழுத்தத்தில் 1000-3000 L/h சுத்த நீரை வழங்குகிறது. தோற்றம், செயல்முறை ஓட்டம், அமைப்பு மற்றும் செயல்பாடுகள் நீர் பகுப்பாய்வு மற்றும் வாங்குபவர் தேவைக்கு ஏற்ப மாற்றப்படலாம்.	OEM திட்டங்களுக்கு தானியங்கி மணல் மற்றும் கார்பன் தொட்டிகள், துல்லிய வடிகட்டல் மற்றும் 1000-3000 L/h சுத்த நீர் வெளியீடு கொண்ட ஒருங்கிணைந்த skid RO அமைப்பு.	தானியங்கி மணல் தொட்டி + தானியங்கி கார்பன் தொட்டி + துல்லிய வடிகட்டி + எதிர்மறை ஒஸ்மோசிஸ்	நுழைவு அழுத்தம்	திட்ட தனிப்பயனாக்கம்	தோற்றம், செயல்முறை ஓட்டம், உபகரண அமைப்பு, கட்டுப்பாட்டு பலகை மற்றும் பாதுகாப்பு செயல்பாடுகள் மூலநீர் மற்றும் திட்ட இடத்திற்கு ஏற்ப மாற்றப்படலாம்	ஹோட்டல்கள், தொழிற்சாலைகள், பள்ளிகள், குடியிருப்பு வளாகங்கள், வணிக சமையலறைகள் மற்றும் நீர் சிகிச்சை திட்டங்கள்
tg	Таҷҳизоти skid RO-и ҳамгиро бо пештозакунии ду бак 1000-3000 L/h	Системаи skid RO бо пештозакунии ду бак	Таҷҳизоти skid RO-и ҳамгиро бо пештозакунии ду бак аз Yuchen Water барои лоиҳаҳои B2B тиҷоратӣ ва саноати сабук пешбинӣ шудааст, ки оби лӯла ё оби зеризаминиро тоза мекунанд. Система ба як чорчӯба баки қуми автоматӣ, баки карбони автоматӣ, филтри дақиқ ва осмоси баръаксро муттаҳид мекунад, бо фишори воридотӣ 0.1-0.4 MPa 1000-3000 L/h оби тозашуда медиҳад. Намуди зоҳирӣ, ҷараёни раванд, конфигуратсия ва функсияҳо мувофиқи таҳлили об ва талаботи харидор танзим мешаванд.	Системаи skid RO бо бакҳои қум ва карбони автоматӣ, филтратсияи дақиқ ва 1000-3000 L/h оби тоза барои лоиҳаҳои OEM.	Баки қуми автоматӣ + баки карбони автоматӣ + филтри дақиқ + осмоси баръакс	Фишори воридотӣ	Мутобиқсозии лоиҳа	Намуди зоҳирӣ, ҷараёни раванд, конфигуратсияи таҷҳизот, панели идоракунӣ ва функсияҳои муҳофизатӣ ба манбаи об ва фазои лоиҳа мутобиқ мешаванд	Меҳмонхонаҳо, корхонаҳо, мактабҳо, маҷмааҳо, ошхонаҳои тиҷоратӣ ва лоиҳаҳои тозакунии об
th	อุปกรณ์ RO สกิดรวมชุดพร้อมระบบปรับสภาพสองถัง 1000-3000 L/h	ระบบ RO สกิดพร้อมระบบปรับสภาพสองถัง	อุปกรณ์ RO สกิดรวมชุดพร้อมระบบปรับสภาพสองถังของ Yuchen Water ออกแบบสำหรับโครงการ B2B เชิงพาณิชย์และอุตสาหกรรมเบาที่ต้องการกรองน้ำประปาหรือน้ำบาดาล ระบบรวมถังกรองทรายอัตโนมัติ ถังคาร์บอนอัตโนมัติ ไส้กรองละเอียด และระบบรีเวิร์สออสโมซิสไว้บนโครงเดียว ให้ปริมาณน้ำบริสุทธิ์ 1000-3000 L/h ที่แรงดันน้ำเข้า 0.1-0.4 MPa รูปลักษณ์ กระบวนการ การจัดวาง และฟังก์ชันสามารถปรับตามผลวิเคราะห์น้ำและความต้องการของผู้ซื้อ	ระบบ RO สกิดรวมชุดพร้อมถังกรองทรายและถังคาร์บอนอัตโนมัติ การกรองละเอียด และน้ำบริสุทธิ์ 1000-3000 L/h สำหรับโครงการ OEM.	ถังกรองทรายอัตโนมัติ + ถังคาร์บอนอัตโนมัติ + ไส้กรองละเอียด + รีเวิร์สออสโมซิส	แรงดันน้ำเข้า	การปรับแต่งตามโครงการ	รูปลักษณ์ กระบวนการ การจัดวางอุปกรณ์ แผงควบคุม และฟังก์ชันป้องกันสามารถปรับตามแหล่งน้ำและพื้นที่โครงการ	โรงแรม โรงงาน โรงเรียน ชุมชน ครัวพาณิชย์ และโครงการบำบัดน้ำ
tk	Iki bakly öňünden arassalamaly integrirlenen skid RO enjamy 1000-3000 L/h	Iki bakly öňünden arassalama skid RO ulgamy	Yuchen Water iki bakly öňünden arassalamaly integrirlenen skid RO enjamy kran suwuny ýa-da ýerasty suwuny arassalaýan söwda we ýeňil senagat B2B taslamalary üçin niýetlenýär. Ulgam awtomatik çäge bakyny, awtomatik karbon bakyny, takyk filtri we ters osmosy bir rama birleşdirýär, 0.1-0.4 MPa giriş basyşynda 1000-3000 L/h arassalanan suw berýär. Daş görnüş, proses akymy, konfigurasiýa we funksiýalar suw derňewine we alyjynyň talaplaryna görä sazlanýar.	OEM taslamalary üçin awtomatik çäge we karbon baklary, takyk filtrasiýa we 1000-3000 L/h arassa suw berýän integrirlenen skid RO ulgamy.	Awtomatik çäge baky + awtomatik karbon baky + takyk filtr + ters osmos	Giriş basyşy	Taslama boýunça sazlama	Daş görnüş, proses akymy, enjam konfigurasiýasy, dolandyryş paneli we gorag funksiýalary suw çeşmesine we taslama giňişligine görä sazlanýar	Myhmanhanalar, zawodlar, mekdepler, ýaşaýyş toplumlary, söwda aşhanalary we suw arassalama taslamalary
tl	Pinagsamang skid RO kagamitan na may dalawang tangke ng pretreatment 1000-3000 L/h	Skid RO system na may dalawang tangke ng pretreatment	Ang pinagsamang skid RO kagamitan ng Yuchen Water na may dalawang tangke ng pretreatment ay ginawa para sa komersyal at magaan na industriyal na B2B proyekto na naglilinis ng tubig gripo o tubig bukal. Pinagsasama ng sistema ang awtomatikong tangke ng buhangin, awtomatikong tangke ng carbon, maselang filter at reverse osmosis sa isang frame, na nagbibigay ng 1000-3000 L/h malinis na tubig sa 0.1-0.4 MPa presyon ng pasok. Ang hitsura, proseso, pagsasaayos at mga function ay maaaring iayon sa pagsusuri ng tubig at pangangailangan ng mamimili.	Pinagsamang skid RO system na may awtomatikong tangke ng buhangin at carbon, maselang pagsala at 1000-3000 L/h malinis na tubig para sa mga proyektong OEM.	Awtomatikong tangke ng buhangin + awtomatikong tangke ng carbon + maselang filter + reverse osmosis	Presyon ng pasok	Pag-angkop sa proyekto	Ang hitsura, daloy ng proseso, pagsasaayos ng kagamitan, control panel at proteksiyon ay maaaring iayon sa pinagmumulan ng tubig at lugar ng proyekto	Mga hotel, pabrika, paaralan, komunidad, komersyal na kusina at proyekto sa paggamot ng tubig
tr	İki tank ön arıtmalı entegre skid RO ekipmanı 1000-3000 L/saat	İki tank ön arıtmalı skid RO sistemi	Yuchen Water iki tank ön arıtmalı entegre skid RO ekipmanı; şebeke suyu veya yeraltı suyunu arıtan ticari ve hafif endüstriyel B2B projeleri için tasarlanır. Sistem otomatik kum tankı, otomatik karbon tankı, hassas filtre ve ters ozmoz ünitesini tek şasede birleştirir; 0.1-0.4 MPa giriş basıncıyla 1000-3000 L/saat arıtılmış su sağlar. Görünüm, proses akışı, konfigürasyon ve fonksiyonlar su analizine ve alıcı gereksinimlerine göre özelleştirilebilir.	OEM projeleri için otomatik kum ve karbon tankları, hassas filtrasyon ve 1000-3000 L/saat arıtılmış su çıkışına sahip entegre skid RO sistemi.	Otomatik kum tankı + otomatik karbon tankı + hassas filtre + ters ozmoz	Giriş basıncı	Proje özelleştirmesi	Görünüm, proses akışı, ekipman konfigürasyonu, kontrol paneli ve koruma fonksiyonları kaynak suya ve proje alanına göre özelleştirilebilir	Oteller, fabrikalar, okullar, siteler, ticari mutfaklar ve su arıtma projeleri
uk	Інтегрована skid RO установка з двобаковою попередньою підготовкою 1000-3000 L/h	Skid RO система з двобаковою попередньою підготовкою	Інтегрована skid RO установка Yuchen Water з двобаковою попередньою підготовкою призначена для комерційних і легких промислових B2B проєктів, що очищають водопровідну або підземну воду. Система поєднує автоматичний піщаний бак, автоматичний вугільний бак, фільтр тонкого очищення і зворотний осмос на одній рамі, забезпечуючи 1000-3000 L/h очищеної води при вхідному тиску 0.1-0.4 MPa. Зовнішній вигляд, процес, конфігурація і функції налаштовуються за аналізом води та вимогами покупця.	Інтегрована skid RO система з автоматичними піщаним і вугільним баками, тонкою фільтрацією та 1000-3000 L/h очищеної води для OEM проєктів.	Автоматичний піщаний бак + автоматичний вугільний бак + фільтр тонкого очищення + зворотний осмос	Вхідний тиск	Налаштування проєкту	Зовнішній вигляд, процесний потік, конфігурацію обладнання, панель керування і захисні функції можна адаптувати до джерела води та простору проєкту	Готелі, заводи, школи, житлові комплекси, комерційні кухні та проєкти очищення води
ur	دو ٹینک پری ٹریٹمنٹ انٹیگریٹڈ اسکیڈ RO سامان 1000-3000 L/h	دو ٹینک پری ٹریٹمنٹ اسکیڈ RO سسٹم	Yuchen Water کا دو ٹینک پری ٹریٹمنٹ انٹیگریٹڈ اسکیڈ RO سامان تجارتی اور ہلکی صنعتی B2B منصوبوں کے لیے ہے جہاں نل کا پانی یا زیر زمین پانی صاف کیا جاتا ہے۔ یہ سسٹم ایک ہی فریم پر خودکار ریت ٹینک، خودکار کاربن ٹینک، پریسیژن فلٹر اور ریورس اوسموسس یونٹ کو جوڑتا ہے، 0.1-0.4 MPa داخلہ دباؤ پر 1000-3000 L/h صاف پانی فراہم کرتا ہے۔ شکل، عمل کا بہاؤ، ترتیب اور افعال پانی کے تجزیے اور خریدار کی ضرورت کے مطابق حسب ضرورت بن سکتے ہیں۔	OEM منصوبوں کے لیے خودکار ریت اور کاربن ٹینک، پریسیژن فلٹریشن اور 1000-3000 L/h صاف پانی والا انٹیگریٹڈ اسکیڈ RO سسٹم۔	خودکار ریت ٹینک + خودکار کاربن ٹینک + پریسیژن فلٹر + ریورس اوسموسس	داخلہ دباؤ	منصوبہ حسب ضرورت	شکل، عمل کا بہاؤ، سامان کی ترتیب، کنٹرول پینل اور حفاظتی افعال پانی کے منبع اور منصوبے کی جگہ کے مطابق بنائے جا سکتے ہیں	ہوٹل، فیکٹریاں، اسکول، کمیونٹیز، تجارتی کچن اور پانی صاف کرنے کے منصوبے
uz	Ikki bakli oldindan tozalashga ega integratsiyalangan skid RO uskunasi 1000-3000 L/soat	Ikki bakli oldindan tozalash skid RO tizimi	Yuchen Water ikki bakli oldindan tozalashga ega integratsiyalangan skid RO uskunasi vodoprovod yoki yerosti suvini tozalaydigan tijorat va yengil sanoat B2B loyihalari uchun ishlab chiqilgan. Tizim bitta ramada avtomatik qum baki, avtomatik ko‘mir baki, nozik filtr va teskari osmos blokini birlashtiradi, 0.1-0.4 MPa kirish bosimida 1000-3000 L/soat tozalangan suv beradi. Tashqi ko‘rinish, jarayon oqimi, konfiguratsiya va funksiyalar suv tahlili hamda xaridor talabiga ko‘ra moslashtiriladi.	OEM loyihalari uchun avtomatik qum va ko‘mir baklari, nozik filtrlash va 1000-3000 L/soat tozalangan suv chiqishiga ega integratsiyalangan skid RO tizimi.	Avtomatik qum baki + avtomatik ko‘mir baki + nozik filtr + teskari osmos	Kirish bosimi	Loyiha bo‘yicha moslashtirish	Tashqi ko‘rinish, jarayon oqimi, uskuna konfiguratsiyasi, boshqaruv paneli va himoya funksiyalari suv manbai va loyiha maydoniga ko‘ra moslashtiriladi	Mehmonxonalar, zavodlar, maktablar, turar joy majmualari, tijorat oshxonalari va suv tozalash loyihalari
vi	Thiết bị RO skid tích hợp tiền xử lý hai bồn 1000-3000 L/giờ	Hệ thống RO skid tiền xử lý hai bồn	Thiết bị RO skid tích hợp tiền xử lý hai bồn của Yuchen Water được thiết kế cho dự án B2B thương mại và công nghiệp nhẹ xử lý nước máy hoặc nước ngầm. Hệ thống kết hợp bồn cát tự động, bồn than hoạt tính tự động, bộ lọc tinh và thẩm thấu ngược trên một khung, tạo nước tinh khiết 1000-3000 L/giờ với áp lực nước vào 0.1-0.4 MPa. Ngoại hình, quy trình, cấu hình và chức năng có thể tùy chỉnh theo phân tích nước nguồn và yêu cầu của người mua.	Hệ thống RO skid tích hợp với bồn cát và bồn than tự động, lọc tinh và lưu lượng nước tinh khiết 1000-3000 L/giờ cho dự án OEM.	Bồn cát tự động + bồn than hoạt tính tự động + bộ lọc tinh + thẩm thấu ngược	Áp lực nước vào	Tùy chỉnh theo dự án	Ngoại hình, dòng quy trình, cấu hình thiết bị, tủ điều khiển và chức năng bảo vệ có thể điều chỉnh theo nước nguồn và không gian dự án	Khách sạn, nhà máy, trường học, khu dân cư, bếp thương mại và dự án xử lý nước
zu	Imishini ye-skid RO ehlanganisiwe ene-pretreatment yamathangi amabili 1000-3000 L/h	Uhlelo lwe-skid RO olunamathangi amabili e-pretreatment	Imishini ye-skid RO ehlanganisiwe ka Yuchen Water ene-pretreatment yamathangi amabili yakhelwe amaphrojekthi e-B2B ezohwebo nezimboni ezincane ahlanza amanzi ompompi noma angaphansi komhlaba. Uhlelo luhlanganisa ithangi lesihlabathi elizenzakalelayo, ithangi lekhabhoni elizenzakalelayo, isihlungi esinembile kanye ne-reverse osmosis kuhlaka olulodwa, lunikeza 1000-3000 L/h amanzi ahlanzekile ngo-0.1-0.4 MPa ingcindezi yokungena. Ukubukeka, ukugeleza kwenqubo, ukucushwa nemisebenzi kulungiswa ngokuhlaziywa kwamanzi nezidingo zomthengi.	Uhlelo lwe-skid RO oluhlanganisiwe olunamathangi esihlabathi nekhabhoni azenzakalelayo, ukuhlunga okunembile kanye no-1000-3000 L/h wamanzi ahlanzekile kumaphrojekthi e-OEM.	Ithangi lesihlabathi elizenzakalelayo + ithangi lekhabhoni elizenzakalelayo + isihlungi esinembile + reverse osmosis	Ingcindezi yokungena	Ukwenza ngokwezifiso iphrojekthi	Ukubukeka, ukugeleza kwenqubo, ukucushwa kwemishini, iphaneli yokulawula nemisebenzi yokuvikela kungalungiswa ngokomthombo wamanzi nendawo yephrojekthi	Amahhotela, amafekthri, izikole, imiphakathi, amakhishi ezohwebo namaphrojekthi okwelapha amanzi
""".strip()


def esc(value: str) -> str:
    return html.escape(value, quote=True)


TEXT_FIXES: dict[str, list[tuple[str, str]]] = {
    "az": [("skid RO", "karkaslı RO"), ("skid", "karkaslı")],
    "bs": [("Skid RO", "Ramni RO"), ("skid RO", "ramni RO"), ("skid", "ramni")],
    "cs": [("Skidový", "Rámový"), ("skidové", "rámové"), ("skidový", "rámový")],
    "da": [("Skid-RO", "Ramme-RO"), ("skid-RO", "ramme-RO")],
    "de": [("Skid-RO", "Rahmen-RO")],
    "el": [("RO skid", "RO σε πλαίσιο"), ("skid", "πλαίσιο")],
    "et": [("skid-RO", "raam-RO")],
    "fi": [("skid-RO", "runko-RO")],
    "ha": [("RO ta skid", "RO a kan firam"), ("RO na skid", "RO na firam"), ("reverse osmosis", "osmosis na baya")],
    "hr": [("Skid RO", "Okvirni RO"), ("skid RO", "okvirni RO"), ("skid", "okvirni")],
    "hu": [("skid RO", "keretes RO"), ("skid", "keretes")],
    "hy": [("skid RO", "շրջանակային RO"), ("skid", "շրջանակային")],
    "id": [("RO skid", "RO rangka"), ("reverse osmosis", "osmosis balik")],
    "it": [("RO integrato su skid", "RO integrato su telaio"), ("RO su skid", "RO su telaio"), ("skid", "telaio")],
    "ja": [("スキッドRO", "架台一体型RO"), ("スキッド", "架台一体型"), ("一体型架台一体型", "架台一体型")],
    "ka": [("skid RO", "ჩარჩოიანი RO"), ("skid", "ჩარჩოიანი")],
    "kk": [("skid RO", "рамалы RO"), ("skid", "рамалы")],
    "ku": [("skidê", "çarçoveyê")],
    "ky": [("skid RO", "рамалуу RO"), ("skid", "рамалуу")],
    "lt": [("Skid RO", "Rėminė RO"), ("skid RO", "rėminė RO"), ("skid", "rėminė")],
    "lv": [("Skid RO", "Rāmja RO"), ("skid RO", "rāmja RO"), ("skid", "rāmja")],
    "ms": [("RO skid", "RO berkerangka"), ("skid", "berkerangka")],
    "nl": [("Skid-RO", "Frame-RO"), ("skid-RO", "frame-RO")],
    "no": [("Skid-RO", "Ramme-RO"), ("skid-RO", "ramme-RO")],
    "pl": [("Skid RO", "Ramowa RO"), ("skid RO", "ramowa RO"), ("skid", "ramowa")],
    "pt": [("RO em skid", "RO em bastidor"), ("skid", "bastidor")],
    "ro": [("RO pe skid", "RO pe cadru"), ("skid", "cadru")],
    "sk": [("Skidový", "Rámový"), ("skidové", "rámové"), ("skidový", "rámový")],
    "sl": [("Skid RO", "Okvirni RO"), ("skid RO", "okvirni RO"), ("skid", "okvirni")],
    "sq": [("RO skid", "RO me kornizë"), ("skid", "kornizë")],
    "sr": [("Skid RO", "Рамски RO"), ("skid RO", "рамски RO"), ("skid", "рамски")],
    "sr-me": [("Skid RO", "Ramni RO"), ("skid RO", "ramni RO"), ("skid", "ramni")],
    "sv": [("Skid-RO", "Ram-RO"), ("skid-RO", "ram-RO")],
    "sw": [("RO skid", "RO ya fremu"), ("skid", "fremu"), ("reverse osmosis", "osmosisi ya kinyume")],
    "ta": [("skid RO", "சட்டக RO"), ("skid", "சட்டக")],
    "tg": [("skid RO", "RO-и чорчӯбадор"), ("skid", "чорчӯбадор")],
    "tk": [("skid RO", "ramaly RO"), ("skid", "ramaly")],
    "tl": [("Skid RO", "Nakabalangkas na RO"), ("skid RO", "nakabalangkas na RO"), ("skid", "nakabalangkas"), ("reverse osmosis", "baliktad na osmosis"), ("Feed water", "Tubig na pinapasok"), ("control panel", "panel ng kontrol"), ("mga function", "mga tungkulin"), ("packaging", "pag-iimpake")],
    "tr": [("skid RO", "şasili RO"), ("skid", "şasili")],
    "uk": [("Skid RO", "Рамна RO"), ("skid RO", "рамна RO"), ("skid", "рамна")],
    "uz": [("skid RO", "ramali RO"), ("skid", "ramali")],
    "vi": [("RO skid", "RO khung tích hợp"), ("skid", "khung tích hợp"), ("RO khung tích hợp tích hợp", "RO khung tích hợp"), ("khung tích hợp tích hợp", "khung tích hợp")],
    "zu": [("ye-skid", "yohlaka"), ("lwe-skid", "lohlaka"), ("skid", "uhlaka"), ("reverse osmosis", "i-osmosis ephambene")],
}

FAQ_LABELS = {
    "af": "Gereelde vrae", "ar": "الأسئلة الشائعة", "az": "Tez-tez verilən suallar",
    "bg": "Често задавани въпроси", "bn": "সাধারণ প্রশ্ন", "bs": "Česta pitanja",
    "cs": "Časté otázky", "da": "Ofte stillede spørgsmål", "de": "Häufige Fragen",
    "el": "Συχνές ερωτήσεις", "en": "FAQ", "es": "Preguntas frecuentes",
    "et": "Korduma kippuvad küsimused", "fa": "پرسش‌های متداول", "fi": "Usein kysytyt kysymykset",
    "fr": "Questions fréquentes", "ha": "Tambayoyi akai-akai", "he": "שאלות נפוצות",
    "hi": "अक्सर पूछे जाने वाले प्रश्न", "hr": "Česta pitanja", "hu": "Gyakori kérdések",
    "hy": "Հաճախ տրվող հարցեր", "id": "Pertanyaan umum", "it": "Domande frequenti",
    "ja": "よくある質問", "ka": "ხშირად დასმული კითხვები", "kk": "Жиі қойылатын сұрақтар",
    "ko": "자주 묻는 질문", "ku": "Pirsên pir tên kirin", "ky": "Көп берилүүчү суроолор",
    "lt": "Dažniausi klausimai", "lv": "Biežāk uzdotie jautājumi", "ms": "Soalan lazim",
    "nl": "Veelgestelde vragen", "no": "Vanlige spørsmål", "pl": "Częste pytania",
    "pt": "Perguntas frequentes", "ro": "Întrebări frecvente", "ru": "Частые вопросы",
    "sk": "Časté otázky", "sl": "Pogosta vprašanja", "sq": "Pyetje të shpeshta",
    "sr": "Честа питања", "sr-me": "Česta pitanja", "sv": "Vanliga frågor",
    "sw": "Maswali ya kawaida", "ta": "அடிக்கடி கேட்கப்படும் கேள்விகள்",
    "tg": "Саволҳои маъмул", "th": "คำถามที่พบบ่อย", "tk": "Ýygy berilýän soraglar",
    "tl": "Madalas itanong", "tr": "Sık sorulan sorular", "uk": "Часті запитання",
    "ur": "عام سوالات", "uz": "Ko‘p so‘raladigan savollar", "vi": "Câu hỏi thường gặp",
    "zu": "Imibuzo evame ukubuzwa",
}

TABLE_HEADS = {
    "af": ("Parameter", "Spesifikasie"), "ar": ("البند", "المواصفة"), "az": ("Bənd", "Göstərici"),
    "bg": ("Параметър", "Спецификация"), "bn": ("বিষয়", "বিবরণ"), "bs": ("Stavka", "Specifikacija"),
    "cs": ("Položka", "Specifikace"), "da": ("Punkt", "Specifikation"), "de": ("Punkt", "Spezifikation"),
    "el": ("Στοιχείο", "Προδιαγραφή"), "en": ("Item", "Specification"), "es": ("Parámetro", "Especificación"),
    "et": ("Üksus", "Spetsifikatsioon"), "fa": ("مورد", "مشخصات"), "fi": ("Kohta", "Erittely"),
    "fr": ("Élément", "Spécification"), "ha": ("Abu", "Bayani"), "he": ("פריט", "מפרט"),
    "hi": ("मद", "विनिर्देश"), "hr": ("Stavka", "Specifikacija"), "hu": ("Tétel", "Specifikáció"),
    "hy": ("Կետ", "Բնութագիր"), "id": ("Parameter", "Spesifikasi"), "it": ("Voce", "Specifica"),
    "ja": ("項目", "仕様"), "ka": ("პუნქტი", "სპეციფიკაცია"), "kk": ("Параметр", "Сипаттама"),
    "ko": ("항목", "사양"), "ku": ("Xal", "Taybetmendî"), "ky": ("Параметр", "Спецификация"),
    "lt": ("Pozicija", "Specifikacija"), "lv": ("Pozīcija", "Specifikācija"), "ms": ("Perkara", "Spesifikasi"),
    "nl": ("Onderdeel", "Specificatie"), "no": ("Punkt", "Spesifikasjon"), "pl": ("Pozycja", "Specyfikacja"),
    "pt": ("Parâmetro", "Especificação"), "ro": ("Element", "Specificație"), "ru": ("Параметр", "Спецификация"),
    "sk": ("Položka", "Špecifikácia"), "sl": ("Postavka", "Specifikacija"), "sq": ("Artikull", "Specifikim"),
    "sr": ("Ставка", "Спецификација"), "sr-me": ("Stavka", "Specifikacija"), "sv": ("Post", "Specifikation"),
    "sw": ("Kipengee", "Maelezo"), "ta": ("உருப்படி", "விவரம்"), "tg": ("Банд", "Спецификатсия"),
    "th": ("รายการ", "ข้อมูลจำเพาะ"), "tk": ("Bölüm", "Spesifikasiýa"), "tl": ("Bahagi", "Detalye"),
    "tr": ("Kalem", "Özellik"), "uk": ("Параметр", "Специфікація"), "ur": ("مد", "وضاحت"),
    "uz": ("Band", "Spetsifikatsiya"), "vi": ("Hạng mục", "Thông số"), "zu": ("Into", "Imininingwane"),
}

LABEL_OVERRIDES = {
    "tl": {4: "Tubig na pinapasok"},
}

VALUE_OVERRIDES = {
    "tl": {
        1: "Ganap na awtomatikong matalinong pagpapatakbo, may manwal na serbisyo ayon sa pangangailangan ng proyekto",
        4: "Tubig sa gripo at tubig sa ilalim ng lupa",
        8: "Maaaring iangkop ang daloy, bomba, lamad, mga tangke, materyal ng tubo, boltahe, wika ng panel at pag-iimpake",
        9: "Kinukumpirma ayon sa kapasidad, pagsasaayos at antas ng OEM",
    },
}


def load_terms() -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for line in TERMS_ROWS.splitlines():
        parts = line.split("\t")
        if len(parts) != 10:
            raise ValueError(f"Bad terms row for {parts[0] if parts else 'unknown'}: {len(parts)} fields")
        lang, name, category, intro, card, treatment, pressure_label, custom_label, custom_value, app_value = parts
        for old, new in TEXT_FIXES.get(lang, []):
            name = name.replace(old, new)
            category = category.replace(old, new)
            intro = intro.replace(old, new)
            card = card.replace(old, new)
            treatment = treatment.replace(old, new)
            pressure_label = pressure_label.replace(old, new)
            custom_label = custom_label.replace(old, new)
            custom_value = custom_value.replace(old, new)
            app_value = app_value.replace(old, new)
        rows[lang] = {
            "name": name,
            "category": category,
            "intro": intro,
            "card": card,
            "treatment": treatment,
            "pressure_label": pressure_label,
            "custom_label": custom_label,
            "custom_value": custom_value,
            "app_value": app_value,
        }
    return rows


TERMS = load_terms()


def dirs() -> list[str]:
    return sorted(p.name for p in ROOT.iterdir() if p.is_dir() and (p / "index.html").exists())


def ui_for(lang: str) -> dict[str, str]:
    ui = BASE_UI_FOR(lang)
    item, spec = TABLE_HEADS.get(lang, (ui.get("item", "Item"), ui.get("spec", "Specification")))
    return {
        "home": ui.get("home", "Home"),
        "products": ui.get("products", "Products"),
        "specs": ui.get("specs", "Technical Specifications"),
        "process": ui.get("process", ui.get("options", "System Configuration")),
        "faq": FAQ_LABELS.get(lang, ui.get("faq", "FAQ")),
        "related": ui.get("related", "Related Products"),
        "request": ui.get("request", "Request OEM Quote"),
        "whatsapp": ui.get("whatsapp", "WhatsApp"),
        "send": ui.get("send", "Send Inquiry"),
        "item": item,
        "spec": spec,
    }


def copy_for(lang: str) -> dict:
    if lang not in TERMS:
        raise KeyError(f"No translation terms for {lang}")
    base = BASE_DATA[lang]
    t = TERMS[lang].copy()
    labels = [
        base["labels"][0],
        base["labels"][1],
        base["labels"][2],
        base["labels"][3],
        base["labels"][4],
        t["pressure_label"],
        t["custom_label"],
        base["labels"][8],
        base["labels"][9],
        base["labels"][10],
    ]
    for index, value in LABEL_OVERRIDES.get(lang, {}).items():
        labels[index] = value
    values = [
        t["name"],
        base["values"][1],
        t["treatment"],
        "1000-3000 L/h",
        base["values"][4],
        "0.1-0.4 MPa",
        t["custom_value"],
        t["app_value"],
        base["values"][9],
        base["values"][10],
    ]
    for index, value in VALUE_OVERRIDES.get(lang, {}).items():
        values[index] = value
    c = {
        **t,
        **ui_for(lang),
        "labels": labels,
        "values": values,
    }
    c["title"] = f"{c['name']} | Yuchen Water"
    c["meta"] = re.sub(r"\s+", " ", c["intro"]).strip()
    if len(c["meta"]) > 260:
        c["meta"] = c["meta"][:257].rsplit(" ", 1)[0] + "..."
    c["quote"] = f"{c['request']}: {c['name']}"
    c["quote_desc"] = c["intro"]
    c["faq_pairs"] = [
        (f"{labels[2]}?", values[2]),
        (f"{labels[3]}?", values[3]),
        (f"{labels[5]}?", values[5]),
        (f"{labels[6]}?", values[6]),
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
    if lang == "en":
        commercial_titles = COMMERCIAL_RELATED.get(lang, {})
        commercial_title = commercial_titles.get(
            "product-20-inch-commercial-ro-water-purifier-800g-2000g.html",
            c["category"],
        )
        related = [
            ("product-large-industrial-reverse-osmosis-water-treatment-equipment.html", BASE_DATA[lang]["name"], "large-industrial-reverse-osmosis-water-treatment-equipment-3-100tph-oem.webp", c["category"]),
            ("product-small-medium-seawater-desalination-ro-equipment.html", SMALL_DATA[lang]["name"], "small-medium-seawater-desalination-ro-equipment-60l-10000l-oem.webp", c["category"]),
            ("product-20-inch-commercial-ro-water-purifier-800g-2000g.html", commercial_title, "20-inch-commercial-ro-water-purifier-800g-2000g-front-full-frame-oem.webp", c["category"]),
        ]
    else:
        related = [
            ("product-large-industrial-reverse-osmosis-water-treatment-equipment.html", c["category"], "large-industrial-reverse-osmosis-water-treatment-equipment-3-100tph-oem.webp", c["category"]),
            ("product-small-medium-seawater-desalination-ro-equipment.html", c["category"], "small-medium-seawater-desalination-ro-equipment-60l-10000l-oem.webp", c["category"]),
            ("product-20-inch-commercial-ro-water-purifier-800g-2000g.html", c["category"], "20-inch-commercial-ro-water-purifier-800g-2000g-front-full-frame-oem.webp", c["category"]),
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
    inquiry_text = "Inquiry%20about%20Dual%20Tank%20Pretreatment%20Integrated%20Skid%20RO%20Equipment"
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
      <div class="product-actions"><a href="contact.html" class="btn btn-gold">{esc(c["request"])}</a><a href="https://wa.me/8619908311885?text={inquiry_text}" class="btn" target="_blank" rel="noopener">{esc(c["whatsapp"])}</a></div>
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
      <tr><th>{esc(c["labels"][2])}</th><td>{esc(c["values"][2])}</td></tr>
      <tr><th>{esc(c["labels"][4])}</th><td>{esc(c["values"][4])}</td></tr>
      <tr><th>{esc(c["labels"][5])}</th><td>{esc(c["values"][5])}</td></tr>
      <tr><th>{esc(c["labels"][6])}</th><td>{esc(c["values"][6])}</td></tr>
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
    <div class="hero-actions"><a href="contact.html" class="btn btn-gold">{esc(c["request"])}</a><a href="https://wa.me/8619908311885?text={inquiry_text}" class="btn" target="_blank" rel="noopener">{esc(c["whatsapp"])}</a></div>
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
    match = None
    for anchor in [
        AFTER_SLUG,
        "product-small-medium-seawater-desalination-ro-equipment.html",
        "product-ro-seawater-desalination-machine.html",
    ]:
        match = re.search(r'(<article class="[^"]*\bproduct-card\b[^"]*"[^>]*>.*?' + re.escape(anchor) + r'.*?</article>\s*)', text, flags=re.S)
        if match:
            break
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
    c = copy_for("en")
    insert_at = next((i + 1 for i, item in enumerate(products) if item.get("id") == "large-industrial-reverse-osmosis-water-treatment-equipment"), 4)
    products.insert(insert_at, {
        "id": PRODUCT_ID,
        "name": c["name"],
        "category": "RO System",
        "desc": c["card"],
        "specs": dict(zip(c["labels"], c["values"])),
        "image": f"../assets/products/{MAIN_IMAGE}",
        "image_local": f"assets/products/{MAIN_IMAGE}",
        "image_orig": f"../assets/products/{MAIN_IMAGE}",
        "summary": c["intro"],
        "features": ["Automatic sand tank and carbon tank", "Precision filter plus RO purification", "1000-3000 L/h purified water flow", "0.1-0.4 MPa feed pressure", "Customized frame, process and control functions"],
        "applications": "Hotels, factories, schools, communities, commercial kitchens and water treatment projects.",
        "related": ["large-industrial-reverse-osmosis-water-treatment-equipment", "ro-seawater-desalination-machine", "20-inch-commercial-ro-water-purifier-800g-2000g"],
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
    line = f"- Dual-Tank Pretreatment Integrated Skid RO Equipment: https://www.yuchensy.com/en/{NEW_SLUG}\n"
    for name in ["llms.txt", "llms-full.txt"]:
        path = ROOT / name
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if NEW_SLUG not in text:
                path.write_text(text.rstrip() + "\n" + line, encoding="utf-8")


def main() -> None:
    languages = dirs()
    missing = [lang for lang in languages if lang not in TERMS]
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
