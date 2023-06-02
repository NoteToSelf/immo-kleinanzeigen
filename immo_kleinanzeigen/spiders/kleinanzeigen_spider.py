import datetime

import scrapy

from immo_kleinanzeigen.items import RealEstateItem
from datetime import datetime
import re
import html2text
import logging

location_pattern = r"(?P<zipcode>\d{5}) (?P<state>.*?) - (?P<city>.*)"
converter = html2text.HTML2Text()
converter.ignore_links = True


def strip_if_exist(response, selector):
    return response.css(selector).get().strip() if response.css(selector).get() is not None else ''


def strip_if_exist_else(response, selector, selector2):
    return response.css(selector).get().strip() if response.css(selector).get() is not None else strip_if_exist(
        response, selector2)


def parse_details_page(response):
    if response.url.endswith('DELETED_AD'):
        logging.debug("deleted AD")
        return
    details = response.css('li[class*="addetailslist--detail"]')
    detail_map = {
        detail.xpath('.//text()').get().strip(): detail.css('span::text').get().strip()
        for detail in details
    }

    check_tags = response.css('li[class*="checktag"]::text').getall()

    location = strip_if_exist(response, '#viewad-locality::text')
    location_match = re.search(location_pattern, location)

    yield RealEstateItem(
        _id=strip_if_exist(response, '#viewad-ad-id-box li:nth-child(2)::text'),
        caption=strip_if_exist(response, 'h1::text'),
        benefits=','.join(check_tags),
        price=strip_if_exist(response, 'h2[class*="boxedarticle--price"]::text'),
        street=strip_if_exist(response, '#street-address::text'),
        location=location,
        zip_code=location_match.group("zipcode") if location_match else "",
        state=location_match.group("state") if location_match else "",
        city=location_match.group("city") if location_match else "",
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
        description=converter.handle(strip_if_exist(response, '#viewad-description-text')),
        date_inserted=strip_if_exist(response, '#viewad-extra-info span:nth-child(2)::text'),
        views=strip_if_exist(response, '#viewad-extra-info span:nth-child(1)::text'),
        offerer=strip_if_exist_else(response, '#viewad-contact .text-force-linebreak a::text',
                                    '#viewad-contact .text-force-linebreak::text'),
        offerer_phone_number=strip_if_exist(response, '#viewad-contact-phone a::text'),
        url=response.url,
        created_datetime=datetime.now()
    )


class KleinanzeigenSpider(scrapy.Spider):
    name = "kleinanzeigen"

    def start_requests(self):
        urls = [
            'https://www.kleinanzeigen.de/s-haus-kaufen/baden-wuerttemberg/anzeige:angebote/c208l7970',
            'https://www.kleinanzeigen.de/s-haus-kaufen/bayern/anzeige:angebote/c208l5510',
            'https://www.kleinanzeigen.de/s-haus-kaufen/berlin/anzeige:angebote/c208l3331',
            'https://www.kleinanzeigen.de/s-haus-kaufen/brandenburg/anzeige:angebote/c208l7711',
            'https://www.kleinanzeigen.de/s-haus-kaufen/bremen/anzeige:angebote/c208l1',
            'https://www.kleinanzeigen.de/s-haus-kaufen/hamburg/anzeige:angebote/c208l9409',
            'https://www.kleinanzeigen.de/s-haus-kaufen/hessen/anzeige:angebote/c208l4279',
            'https://www.kleinanzeigen.de/s-haus-kaufen/mecklenburg-vorpommern/anzeige:angebote/c208l61',
            'https://www.kleinanzeigen.de/s-haus-kaufen/niedersachsen/anzeige:angebote/c208l2428',
            'https://www.kleinanzeigen.de/s-haus-kaufen/nordrhein-westfalen/anzeige:angebote/c208l928',
            'https://www.kleinanzeigen.de/s-haus-kaufen/rheinland-pfalz/anzeige:angebote/c208l4938',
            'https://www.kleinanzeigen.de/s-haus-kaufen/saarland/anzeige:angebote/c208l285',
            'https://www.kleinanzeigen.de/s-haus-kaufen/sachsen/anzeige:angebote/c208l3799',
            'https://www.kleinanzeigen.de/s-haus-kaufen/sachsen-anhalt/anzeige:angebote/c208l2165',
            'https://www.kleinanzeigen.de/s-haus-kaufen/schleswig-holstein/anzeige:angebote/c208l408',
            'https://www.kleinanzeigen.de/s-haus-kaufen/thueringen/anzeige:angebote/c208l3548'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        cities = response.xpath('//h2[text()="Ort"]/../..').css('a[class="text-link-subdued"]::attr(href)').getall()
        yield from response.follow_all(cities, self.parse_city_page)

    def parse_city_page(self, response):
        article_links = response.css('.ellipsis').css('a::attr(href)').getall()

        yield from response.follow_all(article_links, parse_details_page)

        next_link = response.css('.pagination-next').css('a::attr(href)').get()
        if next_link is not None:
            print('Next Link: ' + next_link)
            yield response.follow(url=next_link, callback=self.parse_city_page)
