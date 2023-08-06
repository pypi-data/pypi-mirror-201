from Crypto.PublicKey import RSA

class GenerateSSH:
    def __init__(self,password,private_key_name,public_key_name):
        self.password = password
        self.public = public_key_name
        self.private = private_key_name

        self.key = RSA.generate(4096)

        with open(self.private,'wb') as f:
            f.write(self.key.export_key("PEM",self.password))

        with open(self.public,'wb') as f:
            f.write(self.key.public_key().export_key("OpenSSH"))
