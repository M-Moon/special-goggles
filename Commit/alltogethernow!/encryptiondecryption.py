""" Self-made encryption algorithm for the message app """

class Encryptor:

    def __init__(self, pub_key):
        self.pub_key = pub_key
        self.encrypted = ""

    def encrypt(self, msg):
        pass
        #self.encrypted = enc_msg

    def return_msg(self):
        return self.encrypted


class Decryptor:

    def __init__(self, priv_key):
        self.priv_key = priv_key
        self.decrypted = ""

    def decrypt(self, msg):
        pass
        #self.decrypted = dec_msg

    def return_msg(self):
        return self.decrypted
