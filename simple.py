from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from random import randint, random

with open('proxy_list.txt', 'r') as file:
    links = file.read()
with open('links.txt', 'r') as file:
    catalog_links = file.read()


for item in range(0, len(catalog_links)):

    ip, port =  links[int(item)/10].split(':')

    profile = FirefoxProfile()
    profile.set_preference(f"general.useragent.override", f"Godzilla/{randint(1, 20)}.0 (Linux Ubuntu {randint(1, 20)}.04 LTS; x64; rv:22.04) Gecko/20100101 Firebox/{randint(100, 120)}.0")
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
    driver.get()


