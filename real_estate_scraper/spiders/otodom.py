import time
import re 

import scrapy
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector

from scrapy.shell import inspect_response
from scrapy_selenium import SeleniumRequest

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By



class OtodomSpider(scrapy.Spider):

    name = 'otodom'
    allowed_domains = ['otodom.pl']
    start_urls = ['https://www.otodom.pl/']
    custom_settings = {'CLOSE_SPIDER_PAGE_COUNT': 1}


    WEBDRIVER_PATH = 'C:\Program Files (x86)\chromedriver.exe' 

    js_page_scroll = """
    function pageScroll() {
        window.scrollBy(0, 50); // horizontal and vertical scroll increments
        scrolldelay = setTimeout('pageScroll()', 100); // scrolls every 100 milliseconds
        if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
            clearTimeout(scrolldelay);
        }
    }
    pageScroll();
    """

    def start_requests(self):
        # from selenium.webdriver.support import expected_conditions as EC 
        # TODO: GO TO THE NEXT PAGE!
        url = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?page=1&limit=36&market=ALL&by=LATEST&direction=DESC&viewType=listing'

        # THIS IS TO CONSENT TO TERMS AND CONDITIONS
        chrome_options = Options() 
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(self.WEBDRIVER_PATH, options=chrome_options)
        self.driver.get(url='https://www.otodom.pl/')

        def confirm_consent():
            consent = self.driver.find_element(By.ID, 'onetrust-accept-btn-handler')
            time.sleep(3) # wait for selector to be loaded on page
            consent.click() 
        
        try:
            confirm_consent()
        except NoSuchElementException:
            self.logger.info('Waiting for consent window...')
            time.sleep(10)
            confirm_consent()

        ############################################

        self.driver.get(url=url)
        self.driver.execute_script(self.js_page_scroll)
        time.sleep(5)

        sel = Selector(text=self.driver.page_source)        
        offers = sel.css('a[data-cy*=listing-item-link]::attr(href)').getall()
        
        for offer in offers[:]:
            url = 'https://www.otodom.pl' + offer
            yield Request(url, callback=self.parse)

    def parse(self, response):
        self.driver.get(url=response.request.url)
        # self.driver.execute_script(self.js_page_scroll)
        sel = Selector(text=self.driver.page_source)
        title = sel.xpath('normalize-space(.//h1[@data-cy="adPageAdTitle"]/text())').extract_first() # .re('(\[a-zA-z0-9 ]+)') # extract_first() 
        price = sel.xpath('normalize-space(.//strong[@data-cy="adPageHeaderPrice"]/text())').extract_first()
        price_per_meter = sel.xpath('normalize-space(.//div[@aria-label="Cena za metr kwadratowy"]/text())').extract_first()
        location = sel.xpath('normalize-space(.//a[@aria-label="Adres"]/text())').extract() # to be fixed # can have full addr
        # can add advertiser phone number and name

        mortgage = sel.xpath('normalize-space(.//span[@data-cy="ad.mortgage-simulator.monthly-installment"]/text())').extract_first()
        downpayment = sel.xpath('normalize-space(.//span[@data-cy="ad.mortgage-simulator.downpayment-price"]/text())').extract_first()
        loan_term = sel.xpath('.//span[@data-cy="ad.mortgage-simulator.loan-term"]/text()').extract_first()

        area = sel.xpath('.//div[@aria-label="Powierzchnia"]/div[2]/div[1]/text()').extract_first()
        ownership = sel.xpath('.//div[@aria-label="Forma własności"]/div[2]/div[1]/text()').extract_first()
        rooms = sel.xpath('.//div[@aria-label="Liczba pokoi"]/div[2]/div[1]/text()').extract_first()
        state = sel.xpath('.//div[@aria-label="Stan wykończenia"]/div[2]/div[1]/text()').extract_first()
        floor = sel.xpath('.//div[@aria-label="Piętro"]/div[2]/div[1]/text()').extract_first()
        balcony_garden_terrace = sel.xpath('.//div[@aria-label="Balkon / ogród / taras"]/div[2]/div[1]/text()').extract_first()
        rent = sel.xpath('.//div[@aria-label="Czynsz"]/div[2]/div[1]/text()').extract_first()
        parking = sel.xpath('.//div[@aria-label="Miejsce parkingowe"]/div[2]/div[1]/text()').extract_first()
        remote_service = sel.xpath('.//div[@aria-label="Obsługa zdalna"]/div[2]/div[1]/text()').extract_first()
        heating = sel.xpath('.//div[@aria-label="Ogrzewanie"]/div[2]/div[1]/text()').extract_first()

        market = sel.xpath('.//div[@aria-label="Rynek"]/div[2]/div[1]/text()').extract_first()
        advertiser = sel.xpath('.//div[@aria-label="Typ ogłoszeniodawcy"]/div[2]/div[1]/text()').extract_first()
        availability = sel.xpath('.//div[@aria-label="Dostępne od"]/div[2]/div[1]/text()').extract_first()
        construction_year = sel.xpath('.//div[@aria-label="Rok budowy"]/div[2]/div[1]/text()').extract_first()
        construction_type = sel.xpath('.//div[@aria-label="Rodzaj zabudowy"]/div[2]/div[1]/text()').extract_first()
        windows = sel.xpath('.//div[@aria-label="Okna"]/div[2]/div[1]/text()').extract_first()
        elevator = sel.xpath('.//div[@aria-label="Winda"]/div[2]/div[1]/text()').extract_first()
        media = sel.xpath('.//div[@aria-label="Media"]/div[2]/div[1]/text()').extract_first()
        security = sel.xpath('.//div[@aria-label="Zabezpieczenia"]/div[2]/div[1]/text()').extract_first()
        equipment = sel.xpath('.//div[@aria-label="Wyposażenie"]/div[2]/div[1]/text()').extract_first()
        additional_info = sel.xpath('.//div[@aria-label="Informacje dodatkowe"]/div[2]/div[1]/text()').extract_first()
        building_material = sel.xpath('.//div[@aria-label="Materiał budynku"]/div[2]/div[1]/text()').extract_first()
        offer_id = sel.xpath('.//div[@class="css-j6nvwa euuef475"]/div[1]/text()').extract_first()
        created_at = sel.xpath('.//div[@class="css-j6nvwa euuef475"]/div[3]/text()').extract_first()
        updated_at = sel.xpath('.//div[@class="css-j6nvwa euuef475"]/div[4]/text()').extract_first()

        url = response.request.url
        # self.driver.quit()
        # to be json
        yield {
            'title': title,
            'price': price,
            'price_per_meter': price_per_meter,
            'location': location,
            'motgage': mortgage,
            'loan_term': loan_term,
            'downpayment': downpayment,
            'area': area,
            'ownership': ownership,
            'rooms': rooms,
            'state': state,
            'floor': floor,
            'balcony_garden_terrace': balcony_garden_terrace,
            'rent': rent,
            'parking': parking,
            'remote_service': remote_service,
            'heating': heating,
            'market': market,
            'advertiser': advertiser,
            'availability': availability,
            'construction_year': construction_year,
            'construction_type': construction_type,
            'windows': windows,
            'elevator': elevator,
            'media': media,
            'security': security,
            'equipment': equipment,
            'additional_info': additional_info,
            'building_material': building_material,
            'offer_id': offer_id,
            'created_at': created_at,
            'updated_at': updated_at,
            'url': url
            }
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


