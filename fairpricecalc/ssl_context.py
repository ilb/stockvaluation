import ssl
import os
from urllib.request import urlretrieve

def create_ssl_context():
    SSL_CLIENT_AUTH_FILE = os.environ.get('python.net.ssl.trustStore')
    SSL_CERT_FILE = os.environ.get('python.net.ssl.keyStore')
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    #FIXME
    #ssl_context.verify_mode=ssl.CERT_REQUIRED
    if SSL_CLIENT_AUTH_FILE!=None:
        ssl_context.load_verify_locations(capath=SSL_CLIENT_AUTH_FILE)
    if SSL_CERT_FILE!=None:
        ssl_context.load_cert_chain(certfile=SSL_CERT_FILE)
    return ssl_context

ssl._create_default_https_context = create_ssl_context
