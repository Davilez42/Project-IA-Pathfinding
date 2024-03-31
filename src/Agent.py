
import numpy as np
from Node import Node

class Agent:
    def __init__(self,init_matrix,pos_agent,pos_chiriken) -> None:
        self.init_matrix:np.Arrayterator = init_matrix
        self.pos_churiken = pos_chiriken
        self.pos_agent = pos_agent


    def run(self,algorithm,avoid_backing_out,updateInfoScreen):
        
        self.nodes_explored = [] 
        inital_node =  Node(self.init_matrix.copy(),self.pos_agent,self.pos_churiken,0,None,None)
        inital_node.calculate_f()  
        nodes_expanded=0
        total_nodes_created= 0    
        queue=[inital_node]

        all_moviments = []
        
        while len(queue)>0:          
            updateInfoScreen(total_nodes_created,nodes_expanded,algorithm)
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
                if(current_node.posAgente in self.nodes_explored and avoid_backing_out):#si esta activado el evitar devolvsere verifico si el nodo antes de expandir ya ha sido visitado
                    continue 
      
            if(current_node.meta()):
                return current_node, nodes_expanded,total_nodes_created,all_moviments   
           
            if avoid_backing_out :#llevo un registro de los nodos visitidados para no volver a visitarlos 
                self.nodes_explored.append(current_node.posAgente) 
                
            nodes_expanded+=1           
            all_moviments.append((current_node.posAgente,True))
            
            #genero los hijos en el orden de las manesillas del reloj arriba,derecha, abajo, izquierda
            childs = [current_node.up(),current_node.right(),current_node.down(),current_node.left()]
            for child in childs:
                if(isinstance(child,Node)  and not (child.posAgente in self.nodes_explored)):
                    child.calculate_f()
                    all_moviments.append((child.posAgente,False))
                    total_nodes_created+=1
                    queue.append(child)
        raise Exception('No Tiene solucion')   
