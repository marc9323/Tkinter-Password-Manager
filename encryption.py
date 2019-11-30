"""
Marc D. Holman
11 / 22 / 2019
CIS 2531 - Introduction to Python Programming

Term Project - Tkinter Password Manager Application

Module encryption, consists of class Encryption
Used for encrypting and verifying passwords for
user login and registration.  This class sets up
an encryption context and holds methods for encrypting
and verifying passwords.

passlib does all the work for us.
"""

from passlib.context import CryptContext

class Encryption:
    """ This class sets up an encryption context and contains methods
    for encrypting and verifying passwords"""
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000
        )

    #  encrypt password
    def encrypt_password(self, password):
        return self.pwd_context.encrypt(password)

    #  verify password
    def check_encrypted_password(self, password, hashed):
        return self.pwd_context.verify(password, hashed)