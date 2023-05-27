import scrapy

from immo_kleinanzeigen.items import RealEstateItem


def strip_if_exist(response, selector):
    return response.css(selector).get().strip() if response.css(selector).get() is not None else ''

def strip_if_exist_else(response, selector, selector2):
    return response.css(selector).get().strip() if response.css(selector).get() is not None else strip_if_exist(response, selector2)


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
            id=strip_if_exist(response, '#viewad-ad-id-box li:nth-child(2)::text'),
            caption=strip_if_exist(response, 'h1::text'),
            price=strip_if_exist(response, 'h2[class*="boxedarticle--price"]::text'),
            street=strip_if_exist(response, '#street-address::text'),
            location=strip_if_exist(response, '#viewad-locality::text'),
            area_living=detail_map.get('Wohnfläche'),
            area_plot=detail_map.get('Grundstücksfläche'),
            total_rooms=detail_map.get('Zimmer'),
            bedrooms=detail_map.get('Schlafzimmer'),
            bathrooms=detail_map.get('Badezimmer'),
            available_from=detail_map.get('Verfügbar ab'),
            house_type=detail_map.get('Haustyp'),
            floors=detail_map.get('Etagen'),
            year_build=detail_map.get('Baujahr'),
            commission=detail_map.get('Provision'),
            date_inserted=strip_if_exist(response, '#viewad-extra-info span:nth-child(2)::text'),
            views=strip_if_exist(response, '#viewad-extra-info span:nth-child(1)::text'),
            offerer=strip_if_exist_else(response, '#viewad-contact .text-force-linebreak a::text', '#viewad-contact .text-force-linebreak::text'),
            offerer_phone_number=strip_if_exist(response, '#viewad-contact-phone a::text')
        )
