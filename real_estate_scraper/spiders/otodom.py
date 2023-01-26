import time
import json

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from real_estate_scraper.items import get_estate
from real_estate_scraper.drivers.chrome import OtoDomChromeDriver


class OtodomSpider(scrapy.Spider):

    name = 'otodom'
    allowed_domains = ['otodom.pl']

    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    
    page_number = 1

    estate_type = 'dom' # 'mieszkanie'
    ownership_type = 'sprzedaz' # wynajem


    def start_requests(self):
        # url = 'https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/cala-polska?market=ALL&ownerTypeSingleSelect=ALL&daysSinceCreated=3&by=LATEST&direction=DESC&viewType=listing&lang=pl&searchingCriteria=sprzedaz&searchingCriteria=dom&limit=72&page=1000'
        # tag = getattr(self, 'tag', None)
        # if tag is not None:
        #     url = url.replace('mieszkanie', tag) # dom
        url = f'https://www.otodom.pl/pl/oferty/{self.ownership_type}/{self.estate_type}/cala-polska?limit=72&market=ALL&ownerTypeSingleSelect=ALL&daysSinceCreated=3&by=LATEST&page={self.page_number}'

        yield scrapy.Request(url, self.parse)


    def parse(self, response):

        page_has_new_offers = not(bool(response.xpath('//h3[contains(text(),"Nie znaleźliśmy żadnych ogłoszeń")]').getall()))

        if page_has_new_offers:

            offers = response.css('a[data-cy*=listing-item-link]::attr(href)').getall()
            print(f'FOUND {str(len(offers))} OFFERS')
        
            for offer in offers:
                url = 'https://www.otodom.pl' + offer
                yield Request(url, callback=self.parse_ad)
        
            self.page_number += 1
            print(f'WILL LOAD {str(self.page_number)} PAGE')
            url = response.url[:response.url.index('page=')] + f'page={str(self.page_number)}'
            yield response.follow(url, self.parse)


    def parse_ad(self, response):

        raw_data = response.xpath('.//script[@id="__NEXT_DATA__"]/text()').extract_first()
        data = json.loads(raw_data)["props"]["pageProps"]['ad']
        data['request_url'] = response.request.url
        
        yield from get_estate(data=data)
