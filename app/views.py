from flask import request, render_template
import os
from app import app
from core import Painter, Collector

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

    NAME = request.form['NAME']  # max 160
    PERSONAL_ACC = request.form['PERSONAL_ACC']  # max 20
    BANK_NAME = request.form['BANK_NAME']  # max 45
    BIC = request.form['BIC']  # max 9
    CORRESP_ACC = request.form['CORRESP_ACC']  # max 20

    SUM = request.form['SUM']  # max 18
    PURPOSE = request.form['PURPOSE']  # max 210
    LAST_NAME = request.form['LAST_NAME']
    FIRST_NAME = request.form['FIRST_NAME']
    MIDDLE_NAME = request.form['MIDDLE_NAME']
    PAYER_ADRESS = request.form['PAYER_ADRESS']
    PAYEE_INN = request.form['PAYEE_INN']
    KPP = request.form['KPP']

    textcode = Collector()
    textcode.obligatory_block(name=NAME, personalacc=PERSONAL_ACC, bankname=BANK_NAME, bik=BIC, correspacc=CORRESP_ACC)
    textcode.additioanl_block(summ=SUM, purpose=PURPOSE, firstname=FIRST_NAME, lastname=LAST_NAME, middlename=MIDDLE_NAME, payeeinn=PAYEE_INN, kpp=KPP, payeradress=PAYER_ADRESS)
    textcode = textcode.compose()
    image = Painter(textcode)
    # image.save('img.png')
    return render_template('code.html', image='static/' + image.fullPath, alt=image.fullPath, title=textcode)


# def get_description(title):
#     """
#     Get short description given article.
#     Returns a string of page description.
#     If description is absent for the page, takes the first sentence of the article summary.
#
#     Keyword arguments:
#
#     * title - the title of the page to load.
#     """
#     try:
#         params = {
#             "action": "query",
#             "format": "json",
#             "formatversion": "2",
#             "titles": title,
#             "prop": "description",
#             "redirects": True,
#         }
#         response = requests.Session().get(url="https://wikipedia.org/w/api.php", params=params)
#         data = response.json()
#         return data["query"]["pages"][0]["description"].capitalize() + '.'
#     except KeyError:
#         params = {
#             "action": "query",
#             "format": "json",
#             "titles": title,
#             'prop': 'extracts',
#             'explaintext': True,
#             'redirects': True,
#         }
#         response = requests.Session().get(url="https://wikipedia.org/w/api.php", params=params)
#         data = response.json()
#         return list(data["query"]["pages"].values())[0]['extract'].partition('.')[0] + '.'
#
#
# def get_image(title):
#     """
#     Get a main image of a given article.
#     Returns a direct image link or 'False' if image is not presented in the article.
#
#     Keyword arguments:
#
#     * title - the title of the page to load.
#     """
#     try:
#         params = {
#             "action": "query",
#             "format": "json",
#             "titles": title,
#             "prop": "pageimages",
#             "piprop": "original",
#             "redirects": True,
#         }
#         response = requests.Session().get(url="https://wikipedia.org/w/api.php", params=params)
#         data = response.json()
#         return list(data["query"]["pages"].values())[0]['original']['source']
#     except KeyError:
#         return False
#
#
# def get_links(title):
#     """
#     Get a list of titles for requested query.
#     The func finds all referred articles and returns the list of their titles.
#
#     Keyword arguments:
#
#     * title - the title of the page to load.
#     """
#     try:
#         params = {
#             "action": "query",
#             "format": "json",
#             "titles": title,
#             'prop': 'revisions',
#             'rvprop': 'content',
#             "redirects": True,
#         }
#         response = requests.Session().get(url="https://wikipedia.org/w/api.php", params=params)
#         data = response.json()
#         refers = list(data["query"]["pages"].values())[0]['revisions'][0]['*']
#         my_links = re.findall(r'\[\[(.*?)\]\]', refers)
#         return [link.partition('|')[0] for link in my_links]
#     except KeyError:
#         return False
