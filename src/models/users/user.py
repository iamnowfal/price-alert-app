import uuid

from src.common.database import Database

from src.common.utils import Utils
import src.models.users.errors as UserErrors
from src.models.alerts.alert import Alert
from src.models.users import constants as UserConstant


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User   {}>".format(self.email)
    def json(self):
        return {
            "email":self.email,
            "password": self.password,
            "_id": self._id
        }
    @staticmethod
    def is_login_valid(email, password):

        user = Database.find_one(UserConstant.COLLECTION, query={"email":email})
        if user is None:
            raise UserErrors.UserNotExistsError("User does not exist")
        if not Utils.check_hashed_password(password, user['password']):
            raise UserErrors.IncorrectPasswordError("password incorrect!")
        return True
        # elif user['password'] == password :
        #     return  True
        # else:
        #     raise UserErrors.IncorrectPasswordError("password incorrect!")

    @staticmethod
    def register_user(email, password):

        user_data = Database.find_one(UserConstant.COLLECTION, {"email":email})
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("User exists")
        if not Utils.is_email_valid(email):
            raise UserErrors.InvalidEmailError("Email format is incorrect")
        db_passwd = Utils.hash_password(password)
        user_data = User(email,db_passwd,_id=None)
        user_data.save_to_db()
        return True

    def save_to_db(self):
        Database.insert("users", self.json())

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstant.COLLECTION, {"email":email}))

    def get_alerts(self): ##Alert model is handled here rather than on the user views section.
         return Alert.find_alert_by_email(self.email)
