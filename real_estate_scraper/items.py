# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import datetime

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

from .items_utils import *


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
    # description = scrapy.Field(
    #     input_processor = MapCompose(remove_tags),
    #     output_processor = TakeFirst()
    # )
    title = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()         
    )
    url = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst() 
    )
    terrain_area = scrapy.Field(
        input_processor = MapCompose(float),
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
    estate_floors_num = scrapy.Field(
        input_processor = MapCompose(str),
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
    floor_no = scrapy.Field(
        input_processor = MapCompose(lambda value: extract_floor(value=value), int),
        output_processor = TakeFirst()   
    )
    heating = scrapy.Field(
            input_processor = MapCompose(str),
            output_processor = TakeFirst()
    )
    heating_2 = scrapy.Field(
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
        input_processor = MapCompose(lambda value: translate_proper_type(value), str),
        output_processor = TakeFirst()
    )
    regular_user = scrapy.Field(
        input_processor = MapCompose(lambda value: translate_regular_user(value), bool),
        output_processor = TakeFirst()
    )
    rent = scrapy.Field(
        input_processor = MapCompose(float),
        output_processor = TakeFirst()
    )
    rooms_num = scrapy.Field(
        input_processor = MapCompose(lambda value: extract_rooms_count(value), int),
        output_processor = TakeFirst()
    )
    title = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )
    windows_type = scrapy.Field(
        input_processor = MapCompose(str),
        output_processor = TakeFirst()
    )

    # SELLER AND LOCATION
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

    # FEATURES & MEDIA
    air_conditioning = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    alarm = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    anti_burglary_door = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    attic = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    balcony = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    basement = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    cable_television = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    cesspool = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    closed_area = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    dishwasher = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    electricity = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    entryphone = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    fridge = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    furniture = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    garage = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    garden = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    gas = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    internet = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    lift = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    monitoring = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    oven = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    phone = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    pool = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    roller_shutters = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    separate_kitchen = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    sewage = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    stove = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    terrace = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    tv = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    usable_room = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    water = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    water_purification = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    washing_machine = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    forest = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    lake = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    mountains = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    access_type = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    fence = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    roof_type = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    roofing = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )
    location_type = scrapy.Field(
        input_processor = MapCompose(bool),
        output_processor = TakeFirst()
    )

    # FEATURES AND MEDIAS BY CATEGORY
    all_features = scrapy.Field()

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
    # item_loader.add_value("description", data.get("description"))
    item_loader.add_value("title", data.get('title'))
    item_loader.add_value("url", data.get('request_url'))

    # TARGET DATA
    target = data.get('target') or dict()
    heating_types = target.get('Heating_types', [])

    item_loader.add_value("terrain_area", target.get('Terrain_area'))
    item_loader.add_value("area", target.get('Area'))
    item_loader.add_value("area_range_min", target.get('AreaRange'))
    item_loader.add_value("area_range_max", target.get('AreaRange'))
    item_loader.add_value("build_year", target.get('Build_year'))

    item_loader.add_value("building_floors_num", target.get('Building_floors_num'))
    item_loader.add_value("estate_floors_num", target.get('Floors_num'))

    item_loader.add_value("building_material", target.get('Building_material'))
    item_loader.add_value("building_ownership", target.get('Building_ownership'))
    item_loader.add_value("building_type", target.get('Building_type'))
    item_loader.add_value("construction_status", target.get('Construction_status'))
    item_loader.add_value("deposit", target.get('Deposit'))
    item_loader.add_value("floor_no", target.get('Floor_no'))

    heating_1 = get_heating(target.get('Heating') or [], heating_types)
    heating_2 = get_secondary_heating(heating_1, heating_types)
    item_loader.add_value("heating", heating_1)
    item_loader.add_value('heating_2', heating_2)
    

    item_loader.add_value("market_type", target.get('MarketType'))
    item_loader.add_value("offer_type", translate_offer_type(target.get('OfferType')))
    item_loader.add_value("price", target.get('Price'))
    item_loader.add_value("price_range_min", target.get('PriceRange'))
    item_loader.add_value("price_range_max", target.get('PriceRange'))
    item_loader.add_value("price_per_m", target.get('Price_per_m'))
    item_loader.add_value("proper_type", target.get('ProperType'))
    item_loader.add_value("regular_user", target.get('RegularUser'))
    item_loader.add_value("rent", target.get('Rent'))
    item_loader.add_value("rooms_num", target.get('Rooms_num'))
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

    # HOUSE ONLY DATA
    item_loader.add_value('access_type', target.get('Access_types'))
    item_loader.add_value('fence', target.get('Fence_types'))
    item_loader.add_value('roof_type', target.get('Roof_type'))
    item_loader.add_value('roofing', target.get('Roofing'))
    item_loader.add_value('location_type', target.get('Location'))

    # FEATURES & MEDIAS
    media_list = target.get('Media_types') or list()
    security = target.get('Equipment_types') or list()
    equipment = target.get('Equipment_types') or list()
    extras = target.get('Extras_types') or list()
    vicinities =  target.get('Vicinity_types') or list()
    all_features = merge_all_features(security, equipment, extras, media_list, vicinities) or list()

    item_loader.add_value("all_features", all_features)
    item_loader.add_value("air_conditioning", has_feature(all_features, "air_conditioning"))
    item_loader.add_value("alarm", has_feature(all_features, "alarm"))
    item_loader.add_value("anti_burglary_door", has_feature(all_features, "anti_burglary_door"))
    item_loader.add_value("attic", has_feature(all_features, "attic"))
    item_loader.add_value("balcony", has_feature(all_features, "balcony"))
    item_loader.add_value("basement", has_feature(all_features, "basement"))
    item_loader.add_value("cable_television", has_feature(all_features, "cable_television"))
    item_loader.add_value("cesspool", has_feature(all_features, "cesspool"))
    item_loader.add_value("closed_area", has_feature(all_features, "closed_area"))
    item_loader.add_value("dishwasher", has_feature(all_features, "dishwasher"))
    item_loader.add_value("electricity", has_feature(media_list, "electricity"))
    item_loader.add_value("entryphone", has_feature(all_features, "entryphone"))
    item_loader.add_value("fridge", has_feature(all_features, "fridge"))
    item_loader.add_value("furniture", has_feature(all_features, "furniture"))
    item_loader.add_value("garage", has_feature(all_features, "garage"))
    item_loader.add_value("garden", has_feature(all_features, "garden"))
    item_loader.add_value("gas", has_feature(media_list, "gas"))
    item_loader.add_value("internet", has_feature(media_list, "internet"))
    item_loader.add_value("lift", has_feature(all_features, "lift"))
    item_loader.add_value("monitoring", has_feature(all_features, "monitoring"))
    item_loader.add_value("oven", has_feature(all_features, "oven"))
    item_loader.add_value("phone", has_feature(all_features, "phone"))
    item_loader.add_value("pool", has_feature(all_features, "pool"))
    item_loader.add_value("roller_shutters", has_feature(all_features, "roller_shutters"))
    item_loader.add_value("separate_kitchen", has_feature(all_features, "separate_kitchen"))
    item_loader.add_value("sewage", has_feature(all_features, "sewage"))
    item_loader.add_value("stove", has_feature(all_features, "stove"))
    item_loader.add_value("terrace", has_feature(all_features, "terrace"))
    item_loader.add_value("tv", has_feature(all_features, "tv"))
    item_loader.add_value("usable_room", has_feature(all_features, "usable_room"))
    item_loader.add_value("water", has_feature(all_features, "water"))
    item_loader.add_value("water_purification", has_feature(all_features, "water_purification"))
    item_loader.add_value("washing_machine", has_feature(all_features, "washing_machine"))
    item_loader.add_value("forest", has_feature(all_features, "forest"))
    item_loader.add_value("lake", has_feature(all_features, "lake"))
    item_loader.add_value("mountains", has_feature(all_features, "mountains"))

    #FEATURES BY CATEGORY
    # item_loader.add_value("equipment_types", target.get('Equipment_types'))
    # item_loader.add_value("extras_types", target.get('Extras_types'))
    # item_loader.add_value("security_types", target.get('Security_types'))
    # item_loader.add_value("all_medias", target.get('Media_types'))


    yield item_loader.load_item()

