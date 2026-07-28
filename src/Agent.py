from queue import Queue

from Node import Node


class Agent:
    def __init__(self, init_matrix, pos_agent, pos_target) -> None:
        self.init_matrix = init_matrix
        self.pos_target = pos_target
        self.pos_agent = pos_agent

    def bfs(self, avoid_backing_out, updateInfoScreen):
        inital_node = Node(
            self.init_matrix.copy(), self.pos_agent, self.pos_target, 0, None, None
        )
        nodes_expanded = 0
        nodes_created = 0
        queue: Queue = Queue(maxsize=-1)
        queue.put(inital_node)
        positions_explored = []
        all_movements = []
        while not queue.empty():
            updateInfoScreen(nodes_created, nodes_expanded, "bfs")

            current_node: Node = queue.get()

            # When backtracking prevention is enabled, skip nodes that were already expanded.
            if current_node.agent_pos in positions_explored and avoid_backing_out:
                continue

            if current_node.meta():
                return current_node, nodes_expanded, nodes_created, all_movements

            if avoid_backing_out:
                positions_explored.append(current_node.agent_pos)

            nodes_expanded += 1
            all_movements.append((current_node.agent_pos, True))

            # Generate children clockwise: up, right, down, left.
            childs = [
                current_node.up(),
                current_node.right(),
                current_node.down(),
                current_node.left(),
            ]

            for child in childs:
                if isinstance(child, Node) and not (
                    child.agent_pos in positions_explored
                ):
                    all_movements.append((child.agent_pos, False))
                    nodes_created += 1
                    queue.put(child)

        raise Exception("No solution")

    def aStar(self, avoid_backing_out, updateInfoScreen):
        inital_node = Node(
            self.init_matrix.copy(), self.pos_agent, self.pos_target, 0, None, None
        )
        inital_node.calculate_f()
        nodes_expanded = 0
        nodes_created = 0
        queue = [inital_node]
        positions_explored = []
        all_movements = []

        while len(queue) > 0:
            updateInfoScreen(nodes_created, nodes_expanded, "a*")

            _f = float("inf")
            node_min = None
            for node in queue:
                if node.f <= _f:
                    _f = node.f
                    node_min = node
            queue.remove(node_min)
            current_node: Node = node_min

            if current_node.meta():
                return current_node, nodes_expanded, nodes_created, all_movements

            if avoid_backing_out:
                positions_explored.append(current_node.agent_pos)

            nodes_expanded += 1
            all_movements.append((current_node.agent_pos, True))

            # Generate children clockwise: up, right, down, left.
            childs = [
                current_node.up(),
                current_node.right(),
                current_node.down(),
                current_node.left(),
            ]

            for child in childs:
                # Skip invalid movements.
                if not isinstance(child, Node):
                    continue

                child.calculate_f()

                create = True

                # If the node already exists in the open list, keep the cheaper path.
                for i, node in enumerate(queue):
                    if node.agent_pos == child.agent_pos:
                        if child.cost_accumulated < node.cost_accumulated:
                            queue[i] = child
                        create = False
                        break

                if create and child.agent_pos not in positions_explored:
                    all_movements.append((child.agent_pos, False))
                    nodes_created += 1
                    queue.append(child)

        raise Exception("No solution")
