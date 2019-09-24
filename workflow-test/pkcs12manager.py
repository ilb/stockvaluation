import os
import atexit
from OpenSSL import crypto

class PKCS12Manager():

    def __init__(self, p12file, passphrase):
        self.unlock = passphrase
        self.certs_dir = ''
        self.certfile = ''
        self.createPrivateCertStore()
        if ~os.path.isabs(p12file):
            p12file=os.path.join(self.certs_dir,p12file)
        self.p12file = p12file

        # Get filename without extension
        ext = os.path.splitext(p12file)
        self.filebasename = os.path.basename(ext[0])


        self.p12topem()

    def getCert(self):
        return self.certfile

    def createPrivateCertStore(self):
        home = os.path.expanduser('~')
        certs_dir = os.path.join(home, '.certs')
        if not os.path.exists(certs_dir):
            os.mkdir(certs_dir)
        os.chmod(certs_dir, 0o700)
        self.certs_dir = certs_dir

    def p12topem(self):
        p12 = crypto.load_pkcs12(open(self.p12file, 'rb').read(), bytes(self.unlock, 'utf-8'))

        # PEM formatted private key
        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())

        self.certfile = os.path.join(self.certs_dir, self.filebasename + ".temp.pem")
        open(self.certfile, 'a').close()

        def cleanup():
            if os.path.exists(self.certfile):
                os.remove(self.certfile)
        atexit.register(cleanup)

        os.chmod(self.certfile, 0o600)
        with open(self.certfile, 'wb') as f:
            f.write(key)


        # PEM formatted certificate
        cert = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())

        #self.certfile = os.path.join(self.certs_dir, self.filebasename + ".crt.pem")
        #open(self.certfile, 'a').close()
        #os.chmod(self.certfile, 0o644)
        with open(self.certfile, 'ab') as f:
            f.write(cert)
