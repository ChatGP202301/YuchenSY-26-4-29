#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepL 产品描述翻译 - 完整版
一键翻译所有产品描述到44种语言

使用方法：
1. 安装: pip install deepl
2. 注册DeepL API (免费): https://www.deepl.com/pro-api
3. 替换 API_KEY
4. 运行: python3 translate_product_descriptions.py
"""

try:
    import deepl
    DEEPL_AVAILABLE = True
except ImportError:
    DEEPL_AVAILABLE = False
    print("⚠️  DeepL未安装。安装方法: pip install deepl")
    print()

import re
from pathlib import Path
import time

# ========================================
# 配置
# ========================================

# 替换为您的DeepL API Key
API_KEY = "YOUR-DEEPL-API-KEY"  # 从 https://www.deepl.com/pro-api 获取

SITE_DIR = Path('/home/claude/FINAL-V2')

# DeepL支持的语言
LANG_MAP = {
    'ar': 'AR', 'bg': 'BG', 'cs': 'CS', 'da': 'DA', 'de': 'DE',
    'el': 'EL', 'es': 'ES', 'et': 'ET', 'fi': 'FI', 'fr': 'FR',
    'hu': 'HU', 'id': 'ID', 'it': 'IT', 'ja': 'JA', 'ko': 'KO',
    'lt': 'LT', 'lv': 'LV', 'nl': 'NL', 'pl': 'PL', 'pt': 'PT-PT',
    'ro': 'RO', 'ru': 'RU', 'sk': 'SK', 'sl': 'SL', 'sv': 'SV',
    'tr': 'TR', 'uk': 'UK',
}

# ========================================
# 提取产品描述
# ========================================

def extract_product_descriptions():
    """从英文产品页面提取所有描述"""
    print("📋 扫描英文产品页面...")
    
    en_dir = SITE_DIR / 'en'
    products = {}
    
    for html_file in en_dir.glob('product-*.html'):
        content = html_file.read_text(encoding='utf-8')
        
        # 提取产品描述段落 <p class="desc">...</p>
        desc_match = re.search(r'<p class="desc">(.+?)</p>', content, re.DOTALL)
        if desc_match:
            desc = desc_match.group(1)
            # 清理HTML实体
            desc = desc.replace('&amp;', '&')
            products[html_file.name] = desc
    
    print(f"✅ 找到 {len(products)} 个产品描述")
    return products

# ========================================
# 翻译产品描述
# ========================================

def translate_all_products():
    """翻译所有产品描述到所有语言"""
    
    if not DEEPL_AVAILABLE:
        print("❌ 请先安装DeepL: pip install deepl")
        return
    
    if API_KEY == "YOUR-DEEPL-API-KEY":
        print("❌ 请先配置DeepL API Key")
        print("   1. 访问: https://www.deepl.com/pro-api")
        print("   2. 注册并获取API Key")
        print("   3. 替换脚本中的 API_KEY")
        return
    
    # 初始化DeepL
    try:
        translator = deepl.Translator(API_KEY)
        usage = translator.get_usage()
        print(f"✅ DeepL API 已连接")
        print(f"   配额: {usage.character.count:,} / {usage.character.limit:,}")
        print()
    except Exception as e:
        print(f"❌ DeepL API 错误: {e}")
        return
    
    # 提取英文产品描述
    products = extract_product_descriptions()
    
    # 开始翻译
    print("=" * 70)
    print("开始翻译产品描述")
    print("=" * 70)
    print()
    
    for lang, deepl_lang in LANG_MAP.items():
        lang_dir = SITE_DIR / lang
        if not lang_dir.exists():
            continue
        
        print(f"🌐 翻译到 {lang.upper()}...")
        
        translated_count = 0
        for filename, english_desc in products.items():
            lang_file = lang_dir / filename
            if not lang_file.exists():
                continue
            
            try:
                # 翻译描述
                result = translator.translate_text(
                    english_desc,
                    target_lang=deepl_lang,
                    formality='more'  # 商务正式语气
                )
                translated_desc = result.text
                
                # 读取文件并替换
                content = lang_file.read_text(encoding='utf-8')
                
                # 查找并替换 <p class="desc">...</p>
                pattern = r'<p class="desc">(.+?)</p>'
                replacement = f'<p class="desc">{translated_desc}</p>'
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                
                # 写回文件
                lang_file.write_text(content, encoding='utf-8')
                translated_count += 1
                
                # 避免API限流
                time.sleep(0.1)
                
            except Exception as e:
                print(f"   ⚠️  {filename}: {e}")
        
        print(f"   ✅ {translated_count} 个产品描述已翻译")
    
    # 显示最终使用量
    usage = translator.get_usage()
    print()
    print("=" * 70)
    print("✅ 翻译完成！")
    print("=" * 70)
    print(f"📊 API使用: {usage.character.count:,} / {usage.character.limit:,}")
    print(f"   剩余: {usage.character.limit - usage.character.count:,} 字符")

# ========================================
# 无DeepL方案：使用Google Translate
# ========================================

def translate_with_google():
    """备选方案：使用Google Translate（免费但需要额外设置）"""
    print("=" * 70)
    print("备选方案：Google Translate")
    print("=" * 70)
    print()
    print("如果不想使用DeepL，可以使用Google Translate:")
    print()
    print("1. 安装: pip install googletrans==4.0.0rc1")
    print("2. 运行翻译脚本")
    print()
    print("注意：Google Translate免费版有使用限制")
    print("     质量略低于DeepL")

# ========================================
# 主程序
# ========================================

def main():
    print()
    print("🌍 产品描述翻译工具")
    print("=" * 70)
    print()
    
    if DEEPL_AVAILABLE and API_KEY != "YOUR-DEEPL-API-KEY":
        translate_all_products()
    else:
        print("请先配置DeepL API:")
        print()
        print("步骤1: 注册DeepL API (免费)")
        print("  访问: https://www.deepl.com/pro-api")
        print("  免费套餐: 每月500,000字符")
        print()
        print("步骤2: 安装DeepL库")
        print("  命令: pip install deepl")
        print()
        print("步骤3: 配置API Key")
        print("  编辑此文件，替换 API_KEY")
        print()
        print("步骤4: 运行翻译")
        print("  命令: python3 translate_product_descriptions.py")
        print()
        translate_with_google()

if __name__ == '__main__':
    main()
