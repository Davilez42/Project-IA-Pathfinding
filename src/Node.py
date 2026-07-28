class Node:
    def __init__(
        self, matrix, agent_pos, target_pos, cost_accumulated, movement: str, parent
    ) -> None:
        self.matrix = matrix
        self.parent = parent
        self.agent_pos: tuple = agent_pos
        self.target_pos: tuple = target_pos
        self.movement: str = movement
        self.cost_accumulated = cost_accumulated

    def meta(self) -> bool:
        return (
            self.matrix[self.agent_pos[1]][self.agent_pos[0]] == "*"
            and self.heuristics() == 0
        )

    def heuristics(self) -> int:  # Manhattan distance
        return abs(self.target_pos[0] - self.agent_pos[0]) + abs(
            self.target_pos[1] - self.agent_pos[1]
        )

    def calculate_f(self) -> int:
        self.f = self.cost_accumulated + self.heuristics()
        return self.f

    # Movements
    def up(self):
        xI = self.agent_pos[0]
        yI = self.agent_pos[1] - 1
        if yI >= 0 and self.matrix[yI, xI] != "H" and self.matrix[yI, xI] != "X":
            return Node(
                self.matrix.copy(),
                (xI, yI),
                self.target_pos,
                self.cost_accumulated + 1,
                "U",
                self,
            )

    def down(self):
        xI = self.agent_pos[0]
        yI = self.agent_pos[1] + 1
        if (
            yI <= self.matrix.shape[0] - 1
            and self.matrix[self.agent_pos[1], self.agent_pos[0]] != "H"
            and self.matrix[yI, xI] != "X"
        ):
            return Node(
                self.matrix.copy(),
                (xI, yI),
                self.target_pos,
                self.cost_accumulated + 1,
                "D",
                self,
            )

    def left(self):
        xI = self.agent_pos[0] - 1
        yI = self.agent_pos[1]
        if (
            xI >= 0
            and self.matrix[self.agent_pos[1], self.agent_pos[0]] != "V"
            and self.matrix[yI, xI] != "X"
        ):
            return Node(
                self.matrix.copy(),
                (xI, yI),
                self.target_pos,
                self.cost_accumulated + 1,
                "L",
                self,
            )

    def right(self):
        xI = self.agent_pos[0] + 1
        yI = self.agent_pos[1]
        if (
            xI <= self.matrix.shape[1] - 1
            and self.matrix[yI, xI] != "V"
            and self.matrix[yI, xI] != "X"
        ):
            return Node(
                self.matrix.copy(),
                (xI, yI),
                self.target_pos,
                self.cost_accumulated + 1,
                "R",
                self,
            )
