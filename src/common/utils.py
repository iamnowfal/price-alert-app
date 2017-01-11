from passlib.hash import pbkdf2_sha512
import re

class Utils(object):


    @staticmethod
    def is_email_valid(email):
        search_pattern = '^[a-z][a-z0-9\.\-_]+@{1}[a-zA-Z\.]+$'
        search_handle = re.compile(search_pattern)
        return True if search_handle.match(email) else False

    @staticmethod
    def hash_password(password):
        """

        :param password: the input password is sha512 encrypted and sent to this method
        :return: sha512 -> pbkdf2_sha512 password
        """

        return pbkdf2_sha512.encrypt(password)
    @staticmethod
    def check_hashed_password(password, hashed_password):
        return pbkdf2_sha512.verify(password, hashed_password)

