import time

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver # consider splash, it's headless and can scroll
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 

class OtoDomChromeDriver():

    WEBDRIVER_PATH = 'C:\Program Files (x86)\chromedriver.exe' 
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service=ChromeService(ChromeDriverManager().install())

    @staticmethod
    def init_webdriver():
        return webdriver.Chrome(service=OtoDomChromeDriver.service,
         options=OtoDomChromeDriver.chrome_options)

    @staticmethod
    def scroll_page(driver):
        js_page_scroll = """
        function pageScroll() {
            window.scrollBy(0, 50); // horizontal and vertical scroll increments
            scrolldelay = setTimeout('pageScroll()', 100); // scrolls every 100 milliseconds
            if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
                clearTimeout(scrolldelay);
            }
        }
        pageScroll();
        """
        driver.execute_script(script=js_page_scroll)
        # return js_page_scroll

    @staticmethod
    def confirm_consent(driver, retries=1):
        if retries < 3:
            try:
                consent = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
                time.sleep(3) # wait for selector to be loaded on page
                consent.click()
            except NoSuchElementException:
                time.sleep(3)
                OtoDomChromeDriver.confirm_consent(driver, retries=retries+1)

    @staticmethod
    def execute(response):
        driver = OtoDomChromeDriver.init_webdriver()
        driver.get(url=response.request.url)
        OtoDomChromeDriver.confirm_consent(driver)
        OtoDomChromeDriver.scroll_page(driver)

        return driver
