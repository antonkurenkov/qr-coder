from proxy_requests import ProxyRequests

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

from solver import Solver
from faker import Faker
from fake_useragent import UserAgent

import random
import time
import requests


class ProxyMiner:

    def __init__(self, u, local):
        if not local:
        #     print('looking for proxy...')
        #     r = ProxyRequests(u)
        #     r.get()
        #     self.proxy = r.get_proxy_used()
        # else:
            self.proxy = None


class Producer:

    def __init__(self):
        self.lastname = None
        self.middlename = None
        self.firstname = None
        self.sex = None
        self.bankname = None
        self.purpose = None
        self.adress = None
        self.useragent = None

    def validate_user(self, items):
        self.lastname = None
        self.middlename = None
        self.firstname = None
        self.sex = None
        for i in items:
            if i.endswith('ович') or i.endswith('овна') or i.endswith('евич') or i.endswith('евич'):
                self.middlename = i
                continue

            if i.endswith('ова') or i.endswith('ева'):
                self.lastname = i
                self.sex = 'female'
                continue
            if i.endswith('ов') or i.endswith('ев'):
                self.lastname = i
                self.sex = 'male'
                continue

            self.firstname = i

        # cut 3/4 of all cases because of mostly male audience
        if self.sex == 'female' and random.randint(1, 100) >= 20:
            return
        else:
            return self.firstname and self.middlename and self.lastname

    def create_useragent(self):
        while True:
            try:
                return UserAgent().random
            except:
                pass

    def create_user(self):
        while True:
            f = Faker('ru_RU')
            i = f.name().split(' ')
            if self.validate_user(i):
                self.adress = f.address()
                self.useragent = self.create_useragent()
                break

        return self.firstname, self.middlename, self.lastname

    def produce_data(self):
        with open('userdata/banknames.txt') as file:
            self.bankname = random.choice(file.read().split('\n'))
        with open('userdata/purposes.txt') as file:
            self.purpose = random.choice(file.read().split('\n'))
        obligatory_block = {
            'Name': f'{self.lastname} {self.firstname} {self.middlename}',
            'PersonalAcc': ''.join([str(random.randint(0, 9)) for _ in range(20)]),
            'BankName': self.bankname,
            'BIC': ''.join([str(random.randint(0, 9)) for _ in range(9)]),
            'CorrespAcc': random.choice(['0', ''.join([str(random.randint(0, 9)) for _ in range(20)])])
        }

        optional_block = {
            'Sum': str((random.randint(1, 100) * 1000) + (random.randint(1, 100) * 100 if random.choice([True, False, False, False]) else 0)),
            'Purpose': self.purpose,
            'FirstName': self.create_user()[0],
            'MiddleName': self.create_user()[1],
            'LastName': self.create_user()[2],
            'PayeeINN': ''.join([str(random.randint(0, 9)) for _ in range(12)]),
            'KPP': ''.join([str(random.randint(0, 9)) for _ in range(9)]),
            'PayerAdress': self.adress
        }

        return obligatory_block, optional_block


