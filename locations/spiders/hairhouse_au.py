from scrapy import Spider

from locations.dict_parser import DictParser

from locations.hours import DAYS_FULL, OpeningHours
from scrapy.spiders import SitemapSpider
from locations.hours import OpeningHours


class HairhouseAUSpider(SitemapSpider):
    name = "hairhouse_au"
    item_attributes = {"brand": "Hairhouse", "brand_wikidata": "Q118383855"}
    allowed_domains = ["www.hairhouse.com.au"]
    sitemap_urls = ["https://www.hairhouse.com.au/store/sitemap.xml"]
    sitemap_rules = [("/store/", "parse")]
    custom_settings = {"ROBOTSTXT_OBEY": False}
