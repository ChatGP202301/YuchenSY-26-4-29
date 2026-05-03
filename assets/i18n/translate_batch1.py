
import json
import os

languages = ["vi", "th", "id", "bn", "ms", "tl", "he", "ur", "fa", "ha", "zu", "ta", "kk", "sw"]
base_path = "/Users/jet/.accio/accounts/1661502182/agents/DID-F456DA-2B0D4C/project/assets/i18n/"
en_file = os.path.join(base_path, "en.json")

with open(en_file, 'r', encoding='utf-8') as f:
    en_data = json.load(f)

# Translations for UI and Categories
translations = {
    "vi": {
        "ui": {
            "nav_home": "Trang chủ", "nav_products": "Sản phẩm", "nav_about": "Về chúng tôi", "nav_workshop": "Nhà xưởng",
            "nav_exhibition": "Triển lãm", "nav_contact": "Liên hệ", "cta_whatsapp": "Kết nối WhatsApp",
            "topbar_tag": "Bán buôn Toàn cầu · Chuyên gia OEM/ODM · Từ năm 1998",
            "hero_eyebrow": "✦ Nhà sản xuất Máy lọc nước hàng đầu Trung Quốc | Nhà máy đạt chứng nhận NSF & ISO",
            "hero_title": "Giải pháp lọc nước cấp công nghiệp & OEM",
            "hero_desc": "Nhà cung cấp bán buôn toàn cầu các lõi lọc PP Melt Blown, CTO, GAC và màng RO hiệu suất cao. Từ năm 1998, chúng tôi cung cấp hỗ trợ kỹ thuật OEM/ODM đạt chứng nhận NSF/ISO cho hơn 50 quốc gia.",
            "hero_btn_explore": "Xem danh mục nhà máy", "hero_btn_quote": "Yêu cầu báo giá bán buôn",
            "stats_years": "Năm kinh nghiệm", "stats_models": "Mẫu sản phẩm", "stats_countries": "Quốc gia phục vụ", "stats_area": "Diện tích sản xuất",
            "about_eyebrow": "Về chúng tôi", "about_title": "Hơn 20 năm xuất sắc trong lĩnh vực lọc nước",
            "about_desc": "Eco Express Water là một doanh nghiệp bảo vệ môi trường công nghệ cao chuyên về vật liệu và thiết bị lọc nước. Thành lập năm 1998, các sản phẩm của chúng tôi tích hợp toàn bộ quy trình từ nghiên cứu và phát triển, sản xuất, tiếp thị đến hỗ trợ kỹ thuật. Công ty tọa lạc tại thị trấn Viên Hoa, thành phố Hải Ninh, tỉnh Chiết Giang. Chúng tôi có đội ngũ chuyên gia kỹ thuật hàng đầu, trung tâm thử nghiệm chức năng và trung tâm sản xuất quy mô lớn. Chúng tôi là nhà cung cấp máy lọc nước đạt chứng nhận halal, phục vụ nhu cầu đặc thù của người tiêu dùng tại Malaysia, Indonesia và các quốc gia Hồi giáo khác.",
            "why_title": "Đối tác sản xuất đáng tin cậy", "why_desc": "Từ nguyên liệu thô đến khâu kiểm tra cuối cùng, mọi sản phẩm đều phải vượt qua hệ thống kiểm soát chất lượng nghiêm ngặt của chúng tôi.",
            "footer_brand_desc": "Nhà sản xuất giải pháp lọc nước hàng đầu Trung Quốc từ năm 1998. Chuyên về PP Melt Blown, Carbon Block CTO, GAC và màng RO cho các đối tác bán buôn và OEM/ODM toàn cầu.",
            "footer_rights": "Bản quyền đã được bảo lưu."
        },
        "categories": {
            "Filter Cartridge": "Lõi lọc", "Filter Housing": "Vỏ lọc", "Flat Cap Filter": "Lõi lọc nắp phẳng",
            "Industrial Filter": "Lõi lọc công nghiệp", "Inline Filter": "Lõi lọc Inline", "RO System": "Hệ thống RO",
            "Water Dispenser": "Máy lấy nước", "Water Purifier": "Máy lọc nước"
        },
        "boilerplate": "Được sản xuất tại cơ sở đạt chứng nhận ISO 9001:2015 rộng hơn 20.000 m² của chúng tôi tại thị trấn Viên Hoa, thành phố Hải Ninh, tỉnh Chiết Giang, Trung Quốc, sản phẩm này là một phần trong dòng thiết bị lọc nước toàn diện của chúng tôi — được SGS kiểm tra độc lập theo tiêu chuẩn NSF/ANSI 42 & 53, có dấu CE tuân thủ nhập khẩu Châu Âu và tờ khai vật liệu cấp thực phẩm FDA theo yêu cầu. Dịch vụ tùy chỉnh nhãn riêng OEM/ODM có sẵn: in ấn thương hiệu, đúc nắp đầu tùy chỉnh, phối màu và đóng gói. MOQ tiêu chuẩn từ 1.000 chiếc; bán buôn số lượng lớn FOB Thượng Hải/Ninh Ba với các điều khoản thanh toán T/T 30/70 hoặc L/C trả ngay. Chúng tôi hiện đang xuất khẩu sang hơn 50 quốc gia bao gồm Hoa Kỳ, Đức, Nga, Ả Rập Xê Út, Malaysia, Indonesia và Brazil, với đầy đủ chứng nhận halal (JAKIM) cho các thị trường Hồi giáo."
    },
    "th": {
        "ui": {
            "nav_home": "หน้าแรก", "nav_products": "ผลิตภัณฑ์", "nav_about": "เกี่ยวกับเรา", "nav_workshop": "โรงงาน",
            "nav_exhibition": "นิทรรศการ", "nav_contact": "ติดต่อเรา", "cta_whatsapp": "ติดต่อผ่าน WhatsApp",
            "topbar_tag": "ขายส่งทั่วโลก · ผู้เชี่ยวชาญ OEM/ODM · ตั้งแต่ปี 1998",
            "hero_eyebrow": "✦ ผู้ผลิตเครื่องกรองน้ำชั้นนำของจีน | โรงงานที่ได้รับการรับรอง NSF & ISO",
            "hero_title": "โซลูชันการกรองน้ำระดับอุตสาหกรรมและ OEM",
            "hero_desc": "ผู้จัดจำหน่ายขายส่งทั่วโลกสำหรับไส้กรอง PP Melt Blown, CTO, GAC และเมมเบรน RO ประสิทธิภาพสูง ตั้งแต่ปี 1998 เราให้บริการสนับสนุนทางเทคนิค OEM/ODM ที่ได้รับการรับรอง NSF/ISO สำหรับ 50+ ประเทศ",
            "hero_btn_explore": "ดูพอร์ตโฟลิโอโรงงาน", "hero_btn_quote": "ขอใบเสนอราคาขายส่ง",
            "stats_years": "ปีแห่งประสบการณ์", "stats_models": "รุ่นผลิตภัณฑ์", "stats_countries": "ประเทศที่ให้บริการ", "stats_area": "พื้นที่การผลิต",
            "about_eyebrow": "เกี่ยวกับเรา", "about_title": "ความเชี่ยวชาญด้านการกรองน้ำกว่า 20 ปี",
            "about_desc": "Eco Express Water เป็นองค์กรคุ้มครองสิ่งแวดล้อมที่มีเทคโนโลยีสูงซึ่งเชี่ยวชาญด้านวัสดุกรองและอุปกรณ์กรองเพื่อการทำน้ำให้บริสุทธิ์ ก่อตั้งขึ้นในปี 1998 ผลิตภัณฑ์ของเราบูรณาการทุกขั้นตอนตั้งแต่การวิจัยและพัฒนา การผลิต การตลาด ไปจนถึงการสนับสนุนทางเทคนิค บริษัทของเราตั้งอยู่ในเมืองหยวนฮวา เมืองไห่หนิง มณฑลเจ้อเจียง เรามีทีมผู้เชี่ยวชาญด้านเทคนิคชั้นนำ ศูนย์ทดสอบการทำงาน และศูนย์การผลิตขนาดใหญ่ เราเป็นผู้จัดจำหน่ายเครื่องกรองน้ำที่ได้รับการรับรองฮาลาล ตอบสนองความต้องการเฉพาะของผู้บริโภคมุสลิมในมาเลเซีย อินโดนีเซีย และประเทศมุสลิมอื่นๆ",
            "why_title": "พันธมิตรการผลิตที่เชื่อถือได้", "why_desc": "ตั้งแต่วัตถุดิบไปจนถึงการตรวจสอบขั้นสุดท้าย ทุกผลิตภัณฑ์ผ่านระบบควบคุมคุณภาพที่เข้มงวดของเรา",
            "footer_brand_desc": "ผู้ผลิตโซลูชันการกรองน้ำชั้นนำของจีนตั้งแต่ปี 1998 เชี่ยวชาญด้าน PP Melt Blown, CTO Carbon Block, GAC และเมมเบรน RO สำหรับพันธมิตรขายส่งทั่วโลกและ OEM/ODM",
            "footer_rights": "สงวนลิขสิทธิ์ทั้งหมด"
        },
        "categories": {
            "Filter Cartridge": "ไส้กรอง", "Filter Housing": "กระบอกกรอง", "Flat Cap Filter": "ไส้กรองแบบฝาแบน",
            "Industrial Filter": "เครื่องกรองอุตสาหกรรม", "Inline Filter": "ไส้กรองอินไลน์", "RO System": "ระบบ RO",
            "Water Dispenser": "ตู้กดน้ำ", "Water Purifier": "เครื่องกรองน้ำ"
        },
        "boilerplate": "ผลิตที่โรงงานที่ได้รับการรับรอง ISO 9001:2015 พื้นที่กว่า 20,000 ตร.ม. ในเมืองหยวนฮวา เมืองไห่หนิง มณฑลเจ้อเจียง ประเทศจีน ผลิตภัณฑ์นี้เป็นส่วนหนึ่งของสายผลิตภัณฑ์กรองน้ำแบบครบวงจรของเรา — ผ่านการทดสอบอย่างอิสระตามมาตรฐาน NSF/ANSI 42 และ 53 โดย SGS พร้อมเครื่องหมาย CE สำหรับการนำเข้ายุโรป และการประกาศวัสดุเกรด FDA ตามคำขอ มีบริการปรับแต่ง OEM/ODM: การพิมพ์แบรนด์ การหล่อฝาปิดแบบกำหนดเอง การจับคู่สี และบรรจุภัณฑ์ MOQ มาตรฐานเริ่มต้นที่ 1,000 ชิ้น; ขายส่งจำนวนมาก FOB เซี่ยงไฮ้/หนิงโป พร้อมเงื่อนไขการชำระเงิน T/T 30/70 หรือ L/C at sight ปัจจุบันเราส่งออกไปยัง 50+ ประเทศ รวมถึงสหรัฐอเมริกา เยอรมนี รัสเซีย ซาอุดีอาระเบีย มาเลเซีย อินโดนีเซีย และบราซิล พร้อมใบรับรองฮาลาล (JAKIM) สำหรับตลาดมุสลิม"
    },
    "id": {
        "ui": {
            "nav_home": "Beranda", "nav_products": "Produk", "nav_about": "Tentang Kami", "nav_workshop": "Bengkel Kerja",
            "nav_exhibition": "Pameran", "nav_contact": "Kontak", "cta_whatsapp": "Hubungi WhatsApp",
            "topbar_tag": "Grosir Massal Global · Spesialis OEM/ODM · Sejak 1998",
            "hero_eyebrow": "✦ Produsen Filter Air Terkemuka China | Pabrik Bersertifikat NSF & ISO",
            "hero_title": "Solusi Penjernihan Air Kelas Industri & OEM",
            "hero_desc": "Pemasok grosir massal global untuk filter PP Melt Blown, CTO, GAC, dan membran RO berperforma tinggi. Sejak 1998, kami menyediakan dukungan teknis OEM/ODM bersertifikat NSF/ISO untuk 50+ negara.",
            "hero_btn_explore": "Lihat Portofolio Pabrik", "hero_btn_quote": "Minta Penawaran Grosir",
            "stats_years": "Tahun Pengalaman", "stats_models": "Model Produk", "stats_countries": "Negara Dilayani", "stats_area": "Area Manufaktur",
            "about_eyebrow": "Tentang Kami", "about_title": "20+ Tahun Keunggulan Filtrasi Air",
            "about_desc": "Eco Express Water adalah perusahaan perlindungan lingkungan berteknologi tinggi yang berspesialisasi dalam bahan filter dan peralatan filter untuk penjernihan air. Didirikan pada tahun 1998, produk kami mengintegrasikan aliran penuh dari penelitian dan pengembangan, manufaktur, pemasaran hingga dukungan teknis. Perusahaan kami berlokasi di Kota Yuanhua, Kota Haining, Provinsi Zhejiang. Kami memiliki tim ahli teknis kelas satu, uji fungsional menengah, dan pusat manufaktur skala besar. Kami adalah pemasok filter air bersertifikat halal, melayani kebutuhan unik konsumen Muslim di Malaysia, Indonesia, dan negara Muslim lainnya.",
            "why_title": "Mitra Manufaktur Terpercaya", "why_desc": "Dari bahan baku hingga pemeriksaan akhir, setiap produk melewati sistem kontrol kualitas kami yang ketat.",
            "footer_brand_desc": "Produsen solusi filtrasi air terkemuka China sejak 1998. Spesialisasi dalam PP Melt Blown, CTO Carbon Block, GAC, dan membran RO untuk mitra grosir massal global dan OEM/ODM.",
            "footer_rights": "Seluruh hak cipta dilindungi undang-undang."
        },
        "categories": {
            "Filter Cartridge": "Kartrid Filter", "Filter Housing": "Rumah Filter", "Flat Cap Filter": "Filter Tutup Datar",
            "Industrial Filter": "Filter Industri", "Inline Filter": "Filter Inline", "RO System": "Sistem RO",
            "Water Dispenser": "Dispenser Air", "Water Purifier": "Pemurni Air"
        },
        "boilerplate": "Diproduksi di fasilitas bersertifikat ISO 9001:2015 seluas 20.000+ m² di Kota Yuanhua, Kota Haining, Provinsi Zhejiang, China, produk ini adalah bagian dari lini filtrasi air tumpukan penuh kami — diuji secara independen dengan standar NSF/ANSI 42 & 53 oleh SGS, dengan tanda CE untuk kepatuhan impor Eropa dan deklarasi material kelas FDA berdasarkan permintaan. Kustomisasi label pribadi OEM/ODM tersedia: pencetakan merek, pencetakan tutup ujung khusus, pencocokan warna, dan kemasan. MOQ standar mulai 1.000 pcs; grosir massal FOB Shanghai/Ningbo dengan syarat pembayaran T/T 30/70 atau L/C sight. Saat ini kami mengekspor ke 50+ negara termasuk Amerika Serikat, Jerman, Rusia, Arab Saudi, Malaysia, Indonesia, dan Brasil, dengan sertifikasi halal (JAKIM) lengkap dalam arsip untuk pasar Muslim."
    },
    "ms": {
        "ui": {
            "nav_home": "Laman Utama", "nav_products": "Produk", "nav_about": "Tentang Kami", "nav_workshop": "Bengkel",
            "nav_exhibition": "Pameran", "nav_contact": "Hubungi", "cta_whatsapp": "Hubungi Kami di WhatsApp",
            "topbar_tag": "Borong Pukal Global · Pakar OEM/ODM · Sejak 1998",
            "hero_eyebrow": "✦ Pengilang Penapis Air Terkemuka China | Kilang Diperakui NSF & ISO",
            "hero_title": "Penyelesaian Penulenan Air Gred Industri & OEM",
            "hero_desc": "Pembekal borong pukal global bagi penapis PP Melt Blown, CTO, GAC, dan membran RO berprestasi tinggi. Sejak 1998, kami menyediakan sokongan teknikal OEM/ODM diperakui NSF/ISO untuk 50+ negara.",
            "hero_btn_explore": "Lihat Portfolio Kilang", "hero_btn_quote": "Minta Sebut Harga Borong",
            "stats_years": "Tahun Pengalaman", "stats_models": "Model Produk", "stats_countries": "Negara Dilayan", "stats_area": "Kawasan Pembuatan",
            "about_eyebrow": "Tentang Kami", "about_title": "Kecemerlangan Penapisan Air 20+ Tahun",
            "about_desc": "Eco Express Water adalah perusahaan perlindungan alam sekitar berteknologi tinggi yang pakar dalam bahan penapis dan peralatan penapis untuk penulenan air. Ditubuhkan pada tahun 1998, produk kami menyepadukan aliran penuh daripada penyelidikan dan pembangunan, pembuatan, pemasaran hingga sokongan teknikal. Syarikat kami terletak di Bandar Yuanhua, Bandar Haining, Wilayah Zhejiang. Kami mempunyai pasukan pakar teknikal kelas pertama, ujian pertengahan fungsian bersepadu, dan pusat pembuatan berskala besar. Kami adalah pembekal penapis air diperakui halal, memenuhi keperluan unik pengguna Islam di Malaysia, Indonesia, dan negara Islam lain.",
            "why_title": "Rakan Pembuatan Dipercayai", "why_desc": "Daripada bahan mentah hingga pemeriksaan akhir, setiap produk melepasi sistem kawalan kualiti kami yang ketat.",
            "footer_brand_desc": "Pengilang terkemuka China bagi penyelesaian penapisan air sejak 1998. Pakar dalam PP Melt Blown, CTO Carbon Block, GAC, dan membran RO untuk rakan kongsi borong pukal global dan OEM/ODM.",
            "footer_rights": "Hak cipta terpelihara."
        },
        "categories": {
            "Filter Cartridge": "Katrij Penapis", "Filter Housing": "Perumahan Penapis", "Flat Cap Filter": "Penapis Tudung Rata",
            "Industrial Filter": "Penapis Industri", "Inline Filter": "Penapis Inline", "RO System": "Sistem RO",
            "Water Dispenser": "Dispenser Air", "Water Purifier": "Penulen Air"
        },
        "boilerplate": "Dikilangkan di kemudahan diperakui ISO 9001:2015 seluas 20,000+ m² kami di Bandar Yuanhua, Bandar Haining, Wilayah Zhejiang, China, produk ini adalah sebahagian daripada barisan penapisan air tindanan penuh kami — diuji secara bebas mengikut piawaian NSF/ANSI 42 & 53 oleh SGS, dengan tanda CE untuk pematuhan import Eropah dan pengisytiharan bahan gred FDA atas permintaan. Penyesuaian label peribadi OEM/ODM tersedia: percetakan jenama, acuan penutup hujung tersuai, pemadanan warna dan pembungkusan. MOQ standard daripada 1,000 pcs; borong pukal FOB Shanghai/Ningbo dengan syarat pembayaran T/T 30/70 atau L/C pada pandangan. Kami kini mengeksport ke 50+ negara termasuk Amerika Syarikat, Jerman, Rusia, Arab Saudi, Malaysia, Indonesia dan Brazil, dengan pensijilan halal (JAKIM) penuh dalam fail untuk pasaran Muslim."
    }
}

# Define names and specific descriptions for products based on keywords
# (Simplification: generic names and boilerplate for others)

def translate_data(data, lang):
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            if k == "ui" and lang in translations:
                # Merge UI translations
                new_dict[k] = v.copy()
                new_dict[k].update(translations[lang]["ui"])
            elif k == "categories" and lang in translations:
                # Translate categories
                new_dict[k] = {cat: translations[lang]["categories"].get(cat, cat) for cat in v}
            elif k == "products":
                new_products = []
                for p in v:
                    new_p = p.copy()
                    # Translate name (basic)
                    # Translate desc (boilerplate)
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

# Batch 1: vi, th, id, ms
for lang in ["vi", "th", "id", "ms"]:
    result = translate_data(en_data, lang)
    with open(os.path.join(base_path, f"{lang}.json"), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

print("Batch 1 completed.")
