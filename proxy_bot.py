from proxy_requests import ProxyRequests

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

import random
import time
import requests


class ProxyMiner:

    def __init__(self, u, local):
        if not local:
            r = ProxyRequests(u)
            r.get()
            self.proxy = r.get_proxy_used()
        else:
            self.proxy = None


class User(ProxyMiner):

    def __init__(self, url, local):
        super().__init__(url, local)

    def prepare_driver(self, proxy_used):
        if proxy_used:
            webdriver.DesiredCapabilities.CHROME['proxy'] = {
                "httpProxy": self.proxy,
                "ftpProxy": self.proxy,
                "sslProxy": self.proxy,
                "proxyType": "MANUAL",
            }

        options = Options()
        options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36')
        # options.add_argument('--proxy-server=%s' % proxy)
        # options.headless = True
        # if self.headless:
        # options.add_argument('--start-maximized')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(
            executable_path="/Users/antonkurenkov/Proj/qr-coder/chromedriver-86-osx",
            options=options
        )

    @staticmethod
    def happened(probability_coeff=100):
        """
        # 2 = 2%
        # 5 = 3.5%
        # 10 = 6%
        # 20 = 10%
        # 30 = 16%
        # 50 = 25%
        # 100 = 50%
        # 200 = 75%
        # 250 = 80%
        # 500 = 90%
        # 1000 = 95%
        # 10000 = 99%
        """
        luck = random.random() + random.random()
        return random.randint(0, int(probability_coeff * luck)) >= random.randint(0, 100)

    def find_required_fields_for_input(self):
        print('find_required_fields_for_input')
        # body = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body')))

    def find_optional_fields_for_input(self):
        print('find_optional_fields_for_input')
        # body = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body')))

    def scroll(self):
        print('scroll')

    def solve_captcha(self):
        print('solve_captcha')

    def submit_form(self):
        print('submit_form')

    def click_back(self):
        print('click_back')
        pass

    def click_on_adv_banner(self):
        print('click_on_adv_banner')

    def do_random_stuff(self):
        print('do_random_stuff')
        for _ in range(random.randint(0, 5)):
            try:
                self.scroll()
                self.click_random_button()
            except:
                break

    def click_random_button(self):
        print('click_random_button')
        pass

    def do_job(self):
        print('do_job on website')

        def redirected(probability_coeff=250, adv_magnet=False):
            if adv_magnet:
                probability_coeff = 100000
            if self.happened(probability_coeff=probability_coeff):
                self.click_on_adv_banner()
                if self.happened(probability_coeff=50):  # 25%
                    self.do_random_stuff()
                return True

        if self.happened(probability_coeff=50):  # 25%
            self.scroll()

        if not redirected(probability_coeff=20):  # 10%

            if self.happened(probability_coeff=100):  # 50%
                self.find_required_fields_for_input()
                self.scroll()

                if not redirected(probability_coeff=1):  # 2%

                    if self.happened(probability_coeff=1000):  # 99%
                        self.find_optional_fields_for_input()

                        if self.happened(probability_coeff=500):  # 90%
                            self.solve_captcha()

                            if not redirected(probability_coeff=5):  # 3.5%
                                self.submit_form()

                            if not redirected(probability_coeff=10):  # 6%

                                if self.happened(probability_coeff=20):  # 10%
                                    self.click_back()
                                    redirected(probability_coeff=10)

    def be_human(self, url: str):
        self.driver.get(url)
        if self.driver.title == 'QR CODE GENERATOR':
            body = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body')))
            if self.happened(probability_coeff=250):
                self.do_job()
            success = True
        else:
            success = False
        u.driver.quit()
        return success


if __name__ == '__main__':


    # url_to_visit = 'http://www.payqrcode.ru'
    url_to_visit = 'http://localhost:5000/'
    users_local = True
    bot_number = 1


    used_queue = []
    for i in range(bot_number):
        u = User(url_to_visit, local=users_local)
        print(f'VISIT {url_to_visit} over {u.proxy}')
        u.prepare_driver(u.proxy)
        try:
            success = u.be_human(url_to_visit)
            # success = u.do_job()  # to just test scenario
            if success:
                used_queue.append(u.proxy)
        except Exception as e:
            print(e)
        # if len(used_queue) == 10:
        #     break
        print()







