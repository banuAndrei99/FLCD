from grammar import Grammar
from my_parser import Parser


def display_options():
    print("1 Display Terminals")
    print("2 Display Non-terminals")
    print("3 Display Productions")
    print("4 Choose production to do closure")
    print("5 Choose symbol to do goto on state(ClosureLR of S'->S)")
    print("6 Col Can")


if __name__ == '__main__':
    g: Grammar = Grammar('g1.in')
    p = Parser(g)
    while True:
        display_options()
        i = int(input())
        if i == 1:
            print(p.get_e())
        elif i == 2:
            print(p.get_n())
        elif i == 3:
            print(p.get_p())
        elif i == 4:
            __user_input = input("Give input:")
            print(p.closure_lr(__user_input))
        elif i == 5:
            __user_input = input("Give input:")
            result = p.go_to_lr(p.closure_lr("S'->.S"), __user_input)
            print(result)
        elif i == 6:
            print(p.col_can())
        elif i == 0:
            break
