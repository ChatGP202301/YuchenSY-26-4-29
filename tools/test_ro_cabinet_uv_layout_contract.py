"""Regression contracts for the RO cabinet card and product hero layout."""

import unittest
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "en/products.html"
DETAIL = ROOT / "en/product-cabinet-ro-water-purifier-5-6-stage-uv.html"


class RoCabinetUvLayoutContract(unittest.TestCase):
    def test_products_entry_uses_bounded_taxonomy_card(self):
        soup = BeautifulSoup(PRODUCTS.read_text(encoding="utf-8"), "html.parser")
        entry = soup.select_one(".ro-cabinet-uv-entry")
        self.assertIsNotNone(entry)
        card = entry.select_one(".tx-card.tx-product-card")
        self.assertIsNotNone(card)
        self.assertIsNotNone(card.select_one(".tx-card-media img"))
        self.assertIsNotNone(card.select_one(".tx-card-copy"))

    def test_detail_hero_is_bounded_and_has_one_visible_breadcrumb(self):
        soup = BeautifulSoup(DETAIL.read_text(encoding="utf-8"), "html.parser")
        self.assertEqual(len(soup.select(".rcu-hero-copy > .breadcrumb")), 1)
        css = "".join(node.get_text() for node in soup.select("style"))
        self.assertIn("width:min(100%,460px)", css)
        self.assertIn("max-width:460px", css)
        self.assertIn("max-height:480px", css)

    def test_detail_catalog_copy_matches_ro_product(self):
        soup = BeautifulSoup(DETAIL.read_text(encoding="utf-8"), "html.parser")
        scope = soup.select_one("[data-context-catalog-card] [data-catalog-scope]")
        self.assertIsNotNone(scope)
        self.assertIn("RO water purifier", scope.get_text(" ", strip=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
