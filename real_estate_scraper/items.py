# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import datetime
import re
from w3lib.html import remove_tags

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

# ssor MapCompose: field='floor_no' value=['ground_floor'] error='ValueError: Error in MapCompose with <class 'int'> value=['ground_floor'] error='ValueError: invalid literal for int() with base 10: ''''
def extract_floor(value):
    num = re.sub("[^*\d]", '', value)
    try:
        num = int(num)
        return num
    except ValueError:
        return 0

class RealEstateItem(scrapy.Item):
    # define the fields for your item here like:

    id_ = scrapy.Field(
        input_processor = MapCompose(int),
        output_processor = TakeFirst()
        )
    public_id = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    slug = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    advertiser_type = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()        
    )
    advert_type = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()        
    )
    created_at = scrapy.Field(
        input_processor = MapCompose(datetime.datetime.fromisoformat),
        output_processor = TakeFirst()
    )
    modified_at = scrapy.Field(
        input_processor = MapCompose(datetime.datetime.fromisoformat),
        output_processor = TakeFirst()
    )
    description = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )
    title = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()         
    )
    url = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst() 
    )
    area = scrapy.Field(
        input_processor = MapCompose(float),
        output_processor = TakeFirst() 
    )
    area_range_min = scrapy.Field(
        input_processor = MapCompose(lambda l: min([float(i) for i in l.split('-')]), float),
        output_processor = TakeFirst() 
    )
    area_range_max = scrapy.Field(
        input_processor = MapCompose(lambda l: max([float(i) for i in l.split('-')]), float),
        output_processor = TakeFirst() 
    )    
    building_floors_num = scrapy.Field(
        input_processor = MapCompose(lambda value: extract_floor(value=value), int),
        output_processor = TakeFirst() 
    )
    build_year = scrapy.Field(
        input_processor = MapCompose(int),
        output_processor = TakeFirst() 
    )
    building_material = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst() 
    )
    building_ownership = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()   
    )
    building_type = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()   
    )
    construction_status= scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()   
    )
    deposit = scrapy.Field(
        input_processor = MapCompose(float),
        output_processor = TakeFirst()   
    )
    equipment_types = scrapy.Field()
    extras_types = scrapy.Field()
    floor_no = scrapy.Field(
        input_processor = MapCompose(lambda value: extract_floor(value=value), int),
        output_processor = TakeFirst()   
    )
    heating = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()   
    )
    market_type = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()   
    )
    offer_type = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()   
    )
    price = scrapy.Field(
        input_processor = MapCompose(float),
        output_processor = TakeFirst()   
    )
    price_range_min = scrapy.Field(
        input_processor = MapCompose(lambda l: min([float(i) for i in l.split('-')]), float),
        output_processor = TakeFirst() 
    )
    price_range_max = scrapy.Field(
        input_processor = MapCompose(lambda l: max([float(i) for i in l.split('-')]), float),
        output_processor = TakeFirst() 
    )
    price_per_m = scrapy.Field(
        input_processor = MapCompose(float),
        output_processor = TakeFirst()
    )
    proper_type = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    regular_user = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    rent = scrapy.Field(
        input_processor = MapCompose(float),
        output_processor = TakeFirst()
    )
    rooms_num = scrapy.Field(
        input_processor = MapCompose(int),
        output_processor = TakeFirst()
    )
    security_types = scrapy.Field()
    title = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    windows_type = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    seller_id = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    user_type = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()        
    )
    latitude = scrapy.Field(
        input_processor = MapCompose(float),
        output_processor = TakeFirst()
    )
    longitude = scrapy.Field(
        input_processor = MapCompose(float),
        output_processor = TakeFirst()
    )
    radius = scrapy.Field(
        input_processor = MapCompose(float),
        output_processor = TakeFirst()
    )
    street = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    street_number = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    city = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    county = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    province = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    postal_code = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    owner_name = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    owner_id = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    owner_type = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    phones = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )



