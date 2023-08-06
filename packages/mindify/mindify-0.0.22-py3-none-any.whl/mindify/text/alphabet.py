import json
import numpy as np
import pandas as pd


class Alphabet:
    def __init__(self):
        self.index2name = {}
        self.name2index = {}
        self.current_index = 0
        self.__frozen = False

    def save_to(self, filename):
        with open(filename, 'w', encoding='utf-8') as fp:
            json.dump(self.to_dict(), fp)

    @staticmethod
    def load_from(filename) -> 'Alphabet':
        alphabet = Alphabet()

        with open(filename, 'r', encoding='utf-8') as fp:
            data = json.load(fp)

            alphabet.index2name = data['index2name']
            alphabet.name2index = data['name2index']
            alphabet.current_index = data['current_index']

        return alphabet

    def to_dict(self):
        return dict(
            index2name=self.index2name,
            name2index=self.name2index,
            current_index=self.current_index
        )

    def freeze(self):
        self.__frozen = True

    @property
    def size(self):
        return len(self.index2name)

    @property
    def vocabs(self):
        return list(self.name2index.keys())

    def lookup(self, obj, add_if_not_present=True):
        return self.lookup_index(obj, add_if_not_present=add_if_not_present)

    def lookup_index(self, obj, add_if_not_present=True):
        if isinstance(obj, list) or isinstance(obj, np.ndarray) or isinstance(obj, pd.Series):
            return [self.lookup_index(w, add_if_not_present) for w in list(obj)]

        if obj in self.name2index:
            return self.name2index[obj]
        elif self.__frozen:
            raise ValueError("failed to find " + obj)
        elif not add_if_not_present:
            raise ValueError("failed to find " + obj)

        index = self.current_index
        self.current_index += 1

        self.name2index[obj] = index
        self.index2name[str(index)] = obj

        return index

    def lookup_object(self, index):
        index = str(int(index))

        if index not in self.index2name:
            raise ValueError("failed to find index " + index)

        return self.index2name[index]

    def lookup_objects(self, indices):
        return [self.lookup_object(index) for index in list(indices)]
