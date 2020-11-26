#!flask/bin/python
from app import app, views

if __name__ == '__main__':
    app.run(ssl_context=('/etc/ssl/server.crt', '/etc/ssl/server.key'), debug=True, host='31.31.192.197', port='443')

