# -*- coding: utf-8 -*-

MAX_QUALITY = 50
SULFURAS_QUALITY = 80
BACKSTAGE_PASS_CLOSER_DAYS = 10
BACKSTAGE_PASS_CLOSEST_DAYS = 5
BACKSTAGE_PASS_CLOSEST_DAYS_INCREMENT = 3
BACKSTAGE_PASS_CLOSER_DAYS_INCREMENT = 2
BACKSTAGE_PASS_OTHER_INCREMENT = 1
DAILY_QUALITY_DECREMENT = 1
DAILY_QUALITY_DECREMENT_AFTER_SELL_IN = 2
DAILY_QUALITY_INCREMENT = 1
AGED_BRIE_POST_EXPIRY_QUALITY_INCREMENT = 2
SULFURAS_NAME = "Sulfuras, Hand of Ragnaros"
AGED_BRIE_NAME = "Aged Brie"
BACKSTAGE_PASS_NAME = "Backstage passes to a TAFKAL80ETC concert"
CONJURED_PREFIX = "Conjured"
CONJURED_QUALITY_DECREMENT = 2
CONJURED_QUALITY_DECREMENT_AFTER_SELL_IN = 4

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def get_is_item_updatable(self, item):
        return item.name != SULFURAS_NAME

    def get_sell_in_update(self, item):
        return item.sell_in - 1
    
    def enforce_quality_boundaries(self, candidate_quality):
        if candidate_quality > MAX_QUALITY:
            return MAX_QUALITY
        if candidate_quality < 0:
            return 0
        return candidate_quality
    
    def enforce_quality_rule_non_updatable(self, item):
        if item.quality != SULFURAS_QUALITY:
            item.quality = SULFURAS_QUALITY

    def update_backstage_pass_quality(self, item):
        if item.sell_in < 0:
            return 0
        if item.sell_in < BACKSTAGE_PASS_CLOSEST_DAYS:
            return item.quality+BACKSTAGE_PASS_CLOSEST_DAYS_INCREMENT
        if item.sell_in < BACKSTAGE_PASS_CLOSER_DAYS:
            return item.quality+BACKSTAGE_PASS_CLOSER_DAYS_INCREMENT
        return item.quality+BACKSTAGE_PASS_OTHER_INCREMENT
    
    def update_aged_brie_quality(self, item):
        if item.sell_in < 0:
            return item.quality+AGED_BRIE_POST_EXPIRY_QUALITY_INCREMENT
        return item.quality+DAILY_QUALITY_INCREMENT
    
    def update_generic_quality(self, item):
        if item.sell_in < 0:
            return item.quality-DAILY_QUALITY_DECREMENT_AFTER_SELL_IN
        return item.quality-DAILY_QUALITY_DECREMENT

    def update_conjured_quality(self, item):
        if item.sell_in < 0:
            return item.quality-CONJURED_QUALITY_DECREMENT_AFTER_SELL_IN
        return item.quality-CONJURED_QUALITY_DECREMENT
    
    def get_quality_update(self, item):
        if item.name == AGED_BRIE_NAME:
            return self.update_aged_brie_quality(item)
        elif item.name == BACKSTAGE_PASS_NAME:
            return self.update_backstage_pass_quality(item)
        elif item.name.startswith(CONJURED_PREFIX):
            return self.update_conjured_quality(item)
        else:
            return self.update_generic_quality(item)

    def update_quality(self):
        for item in self.items:
            if self.get_is_item_updatable(item):
                item.sell_in = self.get_sell_in_update(item)
                item.quality = self.enforce_quality_boundaries(self.get_quality_update(item))
            else:
                self.enforce_quality_rule_non_updatable(item)

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
