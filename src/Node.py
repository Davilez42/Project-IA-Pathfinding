class Node:
    def __init__(self, matriz, posAgente, posTarget, cost_acumulated, movement: str, parent) -> None:
        self.matriz = matriz
        self.parent = parent
        self.posAgente: tuple = posAgente
        self.posTarget: tuple = posTarget
        self.movement: str = movement
        self.cost_acumulated = cost_acumulated

    def meta(self) -> bool:
        return self.matriz[self.posAgente[1]][self.posAgente[0]] == '*' and self.heuristics() == 0

    def heuristics(self) -> int:  # dinstancia manhathan
        return abs(self.posTarget[0] - self.posAgente[0]) + abs(self.posTarget[1] - self.posAgente[1])

    def calculate_f(self) -> int:
        self.f = self.cost_acumulated + self.heuristics()
        return self.f

    # movimimientos
    def up(self):
        xI = self.posAgente[0]
        yI = self.posAgente[1] - 1
        if (yI >= 0 and self.matriz[yI, xI] != 'H' and self.matriz[yI, xI] != 'X'):
            return Node(self.matriz.copy(), (xI, yI), self.posTarget, self.cost_acumulated+1, 'U', self)

    def down(self):
        xI = self.posAgente[0]
        yI = self.posAgente[1] + 1
        if (yI <= self.matriz.shape[0]-1 and self.matriz[self.posAgente[1], self.posAgente[0]] != 'H' and self.matriz[yI, xI] != 'X'):
            return Node(self.matriz.copy(), (xI, yI), self.posTarget, self.cost_acumulated+1, 'D', self)

    def left(self):
        xI = self.posAgente[0]-1
        yI = self.posAgente[1]
        if (xI >= 0 and self.matriz[self.posAgente[1], self.posAgente[0]] != 'V' and self.matriz[yI, xI] != 'X'):
            return Node(self.matriz.copy(), (xI, yI), self.posTarget, self.cost_acumulated+1, 'L', self)

    def right(self):
        xI = self.posAgente[0]+1
        yI = self.posAgente[1]
        if (xI <= self.matriz.shape[1]-1 and self.matriz[yI, xI] != 'V' and self.matriz[yI, xI] != 'X'):
            return Node(self.matriz.copy(), (xI, yI), self.posTarget, self.cost_acumulated+1, 'R', self)
