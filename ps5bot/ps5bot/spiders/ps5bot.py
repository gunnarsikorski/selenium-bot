import scrapy
import time
from twilio.rest import Client
from selenium import webdriver
from scrapy.http import Request
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# client = Client("ACCOUNT_SID", "AUTH_TOKEN")


class BestbuySpider(scrapy.Spider):
   name = "bestbuy"
   USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) " \
                "Chrome/43.0.2357.130 Safari/537.36 "
   # Enter Your Product URL Here.
   start_urls = [
       "https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161", ]

   def parse(self, response):

       # Finding Product Status.
       try:
           product = response.xpath(
               "//*[@class='btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button']")
           if product:
               print(f"\nProduct is Currently: Available.\n")
           else:
               print("\nProduct is Out of Stock.\n")
       except NoSuchElementException:
           pass

       if product:
           print("\nFound 1 item to add to cart.\n")

           # Want to Receive text messages?
           client.messages.create(
               to="+13035515667", from_="+14158811380", body="Bot has made a Bestbuy purchase!")

           # Booting WebDriver.
           profile = webdriver.FirefoxProfile('/Users/gunnarsikorski/Library/Application Support/Firefox/Profiles/xw7kz0gz.default')
           driver = webdriver.Firefox(
               profile, executable_path=GeckoDriverManager().install())

           # Starting Webpage.
           driver.get(response.url)
           time.sleep(3)

           # Click Add to Cart.
           print("\nClicking Add To Cart Button.\n")
           driver.find_element_by_xpath(
               "//*[@class='btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button']").click()
           time.sleep(3)

           # Click Cart.
           print("\nGoing to Shopping Cart.\n")
           driver.get("https://www.bestbuy.com/cart")
           time.sleep(3)

           # Click Check-out Button.
           print("\nClicking Checkout Button.\n")
           driver.find_element_by_xpath(
               "//*[@class='btn btn-lg btn-block btn-primary']").click()

           # Giving Website Time To Login.
           print("\nGiving Website Time To Login..\n")
           wait = WebDriverWait(driver, 20)
           wait.until(EC.presence_of_element_located(
               (By.XPATH, "//*[@class='btn btn-lg btn-block btn-primary button__fast-track']")))
           time.sleep(3)

           # CVV Number Input.
           print("\nInputing CVV Number.\n")
           try:
               security_code = driver.find_element_by_id("credit-card-cvv")
               time.sleep(3)
               security_code.send_keys("513")
           except NoSuchElementException:
               pass

           # ARE YOU READY TO BUY?
           print("\nBuying Product.\n")
           driver.find_element_by_xpath(
               "//*[@class='btn btn-lg btn-block btn-primary button__fast-track']").click()

           print("\nBot has Completed Checkout.\n")
           time.sleep(1800)

       else:
           print("\nRetrying Bot In 10 Seconds.\n")
           time.sleep(10)
           yield Request(response.url, callback=self.parse, dont_filter=True)
