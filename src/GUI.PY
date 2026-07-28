import datetime
import threading
from math import ceil, floor
from os import environ, path
from time import sleep

import numpy as np
import pygame

from Agent import Agent
from helpers.generatorMatrices import generateMatrixGame
from InputMatrixModal import InputMatrixModal
from Node import Node

"""
Authors:
Oscar Fernando Rivera Pardo 
Jose David Suarez Cardona
Jeferson Aguiar Dominguez
"""


WIDTH = 1070
HEIGHT = 700


class GUI:
    def __init__(self, width, height, inputMatrixModal) -> None:
        # Constants
        self.WIDTH = width
        self.HEIGHT = height
        self.RED_COLOR = (255, 51, 51)
        self.WHITE_COLOR = "white"
        self.BLACK_COLOR = (29, 29, 29)
        self.GRAY_COLOR = (97, 98, 99)
        self.PURPLE_COLOR = "darkorchid1"
        self.GREEN_COLOR = (81, 124, 87)
        self.BACKGROUND_COLOR = (72, 67, 64)
        self.NODE_EXPANDED_COLOR = (63, 212, 255)
        self.NODE_CREATED_COLOR = (253, 255, 44)
        self.all_movements = []
        self.matrix = None
        self.dimension_y_used = self.HEIGHT
        self.dimension_x_used = self.HEIGHT
        self.time_animation = 0.01
        # Per-algorithm information displayed on screen
        self.counter_nodes_create_star = 0
        self.counter_nodes_expanded_star = 0
        self.counter_total_cost_star = 0
        self.time_star = ""
        self.inputMatrixModal: InputMatrixModal = inputMatrixModal

        self.counter_nodes_create_bfs = 0
        self.counter_nodes_expanded_bfs = 0
        self.counter_total_cost_bfs = 0
        self.time_bfs = ""

        # General information
        self.info_text = ""
        self.info_matrix = ""
        self.run()

    def loadMatrix(self, name: str):
        # Load the selected matrix from the "matrices" folder.
        try:
            with open(
                path.join(path.dirname(__file__), "matrices", f"{name}.txt")
            ) as file:
                matrix_rows = []
                for i, r in enumerate(file.readlines()):
                    row: str = r.replace("\n", "")
                    row: list = [c for c in row]
                    try:
                        self.pos_agent = (row.index("@"), i)
                    except ValueError:
                        pass
                    try:
                        self.pos_target = (row.index("*"), i)
                    except ValueError:
                        pass
                    matrix_rows.append(row)
                self.matrix = np.array(matrix_rows)
            self.calculateScreen()
            self.info_matrix = f"{self.matrix.shape[0]}x{self.matrix.shape[1]}"
            self.mappingMatrixOnScreen()
        except FileNotFoundError:
            self.info_text = "Matrix does not exist"
        finally:
            self.matrix_load_ready = True

    def calculateScreen(self):
        # Calculate matrix dimensions relative to the available screen space.
        rows = self.matrix.shape[0]
        col = self.matrix.shape[1]

        x_d = self.WIDTH / col
        y_d = (self.HEIGHT - 140) / rows

        self.width_block = floor(min([x_d, y_d]))

        # Calculate the occupied dimensions on each axis.
        self.dimension_y_used = self.width_block * rows
        self.dimension_x_used = self.width_block * col

        self.space_x = (self.WIDTH - self.dimension_x_used) / 2
        self.space_y = (self.HEIGHT - 140 - self.dimension_y_used) / 2

        # Load and resize the navigation icon.
        self.agent_icon = pygame.image.load(
            path.join(path.dirname(__file__), "icons", "navigation.png")
        )

        self.agent_icon = pygame.transform.scale(
            self.agent_icon, (self.width_block, self.width_block)
        )
        # Precompute rotated icon copies.
        self.agent_icon_up = pygame.transform.rotate(self.agent_icon, 0)
        self.agent_icon_left = pygame.transform.rotate(self.agent_icon, 90)
        self.agent_icon_right = pygame.transform.rotate(self.agent_icon, 270)
        self.agent_icon_down = pygame.transform.rotate(self.agent_icon, 180)

    def mappingMatrixOnScreen(self):
        if self.matrix is None:
            return
        self.screen.fill(self.BACKGROUND_COLOR)

        r = (self.HEIGHT - 60 - self.dimension_y_used) / 2
        c = (self.WIDTH - self.dimension_x_used) / 2

        # Draw each matrix cell on screen.
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                elem = self.matrix[i, j]
                pygame.draw.rect(
                    self.screen,
                    self.BLACK_COLOR,
                    (c, r, self.width_block, self.width_block),
                )

                if elem == "X":  # obstacle
                    pygame.draw.rect(
                        self.screen,
                        self.GRAY_COLOR,
                        (c, r, self.width_block, self.width_block),
                    )

                if elem == "*":  # target
                    pygame.draw.circle(
                        self.screen,
                        self.RED_COLOR,
                        (c + self.width_block / 2, r + self.width_block / 2),
                        self.width_block / 2.5,
                    )

                if elem == "@":  # player
                    self.agent_coordinates = (c, r)
                    pygame.draw.circle(
                        self.screen,
                        self.WHITE_COLOR,
                        (c + self.width_block / 2, r + self.width_block / 2),
                        self.width_block / 2.5,
                    )

                if elem == "V":  # left/right laser barrier
                    pygame.draw.rect(
                        self.screen,
                        self.RED_COLOR,
                        (c, r, self.width_block * 0.2, self.width_block),
                    )

                if elem == "H":  # up/down laser barrier
                    pygame.draw.rect(
                        self.screen,
                        self.RED_COLOR,
                        (
                            c,
                            r + self.width_block - self.width_block * 0.2,
                            self.width_block,
                            self.width_block * 0.2,
                        ),
                    )

                c += self.width_block
            r += self.width_block
            c = (self.WIDTH - self.dimension_x_used) / 2

        # Cache a clean board snapshot so route drawings can be cleared quickly.
        self.screen_background = pygame.Surface.copy(
            pygame.Surface.subsurface(
                self.screen, (0, 40, self.WIDTH, self.HEIGHT - 140)
            )
        )
        self.matrix_load_ready = True

    def clearTexts(self):
        self.info_text = ""
        self.counter_nodes_create_star = 0
        self.counter_nodes_expanded_star = 0
        self.counter_total_cost_star = 0
        self.time_star = "-------"
        self.depth_star = 0
        self.counter_nodes_create_bfs = 0
        self.counter_nodes_expanded_bfs = 0
        self.counter_total_cost_bfs = 0
        self.time_bfs = "-------"
        self.depth_bfs = 0

    def clearGame(self):
        self.screen.blit(self.screen_background, (0, 40))

    def putTextOnScreen(self):
        pygame.draw.rect(
            self.screen, self.BLACK_COLOR, (0, self.HEIGHT - 100, self.WIDTH, 100)
        )
        pygame.draw.rect(self.screen, self.BLACK_COLOR, (0, 0, self.WIDTH, 40))

        label_text = pygame.font.SysFont("Verdana", 20)
        label_min = pygame.font.SysFont("Verdana", 18)
        text_date = pygame.font.SysFont("Verdana", 16)

        # Legend
        # Player
        pygame.draw.circle(self.screen, self.WHITE_COLOR, (20, 20), 10)
        self.screen.blit(label_min.render("Player", 1, self.WHITE_COLOR), (40, 8))
        # Target
        pygame.draw.circle(self.screen, self.RED_COLOR, (130, 20), 10)
        self.screen.blit(label_min.render("Target", 1, self.WHITE_COLOR), (150, 8))

        # LASER
        pygame.draw.rect(self.screen, self.RED_COLOR, (240, 10, 5, 20), 10)
        self.screen.blit(label_min.render("Laser", 1, self.WHITE_COLOR), (255, 8))

        # NODE EXPANDED
        pygame.draw.rect(self.screen, self.NODE_EXPANDED_COLOR, (320, 10, 20, 20), 10)
        self.screen.blit(label_min.render("Expanded", 1, self.WHITE_COLOR), (350, 8))

        # NODE CREATED
        pygame.draw.rect(self.screen, self.NODE_CREATED_COLOR, (460, 10, 20, 20), 10)
        self.screen.blit(label_min.render("Created", 1, self.WHITE_COLOR), (490, 8))

        self.label_tittle_info = label_text.render(
            str(self.info_text), 1, (252, 251, 252)
        )
        self.label_matrix_info = label_text.render(
            str(self.info_matrix), 1, (252, 251, 252)
        )
        self.label_astar = label_text.render("A*", 1, self.PURPLE_COLOR)
        self.label_bfs = label_text.render("BFS", 1, self.GREEN_COLOR)

        self.label_time = label_min.render("Time", 1, (252, 251, 252))
        self.label_nodes_expanded = label_min.render("Expanded", 1, (252, 251, 252))
        self.label_nodes_created = label_min.render("Created", 1, (252, 251, 252))
        self.label_total_cost = label_min.render("Total cost", 1, (252, 251, 252))

        # A* metric labels
        self.text_nodes_created_astar = label_min.render(
            str(self.counter_nodes_create_star), 1, self.PURPLE_COLOR
        )
        self.text_nodes_expanded_astar = label_min.render(
            str(self.counter_nodes_expanded_star), 1, self.PURPLE_COLOR
        )
        self.text_time_astar = text_date.render(
            str(self.time_star), 1, self.PURPLE_COLOR
        )
        self.text_total_cost_astar = label_min.render(
            str(self.counter_total_cost_star), 1, self.PURPLE_COLOR
        )

        # BFS metric labels
        self.text_nodes_created_bfs = label_min.render(
            str(self.counter_nodes_create_bfs), 1, self.GREEN_COLOR
        )
        self.text_nodes_expanded_bfs = label_min.render(
            str(self.counter_nodes_expanded_bfs), 1, self.GREEN_COLOR
        )
        self.text_time_bfs = text_date.render(str(self.time_bfs), 1, self.GREEN_COLOR)
        self.text_total_cost_bfs = label_min.render(
            str(self.counter_total_cost_bfs), 1, self.GREEN_COLOR
        )

        # Headers
        self.screen.blit(self.label_tittle_info, ((self.WIDTH / 2) + 50, 8))
        self.screen.blit(self.label_matrix_info, (self.WIDTH - 100, 10))
        self.screen.blit(self.label_nodes_expanded, (70, self.HEIGHT - 95))
        self.screen.blit(self.label_nodes_created, (210, self.HEIGHT - 95))
        self.screen.blit(self.label_total_cost, (320, self.HEIGHT - 95))
        self.screen.blit(self.label_time, (430, self.HEIGHT - 95))

        # Algorithm labels
        self.screen.blit(self.label_astar, (15, self.HEIGHT - 68))
        self.screen.blit(self.label_bfs, (10, self.HEIGHT - 35))

        # A* metrics
        self.screen.blit(self.text_nodes_expanded_astar, (70, self.HEIGHT - 68))
        self.screen.blit(self.text_nodes_created_astar, (210, self.HEIGHT - 68))
        self.screen.blit(self.text_total_cost_astar, (320, self.HEIGHT - 68))
        self.screen.blit(self.text_time_astar, (430, self.HEIGHT - 68))

        # BFS metrics
        self.screen.blit(self.text_nodes_expanded_bfs, (70, self.HEIGHT - 35))
        self.screen.blit(self.text_nodes_created_bfs, (210, self.HEIGHT - 35))
        self.screen.blit(self.text_total_cost_bfs, (320, self.HEIGHT - 35))
        self.screen.blit(self.text_time_bfs, (430, self.HEIGHT - 35))

        # Keyboard help
        label_buttons = pygame.font.SysFont("Verdana", 20)
        label_info_button = pygame.font.SysFont("Verdana", 14)
        text_q_button = label_buttons.render("Q", 1, self.WHITE_COLOR)
        text_e_button = label_buttons.render("E", 1, self.WHITE_COLOR)
        text_l_button = label_buttons.render("L", 1, self.WHITE_COLOR)
        text_a_button = label_buttons.render("A", 1, self.WHITE_COLOR)
        text_s_button = label_buttons.render("S", 1, self.WHITE_COLOR)
        text_d_button = label_buttons.render("D", 1, self.WHITE_COLOR)
        text_c_button = label_buttons.render("C", 1, self.WHITE_COLOR)
        text_r_button = label_buttons.render("R", 1, self.WHITE_COLOR)
        text_inf_a_button = label_info_button.render("run A*", 1, self.WHITE_COLOR)
        text_inf_d_button = label_info_button.render("run BFS", 1, self.WHITE_COLOR)
        text_inf_s_button = label_info_button.render("animation", 1, self.WHITE_COLOR)
        text_inf_r_button = label_info_button.render("generate", 1, self.WHITE_COLOR)
        text_inf_c_button = label_info_button.render("clear", 1, self.WHITE_COLOR)
        text_inf_l_button = label_info_button.render("load", 1, self.WHITE_COLOR)
        text_inf_q_button = label_info_button.render("speed -1", 1, self.WHITE_COLOR)
        text_inf_e_button = label_info_button.render("speed +1", 1, self.WHITE_COLOR)

        # Run A*
        pygame.draw.rect(
            self.screen,
            self.BACKGROUND_COLOR,
            (570, self.HEIGHT - 95, 45, 42),
            border_radius=5,
        )
        self.screen.blit(text_a_button, (585, self.HEIGHT - 90))
        self.screen.blit(text_inf_a_button, (620, self.HEIGHT - 86))

        # Run BFS
        pygame.draw.rect(
            self.screen,
            self.BACKGROUND_COLOR,
            (570, self.HEIGHT - 45, 45, 42),
            border_radius=5,
        )
        self.screen.blit(text_d_button, (585, self.HEIGHT - 40))
        self.screen.blit(text_inf_d_button, (620, self.HEIGHT - 35))

        # Animation
        pygame.draw.rect(
            self.screen,
            self.BACKGROUND_COLOR,
            (710, self.HEIGHT - 95, 45, 42),
            border_radius=5,
        )
        self.screen.blit(text_s_button, (725, self.HEIGHT - 86))
        self.screen.blit(text_inf_s_button, (760, self.HEIGHT - 86))

        # Generate matrix
        pygame.draw.rect(
            self.screen,
            self.BACKGROUND_COLOR,
            (710, self.HEIGHT - 45, 45, 42),
            border_radius=5,
        )
        self.screen.blit(text_r_button, (725, self.HEIGHT - 40))
        self.screen.blit(text_inf_r_button, (760, self.HEIGHT - 35))

        # Clear
        pygame.draw.rect(
            self.screen,
            self.BACKGROUND_COLOR,
            (840, self.HEIGHT - 95, 45, 42),
            border_radius=5,
        )
        self.screen.blit(text_c_button, (855, self.HEIGHT - 86))
        self.screen.blit(text_inf_c_button, (890, self.HEIGHT - 86))

        # Load
        pygame.draw.rect(
            self.screen,
            self.BACKGROUND_COLOR,
            (870, self.HEIGHT - 45, 45, 42),
            border_radius=5,
        )
        self.screen.blit(text_l_button, (885, self.HEIGHT - 40))
        self.screen.blit(text_inf_l_button, (920, self.HEIGHT - 35))

        # Decrease speed
        pygame.draw.rect(
            self.screen,
            self.BACKGROUND_COLOR,
            (950, self.HEIGHT - 95, 45, 42),
            border_radius=5,
        )
        self.screen.blit(text_q_button, (965, self.HEIGHT - 86))
        self.screen.blit(text_inf_q_button, (1000, self.HEIGHT - 86))

        # Increase speed
        pygame.draw.rect(
            self.screen,
            self.BACKGROUND_COLOR,
            (970, self.HEIGHT - 45, 45, 42),
            border_radius=5,
        )
        self.screen.blit(text_e_button, (985, self.HEIGHT - 40))
        self.screen.blit(text_inf_e_button, (1020, self.HEIGHT - 35))

    def animationExpanded(self, all_movements):
        # Animate expanded and created nodes.
        self.time_animation = 0.01
        for action in all_movements:
            isExpanded = action[1]
            coordinate = action[0]

            x_block = coordinate[0] * self.width_block
            y_block = coordinate[1] * self.width_block
            if isExpanded:
                pygame.draw.rect(
                    self.screen,
                    self.NODE_EXPANDED_COLOR,
                    (
                        self.space_x + x_block,
                        40 + self.space_y + y_block,
                        self.width_block,
                        self.width_block,
                    ),
                )
            else:
                pygame.draw.rect(
                    self.screen,
                    self.NODE_CREATED_COLOR,
                    (
                        self.space_x + x_block,
                        40 + self.space_y + y_block,
                        self.width_block,
                        self.width_block,
                    ),
                )

            sleep(self.time_animation)
        self.animation = False

    def updateInfoScreen(self, nodes_create, nodes_expanded, algorithm):
        if algorithm == "a*":
            self.counter_nodes_expanded_star = nodes_expanded
            self.counter_nodes_create_star = nodes_create
        else:
            self.counter_nodes_expanded_bfs = nodes_expanded
            self.counter_nodes_create_bfs = nodes_create

    def initAlgorithm(self, algorithm, avoid_backing_out):
        try:
            self.all_movements = []
            agent = Agent(self.matrix, self.pos_agent, self.pos_target)
            init_time = datetime.datetime.now()
            if algorithm == "a*":
                result = agent.aStar(avoid_backing_out, self.updateInfoScreen)
            else:
                result = agent.bfs(avoid_backing_out, self.updateInfoScreen)

            end_time = datetime.datetime.now()
            node_winner: Node = result[0]

            self.all_movements = result[3]

            if algorithm == "a*":
                self.time_star = end_time - init_time
                self.counter_total_cost_star = node_winner.cost_accumulated

            else:
                self.time_bfs = end_time - init_time
                self.counter_total_cost_bfs = node_winner.cost_accumulated

            route = []
            movements = []
            parent_ = node_winner
            while parent_ != None:
                route.insert(0, parent_.agent_pos)
                movements.insert(0, parent_.movement)
                parent_ = parent_.parent
            self.animationRoute(algorithm, movements, route[0])
        except Exception as e:
            self.info_text = e
        finally:
            self.animation = False

    def animationRoute(self, algorithm, movements, init_coordinate):
        if algorithm == "a*":
            self.clearGame()

        width = self.width_block / 2
        x = init_coordinate[0]
        y = init_coordinate[1]

        route_color = self.PURPLE_COLOR if algorithm == "a*" else self.GREEN_COLOR

        # Add half a cell so the route is drawn from the center.
        vector_route = pygame.Vector2(
            self.space_x + x * self.width_block + width,
            self.space_y + y * self.width_block + width,
        )
        vector_agent = pygame.Vector2(
            self.space_x + x * self.width_block, self.space_y + y * self.width_block
        )

        frame_s = ceil(self.width_block)

        copy = pygame.Surface.copy(
            pygame.Surface.subsurface(
                # Copy the clean frame before drawing the agent.
                self.screen,
                (0, 40, self.WIDTH, self.HEIGHT - 140),
            )
        )
        # Keep the last frame without the agent so it does not leave a trail.
        last_ = copy.copy()
        image_agent = self.agent_icon.copy()
        for i in movements:
            # Move one pixel at a time across the current cell size.
            for j in range(frame_s):
                aux = pygame.Surface.copy(last_)
                if i == "R":
                    vector_route.x += 1
                    vector_agent.x += 1
                    image_agent = self.agent_icon_right

                if i == "L":
                    vector_route.x -= 1
                    vector_agent.x -= 1
                    image_agent = self.agent_icon_left

                if i == "D":
                    vector_route.y += 1
                    vector_agent.y += 1
                    image_agent = self.agent_icon_down
                if i == "U":
                    vector_route.y -= 1
                    vector_agent.y -= 1
                    image_agent = self.agent_icon_up

                pygame.draw.circle(aux, route_color, vector_route, width / 2)
                last_ = pygame.Surface.copy(aux)
                aux.blit(image_agent, vector_agent)
                self.screen.blit(aux, (0, 40))
                sleep(0.001)

        self.animation = True

    def run(self):
        environ["SDL_VIDEO_WINDOW_POS"] = "1"
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen_background = pygame.Surface.copy(
            pygame.Surface.subsurface(
                self.screen, (0, 40, self.WIDTH, self.HEIGHT - 140)
            )
        )

        pygame.font.init()
        pygame.display.set_caption("A* and BFS Pathfinding Visualizer")

        self.clock = pygame.time.Clock()
        self.running = True

        # Initial screen elements
        self.putTextOnScreen()
        # Prevent repeated execution while an animation is running.
        self.animation = False
        self.matrix_load_ready = True
        self.random_matrix_ready = True
        self.loadMatrix("18x20_1_default")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.putTextOnScreen()

            # Run A*
            if (
                not self.animation
                and self.info_matrix is not None
                and pygame.key.get_pressed()[pygame.K_a]
            ):
                self.animation = True
                self.clearGame()
                # Skipping already expanded nodes improves large-map performance.
                self.thread_astar = threading.Thread(
                    target=self.initAlgorithm, args=("a*", True)
                )
                self.thread_astar.start()

            # Created/expanded node animation
            if (
                not self.animation
                and len(self.all_movements) > 0
                and pygame.key.get_pressed()[pygame.K_s]
            ):
                self.animation = True
                self.clearGame()
                self.thread_animation = threading.Thread(
                    target=self.animationExpanded, args=(self.all_movements,)
                )
                self.thread_animation.start()

            # Run BFS
            if (
                not self.animation
                and self.info_matrix is not None
                and pygame.key.get_pressed()[pygame.K_d]
            ):
                self.animation = True
                self.thread_bfs = threading.Thread(
                    target=self.initAlgorithm, args=("bfs", True)
                )
                self.thread_bfs.start()

            # Increase animation speed.
            if self.animation and pygame.key.get_pressed()[pygame.K_e]:
                aux = self.time_animation - 0.001
                if aux >= 0.001:
                    self.time_animation = aux

            # Slow down animation speed.
            if (
                self.animation
                and self.time_animation < 1
                and pygame.key.get_pressed()[pygame.K_q]
            ):
                self.time_animation += 0.001

            # Load matrix.
            if (
                not self.animation
                and self.matrix_load_ready
                and pygame.key.get_pressed()[pygame.K_l]
            ):
                self.matrix_load_ready = False
                self.clearTexts()
                matrix_name = self.inputMatrixModal.openModal()
                if matrix_name is not None:
                    self.loadMatrix(matrix_name)
                else:
                    self.matrix_load_ready = True

            if (
                not self.animation
                and self.random_matrix_ready
                and pygame.key.get_pressed()[pygame.K_r]
            ):
                self.all_movements = []
                matrix_name = generateMatrixGame()
                self.loadMatrix(matrix_name)
                self.clearTexts()

                self.random_matrix_ready = False

                def can_generate_matrix():
                    sleep(1)
                    self.random_matrix_ready = True

                threading.Thread(target=can_generate_matrix).start()

            if not self.animation and pygame.key.get_pressed()[pygame.K_c]:
                self.clearGame()
                self.clearTexts()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        exit()


if __name__ == "__main__":
    input_matrix_modal = InputMatrixModal()
    gui = GUI(WIDTH, HEIGHT, input_matrix_modal)
