from locations.storefinders.storelocatorwidgets import StoreLocatorWidgetsSpider
from locations.categories import Categories, apply_category


class ALHHotelsAUAUSpider(StoreLocatorWidgetsSpider):
    name = "alh_hotels_au"
    item_attributes = {"brand": "ALH Hotels", "brand_wikidata": "Q119159708"}
    key = "41fdc8f98fc2738172250baa676b369d"

    def parse_item(self, item, location):
        apply_category(Categories.HOTEL, item)
        yield item