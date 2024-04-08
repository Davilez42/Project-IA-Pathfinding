
import numpy as np
from Node import Node
from queue import Queue


class Agent:
    def __init__(self, init_matrix, pos_agent, pos_target) -> None:
        self.init_matrix = init_matrix
        self.pos_target = pos_target
        self.pos_agent = pos_agent

    def bfs(self, avoid_backing_out, updateInfoScreen):
        inital_node = Node(self.init_matrix.copy(),
                           self.pos_agent, self.pos_target, 0, None, None)
        nodes_expanded = 0
        nodes_created = 0
        queue: Queue = Queue(maxsize=-1)
        queue.put(inital_node)
        positions_explored = []
        all_movements = []
        while not queue.empty():
            updateInfoScreen(nodes_created, nodes_expanded, 'bfs')

            current_node: Node = queue.get()

            # si esta activado el evitar devolvsere verifico si el nodo ya ha sido expandido de esta manera evito expandir los mismo nodos
            if (current_node.posAgente in positions_explored and avoid_backing_out):
                continue

            if (current_node.meta()):
                return current_node, nodes_expanded, nodes_created, all_movements

            if avoid_backing_out:  # llevo un registro de los nodos expandidos para no volver a expandirlo en caso de que este activada
                positions_explored.append(current_node.posAgente)

            nodes_expanded += 1
            all_movements.append((current_node.posAgente, True))

            # genero los hijos en el orden de las manecillas del reloj arriba,derecha, abajo, izquierda
            childs = [current_node.up(), current_node.right(),
                      current_node.down(), current_node.left()]

            for child in childs:
                if (isinstance(child, Node) and not (child.posAgente in positions_explored)):
                    all_movements.append((child.posAgente, False))
                    nodes_created += 1
                    queue.put(child)

        raise Exception('Sin solucion')

    def aStar(self, avoid_backing_out, updateInfoScreen):
        inital_node = Node(self.init_matrix.copy(),
                           self.pos_agent, self.pos_target, 0, None, None)
        inital_node.calculate_f()
        nodes_expanded = 0
        nodes_created = 0
        queue = [inital_node]
        positions_explored = []
        all_movements = []

        while len(queue) > 0:
            updateInfoScreen(nodes_created, nodes_expanded, 'a*')

            _f = float('inf')
            node_min = None
            for node in queue:
                if node.f <= _f:
                    _f = node.f
                    node_min = node
            queue.remove(node_min)
            current_node: Node = node_min

            if (current_node.meta()):
                return current_node, nodes_expanded, nodes_created, all_movements

            if avoid_backing_out:  # llevo un registro de los nodos visitidados para no volver a visitarlos
                positions_explored.append(current_node.posAgente)

            nodes_expanded += 1
            all_movements.append((current_node.posAgente, True))

            # genero los hijos en el orden de las manesillas del reloj arriba,derecha, abajo, izquierda
            childs = [current_node.up(), current_node.right(),
                      current_node.down(), current_node.left()]

            for child in childs:
                # en caso de que sea None lo evito ya que no es un Nodo
                if (not isinstance(child, Node)):
                    continue

                child.calculate_f()  # calculo el f del hijo

                create = True

                # verifico si ya ha sido creado ese hijo buscandolo en la cola
                for i, node in enumerate(queue):
                    if node.posAgente == child.posAgente:
                        # si ya existe ese nodo  verifico los costes acumulados de ambos nodos, en caso de que el actual nodo creado
                        # tenga menor costo acumulado significa la ruta actual del nodo es mejor
                        if child.cost_acumulated < node.cost_acumulated:
                            # remplazo al nodo que mejora la ruta
                            queue[i] = child
                        create = False
                        break

                if create and child.posAgente not in positions_explored:
                    all_movements.append((child.posAgente, False))
                    nodes_created += 1
                    queue.append(child)

        raise Exception('Sin solucion')
