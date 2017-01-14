import os

EMAIL = os.environ.get('ADMIN_EMAIL')
DEBUG = True
ADMINS = frozenset([EMAIL]) # There can be only unique elements in a frozen set