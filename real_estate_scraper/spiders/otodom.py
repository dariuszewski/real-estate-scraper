"""Run with scrapy runspider spiders/otodom.py -o test.csv"""
# consider change to: rassppi + pihole, seleniumhub + docker

import re
import json

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from real_estate_scraper.items import get_estate
from real_estate_scraper.drivers.chrome import OtoDomChromeDriver


class OtodomSpider(scrapy.Spider):

    name = 'otodom'
    allowed_domains = ['otodom.pl']
    start_urls = [
        'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?market=ALL&ownerTypeSingleSelect=ALL&daysSinceCreated=1&by=LATEST&direction=DESC&viewType=listing&lang=pl&searchingCriteria=sprzedaz&searchingCriteria=mieszkanie&page=1',
        'https://www.otodom.pl/pl/oferty/wynajem/mieszkanie/cala-polska?market=ALL&ownerTypeSingleSelect=ALL&daysSinceCreated=1&by=LATEST&direction=DESC&viewType=listing&lang=pl&searchingCriteria=wynajem&searchingCriteria=mieszkanie&page=1',
        'https://www.otodom.pl/pl/oferty/sprzedaz/dom/cala-polska?market=ALL&ownerTypeSingleSelect=ALL&daysSinceCreated=1&by=LATEST&direction=DESC&viewType=listing&lang=pl&searchingCriteria=sprzedaz&searchingCriteria=dom&page=1'
    ]
    
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
            for offer in offers:
                url = 'https://www.otodom.pl' + offer
                yield Request(url, callback=self.parse_ad)
            
            next_page_num = int(re.search(r"page=(\d+)", response.url).group(1)) + 1
            next_page_url = response.url[:response.url.index('page=')] + 'page=' + str(next_page_num)
            if next_page_num < 20:
                yield response.follow(next_page_url, self.parse)

    def parse_ad(self, response):

        raw_data = response.xpath('.//script[@id="__NEXT_DATA__"]/text()').extract_first()
        data = json.loads(raw_data)["props"]["pageProps"]['ad']
        data['request_url'] = response.request.url
        
        yield from get_estate(data=data)
