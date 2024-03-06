# Filter the booking results
from typing import Callable
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


class BookingFiltration:
    _wait = None

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self._wait = WebDriverWait(self.driver, 5)

    def apply_star_rating(self, *star_nums):
        star_filtration_box = self.driver.find_element(
            By.XPATH, f'(//div[@data-testid="filters-sidebar"]//div[@data-testid="filters-group"][contains(.,"住宿評等")])')
        star_child_elements = star_filtration_box.find_elements(
            By.CSS_SELECTOR, '*')
        self._wait.until(EC.invisibility_of_element(
            (By.CSS_SELECTOR, "div.eb33ef7c47")))  # wait until obscured object disappear
        for star_num in star_nums:
            for star_element in star_child_elements:
                # strip for clearing white space
                try:
                    element_text = star_element.text.strip()
                    if (element_text == f'{star_num} 星級'):
                        star_element.click()
                except StaleElementReferenceException:
                    # Handle the exception or refetch the element as needed
                    pass
                # print(str(star_element.get_attribute('innerHTML')).strip())

    def sort_rate_lowest_first(self):
        dropDown_element = self.driver.find_element(
            By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]')
        dropDown_element.click()
        try:
            # price_rate_btn = self.driver.find_element(
            #     By.XPATH, f'(//div[@data-testid="sorters-dropdown"]//button[@data-id="price"])')
            self._wait.until(EC.visibility_of_all_elements_located(
                (By.ID, ':r3u:')))
            sort_rate_btn = self._wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//div[@data-testid="sorters-dropdown"]//button[@data-id="class_asc"]')))

            if (sort_rate_btn):
                sort_rate_btn.click()
        except (NoSuchElementException, TimeoutException):
            print("sort rate button element Not Found")
