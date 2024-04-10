from time import sleep
import pygame
import numpy as np
import threading
from Node import Node
from helpers.generatorMatrices import generatorMatrizGame
from math import ceil, floor
import datetime
from Agent import Agent
from os import path, environ

from InputMatrizModal import InputMatrizModal

WIDTH = 1070
HEIGHT = 700


class GUI:
    def __init__(self, width, heigth, inputMatrizModal) -> None:
        # constantes
        self.WIDTH = width
        self.HEIGHT = heigth
        self.RED_COLOR = (255, 51, 51)
        self.WHITE_COLOR = 'white'
        self.BLACK_COLOR = (29, 29, 29)
        self.GRAY_COLOR = (97, 98, 99)
        self.PURPLE_COLOR = 'darkorchid1'
        self.GREEN_COLOR = (81, 124, 87)
        self.BACKGROUND_COLOR = (72, 67, 64)
        self.NODE_EXPANDED_COLOR = (63, 212, 255)
        self.NODE_CREATED_COLOR = (253, 255, 44)
        #
        self.all_moviements = []
        self.matriz = None
        self.dimention_y_used = self.HEIGHT
        self.dimention_x_used = self.HEIGHT
        self.time_animation = 0.01
        # informacion de cada algoritmo para mostrar en patalla
        self.counter_nodes_create_star = 0
        self.counter_nodes_expanded_star = 0
        self.counter_costo_total_star = 0
        self.time_star = ''
        self.inputMatrizModal: InputMatrizModal = inputMatrizModal

        self.counter_nodes_create_bfs = 0
        self.counter_nodes_expanded_bfs = 0
        self.counter_costo_total_bfs = 0
        self.time_bfs = ''

        # informacion general
        self.info_text = ''
        self.info_matrix = ''
        self.run()

    def loadMatrix(self, name: str):
        # cargo la matriz especificada, debe existir en la carpeta "matrices"
        try:
            with open(path.join(path.dirname(__file__), f'matrices/{name}.txt')) as file:
                matriz_ = []
                for i, r in enumerate(file.readlines()):
                    row: str = r.replace('\n', '')
                    row: list = [c for c in row]
                    try:
                        self.pos_agent = (row.index('@'), i)
                    except ValueError:
                        pass
                    try:
                        self.pos_churiken = (row.index('*'), i)
                    except ValueError:
                        pass
                    matriz_.append(row)
                self.matriz = np.array(matriz_)
            self.calculateScreen()  # calculo las dimensiones de la matrix con relacion a la pantalla
            self.info_matrix = f'{self.matriz.shape[0]}x{self.matriz.shape[1]}'
            self.mappingMatrizOnScreen()  # defino el tamano del juego en base a la matrix leida
        except FileNotFoundError as e:
            self.info_text = 'La matriz no existe'
        finally:
            self.load_matriz = True

    def calculateScreen(self):
        # obtengo las dimensiones de la matriz para calcular su posicion en la pantalla
        rows = self.matriz.shape[0]
        col = self.matriz.shape[1]

        x_d = self.WIDTH/col
        y_d = (self.HEIGHT-140)/rows

        self.width_block = floor(min([x_d, y_d]))

        # calculo las dimensiones que son usadas en cada lado
        self.dimention_y_used = self.width_block*rows
        self.dimention_x_used = self.width_block*col

        self.space_x = (self.WIDTH - self.dimention_x_used)/2
        self.space_y = (self.HEIGHT-140 - self.dimention_y_used)/2

        # cargo y redimensiono el icono de navegacion
        self.agent_icon = pygame.image.load('./src/icons/navigation.png')
        self.agent_icon = pygame.transform.scale(
            self.agent_icon, (self.width_block, self.width_block))
        # genero copias de las rotaciones del icono
        self.agent_icon_up = pygame.transform.rotate(self.agent_icon, 0)
        self.agent_icon_left = pygame.transform.rotate(self.agent_icon, 90)
        self.agent_icon_right = pygame.transform.rotate(self.agent_icon, 270)
        self.agent_icon_down = pygame.transform.rotate(self.agent_icon, 180)

    def mappingMatrizOnScreen(self):
        if self.matriz is None:
            return
        self.screen.fill(self.BACKGROUND_COLOR)  # limpio la pantalla

        r = (self.HEIGHT-60 - self.dimention_y_used)/2
        c = (self.WIDTH - self.dimention_x_used)/2

        # mapeo la matriz en la pantalla recorriendo filas y columnas y creando su correspondiente elemento
        for i in range(self.matriz.shape[0]):
            for j in range(self.matriz.shape[1]):
                elem = self.matriz[i, j]
                pygame.draw.rect(self.screen, self.BLACK_COLOR,
                                 (c, r, self.width_block, self.width_block))

                if (elem == 'X'):  # obstaculo
                    pygame.draw.rect(self.screen, self.GRAY_COLOR,
                                     (c, r, self.width_block, self.width_block))

                if (elem == '*'):  # objectivo
                    pygame.draw.circle(self.screen, self.RED_COLOR, (
                        c+self.width_block/2, r+self.width_block/2), self.width_block/2.5)

                if (elem == '@'):  # jugador
                    self.agent_coordenates = (c, r)
                    pygame.draw.circle(self.screen, self.WHITE_COLOR, (
                        c+self.width_block/2, r+self.width_block/2), self.width_block/2.5)

                if (elem == 'V'):  # laser izquierda y derecha
                    pygame.draw.rect(self.screen, self.RED_COLOR,
                                     (c, r, self.width_block*0.2, self.width_block))

                if (elem == 'H'):  # laser de arriba y abajo
                    pygame.draw.rect(self.screen, self.RED_COLOR, (c, r+self.width_block -
                                     self.width_block*0.2, self.width_block, self.width_block*0.2))

                c += self.width_block
            r += self.width_block
            c = (self.WIDTH - self.dimention_x_used)/2

        # creo una copia de la matriz en pantalla para no tener que volver a mapearla en caso de querer limpiar la pantalla
        self.screen_background = pygame.Surface.copy(
            pygame.Surface.subsurface(self.screen, (0, 40, self.WIDTH, self.HEIGHT-140)))
        self.load_matriz = True

    def clearTexts(self):
        self.info_text = ''
        self.counter_nodes_create_star = 0
        self.counter_nodes_expanded_star = 0
        self.counter_costo_total_star = 0
        self.time_star = '-------'
        self.depth_star = 0
        self.counter_nodes_create_bfs = 0
        self.counter_nodes_expanded_bfs = 0
        self.counter_costo_total_bfs = 0
        self.time_bfs = '-------'
        self.depth_bfs = 0

    def clearGame(self):
        self.screen.blit(self.screen_background, (0, 40))

    def putTextOnScreen(self):
        pygame.draw.rect(self.screen, self.BLACK_COLOR,
                         (0, self.HEIGHT-100, self.WIDTH, 100))
        pygame.draw.rect(self.screen, self.BLACK_COLOR, (0, 0, self.WIDTH, 40))

        label_text = pygame.font.SysFont("Verdana", 20)
        label_min = pygame.font.SysFont("Verdana", 18)
        text_date = pygame.font.SysFont("Verdana", 16)

        # informacion de elementos
        # JUGADOR
        pygame.draw.circle(self.screen, self.WHITE_COLOR, (20, 20), 10)
        self.screen.blit(label_min.render(
            'Jugador', 1, self.WHITE_COLOR), (40, 8))
        # DESTINO
        pygame.draw.circle(self.screen, self.RED_COLOR, (130, 20), 10)
        self.screen.blit(label_min.render(
            'Destino', 1, self.WHITE_COLOR), (150, 8))

        # LASER
        pygame.draw.rect(self.screen, self.RED_COLOR, (240, 10, 5, 20), 10)
        self.screen.blit(label_min.render(
            'Laser', 1, self.WHITE_COLOR), (255, 8))

        # NODE EXPANDED
        pygame.draw.rect(self.screen, self.NODE_EXPANDED_COLOR,
                         (320, 10, 20, 20), 10)
        self.screen.blit(label_min.render(
            'Expandido', 1, self.WHITE_COLOR), (350, 8))

        # NODE EXPANDED
        pygame.draw.rect(self.screen, self.NODE_CREATED_COLOR,
                         (460, 10, 20, 20), 10)
        self.screen.blit(label_min.render(
            'Creado', 1, self.WHITE_COLOR), (490, 8))

        self.label_tittle_info = label_text.render(
            str(self.info_text), 1, (252, 251, 252))
        self.label_matriz_info = label_text.render(
            str(self.info_matrix), 1, (252, 251, 252))
        self.label_astar = label_text.render('A*', 1, self.PURPLE_COLOR)
        self.label_bfs = label_text.render('BFS', 1, self.GREEN_COLOR)

        self.label_time = label_min.render('Tiempo', 1, (252, 251, 252))
        self.label_nodes_expanded = label_min.render(
            'N.Expandidos', 1, (252, 251, 252))
        self.label_nodes_created = label_min.render(
            'N.Creados', 1, (252, 251, 252))
        self.label_total_cost = label_min.render(
            'Costo total', 1, (252, 251, 252))

        # creacion de etiquetas de la informacion de a*
        self.text_nodes_created_astar = label_min.render(
            str(self.counter_nodes_create_star), 1, self.PURPLE_COLOR)
        self.text_nodes_expanded_astar = label_min.render(
            str(self.counter_nodes_expanded_star), 1, self.PURPLE_COLOR)
        self.text_time_astar = text_date.render(
            str(self.time_star), 1, self.PURPLE_COLOR)
        self.text_total_cost_astar = label_min.render(
            str(self.counter_costo_total_star), 1, self.PURPLE_COLOR)

        # creacion de etiquetas de la informacion de bfs
        self.text_nodes_created_bfs = label_min.render(
            str(self.counter_nodes_create_bfs), 1, self.GREEN_COLOR)
        self.text_nodes_expanded_bfs = label_min.render(
            str(self.counter_nodes_expanded_bfs), 1, self.GREEN_COLOR)
        self.text_time_bfs = text_date.render(
            str(self.time_bfs), 1, self.GREEN_COLOR)
        self.text_total_cost_bfs = label_min.render(
            str(self.counter_costo_total_bfs), 1, self.GREEN_COLOR)

        # subtitulos
        self.screen.blit(self.label_tittle_info, ((self.WIDTH/2)+50, 8))
        self.screen.blit(self.label_matriz_info, (self.WIDTH-100, 10))
        self.screen.blit(self.label_nodes_expanded, (70, self.HEIGHT-95))
        self.screen.blit(self.label_nodes_created, (210, self.HEIGHT-95))
        self.screen.blit(self.label_total_cost, (320, self.HEIGHT-95))
        self.screen.blit(self.label_time, (430, self.HEIGHT-95))

        # titulos de algoritmo
        self.screen.blit(self.label_astar, (15, self.HEIGHT-68))
        self.screen.blit(self.label_bfs, (10, self.HEIGHT-35))

        # texto informacion A*
        self.screen.blit(self.text_nodes_expanded_astar, (70, self.HEIGHT-68))
        self.screen.blit(self.text_nodes_created_astar, (210, self.HEIGHT-68))
        self.screen.blit(self.text_total_cost_astar, (320, self.HEIGHT-68))
        self.screen.blit(self.text_time_astar, (430, self.HEIGHT-68))

        # texto informacion BFS
        self.screen.blit(self.text_nodes_expanded_bfs, (70, self.HEIGHT-35))
        self.screen.blit(self.text_nodes_created_bfs, (210, self.HEIGHT-35))
        self.screen.blit(self.text_total_cost_bfs, (320, self.HEIGHT-35))
        self.screen.blit(self.text_time_bfs, (430, self.HEIGHT-35))

        # textos de informacion de teclas
        label_buttons = pygame.font.SysFont("Verdana", 20)
        label_info_button = pygame.font.SysFont("Verdana", 14)
        text_q_button = label_buttons.render('Q', 1, self.WHITE_COLOR)
        text_e_button = label_buttons.render('E', 1, self.WHITE_COLOR)
        text_l_button = label_buttons.render('L', 1, self.WHITE_COLOR)
        text_a_button = label_buttons.render('A', 1, self.WHITE_COLOR)
        text_s_button = label_buttons.render('S', 1, self.WHITE_COLOR)
        text_d_button = label_buttons.render('D', 1, self.WHITE_COLOR)
        text_c_button = label_buttons.render('C', 1, self.WHITE_COLOR)
        text_r_button = label_buttons.render('R', 1, self.WHITE_COLOR)
        text_inf_a_button = label_info_button.render(
            'ejecuta A*', 1, self.WHITE_COLOR)
        text_inf_d_button = label_info_button.render(
            'ejecuta BFS', 1, self.WHITE_COLOR)
        text_inf_s_button = label_info_button.render(
            'animacion', 1, self.WHITE_COLOR)
        text_inf_r_button = label_info_button.render(
            'generar matriz', 1, self.WHITE_COLOR)
        text_inf_c_button = label_info_button.render(
            'limpiar', 1, self.WHITE_COLOR)
        text_inf_l_button = label_info_button.render(
            'cargar', 1, self.WHITE_COLOR)
        text_inf_q_button = label_info_button.render(
            'vel -1', 1, self.WHITE_COLOR)
        text_inf_e_button = label_info_button.render(
            'vel +1', 1, self.WHITE_COLOR)

        # ejectia a*
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR,
                         (570, self.HEIGHT-95, 45, 42), border_radius=5)
        self.screen.blit(text_a_button, (585, self.HEIGHT-90))
        self.screen.blit(text_inf_a_button, (620, self.HEIGHT-86))

        # ejecuta bfs
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR,
                         (570, self.HEIGHT-45, 45, 42), border_radius=5)
        self.screen.blit(text_d_button, (585, self.HEIGHT-40))
        self.screen.blit(text_inf_d_button, (620, self.HEIGHT-35))

        # animacion
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR,
                         (710, self.HEIGHT-95, 45, 42), border_radius=5)
        self.screen.blit(text_s_button, (725, self.HEIGHT-86))
        self.screen.blit(text_inf_s_button, (760, self.HEIGHT-86))

        # generar matriz
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR,
                         (710, self.HEIGHT-45, 45, 42), border_radius=5)
        self.screen.blit(text_r_button, (725, self.HEIGHT-40))
        self.screen.blit(text_inf_r_button, (760, self.HEIGHT-35))

        # limpiar
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR,
                         (840, self.HEIGHT-95, 45, 42), border_radius=5)
        self.screen.blit(text_c_button, (855, self.HEIGHT-86))
        self.screen.blit(text_inf_c_button, (890, self.HEIGHT-86))

        # cargar
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR,
                         (870, self.HEIGHT-45, 45, 42), border_radius=5)
        self.screen.blit(text_l_button, (885, self.HEIGHT-40))
        self.screen.blit(text_inf_l_button, (920, self.HEIGHT-35))

        # bajar velocidad
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR,
                         (950, self.HEIGHT-95, 45, 42), border_radius=5)
        self.screen.blit(text_q_button, (965, self.HEIGHT-86))
        self.screen.blit(text_inf_q_button, (1000, self.HEIGHT-86))

        # subir velocidad
        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR,
                         (970, self.HEIGHT-45, 45, 42), border_radius=5)
        self.screen.blit(text_e_button, (985, self.HEIGHT-40))
        self.screen.blit(text_inf_e_button, (1020, self.HEIGHT-35))

    def animationExpanded(self, all_moviments):
        # animacion de nodos expandidos y creados
        self.time_animation = 0.01
        for action in all_moviments:
            isExpanded = action[1]
            coordenate = action[0]

            x_block = coordenate[0]*self.width_block
            y_block = coordenate[1]*self.width_block
            if (isExpanded):
                pygame.draw.rect(self.screen, self.NODE_EXPANDED_COLOR, (self.space_x +
                                 x_block, 40+self.space_y+y_block, self.width_block, self.width_block))
            else:
                pygame.draw.rect(self.screen, self.NODE_CREATED_COLOR, (self.space_x +
                                 x_block, 40+self.space_y+y_block, self.width_block, self.width_block))

            sleep(self.time_animation)
        self.animation = False

    def updateInfoScreen(self, nodes_create, nodes_expanded, algorithm):
        if (algorithm == 'a*'):
            self.counter_nodes_expanded_star = nodes_expanded
            self.counter_nodes_create_star = nodes_create
        else:
            self.counter_nodes_expanded_bfs = nodes_expanded
            self.counter_nodes_create_bfs = nodes_create

    def initAlgorithm(self, algorithm, avoid_backing_out):
        try:
            self.all_moviements = []
            ambiente = Agent(self.matriz, self.pos_agent, self.pos_churiken)
            init_time = datetime.datetime.now()
            if (algorithm == 'a*'):
                result = ambiente.aStar(
                    avoid_backing_out, self.updateInfoScreen)
            else:
                result = ambiente.bfs(avoid_backing_out, self.updateInfoScreen)

            end_time = datetime.datetime.now()
            node_winner: Node = result[0]

            self.all_moviements = result[3]

            if (algorithm == 'a*'):
                self.time_star = end_time-init_time
                self.counter_costo_total_star = node_winner.cost_acumulated

            else:
                self.time_bfs = end_time-init_time
                self.counter_costo_total_bfs = node_winner.cost_acumulated

            route = []
            movements = []
            parent_ = node_winner
            while parent_ != None:
                route.insert(0, parent_.posAgente)
                movements.insert(0, parent_.movement)
                parent_ = parent_.parent
            # print(f' nodos expandidos: {result[1]} nodos_creados: {result[2]}  tiempo_empleado:{end_time-init_time} costo-total:{node_winner.cost_acumulated}')
            self.animationRoute(algorithm, movements, route[0])
        except Exception as e:
            self.info_text = e
        finally:
            self.animation = False

    def animationRoute(self, algorithm, movements, init_coordanate):
        if algorithm == 'a*':
            self.clearGame()

        width = self.width_block/2
        x = init_coordanate[0]
        y = init_coordanate[1]

        route_color = self.PURPLE_COLOR if algorithm == 'a*' else self.GREEN_COLOR

        # ruta se le suma su mitad para que quede en el centro
        vector_route = pygame.Vector2(
            self.space_x+x*self.width_block+width, self.space_y+y*self.width_block+width)
        vector_agent = pygame.Vector2(
            self.space_x+x*self.width_block, self.space_y+y*self.width_block)

        frame_s = ceil(self.width_block)

        copy = pygame.Surface.copy(pygame.Surface.subsurface(
            # copio el frame de la pantalla sin efecto
            self.screen, (0, 40, self.WIDTH, self.HEIGHT-140)))
        # guardo el ultimo frame generado donde no esta el agente, se hace para que no quede rastro del agente
        last_ = copy.copy()
        image_agent = self.agent_icon.copy()
        for i in movements:
            # me muevo de 1 pixel hasta al tamaño total del cuadrado calculado previamente
            for j in range(frame_s):
                aux = pygame.Surface.copy(last_)
                if i == 'R':
                    vector_route.x += 1
                    vector_agent.x += 1
                    image_agent = self.agent_icon_right

                if i == 'L':
                    vector_route.x -= 1
                    vector_agent.x -= 1
                    image_agent = self.agent_icon_left

                if i == 'D':
                    vector_route.y += 1
                    vector_agent.y += 1
                    image_agent = self.agent_icon_down
                if i == 'U':
                    vector_route.y -= 1
                    vector_agent.y -= 1
                    image_agent = self.agent_icon_up

                pygame.draw.circle(aux, route_color, vector_route, width/2)
                last_ = pygame.Surface.copy(aux)
                aux.blit(image_agent, vector_agent)
                self.screen.blit(aux, (0, 40))
                sleep(0.001)
            rote = True

        self.animation = True

    def run(self):
        environ['SDL_VIDEO_WINDOW_POS'] = '1'  # centrar ventana
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen_background = pygame.Surface.copy(
            pygame.Surface.subsurface(self.screen, (0, 40, self.WIDTH, self.HEIGHT-140)))

        pygame.font.init()
        pygame.display.set_caption('Proyecto 1 - IA - A* & BFS')

        self.clock = pygame.time.Clock()
        self.running = True

        # elementos en la pantalla
        self.putTextOnScreen()
        # para que al precionar no se ejecute mas de 1 vez
        self.animation = False
        self.load_matriz = True
        self.matriz_random = True
        self.loadMatrix('18x20_1_default')
        while self.running:

            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    self.running = False

            self.putTextOnScreen()

            # ejecutar A*
            if not self.animation and self.info_matrix is not None and pygame.key.get_pressed()[pygame.K_a]:
                self.animation = True
                self.clearGame()
                # para demasiados estado es optimo no reccorrer nodos que ya han sido expandido, pero compromete la completitud de algoritmo
                self.thread_astar = threading.Thread(
                    target=self.initAlgorithm, args=('a*', True))
                self.thread_astar.start()

            # animacion
            if not self.animation and len(self.all_moviements) > 0 and pygame.key.get_pressed()[pygame.K_s]:
                self.animation = True
                self.clearGame()
                self.thread_animation = threading.Thread(
                    target=self.animationExpanded, args=(self.all_moviements,))
                self.thread_animation.start()

            # ejecutar BFS
            if not self.animation and self.info_matrix is not None and pygame.key.get_pressed()[pygame.K_d]:
                self.animation = True
                self.thread_bfs = threading.Thread(
                    target=self.initAlgorithm, args=('bfs', True))
                self.thread_bfs.start()

            # aumentar  la velocidadee
            if self.animation and pygame.key.get_pressed()[pygame.K_e]:
                aux = self.time_animation-0.001
                if (aux >= 0.001):
                    self.time_animation = aux

            # realentizar la velocidad
            if self.animation and self.time_animation < 1 and pygame.key.get_pressed()[pygame.K_q]:
                self.time_animation += 0.001

            # cargar matriz
            if not self.animation and self.load_matriz and pygame.key.get_pressed()[pygame.K_l]:
                self.load_matriz = False
                self.clearTexts()
                name_matriz = self.inputMatrizModal.openModal()
                if (name_matriz is not None):
                    self.loadMatrix(name_matriz)
                else:
                    self.load_matriz = True

            if not self.animation and self.matriz_random and pygame.key.get_pressed()[pygame.K_r]:
                self.all_moviements = []
                matriz_name = generatorMatrizGame()
                self.loadMatrix(matriz_name)
                self.clearTexts()

                self.matriz_random = False

                def can_load_matriz():
                    sleep(1)
                    self.matriz_random = True
                threading.Thread(target=can_load_matriz).start()

            if not self.animation and pygame.key.get_pressed()[pygame.K_c]:
                self.clearGame()
                self.clearTexts()
            pygame.display.flip()  # muestra la ventana aqui
            self.clock.tick(60)
        pygame.quit()
        exit()


if __name__ == '__main__':
    inputMatrizModal = InputMatrizModal()
    gui = GUI(WIDTH, HEIGHT, inputMatrizModal)
