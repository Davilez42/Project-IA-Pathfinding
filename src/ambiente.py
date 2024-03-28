
import numpy as np
from Node import Node

class Ambiente:
    def __init__(self,init_matrix,pos_agent,pos_chiriken) -> None:
        self.init_matrix:np.Arrayterator = init_matrix
        self.pos_churiken = pos_chiriken
        self.pos_agent = pos_agent


    def run(self,moveAgent,algorithm,avoid_backing_out):        
        inital_node =  Node(self.init_matrix.copy(),self.pos_agent,self.pos_churiken,0,[],[self.pos_agent])
        inital_node.calculate_f()  
        nodes_expanded=0
        total_nodes_created= 0        
        queue = [inital_node]    
        #registros
        nodes_explored = []       
        while len(queue)>0:          
            if algorithm=='a*':
                _f = float('inf')
                node_min = None
                for node in queue:
                    if node.f<=_f:
                        _f=node.f
                        node_min = node 
                queue.remove(node_min)          
                current_node:Node = node_min
            else: 
                current_node:Node = queue.pop(0)

                if(current_node.posAgente in nodes_explored and avoid_backing_out):#si esta activado el evitar devolvsere verifico si el nodo antes de expandir ya ha sido visitado
                    continue
                
            #print(len(queue),current_node.f,current_node.cost_acumulated, current_node.posAgente)          
            if(current_node.meta()):
                return current_node.route,current_node.movements, nodes_expanded,total_nodes_created,current_node.cost_acumulated         
           
            if avoid_backing_out :#llevo un registro de los nodos visitidados para no volver a visitarlos 
                nodes_explored.append(current_node.posAgente)
           
           
            nodes_expanded+=1           
            moveAgent(current_node.posAgente)
            x= current_node.posAgente[0]
            y= current_node.posAgente[1]
            #creo sus hijos
            #arriba
            x1 = x
            y1 = y-1          
            if(y1>=0 and  self.init_matrix[y1,x1]!='2'  and  self.init_matrix[y1,x1]!='X' and not((x1,y1) in nodes_explored ) ):               
                route = current_node.route.copy()
                movements = current_node.movements.copy()        
                movements.append('U')
                route.append((x1,y1))             
                moveAgent((x1,y1),False)                          
                child_node =  Node(current_node.matriz.copy(),(x1,y1),self.pos_churiken,current_node.cost_acumulated + 1,movements,route)
                child_node.calculate_f()
                queue.append((child_node))
                total_nodes_created+=1
            #derecha
            x1 = x+1
            y1 = y
            if(x1<=self.init_matrix.shape[1]-1  and self.init_matrix[y1,x1]!='3' and  self.init_matrix[y1,x1]!='X' and not((x1,y1) in nodes_explored  )):
                route = current_node.route.copy()
                movements = current_node.movements.copy()          
                movements.append('R')
                route.append((x1,y1))
                moveAgent((x1,y1),False)
                child_node =  Node(current_node.matriz.copy(),(x1,y1),self.pos_churiken,current_node.cost_acumulated + 1,movements,route)
                child_node.calculate_f()
                queue.append(child_node)
                total_nodes_created+=1          
            #abajo
            x1 = x
            y1 = y+1
            if(y1<=self.init_matrix.shape[0]-1  and self.init_matrix[y,x]!='2' and  self.init_matrix[y1,x1]!='X'  and not((x1,y1) in nodes_explored  )):
                route = current_node.route.copy()
                movements = current_node.movements.copy()            
                movements.append('D')
                route.append((x1,y1))
                moveAgent((x1,y1),False)
                child_node =  Node(current_node.matriz.copy(),(x1,y1),self.pos_churiken,current_node.cost_acumulated + 1,movements,route)
                child_node.calculate_f()
                queue.append(child_node)
                total_nodes_created+=1          
            #izquierda
            x1 = x-1
            y1 = y
            if(x1>=0 and self.init_matrix[y,x]!='3' and  self.init_matrix[y1,x1]!='X' and not((x1,y1) in nodes_explored )):
                route = current_node.route.copy()
                movements = current_node.movements.copy()           
                movements.append('L')
                route.append((x1,y1))
                moveAgent((x1,y1),False)
                child_node =  Node(current_node.matriz.copy(),(x1,y1),self.pos_churiken,current_node.cost_acumulated + 1,movements,route)
                child_node.calculate_f()
                queue.append(child_node)
                total_nodes_created+=1    
        

        raise Exception('No existe solucion')