import time
from selenium.webdriver import Chrome, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

from restaurant_lead_gen.helper import find_by_data_test_id


class TripAdvisorScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = Chrome()
        self.restaurant_elements = None

    def open_restaurant_page(self):
        self.driver.get('https://wolt.com/en/discovery/restaurants')
        # Waits for the cookie banner to load
        WebDriverWait(
            self.driver,
            10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//button[@data-localization-key="gdpr-consents.banner.accept-button"]'
            ))
        )

        # finds the cookie button and clicks
        cookie_button = self.driver.find_element(
            By.XPATH,
            '//button[@data-localization-key="gdpr-consents.banner.accept-button"]'
        )
        cookie_button.click()
        time.sleep(2)
        return self

    def set_location(self):
        # Clicks Location dropdown to set location
        location_dropdown = self.driver.find_element(
            By.XPATH,
            "//button[@data-test-id='header.address-select-button']"
        )
        location_dropdown.click()

        # waits for country select to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//select[@data-test-id='CountriesSelect']"
            ))
        )

        # selects Croatia as country
        country_dropdown = self.driver.find_element(
            By.XPATH,
            "//select[@data-test-id='CountriesSelect']"
        )
        country_dropdown_select = Select(country_dropdown)
        country_dropdown_select.select_by_value('HRV')

        # Type in Split into address
        street_name_search_bar = self.driver.find_element(
            By.XPATH,
            "//input[@data-test-id='AddressQueryInput']"
        )
        street_name_search_bar.clear()
        street_name_search_bar.send_keys('Split')
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="addressLocationForm"]/div/p'
            ))
        )
        street_name_search_bar.send_keys(Keys.RETURN)

        # wait for search form button to load up
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="addressLocationForm"]/div/button'
            ))
        )
        continue_button = self.driver.find_element(
            By.XPATH,
            '//*[@id="addressLocationForm"]/div/button'
        )
        time.sleep(2)
        continue_button.click()
        time.sleep(5)
        return self

    def fetch_all_restaurants(self):
        previous_content = None
        while True:
            # Scroll down
            self.driver.find_element(By.XPATH, '/html/body').send_keys(Keys.END)
            time.sleep(5)  # Adjust sleep time as necessary for content to load

            # Extract the current state of the content
            current_content = (self.driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[4]/div/div/div[3]/div[1]')
                               .get_attribute('innerHTML'))

            # Check if new data is the same as the old data
            if current_content == previous_content:
                self.restaurant_elements = self.driver.find_elements(
                    By.CLASS_NAME, 'sc-e9f2d1ce-0.gRDyXw'
                )
                break
            previous_content = current_content
        return self

    def get_restaurant_urls(self):
        urls = [link.get_attribute('href') for link in self.restaurant_elements]
        return urls

    def get_all_restaurant_details(self):
        urls = [link.get_attribute('href') for link in self.restaurant_elements]
        for url in urls:
            self.driver.get(url)
            response = self.__get_restaurant_details(self.driver)
            print(response)

    @staticmethod
    def __get_restaurant_details(restaurant_page_driver):
        WebDriverWait(restaurant_page_driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//button[@data-test-id='venue-more-info-button']"
            ))
        )
        restaurant_page_driver.find_element(By.XPATH, "//button[@data-test-id='venue-more-info-button']").click()
        time.sleep(10)
        name = find_by_data_test_id(restaurant_page_driver, 'h2', 'VenueLargeHeader').text
        address_elements = restaurant_page_driver.find_elements(By.CLASS_NAME, 'sc-28740013-2.fsNozy')
        restaurant_page_driver.execute_script("arguments[0].scrollIntoView();", address_elements[0])
        address = ', '.join([each_element.text for each_element in address_elements])
        phone_and_website = restaurant_page_driver.find_elements(By.CLASS_NAME, 'sc-8bf8f335-0.jkafta')
        restaurant_page_driver.execute_script("arguments[0].scrollIntoView();", phone_and_website[0])
        phone = phone_and_website[0].text
        restaurant_page_driver.execute_script("arguments[0].scrollIntoView();", phone_and_website[1])
        website = phone_and_website[1].text
        return {
            'name': name,
            'address': address,
            'phone': phone,
            'website': website
        }
