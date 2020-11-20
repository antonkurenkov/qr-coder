import psycopg2
import io
import os
import qrcode

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

class BaseConnector():

    def __init__(self):
        # conn = psycopg2.connect(dbname='codes_images', user='heroku',
        #                         password='herokuneverguess123', host='localhost')
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        cursor = conn.cursor()

        cursor.execute(f"CREATE SEQUENCE IF NOT EXISTS image_ids;")
        # cursor.execute(f"DROP TABLE codes;")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS codes ("
                       f"id INTEGER PRIMARY KEY DEFAULT NEXTVAL('image_ids'),"
                       f"code VARCHAR(256),"
                       f"image BYTEA);")

        cursor.close()
        conn.commit()
        conn.close()

    def insert(self, code, imgByteArr):
        # conn = psycopg2.connect(dbname='codes_images', user='heroku',
        #                         password='herokuneverguess123', host='localhost')
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO codes (code, image) VALUES (%s, %s);", (code, imgByteArr))
        # cursor.execute(f"UPDATE codes SET image = %s;", (b_code + b'1test_add',))

        cursor.close()
        conn.commit()
        conn.close()

    def select(self, code):
        # conn = psycopg2.connect(dbname='codes_images', user='heroku',
        #                         password='herokuneverguess123', host='localhost')
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        cursor = conn.cursor()

        cursor.execute(f"SELECT image FROM codes WHERE code = '{code}';")
        for mview in cursor:
                new_b_code = bytes(mview[0])
                return (new_b_code)

        cursor.close()
        conn.commit()
        conn.close()

def main():

    code = "testcode01"

    in_image = Painter(textcode=code).img.get_image()

    imgByteArr = io.BytesIO()
    in_image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    print(f'in arr = {imgByteArr}')

    BaseConnector().insert(code=code, imgByteArr=imgByteArr)

    out_image = BaseConnector().select(code=code)

    print(type(out_image))
    print(f'out arr = {out_image}')

    print(imgByteArr == out_image)
