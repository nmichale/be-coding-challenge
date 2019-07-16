from . import tree
from . import person

SUCCESS_CODE = 200
ERROR_CODE = 400

family = tree.FamilyTree()

def person_add(body):
    ids = []

    for i in range(len(body)):
        p = body[i]
        parent_ids = p.pop('parent_ids', [])
        new_person = person.Person(**p)
        ids.append(new_person.id)
        family.add_person(new_person, parent_ids)

    return ids, SUCCESS_CODE

def modify_person():
    pass

def person_siblings(person_id):
    return family.get_siblings(person_id)

def person_parents(person_id):
    return family.get_parents(person_id)