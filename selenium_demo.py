import time

import selenium
from selenium import webdriver


options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1200x600')
options.add_argument('disable-gpu')
# 沙盒
options.add_argument('--no-sandbox')

options.add_argument("--disable-blink-features=AutomationControlled")  # 以开发者模式
driver = webdriver.Chrome(options=options)


driver.get("https://www.scorptec.com.au")

time.sleep(666)



