import time
import json

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from real_estate_scraper.items import get_estate
from drivers.chrome import OtoDomChromeDriver


class OtodomSpider(scrapy.Spider):

    name = 'otodom'
    allowed_domains = ['otodom.pl']
    start_urls = ['https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?page=1&limit=36&market=ALL&by=LATEST&direction=DESC&viewType=listing']
    custom_settings = {'CLOSE_SPIDER_PAGE_COUNT': 2}

    current_page = 1

    def before_requests(self):
        url = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?page=4&limit=36&market=ALL&by=LATEST&direction=DESC&viewType=listing'
        driver = OtoDomChromeDriver.init_webdriver()
        driver.get(url=url)
        OtoDomChromeDriver.confirm_consent(driver)
        driver.execute_script(script=OtoDomChromeDriver.page_scroll())
        time.sleep(2)
        sel = Selector(text=driver.page_source)
        self.max_page = int(max(sel.xpath('.//nav[@data-cy="pagination"]/button/text()').extract()))

        driver.quit()

    def parse(self, response):

        # this driver will be passed to parse_add() 
        driver = OtoDomChromeDriver.init_webdriver()
        driver.get(url=response.request.url)
        OtoDomChromeDriver.confirm_consent(driver)
        driver.execute_script(script=OtoDomChromeDriver.page_scroll())

        # get offers
        time.sleep(2)
        sel = Selector(text=driver.page_source)

        offers = sel.css('a[data-cy*=listing-item-link]::attr(href)').getall()
        for offer in offers[:]:
            url = 'https://www.otodom.pl' + offer
            yield Request(url, callback=self.parse_ad, cb_kwargs={'driver': driver}) 

        # next page
        for i in range(1, 2):
            url = f'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?page={str(i)}&limit=72&market=ALL&by=LATEST&direction=DESC&viewType=listing'
            yield response.follow(url, self.parse)

    def parse_ad(self, response, driver):
        driver.get(url=response.request.url)
        time.sleep(3)

        sel = Selector(text=driver.page_source)

        raw_data = sel.xpath('.//script[@id="__NEXT_DATA__"]/text()').extract_first()
        data = json.loads(raw_data)["props"]["pageProps"]['ad']
        data['request_url'] = response.request.url
        
        yield from get_estate(data=data)

        # # AD
        # id_ = data.get("id")
        # public_id = data.get("publicId")
        # slug = data.get("slug")
        # advertiser_type = data.get("advertiserType")
        # advert_type = data.get("advertType")
        # created_at = data.get("createdAt")
        # modified_at = data.get("modifiedAt")
        # description = data.get("description")
        # features = data.get("features")
        # title = data.get('title')
        # url = response.request.url

        # # TARGET
        # target = data.get('target', dict())
        
        # area = target.get('Area')
        # area_range = target.get('AreaRange')
        # build_year = target.get('Build_year')
        # building_floors_num = target.get('Building_floors_num')
        # building_material = target.get('Building_material')
        # building_ownership = target.get('Building_ownership')
        # building_type = target.get('Building_type')
        # construction_status = target.get('Construction_status')
        # country = target.get('Country')
        # deposit = target.get('Deposit')
        # equipment_types = target.get('Equipment_types')
        # extras_types = target.get('Extras_types')
        # floor_no = target.get('Floor_no')
        # heating = target.get('Heating')
        # market_type = target.get('MarketType')
        # offer_type = target.get('OfferType')
        # price = target.get('Price')
        # price_range = target.get('PriceRange')
        # price_per_m = target.get('Price_per_m')
        # proper_type = target.get('ProperType')
        # regular_user = target.get('RegularUser')
        # rent = target.get('Rent')
        # rooms_num = target.get('Rooms_num')
        # security_types = target.get('Security_types')
        # windows_type = target.get('Windows_type')
        # seller_id = target.get('seller_id')
        # user_type = target.get('user_type')

        # # LOCATION
        # location = data.get('location') or dict()

        # coordinates = location.get('coordinates', dict())
        # latitude = coordinates.get('latitude')
        # longitude = coordinates.get('longitude')
        
        # radius = location.get('mapDetails', dict()).get("radius")

        # address = location.get('address') or dict()
        # street = address.get('street', dict()).get('name')
        # street_number = address.get('street', dict()).get('number')
        # city = address.get('city', dict()).get('name')
        # county = address.get('county', dict()).get('name')
        # province = address.get('province').get('name')
        # postal_code = address.get('postalCode')

        # #OWNER
        # owner = data.get('owner') or dict()
        # owner_name = owner.get('name')
        # owner_id = owner.get('id')
        # owner_type = owner.get('type')
        # phones = owner.get('phones')

        # url = response.request.url
        # # self.driver.quit()
        # # to be json
        # yield {
        # 'id_': id_,
        # 'public_id': public_id,
        # 'slug': slug,
        # 'advertiser_type': advertiser_type,
        # 'advert_type': advert_type,
        # 'created_at': created_at,
        # 'modified_at': modified_at,
        # 'description': description,
        # 'features': features,
        # 'title': title,
        # 'url': url,
        # 'area': area,
        # 'area_range': area_range,
        # 'build_year': build_year,
        # 'building_floors_num': building_floors_num,
        # 'building_material': building_material,
        # 'building_ownership': building_ownership,
        # 'building_type': building_type,
        # 'construction_status': construction_status,
        # 'country': country,
        # 'deposit': deposit,
        # 'equipment_types': equipment_types,
        # 'extras_types': extras_types,
        # 'floor_no': floor_no,
        # 'heating': heating,
        # 'market_type': market_type,
        # 'offer_type': offer_type,
        # 'price': price,
        # 'price_range': price_range,
        # 'price_per_m': price_per_m,
        # 'proper_type': proper_type,
        # 'province': province,
        # 'regular_user': regular_user,
        # 'rent': rent,
        # 'rooms_num': rooms_num,
        # 'security_types': security_types,
        # 'title': title,
        # 'windows_type': windows_type,
        # 'seller_id': seller_id,
        # 'user_type': user_type,
        # 'latitude': latitude,
        # 'longitude': longitude,
        # 'radius': radius,
        # 'street': street,
        # 'street_number': street_number,
        # 'city': city,
        # 'county': county,
        # 'province': province,
        # 'postal_code': postal_code,
        # 'owner_name': owner_name,
        # 'owner_id': owner_id,
        # 'owner_type': owner_type,
        # 'phones': phones,
        # 'url': url
        #     }
        # self.driver.get('https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?page=1&limit=72&market=ALL&by=LATEST&direction=DESC&viewType=listing')
        # consent = self.driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        # consent.click()

        # yield Request(url,callback=self.parse_after_consent)


        # self.driver.close()
        # yield FormRequest.from_response(
        #                 response, 
        #                 formdata={"value":"Accept"}, 
        #                 callback=self.after_accept)
        # yield Request(
        #     "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?page=1&limit=72&market=ALL&by=LATEST&direction=DESC&viewType=listing", 
        #     callback=self.parse_list)

        # inspect_response(response, self)

