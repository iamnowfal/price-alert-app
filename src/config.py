import os

DEBUG = True
ADMINS = frozenset([os.environ.get('ADMINS')]) # There can be only unique elements in a frozen set