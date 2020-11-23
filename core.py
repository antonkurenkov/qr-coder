import qrcode
import time
import os
import psycopg2
import requests

S = """

http://docs.cntd.ru/document/1200110981

Name — наименование получателя платежа;
PayeeINN — ИНН получателя платежа;
KPP — КПП получателя платежа;
PersonalAcc — номер счета получателя платежа;
BankName — наименование банка получателя платежа;
BIC — БИК банка получателя платежа;
CorrespAcc — номер кор./сч. банка получателя платежа;


Sum — сумма платежа, в копейках;
Purpose — наименование платежа (назначение);
LastName — фамилия плательщика;
FirstName — имя плательщика;
MiddleName — отчество плательщика;
PayerAddress — адрес плательщика.

ST00012|Name=ООО "Рога и копыта"|PayeeINN=9876856765|KPP=345437436|

PersonalAcc=40708407654768768769|BankName=АО "АЛЬФА-БАНК"|BIC=044525593|CorrespAcc=30101810200000000593|
LastName={LASTNAME}|FirstName={FIRSTNAME}|MiddleName={MIDDLENAME}|
PayerAddress={ADDRESS}|Purpose=Оплата заказа {NORDER}|Sum={TOTAL}

"""


class Painter():

    def __init__(self, textcode):
        qr = qrcode.QRCode(
            version=1,  # fit=True
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(textcode)
        qr.make(fit=True)

        self.img = qr.make_image(fill_color="black", back_color="white")
        # self.imgTime = time.time()
        #
        # self.fullPath = f'{self.imgTime}.png'

        # self.fullPath = os.path.join('static', self.name)
        # img.save(('app/static/' + self.fullPath))


class Loader:

    def __init__(self, required_block, optional_block):

        servise_block = {
            'fID': 'ST',
            'formatVersion': '0001',
            'encoding': '1',
            'delimeter': '|'
        }
        captcha_key = required_block.pop('h-captcha-response')

        self.block1 = servise_block['fID'] + servise_block['formatVersion'] + servise_block['encoding'] + servise_block['delimeter']
        self.block2 = servise_block['delimeter'].join([list(required_block.keys())[i] + '=' + list(required_block.values())[i] for i in range(len(required_block))])
        self.block3 = servise_block['delimeter'].join([list(optional_block.keys())[i] + '=' + list(optional_block.values())[i] for i in range(len(required_block)) if list(optional_block.values())[i]])

        self.error = self.apply_constraints(required=required_block, optional=optional_block, captcha=captcha_key)

    def apply_constraints(self, required, optional, captcha):
        try:
            assert self.verify_captcha(captcha) is True, 'Invalid captcha'

            assert len(required.get('Name')) in range(1, 160), 'name must be 1-160 chars'
            assert len(required.get('PersonalAcc')) == 20 and not any(map(str.isalpha, required.get('PersonalAcc'))), 'personalacc must be 20 digits'
            assert len(required.get('BankName')) in range(1, 46), 'bankname must be 1-45 chars'
            assert len(required.get('BIC')) == 9 and not any(map(str.isalpha, required.get('BIC'))), 'bik must be 9 digits'
            assert (len(required.get('CorrespAcc')) == 20 or required.get('CorrespAcc') == '0') and (all(map(str.isdigit, required.get('CorrespAcc')))), 'correspacc must be 20 digits or "0"'

            s = optional.get('Sum')
            if s:
                assert len(s) <= 18 and (all(map(str.isdigit, s))), 'sum must be up to 18 digits'

            p = optional.get('Purpose')
            if p:
                assert len(optional.get('Purpose')) <= 210, 'purpose must be up to 210 chars'

            assert len(self.block2) <= 300, 'block2 length must be less/equal 300 chars'

        except AssertionError as err:
            return err.args[0]

    def compose(self, delimeter='|'):
        return self.block1 + delimeter + self.block2 + delimeter + self.block3

    @staticmethod
    def verify_captcha(captcha_key):
        data = {
            'response': captcha_key,
            'secret': '0x77770aFD19801D14a86f15f685984fE8AA13505f'
        }
        response = requests.post(url='https://hcaptcha.com/siteverify', data=data).json()
        return response['success']


# def main():
#
#     NAME = 'ООО "Рога и копыта"'  # max 160
#     PERSONAL_ACC = '40708407654768768769'  # max 20
#     BANK_NAME = 'АО "АЛЬФА-БАНК"'  # max 45
#     BIC = '044525593'  # max 9
#     CORRESP_ACC = '30101810200000000593'  # max 20
#
#     SUM = '100500'  # max 18
#     PURPOSE = 'Оплата заказа 123123123'  # max 210
#     PAYEE_INN = '9876856765'  # max 12
#     PAYER_INN = '6666131313'  # max 12
#     DRAWER_STATUS = '00'  # max 2
#     KPP = '345437436'  # max 9
#     CBC = '0000000000000000000'  # max 20
#     OKTMO = '00000000000'  # max 11
#     PAYT_REASON = '00'  # max 2
#     TAX_PERIOD = '0000000000'  # max 10
#     DOC_NO = '000000000000000'  # max 15
#     DOC_DATE = '0000000000'  # max 10
#     TAX_PAYT_KIND = '00'  # max 2
#
#     LAST_NAME = 'Куренков'
#     FIRST_NAME = 'Антон'
#     MIDDLE_NAME = 'Андреевич'
#     PAYER_ADRESS = 'Россия, Санкт-Петербург, ул. Ленсовета, д. 50, кв. 19'
#     PERSONAL_ACCOUNT = '00000000'
#
#
# if __name__ == "__main__":
#     main()
#