# >>> ul = response.xpath('//*[@data-cy="listing-item-link"]/@href')
# >>> ul[1].get() 
# '/pl/oferta/kawalerka-z-duzym-balkonem-bienczyce-ID4jiWP'
# https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?page=1&limit=72&market=ALL&by=LATEST&direction=DESC&viewType=listing
# main_divs = response.xpath('//div[@data-cy="search.listing"]')
# main_div = response.xpath('//div[@data-cy="search.listing"]/h2[@data-cy="search.listing.title"]/text()')
# main_div = response.xpath('//div[@data-cy="search.listing"][1]') 
# links = response.xpath('//a[@data-cy="listing-item-link"]/@href').getall() 
# links = response.css('a[data-cy*=listing-item-link]')
# main = response.xpath('//*[@id="__next"]/div[2]/main/div/div[2]/div[1]/div[2]')
# lis = response.xpath('//li/a/@href').getall()
# https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?page=1&limit=36&market=ALL&by=DEFAULT&direction=DESC&viewType=listing&lang=pl&searchingCriteria=sprzedaz&searchingCriteria=mieszkanie
# fetch(url='https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?page=1&limit=36&market=ALL&by=DEFAULT&direction=DESC&viewType=listing&lang=pl&searchingCriteria=sprzedaz&searchingCriteria=mieszkanie', method='POST', formdata={'value':'Accept'})

# def cbf():
#     yield Request("https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?page=1&limit=36&market=ALL&by=DEFAULT&direction=DESC&viewType=listing&lang=pl&searchingCriteria=sprzedaz&searchingCriteria=mieszkanie")
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from scrapy.selector import Selector
# import time
# WEBDRIVER_PATH = 'C:\Program Files (x86)\chromedriver.exe' 
# chrome_options = Options() 
# chrome_options.add_experimental_option("detach", True)
# chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# driver = webdriver.Chrome(WEBDRIVER_PATH, options=chrome_options)
# driver.get(url='https://www.otodom.pl/')
# consent = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
# # time.sleep(3) # wait for selector to be loaded on page
# consent.click()
# url = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?page=1&limit=36&market=ALL&by=LATEST&direction=DESC&viewType=listing'
# driver.get(url=url)
# driver.execute_script(js_script)
# time.sleep(5)
# sel = Selector(text=driver.page_source)
# offers = sel.css('a[data-cy*=listing-item-link]').getall()

# def page_scroll():
#     SCROLL_PAUSE_TIME = 2
#     min_height = driver.execute_script("let minHeight = 0;")
#     max_height = driver.execute_script("const maxHeight = document.body.scrollHeight;")
#     for i in range(20):
#         driver.execute_script("window.scrollTo(0, minHeight);")
#         time.sleep(SCROLL_PAUSE_TIME)
#         driver.execute_script("minHeight += 1000;")

