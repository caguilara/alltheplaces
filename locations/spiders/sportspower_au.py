from locations.storefinders.stockinstore import StockInStoreSpider
from locations.categories import apply_category, Categories


class SportsPowerAUSpider(StockInStoreSpider):
    name = "sportspower_au"
    item_attributes = {"brand": "SportsPower", "brand_wikidata": "Q117747652"}
    api_site_id = "10067"
    api_widget_id = "74"
    api_widget_type = "storelocator"
    api_origin = "https://www.sportspower.com.au"

    def parse_item(self, item, location):
        apply_category(Categories.SHOP_SPORTS, item)
        yield item