class User(ProxyMiner, Solver):

    def __init__(self, url, local, virtual=False):
        self.virtual = virtual
        self.proxy = None
        if not self.virtual:
            p = Producer()
            p.create_user()
            self.required_block, self.optional_block = p.produce_data()
            self.useragent = p.useragent
            super().__init__(url, local)
            self.done = False
            self.speed = 1 + (random.randint(-7, 5) / 10)

    def prepare_driver(self, proxy_used):
        if self.virtual:
            return
        # if proxy_used:
        #     webdriver.DesiredCapabilities.CHROME['proxy'] = {
        #         "httpProxy": self.proxy,
        #         "ftpProxy": self.proxy,
        #         "sslProxy": self.proxy,
        #         "proxyType": "MANUAL",
        #     }
        #

        options = Options()

        # canonic_ua = 'user-agent=Mozilla/5.0 (X11; Linux x86_64) ' \
        #              'AppleWebKit/537.36 (KHTML, like Gecko) ' \
        #              'Chrome/86.0.4240.111 Safari/537.36'
        # if random.randint(0, 100) <= 30:
        #     canonic_ua = self.useragent
        # options.add_argument(canonic_ua)

        options.headless = True
        #
        if random.randint(0, 100) >= 30:
            options.add_argument('--start-maximized')
        elif random.randint(0, 100) >= 30:
            options.add_argument("window-size=1024,768")

        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

        options.add_argument('--no-sandbox')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(
            executable_path="/home/antonkurenkov/qr-coder/chromedriver-86-linux",
            options=options
        )



        # opera_profile = '/home/antonkurenkov/qr-coder/opera-conf'
        # options = Options()
        # options.headless = True
        # # options.add_argument('user-data-dir=' + opera_profile)
        # # driver = webdriver.Opera(options=options, executable_path='/home/antonkurenkov/Proj/qr-coder/operadriver-86-linux')
        # options.add_argument("--no-sandbox")
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument("--disable-extensions")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--start-maximized")
        # options.add_argument("--disable-infobars")
        #
        # options.add_argument("--disable-setuid-sandbox")
        # options.add_argument("--remote-debugging-port=9222")
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # self.driver = webdriver.Opera(options=options,
        #                         executable_path='/home/antonkurenkov/qr-coder/operadriver-86-linux')

    @staticmethod
    def happened(probability_coeff=100, always=False):
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

    def typewrite(self, string, elem):
        seed = self.speed / 10
        if not any(map(str.isalpha, string)):
            seed *= 5
        for idx, letter in enumerate(string):
            elem.send_keys(letter)
            time.sleep(seed)
            if letter == ' ':
                time.sleep(1)
            if not idx % random.randint(4, 6):
                time.sleep(1)

    def find_required_fields_for_input(self, required_block=None):
        print('find_required_fields_for_input')
        if self.virtual:
            return
        order = ('Name', 'PersonalAcc', 'BankName', 'BIC', 'CorrespAcc')
        fields = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="wrap-input100 validate-input m-b-23"]/input[@class="input100"]')))
        for f, data in zip(fields, order):
            self.scroll(px=random.randint(30, 120), scrollback=False)
            f.click()
            time.sleep(random.randint(1, 5) + random.random())
            self.typewrite(string=self.required_block[data], elem=f)
            time.sleep(random.randint(1, 5) + random.random())

    def find_optional_fields_for_input(self, optional_block=None):
        print('find_optional_fields_for_input')
        if self.virtual:
            return
        order = ('Sum', 'Purpose', 'FirstName', 'LastName', 'MiddleName', 'PayeeINN',  'KPP', 'PayerAdress')
        fields = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="wrap-input100 m-b-23"]/input[@class="input100"]')))
        for f, data in zip(fields, order):
            self.scroll(px=random.randint(30, 120), scrollback=False)
            if self.happened(probability_coeff=1000):
                f.click()
                time.sleep(random.randint(1, 5) + random.random())
                self.typewrite(string=self.optional_block[data], elem=f)
                time.sleep(random.randint(1, 5) + random.random())
            if order == 'Purpose' and self.happened(probability_coeff=250):
                break
            if self.happened(probability_coeff=10):
                break

    def scroll(self, px=None, scrollback=True, forward=True):
        print('scroll')
        if not forward:
            forward = -1
        if self.virtual:
            return
        if px is None:
            seed = random.randint(500, 1000)
        else:
            seed = px
        scrolled = 0

        while True:
            mouse_wheel_move = round(random.randint(2, 12) * self.speed)
            self.driver.execute_script(f"window.scrollBy(0,{mouse_wheel_move * forward})")
            scrolled += mouse_wheel_move
            if scrolled >= seed:
                break
            if time.time() % mouse_wheel_move:
                time.sleep(random.random() / 100)
        time.sleep(random.random())

        if scrollback:
            while True:
                mouse_wheel_move = -round(random.randint(2, 12) * self.speed)
                self.driver.execute_script(f"window.scrollBy(0,{mouse_wheel_move * forward})")
                scrolled += mouse_wheel_move
                if scrolled <= 0:
                    break
                if time.time() % mouse_wheel_move:
                    time.sleep(random.randint(0, 1) / float(random.randint(1, 100)))
            time.sleep(random.random())

        time.sleep(random.randint(1, 5))

    def solve_captcha(self, on_login_page):
        print('solve_captcha')
        if self.virtual:
            return
        self.solve_hcaptcha(on_login_page=on_login_page)

    def submit_form(self):
        print('submit_form')
        if self.virtual:
            return
        self.driver.switch_to.default_content()
        button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@class="login100-form-btn"]')))
        time.sleep(random.random())
        button.click()

    def click_back(self):
        print('click_back')
        if self.virtual:
            return

        def inner():
            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@class="login100-form-btn"]')))
            time.sleep(random.random())
            button.click()

        def outer():
            self.driver.execute_script('history.back();')

        func = random.choice([inner, outer])
        func()

    def click_random_button(self):
        print('click_random_button')
        if self.virtual:
            return

        def fake_submit():
            try:
                buttons = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//button')))
                b = random.choice(buttons)
                time.sleep(random.random())
                b.click()
                time.sleep(random.randint(1, 3))
                self.driver.switch_to.default_content()
            except:
                pass

        def fake_click():
            try:
                forms = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//input')))
                f = random.choice(forms)
                time.sleep(random.random())
                f.submit()
                time.sleep(random.randint(1, 3))
                self.driver.switch_to.default_content()
            except:
                pass

        func = random.choice([fake_click, fake_submit])
        func()

    def click_on_adv_banner(self):
        print('click_on_adv_banner')
        if self.virtual:
            return
        self.scroll(px=2000, scrollback=False)
        button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//footer/div/p/a')))
        time.sleep(random.random())
        button.click()
        self.driver.switch_to.default_content()

    def do_random_stuff(self):
        print('do_random_stuff')
        for _ in range(random.randint(0, 5)):
            try:
                self.scroll()
                self.click_random_button()
            except:
                break

    def do_job(self):
        print('do_job on website')

        def redirected(probability_coeff=250):
            # probability_coeff = 100000  # TODO
            if self.happened(probability_coeff=probability_coeff):
                self.click_on_adv_banner()
                if self.happened(probability_coeff=50):  # 25%
                    self.do_random_stuff()
                return True

        if self.happened(probability_coeff=50):  # 25%
            self.scroll()
        if self.happened(probability_coeff=20):  # 25%
            time.sleep(random.randint(1, 6))

        if not redirected(probability_coeff=20):  # 10%

            if self.happened(probability_coeff=500):  # 90%
                self.find_required_fields_for_input()
                self.scroll(px=random.randint(100, 200), scrollback=False)

                if self.happened(probability_coeff=20):  # 25%
                    time.sleep(random.randint(1, 6))

                if not redirected(probability_coeff=1):  # 2%

                    if self.happened(probability_coeff=100):  # 50%
                        self.find_optional_fields_for_input()

                        if self.happened(probability_coeff=20):
                            self.scroll(forward=False)

                        if self.happened(probability_coeff=20):  # 25%
                            time.sleep(random.randint(1, 6))

                        if self.happened(probability_coeff=500):  # 90%
                            self.solve_captcha(on_login_page=True)

                            if not redirected(probability_coeff=5):  # 3.5%

                                if self.happened(probability_coeff=20):
                                    self.scroll(forward=False)

                                self.submit_form()

                            if not redirected(probability_coeff=10):  # 6%

                                if self.happened(probability_coeff=20):  # 10%
                                    self.click_back()

                                    if self.happened(probability_coeff=20):  # 25%
                                        time.sleep(random.randint(1, 6))

                                    redirected(probability_coeff=10)  # 6%

    def be_human(self, url: str):
        if not self.virtual:
            self.driver.get(url)
        if self.virtual or self.driver.title == 'Payment QR-code generator':
            if not self.virtual:
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body')))
            if self.happened(probability_coeff=1000):
                self.do_job()
            else:
                time.sleep(random.randint(1, 20))
            success = True
        else:
            success = False
        return success


