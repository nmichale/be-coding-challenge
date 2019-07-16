import networkx as nx

class FamilyTree(object):

    def __init__(self, edgelist=None):
        self.dg = nx.DiGraph()

    def _changes_to_db(func):
        '''
        In a more complete project, this would push any changes to a database to persist
        the data.

        :return: Wrapper for decorator
        '''
        def wrapper(self, *args, **kwargs):
            before = nx.to_pandas_edgelist(self.dg)
            print('Before:', before)
            func(self, *args, **kwargs)
            after = nx.to_pandas_edgelist(self.dg)
            print('After:', after)
        return wrapper

    def add_person(self, person, parent_ids=[]):
        '''
        Add a person to the family tree. Parents are not required.

        :param person:
        :param parent_ids:
        :return:
        '''
        self.dg.add_node(person.id, person=person)
        if len(parent_ids) > 0:
            self.add_parents(person.id, parent_ids)

    @_changes_to_db
    def add_parents(self, person_id, parent_ids):
        '''
        Add parents.

        :param person_id:
        :param parent_ids:
        :return:
        '''
        print([(i, person_id) for i in parent_ids])
        self.dg.add_edges_from([(i, person_id) for i in parent_ids])

    def get_people(self, node_id_gen):
        people = []

        for n in node_id_gen:
            people.append(self.dg.nodes[n]['person'].to_dict())

        return people

    def get_siblings(self, person_id):
        pass

    def get_parents(self, person_id):
        parents = self.dg.predecessors(person_id)
        print(list(parents))
        parents = self.get_people(parents)

        return parents



