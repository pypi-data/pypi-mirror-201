class Cell:
    instances = []

    @classmethod
    def write_instances_to_file(cls, filename) -> None:
        """
        Class method to write all instances into the file
        :param filename: name of the file
        :type filename: str
        :return: None
        """
        with open(filename, 'w') as file:
            for instance in cls.instances:
                file.writelines(instance.lines)

    def __init__(self, name, universe, material, surfaces, delimiter='  '):
        self.__class__.instances.append(self)
        self.name = f'c{name}'
        self.delimiter = delimiter
        self.line = f'{self.name}{delimiter}{universe}{delimiter}{material}'
        for surface in surfaces:
            self.line += f'{delimiter}{surface}'
        pass

    def __str__(self):
        return self.line

    def __add__(self, other):
        if type(other) == str:
            self.line += f'{self.delimiter}{other}'
            return self.line
        elif type(other) == Cell:
            self.line += f'{self.delimiter}{other.name}'
            return self.line

    def __sub__(self, other):
        if type(other) == str:
            self.line += f'{self.delimiter}-{other}'
            return self.line
        elif type(other) == Cell:
            self.line += f'{self.delimiter}#{other.name}'
            return self.line
        elif type(other) == list:
            for i, cell in enumerate(other):
                if type(cell) == Cell:
                    _cell_name = cell.name
                elif type(cell) == str:
                    _cell_name = cell
                else:
                    raise RuntimeError('should be list of str or Cell')

                if i == 0:
                    self.line += f'{self.delimiter} -({_cell_name}'
                elif i == len(other) - 1:
                    self.line += f'{self.delimiter} {_cell_name})'
                else:
                    self.line += f'{self.delimiter} {_cell_name}'
            return self.line


if __name__ == '__main__':
    c = Cell('name', 'uni', 'mat', ['1', '2'])
    c1 = Cell('name', 'uni', 'mat', ['1', '2'])
    c2 = Cell('name', 'uni', 'mat', ['1', '2'])
    print(c)
    print(c + 'hello')
    print(c - 'hello')
    print(c - c1)
    print(c + c1)
    print(c - [c1, c2])
    print(c - ['f', 'e'])
    inst = Cell.instances[2]
    print(inst)
    c3 = c2

