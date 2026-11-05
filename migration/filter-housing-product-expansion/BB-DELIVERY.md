# BB terminology and two black products — local review
16 housing URLs + 2 accessory entries. Original 14 URL paths retained. New black paths:
- /en/10-inch-black-bb-filter-housing.html
- /en/20-inch-black-bb-filter-housing.html

Preview: http://127.0.0.1:8765/en/product-housing-filter.html
Generator: build.py followed automatically by split-products.py; product names, metadata, alt, Product schema and RFQ names derive from products.json. Never derive old URLs from renamed titles.

Evidence: bb-page-keywords.csv and bb-keyword-review.md. No measured search-volume or GSC query evidence. No independent brand/compatibility/performance claims.
Checks: bundled Python verify-bb.py (negative cases + page contracts + deterministic rebuild); node verify-split.cjs (80 viewport cases + search); node verify-bb-inquiry.cjs (16 correct handoffs; POST=0).

Important image limitation: 10-inch black white-background image is a derived illustration from the original black housing reference, explicitly captioned; exact 10-inch camera photo unavailable. 20-inch black is a reference-based enhancement. Both source generation paths retained in white-image-map.json.

GitHub review submission: PR #17, https://github.com/ChatGP202301/YuchenSY-26-4-29/pull/17 . This revision is not merged or published. GSC submission and actual AI citation checks remain unverified. Prior production records refer to the previous release only.
