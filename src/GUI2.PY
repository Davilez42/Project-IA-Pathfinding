from time import sleep,gmtime
import pygame
import numpy as np
import threading
from math import ceil
import datetime

from ambiente import Ambiente

#constant

WIDTH = 1200
HEIGHT = 750


class GUI2:
    def __init__(self,width,heigth) -> None: 
        self.historial = []
        self.width = width
        self.heigth = heigth
        
        self.counter_nodes_create_star  =0
        self.counter_nodes_expanded_star  =0
        self.counter_costo_total_star = 0
    
    def loadMatrix(self,juego):
        with open(f'./matrices/{juego}.txt') as m:
            self.init_matrix = []
            for i,r in enumerate(m.readlines()):
                row:str = r.replace('\n','')
                row:list = row.split(' ')
                row = list(map(lambda x: int(x) if str.isnumeric(x) else x.upper(),row))    
                try:
                   self.pos_agent = (row.index(7),i)                
                except ValueError :
                    pass
                try:
                   self.pos_churiken = (row.index('*'),i)                
                except ValueError :
                    pass
                                         
                self.init_matrix.append(row)
                
            self.init_matrix = np.array(self.init_matrix)       
       
        #defino el tamano del juego en base a la matrix leida     
        rows = self.init_matrix.shape[1] #cantidad en y, filas
        col = self.init_matrix.shape[0]# cantidad en x   columnas 
        self.w = self.heigth/col if col>=rows else self.heigth/rows
        self.w= round(self.w)
        #redefino la pantalla
        self.space_x = abs(self.heigth- self.w*rows)
        self.space_y = abs(self.heigth- self.w*col)

        self.run()



    def mappingMatrixOnScreen(self):
        r=0
        c=0
        #mapeo la matrix en la pantalla recorriendo filas y columnas y creando su correspondiebte elemento
        for i in range(self.init_matrix.shape[0]):
            for j in range(self.init_matrix.shape[1]):
                elem = self.init_matrix[i,j]
                pygame.draw.rect(self.screen,(29, 29, 29),(c,r,self.w,self.w))
                    
                if(elem=='X'):
                    pygame.draw.rect(self.screen,(120, 121, 123),(c,r,self.w,self.w))
                            
                if(elem=='*'):
                    pygame.draw.circle(self.screen,'crimson',(c+self.w/2,r+self.w/2),self.w/2)

                if(elem=='7'):
                    pygame.draw.circle(self.screen,'white',(c+self.w/2,r+self.w/2),self.w/2)
         
                if(elem=='3'):
                    pygame.draw.rect(self.screen,'brown1',(c,r,self.w*0.2,self.w))
                    
                if(elem=='2'):
                    pygame.draw.rect(self.screen,'brown1',(c,r+self.w-self.w*0.2,self.w,self.w*0.2))
                                     
                c+= self.w
            r+= self.w
            c=0

    def putTextOnScreen(self):     

        pygame.draw.rect(self.screen,'black',(760,0,500,500))
         
        label_text = pygame.font.SysFont("calabria", 50)
        label_min = pygame.font.SysFont("calabria", 30)
        text_data = pygame.font.SysFont("calabria", 25)
        
        
        self.label_Data = label_text.render('Informacion',1,(252, 251, 252))        
        self.label_astar = label_text.render('A*',1,(252, 251, 252))
        self.label_bfs = label_text.render('BFS',1,(252, 251, 252))
        self.label_time = label_min.render('Tiempo',1,(252, 251, 252))
        self.label_nodes_expanded = label_min.render('N.Expandidos',1,(252, 251, 252))
        self.label_nodes_created = label_min.render('N.Creados',1,(252, 251, 252))
        self.label_total_cost = label_min.render('Costo total',1,(252, 251, 252))
        self.label_deepth = label_min.render('Profundidad',1,(252, 251, 252))
        
        self.text_nodes_created_astar = label_min.render(str(self.counter_nodes_create_star),1,(252, 251, 252))
        self.text_nodes_expanded_astar = label_min.render(str(self.counter_nodes_expanded_star),1,(252, 251, 252))
        self.text_time_astar = label_min.render('--',1,(252, 251, 252))
        self.text_total_cost_astar = label_min.render(str(self.counter_costo_total_star),1,(252, 251, 252))
        self.text_deepth_astar = label_min.render('0',1,(252, 251, 252))
        
                
        
        
        #subtitulos
        self.screen.blit(self.label_Data,(870,10))
        self.screen.blit(self.label_nodes_expanded,(1030,150))
        self.screen.blit(self.label_nodes_created,(1030,200))
        self.screen.blit(self.label_time,(1030,250))
        self.screen.blit(self.label_time,(1030,250))
        self.screen.blit(self.label_total_cost,(1030,300))
        self.screen.blit(self.label_deepth,(1030,350))
        
        
        #titulos de algoritmo
        self.screen.blit(self.label_astar,(800,100))
        self.screen.blit(self.label_bfs,(920,100))    
        
        #texto informacion
        self.screen.blit(self.text_nodes_expanded_astar,(795,150))
        self.screen.blit(self.text_nodes_created_astar,(795,200))
        self.screen.blit(self.text_time_astar,(795,250))
        self.screen.blit(self.text_total_cost_astar,(795,300))
        self.screen.blit(self.text_deepth_astar,(795,350))


       
            
    def animationExpanded(self):  #animacion de nodos expandidos y creados
        self.mappingMatrixOnScreen()
        for action in self.historial:         
            isExpanded = action[0]
            coordenate = action[1]
            if(isExpanded):
                pygame.draw.rect(self.screen,'cyan',(coordenate[0]*self.w,coordenate[1]*self.w,self.w,self.w))
            else:
                pygame.draw.rect(self.screen,'chartreuse2',(coordenate[0]*self.w,coordenate[1]*self.w,self.w,self.w))
            sleep(0.01)
        self.animation = True
        
    def captureNodesExpandedAndCreated(self,coordenate,visited=True):   
        if(visited):
            self.counter_nodes_expanded_star+=1
        else:
            self.counter_nodes_create_star+=1
            
        self.historial.append((visited,coordenate))                     

          
    def initAlgorithm(self,algorithm,avoid_backing_out):   
        self.historial = []       
        ambiente = Ambiente(self.init_matrix,self.pos_agent,self.pos_churiken)        
        init_time = datetime.datetime.now()
        result = ambiente.run(self.captureNodesExpandedAndCreated,algorithm,avoid_backing_out) 
        end_time = datetime.datetime.now()
        
        print(f' nodos expandidos: {result[2]} nodos_creados: {result[3]}  tiempo_empleado:{end_time-init_time} costo-total:{result[4]}')
        route = result[0]
        print(result[3])
        movements = result[1]        
        self.animationRoute(algorithm,movements,route[0])

   
   
   
   
    def animationRoute(self,algorithm,movements,init_coordanate):
        if algorithm=='a*':
            self.mappingMatrixOnScreen()   
        width = self.w/2
        x = init_coordanate[0]
        y = init_coordanate[1]
        color  = 'darkorchid1' if algorithm=='a*' else (81, 124, 87)
        vector = pygame.Vector2(x*self.w+width,y*self.w+width)
        
        frame_s = ceil(self.w)

        for i in movements:   
            for j in range(frame_s):
                if i=='R':
                    vector.x+=1
                if i=='L':
                    vector.x-=1
                if i=='D':
                    vector.y+=1
                if i=='U':
                    vector.y-=1
                pygame.draw.circle(self.screen,color,vector,width/2) 
                sleep(0.001)               
        self.animation = True     
   
   
   
   
   
    def run(self): 
        self.screen = pygame.display.set_mode((self.width-self.space_x,self.heigth-self.space_y),True)
        self.screen2 = pygame.display.set_mode((self.width-self.space_x,self.heigth-self.space_y),True)
        self.screen2.fill('black')
        pygame.font.init()
        pygame.display.set_caption('Proyecto 1 - IA - A* & BFS')
       
        self.clock = pygame.time.Clock()
        self.running = True 
        
        #elementos en la pantalla
        self.mappingMatrixOnScreen()  
        self.putTextOnScreen()
        self.animation = True
        while self.running:
            for event in pygame.event.get():
                if(event.type==pygame.QUIT):
                   self.running=False 
            self.putTextOnScreen()
          
            if self.animation and pygame.key.get_pressed()[pygame.K_a]:
                print('ejecutando A*....')
                self.thread_astar =  threading.Thread(target=self.initAlgorithm,args=('a*',True))#para demasiados estado es optimo no reccorrer nodos que ya han sido expandido, pero compromete la completitud de algoritmo
                self.thread_astar.start()
                self.animation=False
                
            if self.animation and pygame.key.get_pressed()[pygame.K_d]:
                print('ejecutando bfs....')
                self.thread_bfs =  threading.Thread(target=self.initAlgorithm,args=('bfs',True))
                self.thread_bfs.start()
                self.animation=False
                
            if self.animation and pygame.key.get_pressed()[pygame.K_w]:
                h =  threading.Thread(target=self.animationExpanded)
                h.start()
                
            if self.animation and pygame.key.get_pressed()[pygame.K_c]:
                self.mappingMatrixOnScreen()
            
           

                
                
            pygame.display.flip()#muestra la ventana aqui
            self.dt = self.clock.tick(60)/2
        pygame.quit()
        exit()
        

              
gui =GUI2(WIDTH,HEIGHT)
gui.loadMatrix('matrix381')
 

