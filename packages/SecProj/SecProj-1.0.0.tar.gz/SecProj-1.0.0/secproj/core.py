import os
import sys
import dotenv
from cryptography.fernet import Fernet

class Secure(object):
    def __init__(self,gitignore_overwrite=False):
        self.active_path = sys.path[0]
        self.data_path = self.active_path + '/data/'
        self.key_file = self.data_path + 'enc.key'
        self.dotenv_file = self.data_path + ".env"
        self.gitignore_file = self.active_path + "/.gitignore"
        self.base_ignore_file = os.path.dirname(os.path.abspath(__file__)) + "/ignore.txt"

        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        if not os.path.isfile(self.dotenv_file):
            with open(self.dotenv_file, "x") as mk:
                mk.close()

        if gitignore_overwrite is True:
            self.overwrite_gitignore()

        dotenv.load_dotenv(self.dotenv_file)
        self.load_key()

    @staticmethod
    def between(s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return None

    def load_key(self):
        self.key = None
        try: 
            with open(self.key_file) as f:
                self.key = f.readline().strip()
            if self.key:
                self.enc = Fernet(self.key)
        except Exception:
            self.key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(self.key)
            self.enc = Fernet(self.key)

    def overwrite_gitignore(self):
        try:
            contents = ""
            with open(self.base_ignore_file, "r") as reader:
                contents = reader.read()
            if contents != "":
                with open(self.gitignore_file, "w") as writer:
                    writer.write(contents)
            return True
        except:
            return False

    def get_var(self, var_name):
        try:
            rsp = None
            tmp = os.getenv(var_name)
            rsp = self.decrypt(tmp)
            if rsp is None:
                rsp = tmp
                return rsp
            return rsp
        except:
            return None

    def set_var(self,var_name,var_data):
        try:
            tmp = self.encrypt(var_data)
            dotenv.set_key(self.dotenv_file,var_name,tmp)
            os.environ[var_name] = tmp
            return tmp
        except:
            return None

    def encrypt(self,enc_string):
        try:
            if '$$$' in enc_string:
                tmp = self.between(enc_string,'$$$','$$$')
                enc_msg = self.enc.encrypt(tmp.encode('utf-8'))
                repl = enc_string.replace('$$$%s$$$' % tmp, '$$$%s$$$' % enc_msg.decode('utf-8'))
                return repl
            else:
                return '$$$%s$$$' % self.enc.encrypt(enc_string.encode('utf-8')).decode('utf-8')
        except:
            return None

    def decrypt(self,dec_string):
        try:
            if '$$$' in dec_string:
                tmp = self.between(dec_string,'$$$','$$$')
                dec_msg = self.enc.decrypt(tmp.encode('utf-8'))
                repl = dec_string.replace('$$$%s$$$' % tmp, dec_msg.decode('utf-8'))
                return repl
            else:
                return self.enc.decrypt(dec_string.encode('utf-8')).decode('utf-8')
        except:
            return None