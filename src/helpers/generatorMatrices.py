from random import randint, choice
from datetime import datetime
from os import path


def generatorMatrizGame() -> str:
    d = randint(5, 50)
    objects = ['V', 'H']
    matrix = []
    for i in range(d):
        row = []
        for j in range(d):
            pro = randint(0, 100)
            if pro < 30:
                row.append('X')
            elif pro < 40:
                row.append(choice(objects))
            else:
                row.append('1')
        matrix.append(row)

    matrix[randint(0, d-1)][randint(0, d-1)] = '*'
    matrix[randint(0, d-1)][randint(0, d-1)] = '@'
    date_creaion = datetime.now().microsecond
    name = f'{d}x{d}_{str(date_creaion)}_R'
    with open(path.join(path.dirname(__file__), f'../matrices/{name}.txt'), 'w') as file:
        for row in matrix:
            row_str = ''
            for j, obj in enumerate(row):
                row_str += obj
            file.write(row_str+'\n')

    return name
