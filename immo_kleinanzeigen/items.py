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
    negotiable: bool
    street: str
    location: str
    zip_code: str  # to support 0-leading zip code
    state: str
    city: str
    latitude: float
    longitude: float
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
    offerer_rating: str
    offerer_friendliness: str
    offerer_reliability: str
    offerer_type: str
    offerer_active_since: date
    offerer_phone_number: str
    web_url: str
    ios_url: str
    android_url: str
    created_datetime: datetime
    images: list[str]
