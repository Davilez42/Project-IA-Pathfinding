class Node:
    def __init__(self,matriz,posAgente,posChurikenm,cost_acumulated,movement:str,parent) -> None:
        self.matriz = matriz
        self.parent = parent
        self.posAgente:tuple = posAgente
        self.posChuriken:tuple = posChurikenm
        self.movement:str = movement
        self.cost_acumulated = cost_acumulated
         
    def meta(self):
        return self.matriz[self.posAgente[1]][self.posAgente[0]]=='*' and self.heuristica()==0    
    
    def heuristica(self):#dinstancia manhathan
        return abs(self.posChuriken[0] - self.posAgente[0]) +  abs(self.posChuriken[1] - self.posAgente[1])
    
    def calculate_f(self):
        self.f =  self.heuristica()  + self.cost_acumulated
        return self.f

    #movimimientos
    def up(self):
        xI = self.posAgente[0]
        yI = self.posAgente[1] - 1
        if(yI>=0 and  self.matriz[yI,xI]!='2'  and  self.matriz[yI,xI]!='7'):
                return Node(self.matriz.copy(),(xI,yI),self.posChuriken,self.cost_acumulated+1,'U',self)
            
    def down(self):
        xI = self.posAgente[0]
        yI = self.posAgente[1] + 1
        if(yI<=self.matriz.shape[0]-1  and self.matriz[self.posAgente[1],self.posAgente[0]]!='2'  and  self.matriz[yI,xI]!='7' ):

                return Node(self.matriz.copy(),(xI,yI),self.posChuriken,self.cost_acumulated+1,'D',self)
                    
    def left(self):
        xI = self.posAgente[0]-1
        yI = self.posAgente[1] 
        if(xI>=0 and self.matriz[self.posAgente[1],self.posAgente[0]]!='3'  and  self.matriz[yI,xI]!='7' ):
                return Node(self.matriz.copy(),(xI,yI),self.posChuriken,self.cost_acumulated+1,'L',self)
            
            
    def right(self):
        xI = self.posAgente[0]+1
        yI = self.posAgente[1] 
        if(xI<=self.matriz.shape[1]-1  and self.matriz[yI,xI]!='3'  and  self.matriz[yI,xI]!='7' ):               
                return Node(self.matriz.copy(),(xI,yI),self.posChuriken,self.cost_acumulated+1,'R',self)  
            
