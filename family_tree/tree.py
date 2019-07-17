import networkx as nx
import pandas as pd

class FamilyTree(object):

    def __init__(self, edgelist=None):
        self._dg = nx.DiGraph()

    def clear(self):
        self._dg.clear()

    def _changes_to_db(func):
        '''
        Find what changed after the family tree is modified.
        In a more complete project, this would push any changes to a database to persist
        the data. I would later then load the family tree using this function:
        https://networkx.github.io/documentation/latest/reference/generated/networkx.convert_matrix.from_pandas_edgelist.html

        :return: Wrapper for decorator
        '''
        def wrapper(self, *args, **kwargs):
            before = nx.to_pandas_adjacency(self._dg)
            func(self, *args, **kwargs)
            after = nx.to_pandas_adjacency(self._dg)
            idx_union = before.index.union(after.index)
            before = before.reindex(idx_union)
            after = after.reindex(idx_union)
            diff = after.subtract(before)

            # Find symmetric difference. This is what I would use to do CRUD on relational db.
            df = diff.unstack().to_frame()
            df.index = df.index.rename(['edge_to', 'edge_from'])
            df.columns = ['diff']
            df = df[df['diff'] != 0]
            df['changed'] = df['diff'].map(lambda x: 'Added' if x > 0 else 'Removed')
            print('Symmetric diff:\n', df)

        return wrapper

    def add_person(self, person, parent_ids=[]):
        '''
        Add a person to the family tree. Parents are not required.

        :param person:
        :param parent_ids:
        :return:
        '''
        self._dg.add_node(person.id, person=person)
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
        self._dg.add_edges_from([(i, person_id) for i in parent_ids])

    def get_people(self, node_ids):
        '''
        Convert list/generator of person id's to list of dictionaries.

        :param node_id_gen:
        :return:
        '''
        people = []

        for n in node_ids:
            people.append(self._dg.nodes[n]['person'].to_dict())

        return people

    @staticmethod
    def remove_dupes(people, exclude_ids=[]):
        if len(people) <= 0:
            return people

        df = pd.DataFrame(people).drop_duplicates()
        df = df[~df['id'].isin(exclude_ids)]

        return df.to_dict(orient='records')

    def get_siblings(self, person_id):
        '''
        Find the siblings of a person by getting the children of the parents != self.

        :param person_id:
        :return:
        '''
        parents = self.get_parents(person_id)
        siblings = []

        for p in parents:
            siblings.extend(self.get_children(p['id']))

        siblings = self.remove_dupes(siblings, [person_id])

        return siblings

    def get_children(self, person_id):
        '''
        Find teh children of a person by getting the successors.

        :param person_id:
        :return:
        '''
        children = self._dg.successors(person_id)
        children = self.get_people(children)

        return children

    def get_parents(self, person_id):
        '''
        Find the parents of a person by getting the precessors.

        :param person_id:
        :return:
        '''
        parents = self._dg.predecessors(person_id)
        parents = self.get_people(parents)

        return parents

    def get_grandparents(self, person_id):
        '''
        Get grandparents of person.

        :param person_id:
        :return:
        '''
        parents = self.get_parents(person_id)
        grandparents = []

        for p in parents:
            grandparents.extend(self.get_parents(p['id']))

        grandparents = self.remove_dupes(grandparents)

        return grandparents

    def get_parent_siblings(self, person_id):
        '''
        Get siblings of parents (aunts and uncles)

        :param person_id:
        :return:
        '''
        parents = self.get_parents(person_id)
        parent_siblings = []

        for p in parents:
            parent_siblings.extend(self.get_siblings(p['id']))

        parent_siblings = self.remove_dupes(parent_siblings)

        return parent_siblings

    def get_cousins(self, person_id):
        '''
        Get cousins of a person.

        :param person_id:
        :return:
        '''
        parent_siblings = self.get_parent_siblings(person_id)
        cousins = []

        for p in parent_siblings:
            cousins.extend(self.get_children(p['id']))

        cousins = self.remove_dupes(cousins)

        return cousins

    def modify_person(self, person_id, attribute, new_value):
        '''
        Modify a given attribute of a person.

        :param person_id:
        :param attribute:
        :param new_value:
        :return: Dictionary of new person
        '''
        p = self._dg.nodes[person_id]['person']
        setattr(p, attribute, new_value)

        return p.to_dict()

    def query_attribute(self, attribute, value):
        '''
        Query family tree based on where attribute == value.

        :param attribute:
        :param value:
        :return: List of dictionaries of matching people
        '''
        matched = []
        for node, node_attrib in self._dg.nodes.items():
            p = node_attrib['person']
            val = getattr(p, attribute)
            if val == value:
                matched.append(p.to_dict())

        return matched

