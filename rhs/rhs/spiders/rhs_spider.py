from pathlib import Path
import re
from rhs.items import RhsItem

import scrapy


class RhsSpider(scrapy.Spider):
    name = "rhs"

    def start_requests(self):
        urls = [
            "https://www.rhs.org.uk/plants/59375/hedera-helix-goldchild-(v)/details",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = RhsItem()

        div = response.xpath(
            '//*[@id="skip-content"]/app-root/app-plant-details-page/lib-plant-details-full/section[1]/div/div'
        )
        headE = div.xpath('./div[2]/div/div[1]/div[1]/div')

        item['name'] = headE.css('h1 span').xpath('string(.)').extract_first()

        item['summary'], item['ngcontent'] = headE.xpath('p/text()').extract()

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
        position['sun'] = positionE.xpath('./ul/li/div/div[2]/text()').get()
        aspects = positionE.xpath('./p/span/text()').getall()
        position['aspect'] = ''.join(aspects)
        position['exposure'] = positionE.xpath(
            './div/div[1]/div/span/text()').get()
        position['droughtResistance'] = positionE.xpath(
            './div/div[1]/div/span/text()').get()
        position['hardiness'] = positionE.xpath(
            './div/div[2]/div/span/text()').get()
        item['position'] = position

        urls = response.css('.cover-image__img::attr(style)').extract()
        pattern = re.compile(r"https.*?jpg")
        item['image_urls'] = [pattern.findall(url)[0] for url in urls]
        print(item)
        yield item