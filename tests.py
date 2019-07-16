import unittest

from family_tree import api

class FamilyTreeTests(unittest.TestCase):
    family1 = [
  {
    "first_name": "First",
    "last_name": "Last",
    "phone_number": "1-312-555-5555",
    "email_address": "fake@email.com",
    "address": "1234 Main St.",
    "birth_date": "2019-01-01"
  },
    {
        "first_name": "First",
        "last_name": "Last",
        "phone_number": "1-312-555-5555",
        "email_address": "fake@email.com",
        "address": "1234 Main St.",
        "birth_date": "2019-01-01"
      },
    {
        "first_name": "First",
        "last_name": "Last",
        "phone_number": "1-312-555-5555",
        "email_address": "fake@email.com",
        "address": "1234 Main St.",
        "birth_date": "2019-01-01",
       "parent_ids": [1,2]
      },
    {
        "first_name": "First",
        "last_name": "Last",
        "phone_number": "1-312-555-5555",
        "email_address": "fake@email.com",
        "address": "1234 Main St.",
        "birth_date": "2019-01-01",
       "parent_ids": [1,2]
      }
    ]

    def test_parents(self):
        ids, resp_code = api.person_add(self.family1.copy())
        r = api.person_parents(ids[3])
        print(r)
        # self.assertEqual()

    def test_parents2(self):
        ids, resp_code = api.person_add(self.family1.copy())
        print(ids)
        r = api.person_parents(ids[3])
        print(r)
        # self.assertEqual()

    # def test_siblings(self):
    #     ids, resp_code = api.person_add(self.family1)
    #     r = api.person_siblings(ids[3])
    #     print(r)