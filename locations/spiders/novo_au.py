from locations.storefinders.metalocator import MetaLocatorSpider
from locations.categories import apply_category, Categories


class NOVOAUSpider(MetaLocatorSpider):
    name = "novo_au"
    item_attributes = {"brand": "NOVO", "brand_wikidata": "Q120669012"}
    brand_id = "9067"
    country_list = ["Australia"]

    def parse_item(self, item, location):
        apply_category(Categories.SHOP_SHOES, item)
        yield item