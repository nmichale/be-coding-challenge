import os

SPEC_DIR = './family_tree/'
SPEC_FN = "api.yaml"

wd = os.path.dirname(os.path.realpath(__file__))

db_url = 'dialect+driver://username:password@host:port/database'

person_table = 'database.person'
family_tree_table = 'database.family_tree'

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
