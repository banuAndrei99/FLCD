import json
from menu import Menu
from anytree import Node, RenderTree, find, findall


class AutomatonNode(Node):
    def __init__(self, name, parent, transition=None):
        super(AutomatonNode, self).__init__(name, parent)
        self.parent = parent
        self.transition = transition

    def _post_detach(self, parent):
        self.transition = None


class FiniteAutomaton:
    def __init__(self, file_path):
        with open(file_path) as fh:
            data = json.load(fh)
        self.states = data["states"]
        self.start_state = data["start_state"]
        self.final_states = data["final_states"]
        self.alphabet = data["alphabet"]
        self.transitions = data['transitions']
        self.start_node = None
        self.__build_tree()
        self.menu = Menu(options=[
            ("Print states", self.__print_states),
            ("Print alphabet", self.__print_alphabet),
            ("Print final states", self.__print_final_states),
            ("Print transition dictionary", self.__print_transitions),
            ("Print transition tree", self.__print_transition_tree),
            ("Check sequence", self.check_wrapper),
            ("Close", Menu.CLOSE)
        ])

    def __print_states(self):
        print(self.states)

    def __print_alphabet(self):
        print(self.alphabet)

    def __print_final_states(self):
        print(self.final_states)

    def __print_transitions(self):
        print(self.transitions)

    def check_wrapper(self, sequence=None):
        if not sequence:
            sequence = input("Enter a sequence: ")
        ret_val = self.check(sequence=sequence, current_state=self.start_state)
        if ret_val:
            print("everything OK")
        else:
            print("sequence cannot be obtained from this automaton")

    def check(self, sequence=None, current_state=None):
        if sequence == "":
            if current_state in self.final_states:
                return True
            else:
                return False
        char = sequence[0]
        possible_future_states = []
        for transition, future_state in self.transitions[current_state].items():
            if transition == char:
                possible_future_states.append(future_state)
        if not possible_future_states:
            return False
        else:
            return any([self.check(sequence[1:], state) for state in possible_future_states])

    def __build_tree(self):
        for state, transitions in self.transitions.items():
            if self.start_node:
                node = find(self.start_node, filter_=lambda n: n.name == state) or AutomatonNode(name=state, parent=None)
            else:
                node = AutomatonNode(name=state, parent=None)
            if state == self.start_state:
                self.start_node = node
            for t, s in transitions.items():
                AutomatonNode(name=s, parent=node, transition=t)

    def __print_transition_tree(self):
        for pre, _, node in RenderTree(self.start_node):
            print("%s%s (%s)" % (pre, node.name, node.transition or None))


if __name__ == '__main__':
    fa = FiniteAutomaton("FA.json")
    print(fa.transitions)
    fa.menu.open()