from locations.storefinders.stockinstore import StockInStoreSpider
from locations.categories import apply_category, Categories


class KidstuffAUSpider(StockInStoreSpider):
    name = "kidstuff_au"
    item_attributes = {"brand": "Kidstuff", "brand_wikidata": "Q117746407"}
    api_site_id = "10041"
    api_widget_id = "48"
    api_widget_type = "cnc"
    api_origin = "https://www.kidstuff.com.au"

    def parse_item(self, item, location):
        apply_category(Categories.SHOP_TOYS, item)
        yield item