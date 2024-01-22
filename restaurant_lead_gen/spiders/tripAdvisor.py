import scrapy


class TripadvisorSpider(scrapy.Spider):
    name = "tripAdvisor"
    allowed_domains = ["www.tripadvisor.com"]
    start_urls = ["https://www.tripadvisor.com/"]

    def parse(self, response):
        pass
