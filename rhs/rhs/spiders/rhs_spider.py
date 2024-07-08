import json
from pathlib import Path
import re
import time

import requests
from rhs.items import RhsItem
from fake_useragent import UserAgent

import scrapy


class RhsSpider(scrapy.Spider):
    name = "rhs"

    def start_requests(self):
        url = "https://lwapp-uks-prod-psearch-01.azurewebsites.net/api/v1/plants/search/advanced"

        startFrom = 0
        totalHit = 100
        while startFrom < totalHit:
            payload = json.dumps({
                "startFrom": startFrom,
                "pageSize": 100,
                "includeAggregation": False
            })
            ua = UserAgent()
            headers = {
                'Authorization': '',
                'User-Agent': ua.random,
                'Content-Type': 'application/json'
            }
            response = requests.request("POST",
                                        url,
                                        headers=headers,
                                        data=payload)
            data = response.json()
            totalHit = data['totalHit']
            startFrom += 100
            for hit in data['hits']:
                name = hit['botanicalName']
                name = name.replace('em', '')
                name = '-'.join(re.findall(r'[a-zA-Z0-9]+', name)).lower()
                _url = "https://www.rhs.org.uk/plants/%d/%s/details" % (
                    hit['id'], name)

                yield scrapy.Request(
                    url=_url,
                    callback=self.parse,
                    headers=headers,
                )
                time.sleep(1)

    def parse(self, response):
        item = RhsItem()

        div = response.xpath(
            '//*[@id="skip-content"]/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div'
        )
        headE = div.xpath('./div[2]/div/div[1]/div[1]/div')

        item['name'] = headE.css('h1 span').xpath('string(.)').extract_first()

        temp = headE.xpath('p/text()').extract()
        if len(temp)==2:
            item['summary'], item['ngcontent'] = temp
        else:
            item['ngcontent'] = temp[0]

        attributesE = div.xpath('./div[3]/div')
        sizeE = attributesE.xpath('./div[1]/div[2]/div')
        size = {}
        size['ultimateHeight'] = sizeE.xpath(
            './div[1]/div/div/div[2]/text()').get()
        size['timeToUltimateHeight'] = sizeE.xpath(
            './div[2]/div/div/div[2]/text()').get()
        size['ultimateSpread'] = sizeE.xpath(
            './div[3]/div/div/div[2]/text()').get()

        item['size'] = size

        GrowingConditionsE = attributesE.xpath('./div[2]/div[2]')
        growingConditions = {}
        growingConditions['soil'] = GrowingConditionsE.css(
            'div.flag__body::text').extract()
        growingConditions['moisture'] = GrowingConditionsE.xpath(
            './div[2]/div[1]/div/span/text()').get()
        growingConditions['ph'] = GrowingConditionsE.xpath(
            './div[2]/div[2]/div/span/text()').getall()

        item['growingConditions'] = growingConditions

        trs = response.css('table tr')
        colours = {}
        cols = []
        for i in range(len(trs)):
            if i == 0:
                cols = trs[i].css('td::text').getall()
            else:
                th = trs[i].css('th::text').get()
                colours[th] = {}
                tds = trs[i].css('td')
                for j in range(len(tds)):
                    colours[th][cols[j]] = tds[j].css(
                        'span span.tooltip-v2__content::text').getall()
        item['colours'] = colours

        positionE = attributesE.xpath('./div[4]/div[2]')
        position = {}
        position['sun'] = positionE.css('.flag__body::text').getall()
        aspects = positionE.xpath('./p/span/text()').getall()
        position['aspect'] = ''.join(aspects)
        exposure = positionE.xpath('./div/div[1]/div/span/text()').extract()
        position['exposure'] = ''.join(exposure)
        position['hardiness'] = positionE.xpath(
            './div/div[2]/div/span/text()').get()
        item['position'] = position

        urls = response.css('.cover-image__img::attr(style)').extract()
        print(urls)
        pattern = re.compile(r"url\s*\(['\"]?(https?://[^'\")]+)['\"]?\)")
        item['image_urls'] = [pattern.findall(url)[0] for url in urls]

        yield item
