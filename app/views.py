from flask import request, render_template
import os
import io
import base64
from app import app
from core import Painter, Loader

# from post import BaseConnector

import requests
import re


@app.route('/index')
@app.route('/')
def my_form():
    """Returns default form for the index page."""
    return render_template('index.html')


@app.route('/index', methods=['POST'])
@app.route('/', methods=['POST'])
def main_form_post():

    required_keys = ['Name', 'PersonalAcc', 'BankName', 'BIC', 'CorrespAcc', 'h-captcha-response']
    optional_keys = ['Sum', 'Purpose', 'FirstName', 'LastName', 'MiddleName', 'PayerAdress', 'PayeeINN', 'KPP']

    required_data = {key: request.form[key] for key in required_keys}
    optional_data = {key: request.form[key] for key in optional_keys}

    loader = Loader(required_block=required_data, optional_block=optional_data)
    if loader.error:
        return render_template('error.html', error=loader.error)
    else:
        try:
            textcode = loader.compose()
            in_image = Painter(textcode=textcode).img.get_image()
            # in_image.save('img.png')
            imgByteArr = io.BytesIO()
            in_image.save(imgByteArr, format='PNG')
            imgByteArr = imgByteArr.getvalue()

            # BaseConnector().insert(code=textcode, imgByteArr=imgByteArr)
            # out_image = BaseConnector().select(code=textcode)

            return render_template('code.html', img_bin=base64.b64encode(imgByteArr).decode("utf-8"), alt=textcode,
                                   title=textcode)
        except Exception as e:
            return render_template('error.html', error=f'Unexpected {e.args[0]}')

@app.route('/ads.txt', methods=['GET'])
def ads_form_get():

    neon_ads = ['neon.today', '47901', 'DIRECT']
    infolinks_ads = ['infolinks.com', '3301515', 'DIRECT']

    return ', '.join(neon_ads) + '<br>' + ', '.join(infolinks_ads)
