import booking.constants as const
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from prettytable import PrettyTable


class Booking(webdriver.Firefox):
    _wait = None

    def __init__(self, options: Options = None, service: Service = None, keep_alive: bool = True, teardown: bool = False) -> None:
        """
        Initializes a new instance of the class.

        :param options: An instance of Options to configure the class. Default is None.
        :param service: An instance of Service for the class to use. Default is None.
        :param keep_alive: A boolean flag to keep the instance alive. Default is True.
        """
        self.teardown = teardown
        options = webdriver.FirefoxOptions()

        # Set logging level to reduce logs, adjust as needed
        options.set_preference('devtools.console.stdout.content', False)
        # # Set up desired capabilities, specifically to adjust logging
        # capabilities = DesiredCapabilities.FIREFOX
        # capabilities['loggingPrefs'] = {'browser': 'SEVERE', 'driver': 'SEVERE'}

        super(Booking, self).__init__(options, service,
                                      keep_alive)  # Instantiate the webdriver
        self.implicitly_wait(15)
        self.maximize_window()
        self._wait = WebDriverWait(self, 5)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def close_modal(self):
        try:
            modal_element = self.find_element(
                By.CSS_SELECTOR, 'div[aria-modal="true"]')
            if modal_element:
                close_modal_btn = self.find_element(
                    By.CSS_SELECTOR, 'button[aria-label="關閉登入的資訊。"]')
                close_modal_btn.click()
                self.implicitly_wait(5)
        except (NoSuchElementException, TimeoutException):
            print("Modal element Not Found")

    def land_first_page(self):
        self.get(const.BASE_URL)
        self.close_modal()

    def change_currency(self, currency=None):
        try:
            currency_element = self._wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')))
            # wait until only can be used with Certain condiction of "EC"

            self._wait.until(EC.invisibility_of_element(
                (By.CSS_SELECTOR, "div.eb33ef7c47")))  # wait until obscured object disappear
            currency_element.click()
            self._wait.until(EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, 'div[aria-label="選擇您使用的貨幣"]')))
            # f keyword is like template literal `` in javascript
            parent_button = self._wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//button[.//span[text()='{currency}']]")))
            if parent_button:
                parent_button.click()
        except (NoSuchElementException, TimeoutException):
            print("Currency element Not Found")

    def select_place_to_go(self, place_to_go, place_choose=0):
        search_input = self.find_element(By.ID, ":re:")
        search_input.clear()  # clear input
        search_input.send_keys(place_to_go)
        # wait until only can be used with Certain condiction of "EC"
        # self._wait.until(EC.invisibility_of_element(
        #     (By.CSS_SELECTOR, "div.eb33ef7c47")))  # wait until obscured object disappear
        try:
            place_option = self._wait.until(EC.element_to_be_clickable(
                (By.ID, f"autocomplete-result-{place_choose}")))
            if place_option:
                place_option.click()
        except (NoSuchElementException, TimeoutException):
            print("Place option element not found or not visible in time")

    def select_dates(self, check_in_date, check_out_date):
        try:
            check_in_element = self._wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, f'//td[.//span[@data-date="{check_in_date}"]]'))
            )
            check_in_element.click()
            check_out_element = self._wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, f'//td[.//span[@data-date="{check_out_date}"]]'))
            )
            check_out_element.click()
            self.close_modal()
        except (NoSuchElementException, TimeoutException):
            print("Dates option element not found or not visible in time")

    def select_adults(self, count=1):
        selection_element = self.find_element(
            By.XPATH, '//div[@data-testid="searchbox-layout-wide"]//button[@aria-controls=":rf:"]')
        self.implicitly_wait(2)
        selection_element.click()
        while True:
            decrease_adults_elemnet = self.find_element(
                By.XPATH, f'(//div[@data-testid="occupancy-popup"]//button[@type="button"])[1]')
            decrease_adults_elemnet.click()
            # If the value of adults reaches 1, then we should get out of the loop
            adults_value_element = self.find_element(By.ID, 'group_adults')
            adults_value = adults_value_element.get_attribute(
                'value')  # get input value
            if int(adults_value) == 1:
                break

        increase_adults_elemnet = self.find_element(
            # The "@" syntax is used for searching attribute
            By.XPATH, f'(//div[@data-testid="occupancy-popup"]//button[@type="button"])[2]')
        for _ in range(count - 1):
            increase_adults_elemnet.click()

    def click_search(self):
        search_btn = self.find_element(
            By.XPATH, f'(//div[@data-testid="searchbox-layout-wide"]//button[@type="submit"])')
        search_btn.click()

    def apply_filtrations(self):
        # Here is initiating the new instance here
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(4, 5)
        # filtration.sort_rate_lowest_first()

    def report_results(self):
        hotel_boxes = self.find_element(By.CLASS_NAME, 'd4924c9e74')
        booking_report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price", "Hotel Score"])
        table.add_rows(booking_report.pull_deal_boxes_attributes())
        print(table)
        # return hotel_boxes
