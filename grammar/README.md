
## GRAMMAR

### ```constructor(path_to_file: str) -> Grammar```
- pre: path_to_file leads to a file containing a grammar
- post: terminals, non_terminals and productions are build from that file

###  ```get_non_terminals()-> [str]```
Returns a list of non terminals
- pre: None
- post: None

###  ```get_terminals() -> [str] ```
Returns a list of terminals
- pre: None
- post: None

###  ```get_productions() -> dict ```
Returns a dictionary containing all the productions
- pre: None
- post: None

### ```__def get_production_for_non_terminal(self, non_terminal: str) -> [str]```
Returns the list of production for a non terminal, or empty list of the non terminal is not in the grammar.
- pre: None
- post: None
