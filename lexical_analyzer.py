import os
from hash_table import SymbolTable, ConstantsTable
import json
import re


class LexicalAnalyzer:
    OPERATORS = {'=': 44, '+': 40, '-': 41,
                 '/': 43, '*': 42, '<': 45, '>': 50,
                 '==': 47, '<=': 46, ' >=': 48, '!=': 49, '%': 50}

    SEPARATORS = {' ': 30, ';': 31, '[': 32, ']': 33, '{': 34, '}': 35, '(': 36, ')': 37, ',': 38}

    RESERVED_WORDS = {'int': 150, 'char': 151, 'do': 152, 'while': 153, 'if': 154, 'else': 155, 'in': 156, 'out': 157,
                      'main': 158}

    def __init__(self, path_to_program):
        self.OPERATORS_KEYS = list(self.OPERATORS.keys())
        self.SEPARATORS_KEYS = list(self.SEPARATORS.keys())
        self.RESERVED_WORDS_KEYS = list(self.RESERVED_WORDS.keys())
        self.DELIMITERS = self.OPERATORS_KEYS + self.SEPARATORS_KEYS

        self.__symbol_table = SymbolTable()
        self.__constants_table = ConstantsTable()
        self.__pif = []
        self.__set_program(path_to_program)

    def __set_program(self, path_to_program):
        if not os.path.isfile(path_to_program):
            raise Exception(f'path {path_to_program} is not valid.')
        self.__path_to_program = path_to_program
        with open(self.__path_to_program, 'r') as program_file:
            self.__program_text = program_file.read()
        self.__program_text = self.__program_text\
            .strip().\
            replace('\n', '').\
            replace('\r\n', '').\
            replace('\t', '')

    def analyze(self) -> ([], SymbolTable):
        current_index = 0
        while current_index != len(self.__program_text):
            atom, end_pos = self.__detect_atom(current_index)
            current_index = end_pos
            if atom == ' ':
                continue
            self.__place(atom, end_pos)

    def get_pif(self):
        return self.__pif

    def get_st(self):
        return self.__symbol_table

    def get_ct(self):
        return self.__constants_table

    def __detect_atom(self, start_index) -> (str, int):
        atom = ''
        while start_index < len(self.__program_text) and not atom.endswith(tuple(self.DELIMITERS)):
            atom += self.__program_text[start_index]
            start_index += 1

        if atom not in self.DELIMITERS:
            if atom.endswith(tuple(list(filter(lambda delimiter: len(delimiter) == 2, self.DELIMITERS)))):
                atom = atom[:-2]
                start_index -= 2
            else:
                atom = atom[:-1]
                start_index -= 1

        return atom, start_index

    def __place(self, atom: str, pos: int):
        if atom in self.RESERVED_WORDS_KEYS or atom in self.OPERATORS_KEYS or atom in self.SEPARATORS_KEYS:
            self.__gen_pif(atom, pos)
        elif self.__is_identifier(atom):
            try:
                row, col = self.__symbol_table.get(atom)
            except KeyError:
                self.__symbol_table.add(atom)
                row, col = self.__symbol_table.get(atom)
            self.__gen_pif('ID', (row, col))
        elif self.__is_constant(atom):
            try:
                row, col = self.__constants_table.get(atom)
            except KeyError:
                self.__constants_table.add(atom)
                row, col = self.__constants_table.get(atom)
            self.__gen_pif('CONST', (row, col))
        else:
            raise SyntaxError(f'Lexical error on atom `{atom}` on character pos {pos-len(atom)}')

    @staticmethod
    def __is_identifier(var):
        return re.match("^[a-zA-Z][a-zA-Z0-9]*$", var)

    @staticmethod
    def __is_constant(var):
        return re.match(r'^[-+]?([1-9]\d*|0)$', var) or re.match(r"^'[0-9a-zA-Z]'$", var) \
               or re.match(r"^\"\w*\"$", var)  # int or char or string

    def __gen_pif(self, code, pos):
        if isinstance(pos, int):
            self.__pif.append((code, pos - len(code)))
        elif isinstance(pos, tuple):
            self.__pif.append((code, pos))
        else:
            raise TypeError(f'Expected {pos} of type {type(pos)} to be of type `int` or `tuple`')


if __name__ == '__main__':
    with open('token.json') as json_file:
        analyzer_static_data = json.load(json_file)
    LexicalAnalyzer.OPERATORS = analyzer_static_data['operators']
    LexicalAnalyzer.SEPARATORS = analyzer_static_data['separators']
    LexicalAnalyzer.RESERVED_WORDS = analyzer_static_data['reserved_words']
    for program in ["p1", "p2", "p3", "p1err"]:
        with open(f'{program}out', 'w') as out:
            try:
                out.write(f"ANALYZING {program}\n")
                analyzer = LexicalAnalyzer(program + '.txt')
                analyzer.analyze()
                out.write(f'\nSymbol Table:\n')
                out.write(str(analyzer.get_st()))
                out.write(f'\nConstant Table:\n')
                out.write(str(analyzer.get_ct()))
                out.write(f'PIF:\n')
                for entry in analyzer.get_pif():
                    out.write(f'{entry[0]} | {entry[1]}\n')
                out.write(f'\n\nVERDICT: LEXICALLY CORRECT\n\n')
            except Exception as e:
                out.write(f'\n\nVERDICT: LEXICALLY INCORRECT with error: {e}')
