

class HashTable(object):

    def __init__(self, length=4):
        self.table = [None] * length
        self.length = length

    def __hash(self, key):
        """hash() is useful to transform strings into numeric values"""
        return hash(key) % self.length

    def add(self, key) -> None:
        """
        :param key: any hashable
        :return: None
        """
        index = self.__hash(key)
        if not self.table[index]:
            self.table[index] = [key]
        else:
            self.table[index].append(key)

    def get(self, key):
        """
        :param key: any hashable
        :returns index on which the item can be found in the hashtable
        :raises KeyError when key is not in hashtable
        """
        index = self.__hash(key)
        if self.table[index] is None:
            raise KeyError(f'There are no elements for {key} in hashtable')

        for existing_key in self.table[index]:
            if existing_key == key:
                return index
        raise KeyError(f'{key} does not appear in hashtable')

    def __str__(self):
        table_representation = ''
        for idx in range(self.length):
            pairs = '['
            try:
                for x in self.table[idx]:
                    if x:
                        pairs += str(x) + ','
            except TypeError:
                pass
            finally:
                pairs += ']'
            table_representation += f'{idx} --> {pairs}\n'

        return table_representation


class SymbolTable(HashTable):
    def add(self, key) -> None:
        if not isinstance(key, str):
            raise Exception('In symbol table, all keys must be strings')
        super().add(key)

    def get(self, key):
        if not isinstance(key, str):
            raise Exception('In symbol table, all keys must be strings')
        return super().get(key)


if __name__ == '__main__':

    symbols = SymbolTable(2)
    symbols.add("a")
    symbols.add("b")
    symbols.add("c")
    print(symbols)
    print(symbols.get('a'))



