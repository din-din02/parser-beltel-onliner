from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageEnhance
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

class Parser():
    def __init__(self):
        self.byfly_link='https://issaold.beltelecom.by/main.html'
        self.path = r'D:\sx9657\parsing\1610\captcha\secpic4.png'
        #223.205.29.143:8080  Тайвань https
        self.profile = FirefoxProfile()
        self.profile.set_preference("general.useragent.override", "Godzilla/5.0 (Linux Ubuntu 22.04 LTS; x64; rv:22.04) Gecko/20100101 Firebox/121.0")

        # Ручная настройка прокси
        self.profile.set_preference("network.proxy.type", 1)  # 1 = ручная настройка
        self.profile.set_preference("network.proxy.http", "84.52.125.113")
        self.profile.set_preference("network.proxy.http_port", 8082)
        self.profile.set_preference("network.proxy.ssl", "84.52.125.113")
        self.profile.set_preference("network.proxy.ssl_port", 8082)
        self.profile.set_preference("network.proxy.no_proxies_on", "localhost, 127.0.0.1")
        options = Options()
        options.profile = self.profile
        self.driver = webdriver.Firefox(options=options)

    def photo(self):
        driver = self.driver
        driver.get('https://whatmyuseragent.com/')
        driver.get(self.byfly_link)
        print("Текущий User-Agent:", driver.execute_script("return navigator.userAgent;"))

        file_input = driver.find_element(By.XPATH, '//*[@id="capcher"]')
        file_input.screenshot(self.path)

        c = Captcha(self.path)
        c.photo_bright()
        captcha_text = c.get_capcha()

        cap_input = driver.find_element(By.XPATH, '//*[@id="cap_field"]')
        cap_input.clear()
        cap_input.send_keys(captcha_text)
        time.sleep(2)

        user = driver.find_element(By.XPATH, '//*[@id="oper_user"]')
        user.send_keys('Ka_karinochka')

        parol = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[2]/div[3]/form/div/div[2]/input')
        parol.send_keys('123456789k')
        time.sleep(5.5)

        button = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[2]/div[3]/form/div/div[4]/input')
        button.click()

        os.remove(r'D:\sx9657\parsing\1610\captcha\result.png')
        os.remove(self.path)

        driver.get('https://whatmyuseragent.com/')
        time.sleep(15)
        driver.quit()

    def __del__(self):
        print('driver quit')


class Captcha():
    def __init__(self, path):
        self.path=path

    def photo_bright(self):
        image = Image.open(self.path)

        if image.mode != "RGB":
            image = image.convert("RGB")

        brightness_factor = 1.1
        enhancer_b = ImageEnhance.Brightness(image)
        bright_img = enhancer_b.enhance(brightness_factor)

        contrast_factor = 1.4
        enhancer_c = ImageEnhance.Contrast(bright_img)
        final_img = enhancer_c.enhance(contrast_factor)

        final_img = final_img.convert('1')
        final_img.save(r'D:\sx9657\parsing\1610\captcha\result.png')

    def get_capcha(self):
        driver = webdriver.Chrome()
        driver.get('https://www.prepostseo.com/ru/image-to-text')
        file_inp = os.path.abspath(r'D:\sx9657\parsing\1610\captcha\result.png')

        wait = WebDriverWait(driver, 10)
        captcha_send = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        captcha_send.send_keys(file_inp)
        time.sleep(2)


        extrude_text_button = driver.find_element(By.XPATH, '/html/body/main/section[1]/div[4]/div[3]/div[1]')
        extrude_text_button.click()
        time.sleep(10)

        captcha_code = driver.find_element(By.XPATH, '//*[@id="result__text0"]').text
        time.sleep(5.5)
        driver.quit()
        print(captcha_code)
        return captcha_code

itog=Parser()
itog.photo()
print('okay')