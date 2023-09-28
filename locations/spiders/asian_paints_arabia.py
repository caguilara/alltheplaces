import chompjs
from scrapy import Request, Spider

from locations.dict_parser import DictParser
from locations.categories import Categories, apply_category


class AsianPaintsArabiaSpider(Spider):
    name = "asian_paints_arabia"
    item_attributes = {"brand": "Asian Paints", "brand_wikidata": "Q28171825"}

    def start_requests(self):
        for country in ["bahrain", "oman", "uae", "qatar"]:
            yield Request(
                f"https://www.asianpaintsarabia.com/Handlers/getStoreLocator.ashx?type=&state=&country={country}"
            )

    def parse(self, response, **kwargs):
        for shop in chompjs.parse_js_object(response.text):
            shop["name"] = shop.pop("Company_Name")
            shop["street_address"] = shop.pop("Address")
            item = DictParser.parse(shop)
            apply_category(Categories.SHOP_PAINT, item)
            yield item
