class Node:
    def __init__(self,matriz,posAgente,posChurikenm,cost_acumulated,movements=[],route=[]) -> None:
        self.matriz = matriz
        self.posAgente:tuple = posAgente
        self.posChuriken:tuple = posChurikenm
        self.movements:list = movements
        self.route:list = route
        self.cost_acumulated = cost_acumulated

           
    def meta(self):
        return self.matriz[self.posAgente[1]][self.posAgente[0]]=='*' and self.heuristica()==0    
    
    def heuristica(self):#dinstancia manhathan
        return abs(self.posChuriken[0] - self.posAgente[0]) +  abs(self.posChuriken[1] - self.posAgente[1])
    
    def calculate_f(self):
        self.f =  self.heuristica()  + self.cost_acumulated
        return self.f