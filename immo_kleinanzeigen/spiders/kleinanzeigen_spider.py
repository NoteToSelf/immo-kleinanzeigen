import scrapy

from immo_kleinanzeigen.items import RealEstateItem


class KleinanzeigenSpider(scrapy.Spider):
    name = "kleinanzeigen"
    start_urls = ["https://www.kleinanzeigen.de/s-anzeige/hier-eigennutzer-und-vermieter-werden-gepflegtes-mfh-am-schoelerberg-/2374061258-208-3125",
                  "https://www.kleinanzeigen.de/s-anzeige/reserviert-ruhige-lage-am-waldrand/2327844570-208-289"]

    def parse(self, response, **kwargs):
        details = response.css('li[class*="addetailslist--detail"]')
        detail_map = {
            detail.xpath('.//text()').get().strip(): detail.css('span::text').get().strip()
            for detail in details
        }
        print(detail_map)
        yield RealEstateItem(
            id=response.css('#viewad-ad-id-box li:nth-child(2)::text').get().strip(),
            caption=response.css('h1::text').get().strip(),
            price=response.css('h2[class*="boxedarticle--price"]::text').get().strip(),
            area_living=detail_map['Wohnfläche'],
            area_plot=detail_map['Grundstücksfläche'])
