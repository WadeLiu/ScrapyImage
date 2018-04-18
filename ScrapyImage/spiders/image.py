import scrapy
from ScrapyImage.items import ItemPerson
from ScrapyImage.items import ItemImage
import re
import os

class image(scrapy.Spider):
    name = 'image'
    path = '/home/wade/Project/Scrapy/ScrapyImage/download/'
    #allowed_domains = ['mmonly.cc']

    def start_requests(self):
        for i in range(1,3):
            if i == 1:
                url = 'http://www.mmonly.cc/tag/mm/index.html'
            else:
                url = 'http://www.mmonly.cc/tag/mm/' + str(i) + '.html'
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        items = []
        self.log('--------------------------------------------------------')

        pattern=re.compile(r'<div class="title".*?<a.*?href="(.*?)">(.*?)</a></span></div>',re.S)
        mains = re.findall(pattern,response.text)

        for main in mains:
            itemPerson = ItemPerson()
            itemPerson['href'] = main[0]
            itemPerson['title'] = main[1]
            itemPerson['folder'] = self.path + itemPerson['title']
            items.append(itemPerson)
            print(itemPerson)
        print(items)

        '''
        for link in response.xpath('*//div[contains(@class, "title")]/span/a').extract():
            item = ItemPerson()
            link = link.encode('utf-8')
            print(link)
            item['title'] = link.xpath('a/text()')
            item['href'] = link.xpath('a/@href')[0].extract()
            print(item)
'''

        for itemPerson in items:
            folder = itemPerson['folder']
            if not os.path.exists(folder):
                os.makedirs(folder)
            yield scrapy.Request(url=itemPerson['href'], meta={'itemPerson':itemPerson}, callback=self.parse_personal)

        self.log('=======================================================')

    def parse_personal(self, response):
        itemPerson = response.meta['itemPerson']

        totalpage = response.xpath('//span[contains(@class, "totalpage")]/text()').extract_first()
        self.log('totalpage=' + totalpage)
        items = []

        for i in range(1, int(totalpage) + 1):
            itemImage = ItemImage()
            itemImage['filepath'] = itemPerson['folder'] + '/' + str(i) + '.jpg'
            if i == 0:
                itemImage['url'] = response.url
            else:
                itemImage['url'] = response.url[:-5] + '_' + str(i) + '.html'
            items.append(itemImage)

        for itemImage in items:
            yield scrapy.Request(url=itemImage['url'], meta={'itemImage':itemImage}, callback=self.parse_image)


    def parse_image(self, response):
        pattern=re.compile(r'<li class="pic-down h-pic-down"><a target="_blank" class="down-btn" href=\'(.*?)\'>.*?</a>',re.S)
        download = re.search(pattern,response.text).group(1)

        item = response.meta['itemImage']
        item['download'] = download

        yield item