def get_redirected_url():

    def num_postfix():
        return f'{"".join([random.choice(letters) for _ in range(random.randint(1, 5))])}={"".join([random.choice(nums) for _ in range(random.randint(1, 10))])}'

    def letter_postfix():
        return f'{"".join([random.choice(letters) for _ in range(random.randint(1, 5))])}={"".join([random.choice(arr) for _ in range(random.randint(16, 50))])}'

    letters = 'abcdefghijklmnopqrstuvwxyz'
    letters_upper = 'abcdefghijklmnopqrstuvwxyz'.upper()
    nums = '0123456789'
    uu = '_-'
    arr = letters + letters_upper + nums + uu

    fake_args = '&'.join([random.choice([num_postfix, letter_postfix])() for _ in range(random.randint(1, 3))])

    data_dict = {
        'social': [
            f'https://vk.com/away.php?utf={random.randint(1, 6)}&to=https%3A%2F%2Fwww.payqrcode.ru',
            f'https://vk.com/away.php?utf={random.randint(1, 6)}&to=https%3A%2F%2Fwww.payqrcode.ru',
            f'https://vk.com/away.php?utf={random.randint(1, 6)}&to=https%3A%2F%2Fwww.payqrcode.ru',
            f'https://vk.com/away.php?utf={random.randint(1, 6)}&to=https%3A%2F%2Fwww.payqrcode.ru',
            f'https://vk.com/away.php?utf={random.randint(1, 6)}&to=https%3A%2F%2Fwww.payqrcode.ru',
            f'https://www.payqrcode.ru/?lr=2&redircnt={"".join([str(random.randint(1, 9)) for _ in range(10)])}.{random.randint(1, 9)}',
            f'https://www.payqrcode.ru/?fbclid={"".join([random.choice(arr) for _ in range(63)])}',
            f'https://www.payqrcode.ru/?{fake_args}'
        ],
        'direct': [
            'https://payqrcode.ru',
            'https://payqrcode.ru',
            'https://www.payqrcode.ru',
            'https://www.payqrcode.ru',
            'https://www.payqrcode.ru/',
            'https://www.payqrcode.ru/index',
            'https://www.payqrcode.ru/index',
            # 'http://www.payqrcode.ru',
            # 'http://www.payqrcode.ru/index',
            # 'http://payqrcode.ru',
            # 'http://payqrcode.ru/index',
        ]
    }
    source = data_dict[random.choice(list(data_dict.keys()))]
    return random.choice(source)


