# -*- coding: UTF-8 -*-
import os,re,urllib,uuid
from selenium import webdriver
from PIL import Image
from selenium.webdriver.chrome.options import Options
import datetime

def webscreen():
    url = 'https://map.bjsubway.com/mobile?realtime=true'
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=r'E:\work\pycode\util\network\chromedriver.exe', chrome_options=chrome_options)
    driver.set_page_load_timeout(300)
    driver.set_window_size(2048, 1536)

    for i in range(0,4):
        a = datetime.datetime.now()
        print(a.strftime('%Y-%m-%d %H:%M:%S'))
        driver.get(url)
        b = datetime.datetime.now()
        print((b-a).seconds)
        savepath = a.strftime('%Y%m%d%H%M%S') + '.png'
        print(savepath)
        driver.save_screenshot(savepath)


webscreen()