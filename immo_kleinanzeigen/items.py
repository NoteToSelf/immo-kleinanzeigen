# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class RealEstateItem:
    _id: str
    caption: str
    benefits: str
    price: float
    street: str
    location: str
    zip_code: str  # to support 0-leading zip code
    state: str
    city: str
    area_living: float
    area_plot: float
    total_rooms: int
    bedrooms: int
    bathrooms: int
    available_from: str
    house_type: str
    floors: int
    year_build: int
    commission: str
    description: str
    date_inserted: date
    views: int
    offerer: str
    offerer_phone_number: str
    url: str
    created_datetime: datetime
