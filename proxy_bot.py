from proxy_requests import ProxyRequests

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

from solver import Solver

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


class User(ProxyMiner, Solver):

    def __init__(self, url, local):
        super().__init__(url, local)
        self.done = Falsea
        self.speed = 1 + (random.randint(-7, 5) / 10)

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
        options.add_argument('--start-maximized')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(
            executable_path="/Users/antonkurenkov/Proj/qr-coder/chromedriver-86-osx",
            options=options
        )

    @staticmethod
    def happened(probability_coeff=100, always=True):
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
        if always:
            luck = 10000
        return random.randint(0, int(probability_coeff * luck)) >= random.randint(0, 100)

    def find_required_fields_for_input(self, required_block=None):
        print('find_required_fields_for_input')
        fields = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="wrap-input100 validate-input m-b-23"]/input[@class="input100"]')))
        for f in fields:
            self.scroll(px=random.randint(30, 120), scrollback=False)
            f.click()
            time.sleep(random.randint(1, 5) + random.random())
            f.send_keys('lkjlkjldkajlkjdlkajldjadasda')
            time.sleep(random.randint(1, 5) + random.random())

    def find_optional_fields_for_input(self, optional_block=None):
        print('find_optional_fields_for_input')
        fields = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="wrap-input100 m-b-23"]/input[@class="input100"]')))
        for f in fields:
            self.scroll(px=random.randint(30, 120), scrollback=False)
            if self.happened(probability_coeff=100):
                f.click()
                time.sleep(random.randint(1, 5) + random.random())
                f.send_keys('lkjlkjldkajlkjdlkajldjadasda')
                time.sleep(random.randint(1, 5) + random.random())
            if self.happened(probability_coeff=10):
                break

    def scroll(self, px=None, scrollback=True):
        print('scroll')
        if px is None:
            seed = random.randint(500, 1000)
        else:
            seed = px
        scrolled = 0

        while True:
            mouse_wheel_move = round(random.randint(2, 12) * self.speed)
            self.driver.execute_script(f"window.scrollBy(0,{mouse_wheel_move})")
            scrolled += mouse_wheel_move
            if scrolled >= seed:
                break
            if time.time() % mouse_wheel_move:
                time.sleep(random.random() / 100)
        time.sleep(random.random())

        if scrollback:
            while True:
                mouse_wheel_move = -round(random.randint(2, 12) * self.speed)
                self.driver.execute_script(f"window.scrollBy(0,{mouse_wheel_move})")
                scrolled += mouse_wheel_move
                if scrolled <= 0:
                    break
                if time.time() % mouse_wheel_move:
                    time.sleep(random.randint(0, 1) / float(random.randint(1, 100)))
            time.sleep(random.random())

        time.sleep(random.randint(1, 5))

    def solve_captcha(self, on_login_page):
        print('solve_captcha')
        self.solve_hcaptcha(on_login_page=on_login_page)

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

        def redirected(probability_coeff=250):
            probability_coeff = 1  # TODO
            if self.happened(probability_coeff=probability_coeff):
                self.click_on_adv_banner()
                if self.happened(probability_coeff=50):  # 25%
                    self.do_random_stuff()
                return True

        # if self.happened(probability_coeff=50):  # 25%
        #     self.scroll()

        # if not redirected(probability_coeff=20):  # 10%

        if self.happened(probability_coeff=100):  # 50%
            # self.find_required_fields_for_input()
            # self.scroll(px=random.randint(100, 200), scrollback=False)
            self.scroll(px=2000, scrollback=False)

                # if not redirected(probability_coeff=1):  # 2%
                #
                #     if self.happened(probability_coeff=1000):  # 99%
            # self.find_optional_fields_for_input()
                #
                #         if self.happened(probability_coeff=500):  # 90%
            self.solve_captcha(on_login_page=True)
                #
                #             if not redirected(probability_coeff=5):  # 3.5%
                #                 self.submit_form()
                #
                #             if not redirected(probability_coeff=10):  # 6%
                #
                #                 if self.happened(probability_coeff=20):  # 10%
                #                     self.click_back()
                #                     redirected(probability_coeff=10)

    def be_human(self, url: str):
        self.driver.get(url)
        if self.driver.title == 'QR CODE GENERATOR':
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body')))
            if self.happened(probability_coeff=250):
                self.do_job()
            success = True
        else:
            success = False
        return success


if __name__ == '__main__':


    # url_to_visit = 'http://www.payqrcode.ru'
    # url_to_visit = 'http://localhost:5000/'
    url_to_visit = 'http://aqr-coder.herokuapp.com'
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
            # if success:
            #     used_queue.append(u.proxy)
        except Exception as e:
            print(e)

        u.driver.quit()
        # if len(used_queue) == 10:
        #     break
        print()







