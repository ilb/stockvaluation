import ssl
import os
import keyring
import requests
from urllib.request import urlretrieve
from pkcs12manager import PKCS12Manager
import warnings

#FIXME suppress SubjectAltNameWarning
warnings.filterwarnings('ignore')

def create_ssl_context(a=None):
    SSL_CLIENT_AUTH_FILE = os.environ.get('NODE_EXTRA_CA_CERTS')
    SSL_CERT_FILE = os.environ.get('python.net.ssl.keyStore')
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    #FIXME
    ssl_context.verify_mode=ssl.CERT_REQUIRED #ssl.CERT_NONE #
    default_ca_file="/etc/ssl/certs/ourCAbundle.crt"
    if SSL_CLIENT_AUTH_FILE!=None:
        ssl_context.load_verify_locations(cafile=SSL_CLIENT_AUTH_FILE)
    elif os.path.exists(default_ca_file):
        ssl_context.load_verify_locations(cafile=default_ca_file)
    if SSL_CERT_FILE!=None:
        ssl_context.load_cert_chain(certfile=SSL_CERT_FILE)
    else:
        # init: python -m keyring set .certs my.p12
        storepass=keyring.get_password(".certs", "my.p12")
        #print("storepass!")
        if storepass!=None:
            #print("using pkcs12")
            pkcs12 = PKCS12Manager('my.p12', storepass)
            ssl_context.load_cert_chain(certfile=pkcs12.getCert())

    return ssl_context

ssl._create_default_https_context = create_ssl_context
#requests.packages.urllib3.util.ssl_.create_urllib3_context = create_ssl_context
#print(requests.packages.urllib3.util.ssl_.SSLContext)
requests.packages.urllib3.util.ssl_.SSLContext=create_ssl_context

if __name__ == '__main__':
    url = "https://docs.ilb.ru/doc/treasurydocs/repo/data/issuancevolume.xhtml"
    #save_path = "/tmp/ttt"
    #response = urlretrieve(url, save_path)
    #print (response);
    response = requests.get(url)
    print(response.content)