def get_estate(data):
    item_loader = ItemLoader(item=RealEstateItem(), data=data)

    # AD DATA
    item_loader.add_value("id_", data.get("id"))
    item_loader.add_value("public_id", data.get("publicId"))
    item_loader.add_value("slug", data.get("slug"))
    item_loader.add_value("advertiser_type", data.get("advertiserType"))
    item_loader.add_value("advert_type", data.get("advertType"))
    item_loader.add_value("created_at", data.get("createdAt"))
    item_loader.add_value("public_id", data.get("publicId"))
    item_loader.add_value("created_at", data.get("createdAt"))
    item_loader.add_value("modified_at", data.get("modifiedAt"))
    item_loader.add_value("description", data.get("description"))
    item_loader.add_value("title", data.get('title'))
    item_loader.add_value("url", data.get('request_url'))

    # TARGET DATA
    target = data.get('target') or dict()

    item_loader.add_value("area", target.get('Area'))
    # item_loader.add_value("area_range", target.get('AreaRange'))
    item_loader.add_value("area_range_min", target.get('AreaRange'))
    item_loader.add_value("area_range_max", target.get('AreaRange'))
    item_loader.add_value("build_year", target.get('Build_year'))
    item_loader.add_value("building_floors_num", target.get('Building_floors_num'))
    item_loader.add_value("building_material", target.get('Building_material'))
    item_loader.add_value("building_ownership", target.get('Building_ownership'))
    item_loader.add_value("building_type", target.get('Building_type'))
    item_loader.add_value("construction_status", target.get('Construction_status'))
    item_loader.add_value("deposit", target.get('Deposit'))
    item_loader.add_value("equipment_types", target.get('Equipment_types'))
    item_loader.add_value("extras_types", target.get('Extras_types'))
    item_loader.add_value("floor_no", target.get('Floor_no'))
    item_loader.add_value("heating", target.get('Heating'))
    item_loader.add_value("market_type", target.get('MarketType'))
    item_loader.add_value("offer_type", target.get('OfferType'))
    item_loader.add_value("price", target.get('Price'))
    # item_loader.add_value("price_range", target.get('PriceRange'))
    item_loader.add_value("price_range_min", target.get('PriceRange'))
    item_loader.add_value("price_range_max", target.get('PriceRange'))
    item_loader.add_value("price_per_m", target.get('Price_per_m'))
    item_loader.add_value("proper_type", target.get('ProperType'))
    item_loader.add_value("regular_user", target.get('RegularUser'))
    item_loader.add_value("rent", target.get('Rent'))
    item_loader.add_value("rooms_num", target.get('Rooms_num'))
    item_loader.add_value("security_types", target.get('Security_types'))
    item_loader.add_value("windows_type", target.get('Windows_type'))
    item_loader.add_value("seller_id", target.get('seller_id'))
    item_loader.add_value("user_type", target.get('user_type'))

    # LOCATION DATA
    location = data.get('location') or dict()
    coordinates = location.get('coordinates') or dict()
    address = location.get('address') or dict()
    street = address.get('street') or dict()
    city = address.get('city') or dict()
    county = address.get('city') or dict()
    province = address.get('province') or dict()

    item_loader.add_value("latitude", coordinates.get('latitude'))
    item_loader.add_value("longitude", coordinates.get('longitude'))
    
    item_loader.add_value("radius", location.get('mapDetails', dict()).get("radius"))

    item_loader.add_value("street", street.get('name'))
    item_loader.add_value("street_number", street.get('number'))
    item_loader.add_value("city", city.get('name'))
    item_loader.add_value("county", county.get('name'))
    item_loader.add_value("province", province.get('name'))
    item_loader.add_value("postal_code", address.get('postalCode'))

    #OWNER DATA
    owner = data.get('owner') or dict()
    item_loader.add_value("owner_name", owner.get('name'))
    item_loader.add_value("owner_id", owner.get('id'))
    item_loader.add_value("owner_type", owner.get('type'))
    item_loader.add_value("phones", owner.get('phones'))

    yield item_loader.load_item()
