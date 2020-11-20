#!flask/bin/python
from app import app, views

if __name__ == '__main__':
    website_url = 'freeqrcode.ml'
    app.config['SERVER_NAME'] = website_url
    app.run(debug=False)
