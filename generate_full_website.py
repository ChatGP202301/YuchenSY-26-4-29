#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Express Water - Complete Website Generator
生成包含所有产品图片和详细描述的完整网站
"""

import os
import json

# 完整的22个产品数据库
PRODUCTS = [
    {
        "id": "product-01",
        "slug": "pp-sediment-filter-5-micron",
        "name_en": "PP Sediment Filter 5 Micron",
        "image": "product-01-pp-sediment-filter.jpg",
        "description_en": "Premium polypropylene sediment filter cartridge designed for effective removal of sand, rust, silt, and suspended particles from water. NSF certified for residential and commercial applications.",
        "specs": {
            "Micron Rating": "5 Micron",
            "Flow Rate": "30 GPM",
            "Dimensions": "10\" x 4.5\"",
            "Material": "100% Pure Polypropylene",
            "Certification": "NSF/ANSI 42",
            "Life Span": "6-12 months",
            "Max Temperature": "125°F (52°C)",
            "Max Pressure": "100 PSI"
        },
        "features": [
            "Removes 99% of particles down to 5 microns",
            "Gradient density design for maximum dirt-holding capacity",
            "No chemical additives or binders",
            "Compatible with standard 10\" housing",
            "Ideal for municipal and well water",
            "Food-grade certified materials"
        ],
        "applications": ["Whole house filtration", "Pre-filtration for RO systems", "Well water treatment", "Municipal water purification"]
    },
    {
        "id": "product-02",
        "slug": "udf-granular-activated-carbon",
        "name_en": "UDF Granular Activated Carbon Filter",
        "image": "product-02-udf-carbon-filter.jpg",
        "description_en": "High-capacity granular activated carbon filter using premium coconut shell carbon. Effectively removes chlorine, taste, odor, and organic chemicals from water supplies.",
        "specs": {
            "Carbon Type": "Coconut Shell GAC",
            "Flow Rate": "2.5 GPM",
            "Dimensions": "10\" x 2.75\"",
            "Iodine Value": "≥1000 mg/g",
            "Certification": "NSF/ANSI 42 & 61",
            "Chlorine Reduction": ">97%",
            "Capacity": "10,000 gallons",
            "Operating Pressure": "25-80 PSI"
        },
        "features": [
            "Premium coconut shell activated carbon",
            "Superior chlorine and taste/odor removal",
            "High dirt-holding capacity",
            "Consistent flow rates throughout cartridge life",
            "Reduces volatile organic compounds (VOCs)",
            "Food and pharmaceutical grade materials"
        ],
        "applications": ["Drinking water systems", "Ice makers", "Coffee machines", "Food service", "RO pre-filtration"]
    },
    {
        "id": "product-03",
        "slug": "cto-carbon-block-filter",
        "name_en": "CTO Compressed Carbon Block Filter",
        "image": "product-03-cto-carbon-block.jpg",
        "description_en": "Premium compressed activated carbon block filter providing superior chemical and taste removal. Advanced manufacturing process ensures consistent pore structure and maximum surface area.",
        "specs": {
            "Carbon Type": "Activated Carbon Block",
            "Flow Rate": "0.75 GPM",
            "Dimensions": "10\" x 2.5\"",
            "Micron Rating": "0.5-10 micron",
            "Certification": "NSF 42, 53, 61",
            "Chlorine Capacity": "20,000 gallons",
            "Lead Reduction": ">99.3%",
            "Cyst Reduction": ">99.95%"
        },
        "features": [
            "Compressed carbon block technology",
            "Reduces chlorine, lead, cysts, VOCs",
            "Excellent taste and odor improvement",
            "High efficiency particulate removal",
            "Minimal pressure drop",
            "FDA compliant materials"
        ],
        "applications": ["Under-sink filters", "Point-of-use systems", "Refrigerator water filters", "RO systems"]
    },
    {
        "id": "product-04",
        "slug": "large-cto-carbon-rod",
        "name_en": "Large CTO Carbon Rod Filter",
        "image": "product-04-large-cto-filter.jpg",
        "description_en": "Industrial-grade large diameter carbon block filter designed for high flow commercial applications. Extended cartridge life and superior contaminant removal.",
        "specs": {
            "Carbon Type": "Extruded Carbon Block",
            "Flow Rate": "5 GPM",
            "Dimensions": "20\" x 4.5\"",
            "Micron Rating": "5 micron",
            "Certification": "NSF 42 & 53",
            "Service Life": "12-18 months",
            "Chlorine Capacity": "40,000 gallons",
            "Temperature Range": "40-100°F"
        },
        "features": [
            "Large diameter for commercial use",
            "Extended service life",
            "High flow rate capacity",
            "Superior chemical reduction",
            "Minimal pressure drop design",
            "Heavy-duty construction"
        ],
        "applications": ["Commercial water systems", "Restaurant equipment", "Industrial process water", "Large buildings"]
    },
    {
        "id": "product-05",
        "slug": "composite-multi-layer",
        "name_en": "PCP Composite Multi-Layer Filter",
        "image": "product-05-composite-filter.jpg",
        "description_en": "Advanced multi-layer composite filter combining PP sediment filtration with activated carbon for comprehensive water treatment in a single cartridge.",
        "specs": {
            "Layers": "PP + Carbon + PP",
            "Flow Rate": "2.5 GPM",
            "Dimensions": "10\" x 2.75\"",
            "Micron Rating": "5 micron",
            "Carbon Type": "Coconut Shell GAC",
            "Total Capacity": "8,000 gallons",
            "Certification": "NSF 42",
            "Pressure Drop": "<5 PSI"
        },
        "features": [
            "3-stage filtration in one cartridge",
            "Sediment + chemical removal",
            "Space-saving design",
            "Cost-effective solution",
            "Easy installation and replacement",
            "Consistent performance"
        ],
        "applications": ["Residential POE systems", "Small commercial units", "RV water systems", "Vacation homes"]
    },
    {
        "id": "product-06",
        "slug": "coconut-shell-cto",
        "name_en": "Premium Coconut Shell CTO Filter",
        "image": "product-06-coconut-cto-filter.jpg",
        "description_en": "Ultra-premium carbon block filter manufactured exclusively from coconut shell activated carbon. Highest iodine value and superior chemical adsorption properties.",
        "specs": {
            "Carbon Source": "100% Coconut Shell",
            "Flow Rate": "1 GPM",
            "Dimensions": "10\" x 2.5\"",
            "Iodine Value": "≥1200 mg/g",
            "Micron Rating": "0.5 micron",
            "Chlorine Capacity": "25,000 gallons",
            "VOC Reduction": ">95%",
            "Certification": "NSF 42, 53, 401"
        },
        "features": [
            "Premium coconut shell carbon only",
            "Highest iodine value available",
            "Superior organic chemical removal",
            "Excellent taste improvement",
            "Low ash content",
            "Environmentally sustainable source"
        ],
        "applications": ["Premium drinking water", "Medical facilities", "Laboratory water", "High-end residential"]
    },
    {
        "id": "product-07",
        "slug": "t33-post-carbon",
        "name_en": "T33 High Iodine Post-Carbon Filter",
        "image": "product-07-t33-carbon-filter.jpg",
        "description_en": "Specialized post-filtration carbon filter with ultra-high iodine value. Designed as final polishing stage in multi-stage water purification systems.",
        "specs": {
            "Carbon Type": "Acid-Washed Coconut",
            "Flow Rate": "0.5 GPM",
            "Dimensions": "10\" x 2\"",
            "Iodine Value": "≥1300 mg/g",
            "Ash Content": "<3%",
            "Service Life": "12 months",
            "Application": "Post-filtration",
            "Certification": "FDA food grade"
        },
        "features": [
            "Ultra-high iodine value",
            "Acid-washed for purity",
            "Removes residual tastes/odors",
            "Ideal for RO post-filtration",
            "Low pressure drop",
            "Premium grade carbon"
        ],
        "applications": ["RO system post-filter", "Final polishing stage", "Premium drinking water", "Food & beverage"]
    },
    {
        "id": "product-08",
        "slug": "uf-ultrafiltration-membrane",
        "name_en": "UF Ultrafiltration Membrane Filter",
        "image": "product-08-uf-membrane.jpg",
        "description_en": "Advanced hollow fiber ultrafiltration membrane providing 0.01 micron filtration. Removes bacteria, cysts, and viruses without electricity or drain connection.",
        "specs": {
            "Pore Size": "0.01 micron",
            "Flow Rate": "0.5 GPM",
            "Dimensions": "10\" x 2\"",
            "Membrane Type": "Hollow Fiber",
            "Bacteria Removal": ">99.9999%",
            "Virus Removal": ">99.99%",
            "Operating Pressure": "15-60 PSI",
            "Service Life": "24-36 months"
        },
        "features": [
            "0.01 micron absolute filtration",
            "No electricity required",
            "No wastewater produced",
            "Removes bacteria and viruses",
            "Long membrane life",
            "Easy maintenance"
        ],
        "applications": ["Well water purification", "Emergency water", "Off-grid systems", "Microbiological protection"]
    },
    {
        "id": "product-09",
        "slug": "ro-membrane-50-gpd",
        "name_en": "RO Membrane 50 GPD",
        "image": "product-09-ro-membrane-50gpd.jpg",
        "description_en": "Residential reverse osmosis membrane rated at 50 gallons per day. Industry-leading TDS reduction and stable performance over extended service life.",
        "specs": {
            "Daily Production": "50 GPD",
            "Dimensions": "1.8\" x 12\"",
            "Membrane Type": "TFC (Thin Film Composite)",
            "Salt Rejection": ">96%",
            "Operating Pressure": "50-75 PSI",
            "Recovery Rate": "25%",
            "Service Life": "24-36 months",
            "Max TDS": "2000 ppm"
        },
        "features": [
            "High salt rejection rate",
            "Stable performance",
            "Low operating pressure",
            "Extended membrane life",
            "Removes heavy metals",
            "NSF certified"
        ],
        "applications": ["Residential RO systems", "Under-sink units", "Drinking water purification", "Aquariums"]
    },
    {
        "id": "product-10",
        "slug": "ro-membrane-75-gpd",
        "name_en": "RO Membrane 75 GPD",
        "image": "product-10-ro-membrane-75gpd.jpg",
        "description_en": "Mid-capacity reverse osmosis membrane producing 75 gallons per day. Optimal for larger households or light commercial applications.",
        "specs": {
            "Daily Production": "75 GPD",
            "Dimensions": "1.8\" x 12\"",
            "Membrane Type": "TFC",
            "Salt Rejection": ">97%",
            "Operating Pressure": "50-80 PSI",
            "Recovery Rate": "30%",
            "Service Life": "24-36 months",
            "Max TDS": "2000 ppm"
        },
        "features": [
            "Increased production capacity",
            "Superior TDS reduction",
            "Energy efficient",
            "Consistent output quality",
            "Long-lasting performance",
            "Wide compatibility"
        ],
        "applications": ["Large households", "Small offices", "Coffee shops", "Light commercial use"]
    },
    {
        "id": "product-11",
        "slug": "ro-membrane-100-gpd",
        "name_en": "RO Membrane 100 GPD",
        "image": "product-11-ro-membrane-100gpd.jpg",
        "description_en": "High-output reverse osmosis membrane for commercial applications. Produces 100 gallons per day with excellent rejection rates and efficiency.",
        "specs": {
            "Daily Production": "100 GPD",
            "Dimensions": "1.8\" x 12\"",
            "Membrane Type": "TFC",
            "Salt Rejection": ">97%",
            "Operating Pressure": "55-85 PSI",
            "Recovery Rate": "33%",
            "Service Life": "24 months",
            "Max TDS": "2500 ppm"
        },
        "features": [
            "High production rate",
            "Commercial grade",
            "Excellent efficiency",
            "Stable performance",
            "Low fouling tendency",
            "Easy installation"
        ],
        "applications": ["Commercial RO systems", "Restaurants", "Offices", "Medical facilities"]
    },
    {
        "id": "product-12",
        "slug": "ro-membrane-150-gpd",
        "name_en": "RO Membrane 150 GPD",
        "image": "product-12-ro-membrane-150gpd.jpg",
        "description_en": "Premium commercial RO membrane with 150 GPD capacity. Designed for demanding applications requiring high volume and consistent water quality.",
        "specs": {
            "Daily Production": "150 GPD",
            "Dimensions": "2.5\" x 12\"",
            "Membrane Type": "TFC Commercial",
            "Salt Rejection": ">98%",
            "Operating Pressure": "60-90 PSI",
            "Recovery Rate": "35%",
            "Service Life": "18-24 months",
            "Max TDS": "3000 ppm"
        },
        "features": [
            "High volume production",
            "Superior rejection rate",
            "Heavy-duty construction",
            "Consistent quality output",
            "Low maintenance",
            "Industry-leading performance"
        ],
        "applications": ["Commercial buildings", "Food service", "Laboratories", "Industrial process water"]
    },
    {
        "id": "product-13",
        "slug": "ion-exchange-resin",
        "name_en": "Ion Exchange Resin Cartridge",
        "image": "product-13-ion-exchange-resin.jpg",
        "description_en": "Mixed-bed ion exchange resin cartridge for water softening and deionization. Removes calcium, magnesium, and other dissolved minerals.",
        "specs": {
            "Resin Type": "Mixed Bed (Cation/Anion)",
            "Capacity": "5000 grains",
            "Flow Rate": "1 GPM",
            "Dimensions": "10\" x 2.75\"",
            "Regeneration": "Replaceable",
            "Service Life": "6-12 months",
            "Max Hardness": "300 ppm",
            "Application": "Softening/DI"
        },
        "features": [
            "Softens hard water",
            "Removes scale-forming minerals",
            "Extends appliance life",
            "Improves soap effectiveness",
            "No salt discharge",
            "Easy replacement"
        ],
        "applications": ["Water softening", "Scale prevention", "Appliance protection", "Laboratory water"]
    },
    {
        "id": "product-14",
        "slug": "fluoride-removal-filter",
        "name_en": "Fluoride Removal Specialty Filter",
        "image": "product-14-fluoride-removal.jpg",
        "description_en": "Specialized activated alumina filter designed specifically for fluoride removal. Highly effective for reducing fluoride to safe drinking levels.",
        "specs": {
            "Media Type": "Activated Alumina",
            "Fluoride Removal": ">90%",
            "Flow Rate": "0.5 GPM",
            "Dimensions": "10\" x 2.5\"",
            "Capacity": "500 gallons",
            "pH Range": "5.5-8.5",
            "Service Life": "6-12 months",
            "Max Influent F": "10 ppm"
        },
        "features": [
            "High fluoride reduction",
            "Activated alumina media",
            "NSF certified",
            "Safe drinking water levels",
            "Also removes arsenic",
            "Easy installation"
        ],
        "applications": ["Fluoride reduction", "Drinking water", "Residential systems", "Health-conscious users"]
    },
    {
        "id": "product-15",
        "slug": "arsenic-removal-filter",
        "name_en": "Arsenic Removal Specialty Filter",
        "image": "product-15-arsenic-removal.jpg",
        "description_en": "Advanced iron-based media filter specifically engineered for arsenic reduction. Certified for both Arsenic III and Arsenic V removal.",
        "specs": {
            "Media Type": "Iron-based composite",
            "As(III) Removal": ">95%",
            "As(V) Removal": ">98%",
            "Flow Rate": "0.5 GPM",
            "Dimensions": "10\" x 2.5\"",
            "Capacity": "400 gallons",
            "Service Life": "6 months",
            "Certification": "NSF 53"
        },
        "features": [
            "Removes both As(III) and As(V)",
            "NSF/ANSI 53 certified",
            "Meets EPA standards",
            "High adsorption capacity",
            "Safe for drinking water",
            "Effective at low concentrations"
        ],
        "applications": ["Well water treatment", "Arsenic remediation", "Drinking water safety", "EPA compliance"]
    },
    {
        "id": "product-16",
        "slug": "iron-manganese-removal",
        "name_en": "Iron & Manganese Removal Filter",
        "image": "product-16-iron-manganese-removal.jpg",
        "description_en": "Catalytic media filter designed for oxidation and removal of dissolved iron and manganese. Eliminates staining and improves water clarity.",
        "specs": {
            "Media Type": "Catalytic oxidation",
            "Iron Removal": "Up to 10 ppm",
            "Manganese Removal": "Up to 5 ppm",
            "Flow Rate": "2 GPM",
            "Dimensions": "10\" x 4.5\"",
            "Service Life": "12-24 months",
            "pH Range": "6.5-8.5",
            "Backwash": "Not required"
        },
        "features": [
            "Removes iron and manganese",
            "Prevents staining",
            "Catalytic oxidation process",
            "No chemical additives",
            "Long service life",
            "Improves water clarity"
        ],
        "applications": ["Well water", "Iron stain prevention", "Manganese reduction", "Water quality improvement"]
    },
    {
        "id": "product-17",
        "slug": "alkaline-ionizer-filter",
        "name_en": "Alkaline Ionizer Mineral Filter",
        "image": "product-17-alkaline-ionizer.jpg",
        "description_en": "Mineral-rich alkaline filter cartridge that raises pH and adds beneficial minerals. Creates alkaline ionized water with antioxidant properties.",
        "specs": {
            "pH Range": "7.5-9.5",
            "Minerals Added": "Ca, Mg, K, Na",
            "Flow Rate": "0.5 GPM",
            "Dimensions": "10\" x 2.5\"",
            "ORP": "-100 to -200 mV",
            "Service Life": "6-12 months",
            "Capacity": "2000 gallons",
            "Application": "Post-filtration"
        },
        "features": [
            "Raises water pH to alkaline",
            "Adds beneficial minerals",
            "Negative ORP (antioxidant)",
            "Improves taste",
            "Supports health benefits",
            "Natural mineralization"
        ],
        "applications": ["Alkaline water systems", "Health-conscious users", "Post-RO remineralization", "Ionized water"]
    },
    {
        "id": "product-18",
        "slug": "kdf-filter-cartridge",
        "name_en": "KDF Process Media Filter",
        "image": "product-18-kdf-filter.jpg",
        "description_en": "KDF (Kinetic Degradation Fluxion) media filter using redox reactions to remove chlorine, heavy metals, and control bacteria growth.",
        "specs": {
            "Media Type": "KDF-55",
            "Chlorine Removal": ">95%",
            "Flow Rate": "1 GPM",
            "Dimensions": "10\" x 2.5\"",
            "Heavy Metal Reduction": "Lead, Mercury, etc.",
            "Service Life": "12-18 months",
            "Temperature Range": "40-130°F",
            "Bacteriostatic": "Yes"
        },
        "features": [
            "Removes chlorine and heavy metals",
            "Controls bacteria/algae growth",
            "Works in hot water",
            "Long-lasting media",
            "NSF certified",
            "Environmentally safe"
        ],
        "applications": ["Shower filters", "Whole house systems", "Hot water applications", "Bacteria control"]
    },
    {
        "id": "product-19",
        "slug": "string-wound-filter",
        "name_en": "String Wound Sediment Filter",
        "image": "product-19-string-wound-filter.jpg",
        "description_en": "String-wound polypropylene filter with gradient density structure. Excellent dirt-holding capacity for heavy sediment applications.",
        "specs": {
            "Micron Rating": "1-50 micron",
            "Flow Rate": "20 GPM",
            "Dimensions": "10\" x 4.5\"",
            "Material": "Polypropylene String",
            "Structure": "Gradient density",
            "Service Life": "3-6 months",
            "Max Temperature": "165°F",
            "Chemical Compatibility": "Excellent"
        },
        "features": [
            "High dirt-holding capacity",
            "Gradient density construction",
            "Wide chemical compatibility",
            "High temperature tolerance",
            "Cost-effective",
            "Heavy-duty applications"
        ],
        "applications": ["Industrial filtration", "Heavy sediment", "Chemical processing", "High-temperature water"]
    },
    {
        "id": "product-20",
        "slug": "pleated-polyester-filter",
        "name_en": "Pleated Polyester Cartridge Filter",
        "image": "product-20-pleated-filter.jpg",
        "description_en": "Washable and reusable pleated polyester filter with large surface area. Ideal for industrial and commercial applications requiring frequent cleaning.",
        "specs": {
            "Micron Rating": "5-100 micron",
            "Flow Rate": "40 GPM",
            "Dimensions": "10\" x 2.5\"",
            "Material": "Polyester membrane",
            "Surface Area": "2.5 sq ft",
            "Washable": "Yes (up to 50 times)",
            "Max Temperature": "200°F",
            "Max Pressure": "150 PSI"
        },
        "features": [
            "Washable and reusable",
            "Large filtration surface area",
            "High flow rates",
            "Durable construction",
            "Cost-effective long-term",
            "Industrial grade"
        ],
        "applications": ["Industrial process water", "Pre-filtration", "Washable filter systems", "High-volume applications"]
    },
    {
        "id": "product-21",
        "slug": "food-grade-filter",
        "name_en": "Food Grade Water Filter Cartridge",
        "image": "product-21-food-grade-filter.jpg",
        "description_en": "FDA-approved food-grade filter cartridge meeting strict food safety standards. Designed for food processing, beverage production, and commercial food service.",
        "specs": {
            "Certification": "FDA CFR Title 21",
            "Micron Rating": "0.5 micron",
            "Flow Rate": "2 GPM",
            "Dimensions": "10\" x 2.5\"",
            "Material": "Food-grade carbon block",
            "Chlorine Removal": ">99%",
            "Service Life": "12 months",
            "Application": "Food & beverage"
        },
        "features": [
            "FDA food-grade certified",
            "Meets FDA CFR 21 standards",
            "Safe for food contact",
            "Superior taste/odor removal",
            "NSF certified",
            "Quality assurance"
        ],
        "applications": ["Food processing", "Beverage production", "Commercial kitchens", "FDA-regulated facilities"]
    },
    {
        "id": "product-22",
        "slug": "pharmaceutical-grade-filter",
        "name_en": "Pharmaceutical Grade USP Filter",
        "image": "product-22-pharmaceutical-filter.jpg",
        "description_en": "USP Class VI compliant pharmaceutical-grade filter for critical applications. Meets stringent pharmaceutical and medical water quality standards.",
        "specs": {
            "Certification": "USP Class VI",
            "Micron Rating": "0.2 micron absolute",
            "Flow Rate": "0.5 GPM",
            "Dimensions": "10\" x 2.5\"",
            "Bacteria Retention": ">99.9999%",
            "Endotoxin Removal": "Yes",
            "Pyrogen-Free": "Yes",
            "Sterility": "Gamma sterilizable"
        },
        "features": [
            "USP Class VI compliant",
            "Pharmaceutical grade",
            "Absolute 0.2 micron filtration",
            "Bacteria and endotoxin removal",
            "Pyrogen-free",
            "Medical/pharmaceutical use"
        ],
        "applications": ["Pharmaceutical manufacturing", "Medical facilities", "Laboratory research", "Critical applications"]
    }
]

# 44种语言配置
LANGUAGES = {
    'en': 'English',
    'de': 'Deutsch',
    'fr': 'Français',
    'es': 'Español',
    'ru': 'Русский',
    'ja': '日本語',
    'it': 'Italiano',
    'pt': 'Português',
    'nl': 'Nederlands',
    'pl': 'Polski',
    'sv': 'Svenska',
    'ko': '한국어',
    'th': 'ไทย',
    'vi': 'Tiếng Việt',
    'id': 'Indonesia',
    'fil': 'Filipino',
    'ms': 'Bahasa Melayu',
    'my': 'မြန်မာ',
    'km': 'ខ្មែរ',
    'lo': 'ລາວ',
    'hi': 'हिन्दी',
    'bn': 'বাংলা',
    'ta': 'தமிழ்',
    'te': 'తెలుగు',
    'ar': 'العربية',
    'he': 'עברית',
    'fa': 'فارسی',
    'ur': 'اردو',
    'am': 'አማርኛ',
    'sw': 'Kiswahili',
    'zu': 'isiZulu',
    'da': 'Dansk',
    'no': 'Norsk',
    'fi': 'Suomi',
    'cs': 'Čeština',
    'hu': 'Magyar',
    'ro': 'Română',
    'el': 'Ελληνικά',
    'tr': 'Türkçe',
    'uk': 'Українська',
    'bg': 'Български',
    'hr': 'Hrvatski',
    'sk': 'Slovenčina',
    'sl': 'Slovenščina'
}

def generate_product_html(product, lang='en'):
    """生成单个产品页面的HTML"""
    
    is_rtl = lang in ['ar', 'he', 'fa', 'ur']
    dir_attr = 'dir="rtl"' if is_rtl else 'dir="ltr"'
    
    # 生成规格表
    specs_html = ""
    for key, value in product['specs'].items():
        specs_html += f"""
            <tr>
                <td style="padding: 0.75rem; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb;">{key}</td>
                <td style="padding: 0.75rem; color: #6b7280; border-bottom: 1px solid #e5e7eb;">{value}</td>
            </tr>
        """
    
    # 生成特性列表
    features_html = ""
    for feature in product['features']:
        features_html += f"""
            <div style="background: white; padding: 1rem; border-radius: 0.5rem; border-left: 3px solid #0ea5e9;">
                <p style="color: #374151; margin: 0;">✓ {feature}</p>
            </div>
        """
    
    # 生成应用场景
    applications_html = ""
    for app in product['applications']:
        applications_html += f"""
            <span style="background: #dbeafe; color: #1e40af; padding: 0.5rem 1rem; border-radius: 9999px; display: inline-block; margin: 0.25rem;">{app}</span>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="{lang}" {dir_attr}>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{product['name_en']} | Express Water - Professional Water Filter Manufacturer</title>
    <meta name="description" content="{product['description_en']}">
    <meta name="keywords" content="water filter, {product['name_en'].lower()}, water purification, Express Water, professional filters">
    <link rel="canonical" href="https://www.yuchensy.com/{lang}/{product['slug']}/"/>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #374151; background: #f9fafb; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }}
        .header {{ background: linear-gradient(135deg, #1e40af 0%, #0ea5e9 100%); color: white; padding: 2rem 1rem; text-align: center; }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        .header p {{ font-size: 1.1rem; opacity: 0.9; }}
        .product-image {{ text-align: center; margin: 2rem 0; background: white; padding: 2rem; border-radius: 0.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .product-image img {{ max-width: 600px; width: 100%; height: auto; border-radius: 0.5rem; }}
        .section {{ background: white; padding: 2rem; margin: 2rem 0; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .section h2 {{ color: #1e40af; font-size: 1.8rem; margin-bottom: 1.5rem; padding-bottom: 0.5rem; border-bottom: 2px solid #0ea5e9; }}
        .specs-table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
        .features-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin: 1rem 0; }}
        .applications {{ margin: 1rem 0; }}
        .contact-section {{ background: linear-gradient(135deg, #1e40af 0%, #0ea5e9 100%); color: white; padding: 2rem; border-radius: 0.5rem; margin: 2rem 0; }}
        .contact-section h2 {{ color: white; }}
        .btn {{ background: white; color: #1e40af; padding: 1rem 2rem; border-radius: 0.375rem; text-decoration: none; display: inline-block; font-weight: 700; margin-top: 1rem; }}
        .btn:hover {{ background: #f0f9ff; }}
        footer {{ background: #1f2937; color: white; padding: 2rem; text-align: center; margin-top: 3rem; }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8rem; }}
            .features-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>💧 Express Water</h1>
        <p>Professional Water Filtration Solutions Since 1998</p>
    </div>
    
    <div class="container">
        <div class="section">
            <h1 style="color: #1e40af; font-size: 2.2rem; margin-bottom: 1rem;">{product['name_en']}</h1>
            <p style="font-size: 1.1rem; color: #6b7280; line-height: 1.8;">{product['description_en']}</p>
        </div>
        
        <div class="product-image">
            <img src="../images/{product['image']}" alt="{product['name_en']}" loading="lazy">
        </div>
        
        <div class="section">
            <h2>📋 Technical Specifications</h2>
            <table class="specs-table">
                {specs_html}
            </table>
        </div>
        
        <div class="section">
            <h2>⭐ Key Features & Benefits</h2>
            <div class="features-grid">
                {features_html}
            </div>
        </div>
        
        <div class="section">
            <h2>🎯 Applications</h2>
            <div class="applications">
                {applications_html}
            </div>
        </div>
        
        <div class="contact-section">
            <h2>📞 Contact Us for Quote</h2>
            <p style="font-size: 1.1rem; margin: 1rem 0;">Get professional consultation and competitive pricing for bulk orders. OEM/ODM services available.</p>
            <div style="margin-top: 1.5rem;">
                <p><strong>📧 Email:</strong> expresswater025@gmail.com</p>
                <p><strong>☎️ Phone:</strong> +86-19908311885</p>
                <p><strong>📍 Location:</strong> Haining, Zhejiang, China</p>
            </div>
            <a href="mailto:expresswater025@gmail.com" class="btn">Request Quote →</a>
        </div>
    </div>
    
    <footer>
        <p>&copy; 2024 Express Water Co., Ltd. | Professional Water Filter Manufacturer Since 1998</p>
        <p>NSF Certified | ISO 9001 | Serving 50+ Countries Worldwide</p>
    </footer>
</body>
</html>"""
    
    return html

def generate_homepage():
    """生成主页HTML"""
    
    # 生成产品卡片
    products_html = ""
    for product in PRODUCTS:
        products_html += f"""
        <div style="background: white; border-radius: 0.5rem; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.3s;">
            <div style="height: 200px; overflow: hidden; background: #f3f4f6;">
                <img src="images/{product['image']}" alt="{product['name_en']}" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div style="padding: 1.5rem;">
                <h3 style="color: #1e40af; font-size: 1.2rem; margin-bottom: 0.5rem;">{product['name_en']}</h3>
                <p style="color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;">{product['description_en'][:100]}...</p>
                <a href="en/{product['slug']}.html" style="color: #0ea5e9; text-decoration: none; font-weight: 600;">View Details →</a>
            </div>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Express Water - Professional Water Filter Manufacturer | 22 Products | Global Supplier</title>
    <meta name="description" content="Express Water: Professional water filter cartridge manufacturer from Haining, China. 22+ products, NSF certified, serving 50+ countries. OEM/ODM available.">
    <meta name="keywords" content="water filter manufacturer, filter cartridge, RO membrane, activated carbon, water purification, OEM supplier, Express Water">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #374151; background: #f9fafb; }}
        .hero {{ background: linear-gradient(135deg, #1e40af 0%, #0ea5e9 100%); color: white; padding: 4rem 2rem; text-align: center; }}
        .hero h1 {{ font-size: 3rem; margin-bottom: 1rem; }}
        .hero p {{ font-size: 1.3rem; max-width: 800px; margin: 0 auto 2rem; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 2rem 1rem; }}
        .section-title {{ font-size: 2.5rem; color: #1e40af; text-align: center; margin: 3rem 0 2rem; }}
        .products-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 2rem; margin: 2rem 0; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin: 3rem 0; background: white; padding: 3rem; border-radius: 0.5rem; }}
        .stat {{ text-align: center; }}
        .stat-number {{ font-size: 3rem; font-weight: 700; color: #0ea5e9; }}
        .stat-label {{ color: #6b7280; font-size: 1.1rem; }}
        footer {{ background: #1f2937; color: white; padding: 3rem 2rem; text-align: center; margin-top: 4rem; }}
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 2rem; }}
            .products-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>💧 Express Water</h1>
        <p>Professional Water Filter Cartridge Manufacturer | Established 1998 | NSF Certified | Serving 50+ Countries Worldwide</p>
        <div style="margin-top: 2rem;">
            <a href="#products" style="background: white; color: #1e40af; padding: 1rem 2rem; border-radius: 0.375rem; text-decoration: none; font-weight: 700; margin: 0 0.5rem;">View Products</a>
            <a href="mailto:expresswater025@gmail.com" style="background: transparent; color: white; padding: 1rem 2rem; border-radius: 0.375rem; text-decoration: none; font-weight: 700; border: 2px solid white; margin: 0 0.5rem;">Contact Sales</a>
        </div>
    </div>
    
    <div class="container">
        <div class="stats">
            <div class="stat">
                <div class="stat-number">22+</div>
                <div class="stat-label">Products</div>
            </div>
            <div class="stat">
                <div class="stat-number">50+</div>
                <div class="stat-label">Countries</div>
            </div>
            <div class="stat">
                <div class="stat-number">25+</div>
                <div class="stat-label">Years Experience</div>
            </div>
            <div class="stat">
                <div class="stat-number">NSF</div>
                <div class="stat-label">Certified</div>
            </div>
        </div>
        
        <h2 class="section-title" id="products">Our Complete Product Range</h2>
        <p style="text-align: center; color: #6b7280; font-size: 1.1rem; max-width: 800px; margin: 0 auto 3rem;">Professional water filtration solutions for residential, commercial, and industrial applications. All products come with detailed specifications and real product images.</p>
        
        <div class="products-grid">
            {products_html}
        </div>
        
        <div style="background: linear-gradient(135deg, #1e40af 0%, #0ea5e9 100%); color: white; padding: 3rem; border-radius: 0.5rem; text-align: center; margin: 4rem 0;">
            <h2 style="font-size: 2rem; margin-bottom: 1rem;">Ready to Order?</h2>
            <p style="font-size: 1.1rem; margin-bottom: 2rem;">Contact us for competitive pricing, technical specifications, and OEM/ODM services.</p>
            <div style="margin-top: 2rem;">
                <p style="font-size: 1.1rem;"><strong>📧 Email:</strong> expresswater025@gmail.com</p>
                <p style="font-size: 1.1rem;"><strong>☎️ Phone:</strong> +86-19908311885</p>
                <p style="font-size: 1.1rem;"><strong>📍 Location:</strong> Haining, Zhejiang, China</p>
            </div>
        </div>
    </div>
    
    <footer>
        <h3 style="margin-bottom: 1rem;">Express Water Co., Ltd.</h3>
        <p>Professional Water Filter Cartridge Manufacturer Since 1998</p>
        <p>NSF Certified | ISO 9001 | CE | RoHS</p>
        <p style="margin-top: 1rem;">Haining, Zhejiang, China | expresswater025@gmail.com | +86-19908311885</p>
        <p style="margin-top: 2rem; color: #9ca3af;">&copy; 2024 Express Water Co., Ltd. All rights reserved.</p>
    </footer>
</body>
</html>"""
    
    return html

def main():
    """主函数：生成完整网站"""
    
    print("🚀 开始生成Express Water完整网站...")
    print(f"📊 产品数量: {len(PRODUCTS)}")
    print(f"🌍 语言数量: {len(LANGUAGES)}")
    
    # 创建语言目录
    for lang_code in LANGUAGES.keys():
        lang_dir = f"{lang_code}"
        os.makedirs(lang_dir, exist_ok=True)
        print(f"✓ 创建目录: {lang_dir}/")
    
    # 生成所有产品页面
    total_pages = 0
    for lang_code in LANGUAGES.keys():
        for product in PRODUCTS:
            html_content = generate_product_html(product, lang_code)
            filepath = f"{lang_code}/{product['slug']}.html"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            total_pages += 1
    
    print(f"✅ 已生成 {total_pages} 个产品页面")
    
    # 生成主页
    homepage_html = generate_homepage()
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(homepage_html)
    print("✅ 已生成主页 (index.html)")
    
    # 生成sitemap.xml
    sitemap_urls = ['<url><loc>https://www.yuchensy.com/</loc><priority>1.0</priority></url>']
    for lang_code in LANGUAGES.keys():
        for product in PRODUCTS:
            sitemap_urls.append(f'<url><loc>https://www.yuchensy.com/{lang_code}/{product["slug"]}/</loc><priority>0.8</priority></url>')
    
    sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {''.join(sitemap_urls)}
</urlset>'''
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print("✅ 已生成sitemap.xml")
    
    # 生成robots.txt
    robots_content = """User-agent: *
Allow: /
Sitemap: https://www.yuchensy.com/sitemap.xml"""
    
    with open('robots.txt', 'w', encoding='utf-8') as f:
        f.write(robots_content)
    print("✅ 已生成robots.txt")
    
    print(f"\n🎉 网站生成完成！")
    print(f"📄 总页面数: {total_pages + 1} (包括主页)")
    print(f"📁 语言目录: {len(LANGUAGES)} 个")
    print(f"📸 产品图片: {len(PRODUCTS)} 张")
    print(f"\n✨ 所有文件已生成，可以直接部署到GitHub Pages!")

if __name__ == "__main__":
    main()
