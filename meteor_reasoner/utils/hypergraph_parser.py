from collections import defaultdict
import json

class HyperGraphParser:
    def __init__(self, conns, facts):
        self.entities = defaultdict(str)
        self.conns = conns
        self.edges = []
        self.vertices = []
        self.facts = facts

    def initialization(self):
        for fact in self.facts:
            v = GraphEntity(entity_string=fact)
            if v not in self.vertices:
                idx = len(self.vertices)
                self.vertices.append(v)
                v.set_id(idx)
            self.edges.append(([], "Asserted", v))
        for conn in self.conns:
            child = GraphEntityResolver.vertices_from_entity(conn['succ'])
            parents = GraphEntityResolver.vertices_from_entity(conn['pred'])
            rule = conn['rule']
            for v in child + parents:
                if v not in self.vertices:
                    idx = len(self.vertices)
                    self.vertices.append(v)
                    v.set_id(idx)
                else:
                    idx = self.vertices.index(v)
                    v.set_id(idx)
            self.edges.append((parents, conn['rule'], child[0]))


    def compact_edges(self):
        return [([*map(lambda x : x.get_id(), e[0])], e[1], e[2].get_id()) for e in self.edges]

    def describe_v(self, id):
        idx = self.compact_vertices().index(id)
        return self.vertices[idx].__str__()

    def write_to_file_as_json(self, file_path):
        with open(file_path, 'w') as f:
            json.dump({
                'edges': self.compact_edges(),
                'full_vertices': [*map(lambda v: v.__str__(), self.vertices)],
            }, f)


class GraphEntityResolver:
    @classmethod
    def vertices_from_entity(cls, entity):
        vs = []
        if isinstance(entity, dict):
            keys = entity.keys()
            if 'alpha_1' in keys and 'alpha_2' in keys:
                # Entity from binary rule
                for i in range(2):
                    alpha = entity[f'alpha_{i+1}']
                    interval = entity[f'roh_{i+1}']
                    vs.append(GraphEntity(alpha=alpha, interval=interval))
            elif 'interval' in keys:
                # Entity from literal with interval
                alpha = entity['alpha']
                interval = entity['interval']
                vs.append(GraphEntity(alpha=alpha, interval=interval))
            else:
                # Entity from unary rule
                alpha = entity['alpha']
                interval = entity['roh_1']
                vs.append(GraphEntity(alpha=alpha, interval=interval))
        elif isinstance(entity, str):
            # Entity from simple atom
            vs.append(GraphEntity(entity_string=entity))
        elif isinstance(entity, list):
            # Entity is list of entities
            for e in entity:
                vs += GraphEntityResolver.vertices_from_entity(e)
        else:
            raise Exception(f"Unknown entity type: {type(entity)}")

        return vs


class GraphEntity:
    def __init__(self, alpha=None, interval=None, entity_string=None):
        if entity_string is not None:
            alpha, interval = entity_string.split('@')
            if interval[0] != '[':
                interval = f"[{interval},{interval}]"
        self.alpha = alpha
        self.interval = interval
        self.id = None

    def __str__(self):
        return f"{self.alpha}@{self.interval}"

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def set_id(self, id):
        self.id = id

    def get_id(self):
        if self.id is None:
            raise Exception(f"Id not set for {self.__str__()}")
        return self.id
