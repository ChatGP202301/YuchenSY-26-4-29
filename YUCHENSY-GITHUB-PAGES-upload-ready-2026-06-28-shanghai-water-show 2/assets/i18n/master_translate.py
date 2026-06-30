
import json
import os

# Base path
base_path = "/Users/jet/.accio/accounts/1661502182/agents/DID-F456DA-2B0D4C/project/assets/i18n/"
en_file = os.path.join(base_path, "en.json")

with open(en_file, 'r', encoding='utf-8') as f:
    en_data = json.load(f)

# Global translations for common terms
common_trans = {
    "vi": {
        "Years Experience": "Năm kinh nghiệm", "Product Models": "Mẫu sản phẩm", "Countries Served": "Quốc gia phục vụ", "Manufacturing Area": "Diện tích sản xuất",
        "Technical Specifications": "Thông số kỹ thuật", "Inquiry via WhatsApp": "Yêu cầu qua WhatsApp", "Inquiry via Email": "Yêu cầu qua Email",
        "Filtration Stages": "Giai đoạn lọc", "Daily Output": "Công suất hàng ngày", "Material": "Vật liệu", "Working Pressure": "Áp suất làm việc",
        "Working Temperature": "Nhiệt độ làm việc", "Certifications": "Chứng nhận", "Warranty": "Bảo hành", "Application": "Ứng dụng",
        "Type": "Loại", "Connection": "Kết nối", "Service Life": "Tuổi thọ dịch vụ", "Function": "Chức năng", "Benefits": "Lợi ích",
        "Housing": "Vỏ máy", "Filtration Media": "Vật liệu lọc", "Max Working Pressure": "Áp suất làm việc tối đa",
        "Inlet/Outlet": "Đầu vào/Đầu ra", "Seal": "Gióng/Vòng đệm", "Micron Rating": "Độ tinh lọc (Micron)", "Size": "Kích thước", "Flow Rate": "Lưu lượng"
    },
    "th": {
        "Years Experience": "ปีที่สั่งสมประสบการณ์", "Product Models": "รุ่นผลิตภัณฑ์", "Countries Served": "ประเทศที่ให้บริการ", "Manufacturing Area": "พื้นที่โรงงาน",
        "Technical Specifications": "ข้อมูลทางเทคนิค", "Inquiry via WhatsApp": "สอบถามผ่าน WhatsApp", "Inquiry via Email": "สอบถามผ่านอีเมล",
        "Filtration Stages": "ขั้นตอนการกรอง", "Daily Output": "กำลังการผลิตต่อวัน", "Material": "วัสดุ", "Working Pressure": "แรงดันใช้งาน",
        "Working Temperature": "อุณหภูมิใช้งาน", "Certifications": "การรับรอง", "Warranty": "การรับประกัน", "Application": "การใช้งาน",
        "Type": "ประเภท", "Connection": "การเชื่อมต่อ", "Service Life": "อายุการใช้งาน", "Function": "ฟังก์ชัน", "Benefits": "ประโยชน์",
        "Housing": "ตัวเรือน", "Filtration Media": "สารกรอง", "Max Working Pressure": "แรงดันใช้งานสูงสุด",
        "Inlet/Outlet": "ทางเข้า/ทางออก", "Seal": "ซีล", "Micron Rating": "ระดับไมครอน", "Size": "ขนาด", "Flow Rate": "อัตราการไหล"
    },
    "id": {
        "Years Experience": "Tahun Pengalaman", "Product Models": "Model Produk", "Countries Served": "Negara yang Dilayani", "Manufacturing Area": "Area Produksi",
        "Technical Specifications": "Spesifikasi Teknis", "Inquiry via WhatsApp": "Tanya via WhatsApp", "Inquiry via Email": "Tanya via Email",
        "Filtration Stages": "Tahap Filtrasi", "Daily Output": "Output Harian", "Material": "Bahan", "Working Pressure": "Tekanan Kerja",
        "Working Temperature": "Suhu Kerja", "Certifications": "Sertifikasi", "Warranty": "Garansi", "Application": "Aplikasi",
        "Type": "Tipe", "Connection": "Koneksi", "Service Life": "Masa Pakai", "Function": "Fungsi", "Benefits": "Manfaat",
        "Housing": "Wadah", "Filtration Media": "Media Filtrasi", "Max Working Pressure": "Tekanan Kerja Maksimum",
        "Inlet/Outlet": "Saluran Masuk/Keluar", "Seal": "Segel", "Micron Rating": "Peringkat Mikron", "Size": "Ukuran", "Flow Rate": "Laju Aliran"
    },
    "ms": {
        "Years Experience": "Tahun Pengalaman", "Product Models": "Model Produk", "Countries Served": "Negara yang Dilayan", "Manufacturing Area": "Kawasan Kilang",
        "Technical Specifications": "Spesifikasi Teknikal", "Inquiry via WhatsApp": "Pertanyaan melalui WhatsApp", "Inquiry via Email": "Pertanyaan melalui E-mel",
        "Filtration Stages": "Tahap Penapisan", "Daily Output": "Output Harian", "Material": "Bahan", "Working Pressure": "Tekanan Kerja",
        "Working Temperature": "Suhu Kerja", "Certifications": "Pensijilan", "Warranty": "Waranti", "Application": "Aplikasi",
        "Type": "Jenis", "Connection": "Sambungan", "Service Life": "Hayat Perkhidmatan", "Function": "Fungsi", "Benefits": "Faedah",
        "Housing": "Perumahan", "Filtration Media": "Media Penapisan", "Max Working Pressure": "Tekanan Kerja Maksimum",
        "Inlet/Outlet": "Inlet/Outlet", "Seal": "Kedap", "Micron Rating": "Kedudukan Mikron", "Size": "Saiz", "Flow Rate": "Kadar Aliran"
    },
    "he": {
        "Years Experience": "שנות ניסיון", "Product Models": "דגמי מוצרים", "Countries Served": "מדינות שירות", "Manufacturing Area": "שטח ייצור",
        "Technical Specifications": "מפרט טכני", "Inquiry via WhatsApp": "פנייה בוואטסאפ", "Inquiry via Email": "פנייה במייל",
        "Filtration Stages": "שלבי סינון", "Daily Output": "תפוקה יומית", "Material": "חומר", "Working Pressure": "לחץ עבודה",
        "Working Temperature": "טמפרטורת עבודה", "Certifications": "אישורים", "Warranty": "אחריות", "Application": "יישום",
        "Type": "סוג", "Connection": "חיבור", "Service Life": "אורך חיים", "Function": "פונקציה", "Benefits": "יתרונות",
        "Housing": "בית המסנן", "Filtration Media": "מדיה לסינון", "Max Working Pressure": "לחץ עבודה מקסימלי",
        "Inlet/Outlet": "כניסה/יציאה", "Seal": "אטם", "Micron Rating": "דירוג מיקרון", "Size": "גודל", "Flow Rate": "קצב זרימה"
    },
    "fa": {
        "Years Experience": "سال تجربه", "Product Models": "مدل‌های محصول", "Countries Served": "کشورهای تحت پوشش", "Manufacturing Area": "فضای تولید",
        "Technical Specifications": "مشخصات فنی", "Inquiry via WhatsApp": "استعلام از طریق واتس‌اپ", "Inquiry via Email": "استعلام از طریق ایمیل",
        "Filtration Stages": "مراحل فیلتراسیon", "Daily Output": "خروجی روزانه", "Material": "مواد", "Working Pressure": "فشار کاری",
        "Working Temperature": "دمای کاری", "Certifications": "گواهینامه‌ها", "Warranty": "گارانتی", "Application": "کاربرد",
        "Type": "نوع", "Connection": "اتصال", "Service Life": "عمر مفید", "Function": "عملکرد", "Benefits": "مزایا",
        "Housing": "هوزینگ", "Filtration Media": "مدیای فیلتراسیون", "Max Working Pressure": "حداکثر فشار کاری",
        "Inlet/Outlet": "ورودی/خروجی", "Seal": "واشر", "Micron Rating": "درجه میکرون", "Size": "اندازه", "Flow Rate": "نرخ جریان"
    },
    "ur": {
        "Years Experience": "سالوں کا تجربہ", "Product Models": "مصنوعات کے ماڈل", "Countries Served": "خدمت کردہ ممالک", "Manufacturing Area": "پیداواری رقبہ",
        "Technical Specifications": "تکنیکی وضاحتیں", "Inquiry via WhatsApp": "واٹس ایپ کے ذریعے انکوائری", "Inquiry via Email": "ای میل کے ذریعے انکوائری",
        "Filtration Stages": "فلٹریشن کے مراحل", "Daily Output": "روزانہ کی پیداوار", "Material": "مواد", "Working Pressure": "کام کا دباؤ",
        "Working Temperature": "کام کا درجہ حرارت", "Certifications": "سرٹیفیکیشن", "Warranty": "وارنٹی", "Application": "درخواست",
        "Type": "قسم", "Connection": "کنکشن", "Service Life": "سروس لائف", "Function": "فنکشن", "Benefits": "فوائد",
        "Housing": "ہاؤسنگ", "Filtration Media": "فلٹریشن میڈیا", "Max Working Pressure": "زیادہ سے زیادہ کام کا دباؤ",
        "Inlet/Outlet": "انلیٹ/آؤٹ لیٹ", "Seal": "سیل", "Micron Rating": "مائکرون ریٹنگ", "Size": "سائز", "Flow Rate": "بہاؤ کی شرح"
    }
}

# Add translations for the rest as needed...
# For brevity, I will apply a general mapping logic in the script for all 14 languages.

def translate_node(node, lang):
    if isinstance(node, dict):
        return {k: translate_node(v, lang) for k, v in node.items()}
    elif isinstance(node, list):
        return [translate_node(item, lang) for item in node]
    elif isinstance(node, str):
        # Check if we have a direct translation for this exact string
        if lang in common_trans and node in common_trans[lang]:
            return common_trans[lang][node]
        # Otherwise, for this task, I'll provide the logic to keep the structure
        return node
    return node

target_languages = ["vi", "th", "id", "bn", "ms", "tl", "he", "ur", "fa", "ha", "zu", "ta", "kk", "sw"]

# For each language, I will run a specific update that includes the UI, Categories, and Product Names.
# I'll manually provide the UI and Category blocks for each to ensure "deep translation".

def get_full_translation(lang):
    # This function would ideally return the full translated JSON.
    # Since I cannot fit all 14 languages in one go, I'll provide the core logic and do it.
    pass

# (The actual work of providing the 14 translations will be done by the model 
# by writing the files directly or in parts).
