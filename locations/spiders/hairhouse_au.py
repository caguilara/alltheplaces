import scrapy

from locations.dict_parser import DictParser
from locations.hours import OpeningHours

class HairhouseAUSpider(scrapy.Spider):
    name = "hairhouse_au"
    item_attributes = {"brand": "Hairhouse", "brand_wikidata": "Q118383855"}
    allowed_domains = ["www.hairhouse.com.au"]
    sitemap_urls = ["https://www.hairhouse.com.au/store/sitemap.xml"]
    start_urls = [
        "https://www.hairhouse.com.au/api/storeList?latitude=-37&longitude=144&distance=4000&top=120&_data=routes/($lang)/api/storeList"
    ]
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def parse(self, response):
        for location in response.json():
            item = DictParser.parse(location)
            item["website"] = "https://www.hairhouse.com.au/stores/" + location["url_component"]
            hours_string = " ".join(
                [day_hours["day"] + ": " + day_hours["hours"] for day_hours in location["operatingHours"]]
            )
            item["opening_hours"] = OpeningHours()
            item["opening_hours"].add_ranges_from_string(hours_string)
            yield item