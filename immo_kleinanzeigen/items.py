# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class RealEstateItem:
    id: str
    caption: str
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
    date_inserted: date
    views: int
    offerer: str
    offerer_phone_number: str
    url: str
    created_datetime: datetime
    hash: int

    def get_id(self):
        return self.id

    def get_hash(self):
        return self.hash

    def set_hash(self, value):
        self.hash = value

    def __eq__(self, other):
        return (
            self.id == other.id and
            self.hash == other.hash
        )

    def __hash__(self):
        return hash((
            self.id,
            self.caption,
            self.price,
            self.street,
            self.location,
            self.zip_code,
            self.state,
            self.city,
            self.area_living,
            self.area_plot,
            self.total_rooms,
            self.bedrooms,
            self.bathrooms,
            self.available_from,
            self.house_type,
            self.floors,
            self.year_build,
            self.commission,
            self.views,
            self.offerer,
            self.offerer_phone_number
        ))
