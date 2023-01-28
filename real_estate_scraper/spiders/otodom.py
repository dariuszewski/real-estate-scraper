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
    
    page_number = 1

    def start_requests(self):
        url = 'https://www.otodom.pl/pl/oferty/sprzedaz/dom/cala-polska?market=ALL&ownerTypeSingleSelect=ALL&daysSinceCreated=3&by=LATEST&direction=DESC&viewType=listing&lang=pl&searchingCriteria=sprzedaz&searchingCriteria=dom&limit=36&page=1'
        # tag = getattr(self, 'tag', None)
        # if tag is not None:
        #     url = url.replace('mieszkanie', tag) # dom
        yield scrapy.Request(url, self.parse) # consider change to: rassppi + pihole, seleniumhub + docker

    def parse(self, response):

        # this is to get a full list of ads in 1 page
        driver = OtoDomChromeDriver.execute(response=response)

        # get urls and check if page have new offers
        sel = Selector(text=driver.page_source)
        page_has_new_offers = not(bool(sel.xpath('//h3[contains(text(),"Nie znaleźliśmy żadnych ogłoszeń")]').getall()))
        offers = sel.css('a[data-cy*=listing-item-link]::attr(href)').getall()

        # close driver after successfully parsing urls to the ads.
        driver.close()
        driver.quit()

        if page_has_new_offers:
            for offer in offers[:]:
                url = 'https://www.otodom.pl' + offer
                yield Request(url, callback=self.parse_ad)
            
            self.page_number += 1
            print(f"new page number is {self.page_number}")
            url = response.url[:response.url.index('page=')] + 'page=' + str(self.page_number)
            yield response.follow(url, self.parse)

    def parse_ad(self, response):

        raw_data = response.xpath('.//script[@id="__NEXT_DATA__"]/text()').extract_first()
        data = json.loads(raw_data)["props"]["pageProps"]['ad']
        data['request_url'] = response.request.url
        
        yield from get_estate(data=data)
