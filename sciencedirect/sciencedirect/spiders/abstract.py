import scrapy
from sciencedirect.items import SciencedirectItem
from scrapy.loader import ItemLoader

class AbstractSpider(scrapy.Spider):
    name = 'abstract'
    start_urls = [
        'https://www.sciencedirect.com/search?qs=image%20classification'
    ]
    
    def parse(self,response):
        for href in response.xpath("//div[@class='result-item-content']/h2/span/a/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

            next_page = response.xpath("//li[@class='pagination-link next-link']/a/@href").extract_first()
            if next_page is not None:
                next_page_link = response.urljoin(next_page)
                yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parse_dir_contents(self,response):
        l = ItemLoader(item=SciencedirectItem(),response=response)
        l.add_xpath('url', "//head/link[@rel='canonical']/@href")
        l.add_xpath('title',"//span[@class='title-text']/text()")
        l.add_xpath('abstract_text',"//div[@id='abstracts']/div/div/p/text()")
        
        yield l.load_item()
