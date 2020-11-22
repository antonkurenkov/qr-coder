import qrcode
import time
import os
import psycopg2
import requests
"""

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




class Collector():

    def __init__(self):

        self.SERVISE_BLOCK = {
            'fID': 'ST',
            'formatVersion': '0001',
            'encoding': '1',
            'delimeter': '|'
        }

        self.block1 = self.SERVISE_BLOCK['fID'] + self.SERVISE_BLOCK['formatVersion'] + self.SERVISE_BLOCK['encoding'] + self.SERVISE_BLOCK['delimeter']
        assert len(self.block1) == 8, 'block1 length must be 8'

    def obligatory_block(self, name, personalacc, bankname, bik, correspacc):

        assert len(name) in range(1, 160), 'name must be 1-160 chars'
        assert len(personalacc) == 20 and not any(map(str.isalpha, personalacc)), 'personalacc must be 20 digits'
        assert len(bankname) in range(1, 46), 'bankname must be 1-45 chars'
        assert len(bik) == 9 and not any(map(str.isalpha, bik)), 'bik must be 9 digits'
        assert (len(correspacc) == 20 or correspacc == '0') and (not any(map(str.isalpha, correspacc))), 'correspacc must be 20 digits or "0"'

        self.OBLIGATORY_BLOCK = {
            'Name': name,  # Наименование получателя платежа
            'PersonalAcc': personalacc,  # номер счета получателя платежа
            'BankName': bankname,  # наименование банка получателя платежа
            'BIC': bik,  # БИК банка получателя платежа
            'CorrespAcc': correspacc  # номер кор./сч. банка получателя платежа
        }

        self.block2 = self.SERVISE_BLOCK['delimeter'].join([list(self.OBLIGATORY_BLOCK.keys())[i] + '=' + list(self.OBLIGATORY_BLOCK.values())[i] for i in range(len(self.OBLIGATORY_BLOCK))])
        assert len(self.block2) <= 300, 'block2 length must be less/equal 300'

    def additioanl_block(self, summ, purpose, firstname, lastname, middlename, payeeinn, kpp, payeradress):

# todo asserts

        # SUM = request.form['SUM']  # max 18
        # PURPOSE = request.form['PURPOSE']  # max 210
        # LAST_NAME = request.form['LAST_NAME']
        # FIRST_NAME = request.form['FIRST_NAME']
        # MIDDLE_NAME = request.form['MIDDLE_NAME']
        # PAYER_ADRESS = request.form['PAYER_ADRESS']

        self.ADDITIONAL_BLOCK = {
            'Sum': summ,  # сумма платежа, в копейках todo пересчет на рубли
            'Purpose': purpose,  # наименование платежа (назначение)
            'FirstName': firstname,  # имя плательщика
            'LastName': lastname,  # фамилия плательщика
            'MiddleName': middlename,  # отчество плательщика
            'PayeeINN': payeeinn,
            'KPP': kpp,
            'PayerAdress': payeradress  # адрес плательщика
        }

        self.block3 = self.SERVISE_BLOCK['delimeter'].join([list(self.ADDITIONAL_BLOCK.keys())[i] + '=' + list(self.ADDITIONAL_BLOCK.values())[i] for i in range(len(self.OBLIGATORY_BLOCK)) if list(self.ADDITIONAL_BLOCK.values())[i]])


    def compose(self):

        code = self.block1 + self.SERVISE_BLOCK['delimeter'] + self.block2 + self.SERVISE_BLOCK['delimeter'] + self.block3
        return f'{code}'

    @staticmethod
    def verify_captcha(captcha_key):
        data = {
            'response': captcha_key,
            'secret': '0x77770aFD19801D14a86f15f685984fE8AA13505f'
        }
        response = requests.post(url='https://hcaptcha.com/siteverify', data=data).json()
        assert response['success'] is True, 'Wrong captcha'


def main():

    NAME = 'ООО "Рога и копыта"'  # max 160
    PERSONAL_ACC = '40708407654768768769'  # max 20
    BANK_NAME = 'АО "АЛЬФА-БАНК"'  # max 45
    BIC = '044525593'  # max 9
    CORRESP_ACC = '30101810200000000593'  # max 20

    SUM = '100500'  # max 18
    PURPOSE = 'Оплата заказа 123123123'  # max 210
    PAYEE_INN = '9876856765'  # max 12
    PAYER_INN = '6666131313'  # max 12
    DRAWER_STATUS = '00'  # max 2
    KPP = '345437436'  # max 9
    CBC = '0000000000000000000'  # max 20
    OKTMO = '00000000000'  # max 11
    PAYT_REASON = '00'  # max 2
    TAX_PERIOD = '0000000000'  # max 10
    DOC_NO = '000000000000000'  # max 15
    DOC_DATE = '0000000000'  # max 10
    TAX_PAYT_KIND = '00'  # max 2

    LAST_NAME = 'Куренков'
    FIRST_NAME = 'Антон'
    MIDDLE_NAME = 'Андреевич'
    PAYER_ADRESS = 'Россия, Санкт-Петербург, ул. Ленсовета, д. 50, кв. 19'
    PERSONAL_ACCOUNT = '00000000'
    try:
        text = Collector()
        text.obligatory_block(name=NAME, personalacc=PERSONAL_ACC, bankname=BANK_NAME, bik=BIC, correspacc=CORRESP_ACC)
        text.additioanl_block(summ=SUM, purpose=PURPOSE, firstname=FIRST_NAME, lastname=LAST_NAME, middlename=MIDDLE_NAME, payeeinn=PAYEE_INN, kpp=KPP, payeradress=PAYER_ADRESS)
        textcode = text.compose()
        print(textcode)
    except AssertionError as err:
        print(err.args[0])

    # Painter(textcode).img.save('qr.jpg')


if __name__ == "__main__":
    main()

