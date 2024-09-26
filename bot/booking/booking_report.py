# This file is going to include method that will parse
# specific data taht we need from each one of the deal boxes
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class BookingReport:
    _wait = None

    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()
        self._wait = WebDriverWait(self.boxes_section_element, 5)

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(
            By.CSS_SELECTOR, '[aria-label="住宿"]')

    def pull_deal_boxes_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            # Pulling the hotel attribute
            try:
                hotel_name_element = WebDriverWait(deal_box, 10).until(
                    lambda x: x.find_element(
                        By.CSS_SELECTOR, 'div[data-testid="title"]')
                )
                hotel_name = hotel_name_element.get_attribute(
                    'innerHTML').strip()
                hotel_price_element = WebDriverWait(deal_box, 10).until(
                    lambda x: x.find_element(
                        By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]')
                )
                # still working on it for find the score text
                hotel_price = hotel_price_element.get_attribute(
                    'innerHTML').strip()
                hotel_score_element = WebDriverWait(deal_box, 10).until(
                    lambda x: x.find_element(
                        By.CSS_SELECTOR, 'div[data-testid= "review-score"]')
                )
                hotel_score = hotel_score_element.get_attribute(
                    'innerHTML').strip()
                collection.append([
                    hotel_name, hotel_price, hotel_score
                ])
            except (StaleElementReferenceException, TimeoutException) as stale:
                print(f"An error occurred: {stale}")

        return collection
