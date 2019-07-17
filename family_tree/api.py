from . import tree
from . import person
from . import database

SUCCESS_CODE = 200
ERROR_CODE = 400

family = tree.FamilyTree()

def reset_environment():
    '''
    Use this before running tests to clear tree.

    :return:
    '''
    global family

    family = tree.FamilyTree()
    database.fake_conn.last_id = 0

def person_add(body):
    '''
    Add a person from the POST request body.

    :param body:
    :return: id's of person
    '''
    ids = []

    for i in range(len(body)):
        p = body[i]
        parent_ids = p.pop('parent_ids', [])
        new_person = person.Person(**p)
        ids.append(new_person.id)
        family.add_person(new_person, parent_ids)

    return ids, SUCCESS_CODE


def person_get(attribute, value):
    '''
    Get person by attribute and value. In a more complete version I'd probably allow querying on multiple attributes.

    :param attribute:
    :param value:
    :return: List of people that match
    '''

    return family.query_attribute(attribute, value), SUCCESS_CODE


def modify_person(person_id, attribute, value):
    '''
    Modify the attribute of a person.

    :param person_id:
    :param attribute:
    :param new_value:
    :return: New person dict
    '''

    return family.modify_person(person_id, attribute, value), SUCCESS_CODE

def person_siblings(person_id):
    '''

    :param person_id:
    :return: Siblings of a person
    '''
    return family.get_siblings(person_id), SUCCESS_CODE


def person_parents(person_id):
    '''

    :param person_id:
    :return: Parents of a person
    '''
    return family.get_parents(person_id), SUCCESS_CODE

def person_children(person_id):
    '''

    :param person_id:
    :return: Siblings of a person
    '''
    return family.get_children(person_id), SUCCESS_CODE

def person_grandparents(person_id):
    '''

    :param person_id:
    :return: Parents of a person
    '''
    return family.get_grandparents(person_id), SUCCESS_CODE

def person_parent_siblings(person_id):
    '''

    :param person_id:
    :return: Parent siblings (aunts and uncles) of a person
    '''
    return family.get_parent_siblings(person_id), SUCCESS_CODE

def person_cousins(person_id):
    '''

    :param person_id:
    :return: Parent siblings (aunts and uncles) of a person
    '''
    return family.get_cousins(person_id), SUCCESS_CODE

def add_parents(person_id, parent_ids):
    '''
    This would function adds extra parent edges.

    :param person_id:
    :param parent_ids:
    :return:
    '''

    family.add_parents(person_id, parent_ids)
    return family.get_parents(person_id), SUCCESS_CODE

def remove_parents(person_id, parent_ids):
    '''
    This function removes parent edges

    :param person_id:
    :param parent_ids:
    :return:
    '''

    family.remove_parents(person_id, parent_ids)
    return family.get_parents(person_id), SUCCESS_CODE