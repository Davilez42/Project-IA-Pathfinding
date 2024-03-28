from random import randint,choice

def generateMatrixGame():
    rows =  randint(10,20)
    columns =  randint(10,20)
    options = ['0','X','2','3']
    matrix = []
    for i in range(rows):
        row = []
        for j in range(columns):
            obj  = choice(options)            
            row.append(obj)
        matrix.append(row)

    matrix[randint(0,rows-1)][randint(0,columns-1)] = '*'
    matrix[randint(0,rows-1)][randint(0,columns-1)] = '7'


    code_matrix = randint(100,500)
    with open(f'./src/juegos/matrix{code_matrix}.txt','w') as file: 
            for row in matrix:
                row_str = ''
                for j,obj in enumerate(row):
                    if j<columns-1:
                        row_str+=obj+' '
                    else:
                        row_str+=obj
                        
                file.write(row_str+'\n') 
          


    
generateMatrixGame()
    
       
    
    