# js_page_scroll = """
# function pageScroll() {
#   window.scrollBy(0, 50); // horizontal and vertical scroll increments
#   scrolldelay = setTimeout('pageScroll()', 100); // scrolls every 100 milliseconds
#   if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
#     clearTimeout(scrolldelay);
#   }
# }
# pageScroll();
# """
# def page_is_loading(driver):
#     while True:
#         x = driver.execute_script("return document.readyState")
#         if x == "complete":
#             return True
#         else:
#             yield False


        # title = sel.xpath('normalize-space(.//h1[@data-cy="adPageAdTitle"]/text())').extract_first() # .re('(\[a-zA-z0-9 ]+)') # extract_first() 
        # price = sel.xpath('normalize-space(.//strong[@data-cy="adPageHeaderPrice"]/text())').extract_first()
        # price_per_meter = sel.xpath('normalize-space(.//div[@aria-label="Cena za metr kwadratowy"]/text())').extract_first()
        # location = sel.xpath('normalize-space(.//a[@aria-label="Adres"]/text())').extract() # to be fixed # can have full addr
        # can add advertiser phone number and name

        # mortgage = sel.xpath('normalize-space(.//span[@data-cy="ad.mortgage-simulator.monthly-installment"]/text())').extract_first()
        # downpayment = sel.xpath('normalize-space(.//span[@data-cy="ad.mortgage-simulator.downpayment-price"]/text())').extract_first()
        # loan_term = sel.xpath('.//span[@data-cy="ad.mortgage-simulator.loan-term"]/text()').extract_first()

        # area = sel.xpath('.//div[@aria-label="Powierzchnia"]/div[2]/div[1]/text()').extract_first()
        # ownership = sel.xpath('.//div[@aria-label="Forma własności"]/div[2]/div[1]/text()').extract_first()
        # rooms = sel.xpath('.//div[@aria-label="Liczba pokoi"]/div[2]/div[1]/text()').extract_first()
        # state = sel.xpath('.//div[@aria-label="Stan wykończenia"]/div[2]/div[1]/text()').extract_first()
        # floor = sel.xpath('.//div[@aria-label="Piętro"]/div[2]/div[1]/text()').extract_first()
        # balcony_garden_terrace = sel.xpath('.//div[@aria-label="Balkon / ogród / taras"]/div[2]/div[1]/text()').extract_first()
        # rent = sel.xpath('.//div[@aria-label="Czynsz"]/div[2]/div[1]/text()').extract_first()
        # parking = sel.xpath('.//div[@aria-label="Miejsce parkingowe"]/div[2]/div[1]/text()').extract_first()
        # remote_service = sel.xpath('.//div[@aria-label="Obsługa zdalna"]/div[2]/div[1]/text()').extract_first()
        # heating = sel.xpath('.//div[@aria-label="Ogrzewanie"]/div[2]/div[1]/text()').extract_first()

        # market = sel.xpath('.//div[@aria-label="Rynek"]/div[2]/div[1]/text()').extract_first()
        # advertiser = sel.xpath('.//div[@aria-label="Typ ogłoszeniodawcy"]/div[2]/div[1]/text()').extract_first()
        # availability = sel.xpath('.//div[@aria-label="Dostępne od"]/div[2]/div[1]/text()').extract_first()
        # construction_year = sel.xpath('.//div[@aria-label="Rok budowy"]/div[2]/div[1]/text()').extract_first()
        # construction_type = sel.xpath('.//div[@aria-label="Rodzaj zabudowy"]/div[2]/div[1]/text()').extract_first()
        # windows = sel.xpath('.//div[@aria-label="Okna"]/div[2]/div[1]/text()').extract_first()
        # elevator = sel.xpath('.//div[@aria-label="Winda"]/div[2]/div[1]/text()').extract_first()
        # media = sel.xpath('.//div[@aria-label="Media"]/div[2]/div[1]/text()').extract_first()
        # security = sel.xpath('.//div[@aria-label="Zabezpieczenia"]/div[2]/div[1]/text()').extract_first()
        # equipment = sel.xpath('.//div[@aria-label="Wyposażenie"]/div[2]/div[1]/text()').extract_first()
        # additional_info = sel.xpath('.//div[@aria-label="Informacje dodatkowe"]/div[2]/div[1]/text()').extract_first()
        # building_material = sel.xpath('.//div[@aria-label="Materiał budynku"]/div[2]/div[1]/text()').extract_first()
        # offer_id = sel.xpath('.//div[@class="css-j6nvwa euuef475"]/div[1]/text()').extract_first()
        # created_at = sel.xpath('.//div[@class="css-j6nvwa euuef475"]/div[3]/text()').extract_first()
        # updated_at = sel.xpath('.//div[@class="css-j6nvwa euuef475"]/div[4]/text()').extract_first()

        # contact_number = sel.xpath('.//a[contains(@href, "tel:")]/@href').extract_first()