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

driver = webdriver.Firefox()
ads_list = []

driver.get('https://advanced.name/freeproxy/6ad1dfbbc360d?type=http?type=https')

def get_all_links_on_page(ads_list):
    elements = driver.find_element(By.XPATH, "/html/body/pre")


    text=elements.text
    proxi=text.strip().split("\n")
    for proxy in proxi:
        if proxy.strip(): 
            ads_list.append(proxy.strip())
    return ads_list



def clean_list(links):
    print(f'Start size of links list: {len(links)}')
    clear_links = []
    test_links = links[:10]
    print(len(test_links))
    for link in test_links:
        try:
            profile = FirefoxProfile()
            profile.set_preference("general.useragent.override", "Godzilla/5.0 (Linux Ubuntu 22.04 LTS; x64; rv:22.04) Gecko/20100101 Firebox/121.0")
            link = link[1:-1]
            ip, port =  link.split(':')

            # Ручная настройка прокси
            profile.set_preference("network.proxy.type", 1)  # 1 = ручная настройка
            profile.set_preference(f"network.proxy.http", f"{ip}")
            profile.set_preference(f"network.proxy.http_port", port)
            profile.set_preference(f"network.proxy.ssl", f"{ip}")
            profile.set_preference(f"network.proxy.ssl_port", port)
            profile.set_preference("network.proxy.no_proxies_on", "localhost, 127.0.0.1")
            options = Options()
            options.add_argument("--headless=new")
            options.profile = profile
            print(ip, port)
            driver = webdriver.Firefox(options=options)
            driver.get('https:/google.com')
            print("Works")

            clear_links.append(link)
            driver.quit()
        except:
            print('Not works')
    
    return clear_links


if __name__ == '__main__':
    links=get_all_links_on_page(ads_list)
    print(links)
    clean_links = clean_list(links)
    print(clean_links)
    with open('proxy_list.txt', 'w') as file:
        for string in clean_links:
            file.write(string)
            file.write('\n')
    driver.quit()

