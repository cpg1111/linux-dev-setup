#!/usr/bin/env python
from Crypto.PublicKey import RSA
from github import Github
import os
import stat


class NoGithubTokenException(Exception):
    pass

class NoPubKeyException(Exception):
    pass

class KeyManager():
    def __init__(self):
        self.key = RSA.generate(2048)
        self.ssh_dir = "{}/.ssh/".format(os.environ['HOME'])
        self.priv_key_path = "{}id_rsa".format(self.ssh_dir)
        self.pub_key_path = "{}.pub".format(self.priv_key_path)

    def write(self):
        if stat.S_ISDIR(os.stat(self.ssh_dir).st_mode):
            with open(self.priv_key_path, 'w') as priv_file:
                os.chmod(self.priv_key_path, 0600)
                priv_file.write(self.key.exportKey('PEM'))
            self.pub_key = self.key.publickey()
            with open(self.pub_key_path, 'w') as pub_file:
                pub_file.write(self.pub_key.exportKey('OpenSSH'))
        else:
            os.mkdir(self.ssh_dir)
            return self.write()

    def install_to_github(self):
        if len(os.environ['GITHUB_TOKEN']) == 0:
            raise NoGithubTokenException()
        self.g_client = Github(token=os.environ['GITHUB_TOKEN'])
        user = self.g_client.get_user()
        if self.pub_key is not None:
            user.create_key(os.environ['PUB_KEY_TITLE'], self.pub_key)
        else:
            raise NoPubKeyException()


if __name__ == "__main__":
    km = KeyManager()
    km.write()
    km.install_to_github()
