# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from dataclasses import dataclass


@dataclass
class RealEstateItem:
    id: str
    caption: str
    price: float
    area_living: float
    area_plot: float
