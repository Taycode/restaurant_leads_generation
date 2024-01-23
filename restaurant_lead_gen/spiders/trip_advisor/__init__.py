import scrapy
from scrapy.http import Response
from restaurant_lead_gen.spiders.trip_advisor.scraper import TripAdvisorScraper


class TripadvisorSpider(scrapy.Spider):
    name = "tripAdvisor"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selenium_scraper = TripAdvisorScraper()

    def start_requests(self):
        # Use Selenium to navigate and get the initial data
        (self.selenium_scraper
         .open_restaurant_page()
         .set_location()
         .fetch_all_restaurants())

        urls = self.selenium_scraper.get_restaurant_urls()

        self.selenium_scraper.driver.quit()

        for url in urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response: Response):

        name = response.xpath('//span[@data-test-id="venue-hero.venue-title"]/text()').get()
        # Extracting the address
        address_elements = response.css('.sc-584d6769-3.hezLfF::text').getall()
        # address_elements = list(filter(lambda x: bool(x), address_elements))

        address = f"{address_elements[0]}, {''.join(address_elements[1:])}"

        # Extracting the phone number
        phone_number = response.xpath('//a[starts-with(@href, "tel:")]/text()').get()

        # Extracting the website URL
        website_url = response.xpath('//a[contains(text(), "Visit website")]/@href').get()
        yield {
            'name': name,
            'address': address,
            'phone': phone_number,
            'website': website_url,
        }
