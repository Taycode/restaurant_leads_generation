from selenium.webdriver.common.by import By


def find_by_attribute(driver, tag: str, attr: str, value: str):
    return driver.find_element(By.XPATH, f"//{tag}[@{attr}='{value}']")


def find_by_data_test_id(driver, tag: str, value: str):
    return find_by_attribute(driver, tag, 'data-test-id', value)