if __name__ == '__main__':

    url_to_visit = 'https://www.payqrcode.ru'
    # url_to_visit = 'http://localhost:5000/'
    # url_to_visit = 'http://aqr-coder.herokuapp.com'
    users_local = False
    virtual = False
    bot_number = 76

    used_queue = []
    for i in range(bot_number):
        try:
            while True:
                try:
                    u = User(url_to_visit, local=users_local, virtual=virtual)
                    if not virtual:
                        u.prepare_driver(u.proxy)
                    break
                except Exception as e:
                    
                    print(f'user init failed with {str(e).lower()}')
                    raise e

            redirected = get_redirected_url()
            print(f'VISIT {redirected} over {u.proxy}')
            success = u.be_human(redirected)
            # success = u.do_job()  # to just test scenario
            if success:
                used_queue.append(u.proxy)
        except Exception as e:
            print(e)
            raise e
        if not u.virtual:
            time.sleep(random.randint(10, 30))
            u.driver.quit()
        print('---')
        import subprocess
        # ss = subprocess.check_output('sudo rm ~/.config/opera && sudo unzip opera-conf.zip -d ~/.config/opera')
        if not u.virtual:
            zzz = random.randint(10, 1800)
            print(f'sleeping {zzz}s')
            time.sleep(zzz)








