import unittest

from family_tree import api
import copy

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
        "first_name": "Jeffrey",
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

    family2 = [
        {
            "first_name": "First",
            "last_name": "Last",
            "phone_number": "1-312-555-5555",
            "email_address": "fake@email.com",
            "address": "1234 Main St.",
            "birth_date": "2019-01-01"
        },
        {
            "first_name": "Jeffrey",
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
            "parent_ids": [1, 2]
        },
        {
            "first_name": "First",
            "last_name": "Last",
            "phone_number": "1-312-555-5555",
            "email_address": "fake@email.com",
            "address": "1234 Main St.",
            "birth_date": "2019-01-01",
            "parent_ids": [1, 2]
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
            "birth_date": "2019-01-01"
        },
        {
            "first_name": "First",
            "last_name": "Last",
            "phone_number": "1-312-555-5555",
            "email_address": "fake@email.com",
            "address": "1234 Main St.",
            "birth_date": "2019-01-01",
            "parent_ids": [3, 5]
        },
        {
            "first_name": "First",
            "last_name": "Last",
            "phone_number": "1-312-555-5555",
            "email_address": "fake@email.com",
            "address": "1234 Main St.",
            "birth_date": "2019-01-01",
            "parent_ids": [4, 6]
        }

    ]

    def test_parents(self):
        api.reset_environment()
        ids, resp_code = api.person_add(copy.deepcopy(self.family1))
        r, resp_code = api.person_parents(ids[3])
        self.assertEqual(sorted([p['id'] for p in r]), [1,2])

    def test_parents2(self):
        api.reset_environment()
        ids, resp_code = api.person_add(copy.deepcopy(self.family1))
        r, resp_code = api.person_parents(ids[3])
        self.assertEqual(sorted([p['id'] for p in r]), [1,2])

    def test_children(self):
        api.reset_environment()
        ids, resp_code = api.person_add(copy.deepcopy(self.family1))
        r, resp_code = api.person_children(ids[0])
        self.assertEqual(sorted([p['id'] for p in r]), ids[2:])

    def test_siblings(self):
        api.reset_environment()
        ids, resp_code = api.person_add(copy.deepcopy(self.family1))
        r, resp_code = api.person_siblings(ids[3])
        self.assertTrue(3 in [p['id'] for p in r])

    def test_grandparents(self):
        api.reset_environment()
        ids, resp_code = api.person_add(copy.deepcopy(self.family2))
        r, resp_code = api.person_grandparents(ids[6])
        self.assertEqual(sorted(ids[0:2]), sorted([p['id'] for p in r]))

    def test_parent_siblings(self):
        api.reset_environment()
        ids, resp_code = api.person_add(copy.deepcopy(self.family2))
        r, resp_code = api.person_parent_siblings(ids[6])
        self.assertEqual(sorted(ids[3:4]), sorted([p['id'] for p in r]))

    def test_cousins(self):
        api.reset_environment()
        ids, resp_code = api.person_add(copy.deepcopy(self.family2))
        r, resp_code = api.person_cousins(ids[6])
        self.assertEqual(sorted(ids[7:8]), sorted([p['id'] for p in r]))

    def test_modify(self):
        api.reset_environment()
        ids, resp_code = api.person_add(copy.deepcopy(self.family1))
        new_val = 'FirstNAME'
        r, resp_code = api.modify_person(ids[0], 'first_name', new_val)
        self.assertEqual(r['first_name'], new_val)

    def test_query(self):
        api.reset_environment()
        ids, resp_code = api.person_add(copy.deepcopy(self.family1))
        r, resp_code = api.person_get('first_name', 'Jeffrey')
        self.assertTrue(ids[1] in [p['id'] for p in r])