from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # For explicit wait
from selenium.webdriver.support import expected_conditions as EC

# wait for some condition to achieve

driver = webdriver.Firefox()
driver.get("https://www.seleniumeasy.com/playwright-tutorials")
driver.implicitly_wait(3)
element = driver.find_element(By.CLASS_NAME, "node-readmore")
element.click()
print(f"{element.__class__}")
