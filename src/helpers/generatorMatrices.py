from random import randint, choice
from datetime import datetime
from os import path


def generatorMatrizGame() -> str:
    r = 50
    c = 50
    objects = ['V', 'H']
    matrix = []
    for i in range(r):
        row = []
        for j in range(c):
            pro = randint(0, 100)
            if pro < 30:
                row.append('X')
            elif pro < 40:
                row.append(choice(objects))
            else:
                row.append('1')
        matrix.append(row)

    matrix[randint(0, r-1)][randint(0, c-1)] = '*'
    matrix[randint(0, r-1)][randint(0, c-1)] = '@'
    date_creaion = datetime.now().microsecond
    name = f'{r}x{c}_{str(date_creaion)}_R'
    with open(path.join(path.dirname(__file__), f'../matrices/{name}.txt'), 'w') as file:
        for row in matrix:
            row_str = ''
            for j, obj in enumerate(row):
                row_str += obj
            file.write(row_str+'\n')

    return name
