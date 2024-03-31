from random import randint,choice
from datetime import datetime

def generatorMatrizGame()->str:
    r =  randint(10,70)
    c = randint(10,125)
    objects = ['2','3']
    matrix = []
    for i in range(r):
        row = []
        for j in range(c):
            pro = randint(0,100)
            if pro<30:
                row.append('7')
            elif pro<37:
                row.append( choice(objects))
                
            else:
                row.append('0')
        matrix.append(row)

    matrix[randint(0,r-1)][randint(0,c-1)] = '*'
    matrix[randint(0,r-1)][randint(0,c-1)] = '@'


    date_creaion = datetime.now().microsecond
    matriz_name = f'{r}x{c}_{str(date_creaion)}_R'
    with open(f'./src/matrices/{matriz_name}.txt','w') as file: 
            for row in matrix:
                row_str = ''
                for j,obj in enumerate(row):
                        row_str+=obj                  
                file.write(row_str+'\n') 
          
    return matriz_name


       
    
    