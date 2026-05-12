# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):

    def test_normal_item_quality_decreases(self):
        items = [Item(name="+5 Dexterity Vest", sell_in=10, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(19, items[0].quality)

    def test_normal_item_sell_in_decreases(self):
        items = [Item(name="+5 Dexterity Vest", sell_in=10, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(9, items[0].sell_in)

    def test_sulfuras_quality_unchanged(self):
        items = [Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)]
        GildedRose(items).update_quality()
        self.assertEqual(80, items[0].quality)

    def test_sulfuras_sell_in_unchanged(self):
        items = [Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].sell_in)

    def test_sulfuras_wrong_constructor_quality_corrected(self):
        items = [Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=10)]
        GildedRose(items).update_quality()
        self.assertEqual(80, items[0].quality)

    def test_aged_brie_quality_increases(self):
        items = [Item(name="Aged Brie", sell_in=2, quality=0)]
        GildedRose(items).update_quality()
        self.assertEqual(1, items[0].quality)

    def test_aged_brie_sell_in_decreases(self):
        items = [Item(name="Aged Brie", sell_in=2, quality=0)]
        GildedRose(items).update_quality()
        self.assertEqual(1, items[0].sell_in)
    
    def test_aged_brie_quality_increases_after_sell_in(self):
        items = [Item(name="Aged Brie", sell_in=0, quality=0)]
        GildedRose(items).update_quality()
        self.assertEqual(2, items[0].quality)

    def test_backstage_pass_quality_increases_more_than_10_days_before_sell_in(self):
        items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(21, items[0].quality)
    
    def test_backstage_pass_quality_increases_10_days_before_sell_in(self):
        items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(22, items[0].quality)

    def test_backstage_pass_quality_increases_5_days_before_sell_in(self):
        items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(23, items[0].quality)

    def test_backstage_pass_quality_drops_to_0_after_concert(self):
        items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)

    def test_backstage_pass_boundary_at_sell_in_6(self):
        items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=6, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(22, items[0].quality)

    def test_backstage_pass_boundary_at_sell_in_11(self):
        items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=11, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(21, items[0].quality)

    def test_backstage_pass_sell_in_decreases(self):
        items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(14, items[0].sell_in)
    
    def test_backstage_pass_quality_capped_at_50(self):
        items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49)]
        GildedRose(items).update_quality()
        self.assertEqual(50, items[0].quality)

    def test_quality_never_negative(self):
        items = [Item(name="+5 Dexterity Vest", sell_in=10, quality=0)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)
    
    def test_quality_never_exceeds_50(self):
        items = [Item(name="Aged Brie", sell_in=2, quality=50)]
        GildedRose(items).update_quality()
        self.assertEqual(50, items[0].quality)

    def test_normal_item_double_degrades_after_sell_in(self):
        items = [Item(name="+5 Dexterity Vest", sell_in=0, quality=20)]
        GildedRose(items).update_quality()
        self.assertEqual(18, items[0].quality)

    def test_conjured_item_degrades_twice_as_fast(self):
        items = [Item(name="Conjured Mana Cake", sell_in=3, quality=6)]
        GildedRose(items).update_quality()
        self.assertEqual(4, items[0].quality)

    def test_conjured_item_degrades_four_times_after_sell_in(self):
        items = [Item(name="Conjured Mana Cake", sell_in=0, quality=6)]
        GildedRose(items).update_quality()
        self.assertEqual(2, items[0].quality)


if __name__ == '__main__':
    unittest.main()
