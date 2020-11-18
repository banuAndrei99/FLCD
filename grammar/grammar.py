

class Grammar:
    def __init__(self, path_to_file):
        self.__terminals: [str] = []
        self.__non_terminals: [str] = []
        self.__productions: dict = {}
        self.__path_to_file = path_to_file
        self.__read_from_file(self.__path_to_file)

    def __read_from_file(self, __path_to_file):
        with open(self.__path_to_file, 'r') as fh:
            text_lines = fh.readlines()

        self.__non_terminals = [elem for elem in text_lines[0].strip().split(',')]
        self.__terminals = [elem for elem in text_lines[1].strip().split(',')]

        for line in text_lines[2:]:
            split = line.strip().split("->")
            non_terminal = split[0]
            right_side = [elem.strip() for elem in split[1].split('|')]

            __list = self.__productions.get(non_terminal, [])
            for elem in right_side:
                __list.append(elem)

            self.__productions[non_terminal] = __list

    def get_terminals(self):
        return self.__terminals

    def get_non_terminals(self):
        return self.__non_terminals

    def get_productions(self):
        return self.__productions

    def get_production_for_non_terminal(self, non_terminal: str) -> [str]:
        return self.__productions.get(non_terminal, [])


if __name__ == '__main__':
    grammar = Grammar('g1.in')
    print(grammar.get_non_terminals())
    print(grammar.get_terminals())
    print(grammar.get_productions())
    print(grammar.get_production_for_non_terminal('S'))
