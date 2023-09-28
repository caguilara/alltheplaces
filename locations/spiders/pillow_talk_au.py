from locations.storefinders.localisr import LocalisrSpider
from locations.categories import apply_category


class PillowTalkAUSpider(LocalisrSpider):
    name = "pillow_talk_au"
    item_attributes = {"brand": "Pillow Talk", "brand_wikidata": "Q120648495"}
    api_key = "8VPD9W8YJZG9403P62L3RNR7DWKQX15VOEJ4YQO"
    # The search radius appears to be ignored, so a single search
    # coordinate is returning locations all across Australia.
    search_coordinates = [
        (-33.863276, 151.107977),
    ]

    def parse_item(self, item, location):
        apply_category({"shop":"household_linen"} , item)
        yield item