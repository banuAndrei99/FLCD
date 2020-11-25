import json

from grammar import Grammar
from copy import deepcopy


class Parser:
    def __init__(self, grammar: Grammar):
        self.__grammar = grammar

    def get_p(self):
        return self.__grammar.get_productions()

    def get_n(self):
        return self.__grammar.get_non_terminals()

    def get_e(self):
        return self.__grammar.get_terminals()

    def closure_lr(self, analysis: str):
        tokens: list = analysis.replace('->', ' ').split(' ')
        p = {
            tokens[0]: [tokens[1]]
        }
        while True:
            size = len(p.keys())
            filtered_p = deepcopy(p)
            for key, val in filtered_p.items():
                for elem in val:
                    try:
                        index = elem.index('.')
                    except ValueError:
                        index = -1
                    if index != -1 and index < len(elem) - 1:
                        non_terminal = elem[index + 1]
                        productions_for_non_terminal = self.__grammar.get_production_for_non_terminal(non_terminal)
                        for _val in productions_for_non_terminal:
                            if non_terminal not in p.keys():
                                p[non_terminal] = []
                            if f".{_val}" not in p[non_terminal]:
                                p[non_terminal].append(f".{_val}")
            if size == len(p.keys()):
                break
        return p

    def go_to_lr(self, productions: dict, symbol: str):
        nested_list = []
        for key, val in productions.items():
            for idx, elem in enumerate(val):
                if f".{symbol}" in elem:
                    nested_list.append(self.closure_lr(f"{key}->{val[idx]}"))
                    parts = val[idx].split('.')
                    val[idx] = parts[0] + parts[1][0] + '.' + parts[1][1:]
                    print(f"dot moved from {elem} to {val[idx]}")
        return nested_list, productions

    def col_can(self):
        c = [self.closure_lr(f"S'->.S")]

        changed = False
        first_run = True
        while changed or first_run:
            first_run = False
            changed = False
            filtered_c = deepcopy(c)
            for __state in filtered_c:
                for element in self.__grammar.get_non_terminals() + self.__grammar.get_terminals():
                    go_to_result = self.go_to_lr(__state, element)
                    if len(go_to_result[0]) > 0 and not self.includes(c, go_to_result[0], element):
                        c.extend(go_to_result[0])
                        changed = True
        return self.remove_duplicates(c)

    @staticmethod
    def includes(c, go_to_result, elem):
        for __production in c:
            if isinstance(go_to_result, list):
                go_to_result = go_to_result[0]
            if elem in __production and elem in go_to_result:
                if set(go_to_result[elem]) <= set(__production[elem]):
                    return True
        return False

    @staticmethod
    def remove_duplicates(c):
        list_without_duplicates = []
        for x in c:
            if isinstance(x, dict):
                list_without_duplicates.append(json.dumps(x))
            elif isinstance(x, dict):
                for __inner in x:
                    list_without_duplicates.append(json.dumps(__inner))
        list_without_duplicates = list(set(list_without_duplicates))

        return [json.loads(x) for x in list_without_duplicates]