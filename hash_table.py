

class Pair:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return f'(key: {self.key}, value: {self.value})'


class HashTable(object):

    def __init__(self, length=4):
        self.table = [None] * length
        self.length = length

    def hash(self, key):
        """hash() is useful to transform strings into numeric values"""
        return hash(key) % self.length

    def add(self, key, value) -> None:
        """
        :param key: any hashable
        :param value: any
        :return: None
        """
        pair = Pair(key, value)
        index = self.hash(pair.key)
        if not self.table[index]:
            self.table[index] = [pair]
            return
        for existing_pair in self.table[index]:
            if existing_pair.key == pair.key:
                existing_pair.value = pair.value
                break
        else:
            self.table[index].append(pair)

    def __getitem__(self, key):
        """
        :param key: any hashable
        :returns value associated to key
        :raises KeyError when key is not in hashtable
        """
        index = self.hash(key)
        if self.table[index] is None:
            raise KeyError(f'There are no elements for {key} in hashtable')

        for existing_pair in self.table[index]:
            if existing_pair.key == key:
                return existing_pair.value
        raise KeyError(f'{key} does not appear in hashtable')

    def __str__(self):
        table_representation = ''
        for idx in range(self.length):
            pairs = '['
            try:
                for x in self.table[idx]:
                    if x:
                        pairs += str(x)
            except TypeError:
                pass
            finally:
                pairs += ']'
            table_representation += f'{idx} --> {pairs}\n'

        return table_representation


if __name__ == '__main__':
    table = HashTable(7)
    table.add(1, 5)
    table.add(2, 10)
    table.add(8, 20)
    table.add(1, 23)
    print(table[1])
    print(table)

