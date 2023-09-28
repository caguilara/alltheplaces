import scrapy
from scrapy.selector.unified import Selector

from locations.hours import OpeningHours, day_range, sanitise_day
from locations.items import Feature
from locations.categories import apply_category, Categories


class CoenMarketsSpider(scrapy.Spider):
    name = "coen_markets"
    item_attributes = {"name": "Coen", "brand": "Coen Markets", "brand_wikidata": "Q122856721"}
    start_urls = ["https://coen1923.com/locations/search"]

    def parse(self, response):
        for location in response.json()["locations"]:
            if not location:
                continue
            url_title = location["url_title"]
            # Note: embedded in an iframe; not useful as item's website
            store_url = f"https://coen1923.com/locations/location/{url_title}"
            yield scrapy.Request(store_url, self.parse_store, cb_kwargs={"js": location})

    def parse_store(self, response, js):
        props = {}
        props["street_address"] = Selector(text=js["address"]).xpath("//p/text()").get()
        props["ref"] = js["url_title"]
        props["lat"] = js["coordinates"][0]
        props["lon"] = js["coordinates"][1]
        props["city"] = js["city"]
        props["state"] = js["state"]
        props["postcode"] = js["zip"]
        props["phone"] = js["phone_number"]
        if hours := response.css(".hours p:not(:empty)").xpath("text()").get():
            props["opening_hours"] = self.parse_hours(hours)
        item = Feature(**props)
        apply_category(Categories.SHOP_CONVENIENCE, item)
        yield item

    @staticmethod
    def parse_hours(rules: str) -> OpeningHours():
        rules = rules.replace("HOURS", "Mo-Su").replace(" to ", " - ")

        days, times = rules.split(":", maxsplit=1)
        start_day, end_day = days.split("-")
        start_day = sanitise_day(start_day)
        end_day = sanitise_day(end_day)
        start_time, end_time = times.split("-")
        start_time = CoenMarketsSpider.sanitise_time(start_time)
        end_time = CoenMarketsSpider.sanitise_time(end_time)

        if start_day and end_day and start_time and end_time:
            oh = OpeningHours()
            oh.add_days_range(day_range(start_day, end_day), start_time, end_time, time_format="%I:%M%p")
            return oh

    @staticmethod
    def sanitise_time(time: str) -> str:
        time = time.upper().replace("A ", "AM").strip()
        if ":" not in time:
            time = time[:-2] + ":00" + time[-2:]
        return time
