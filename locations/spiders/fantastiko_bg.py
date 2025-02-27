import json

from scrapy.spiders import SitemapSpider

from locations.structured_data_spider import StructuredDataSpider


class FantastikoBGSpider(SitemapSpider, StructuredDataSpider):
    name = "fantastiko_bg"
    item_attributes = {"brand_wikidata": "Q61140834"}
    sitemap_urls = ["https://www.fantastico.bg/robots.txt"]
    sitemap_rules = [("/shops/", "parse_sd")]

    def post_process_item(self, item, response, ld_data, **kwargs):
        item["addr_full"] = response.xpath('//p[@itemprop="address"]/following-sibling::p/text()').get()

        data = json.loads(response.xpath('//input[@id="shops-initial"]/@value').get())[0]
        item["lat"] = data["lat"]
        item["lon"] = data["lng"]
        item["ref"] = response.xpath(
            '//span[@class="feat-title white shop-number inline_block middle"]/text()'
        ).extract_first()
        item["opening_hours"] = (
            response.xpath('//p[@itemprop="openingHours"]/text()')
            .extract_first()
            .replace("ч.", "")
            .replace("от ", "")
            .replace(" до ", "-")
            .replace(".", ":")
            .strip()
        )

        yield item
