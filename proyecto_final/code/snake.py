import pygame as pg
import random
import sys
from pygame.math import Vector2

class SNAKE:
    def __init__(self) -> None:
        self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        self.direction = Vector2(1,0)
        self.newBlock = False
        
    def draw_snake(self):
        for block in self.body:
            #crear rectangulo
            block_rect = pg.Rect(block.x*cell_size, block.y*cell_size, cell_size, cell_size)
            #dibujar el rectangulo
            pg.draw.rect(screen, pg.Color('green'), block_rect)
            
    def move_snake(self):
        if self.newBlock == False:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
        else:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.newBlock = False
        
    def add_block(self):
        self.newBlock = True

class FRUIT:
    def __init__(self):
        self.randomize()
        
    #dibujar un cuadradro (la fruta)    
    def draw_fruit(self):
        #crear un rectangulo
        fruit_rect = pg.Rect(self.pos.x*cell_size, self.pos.y*cell_size, cell_size, cell_size)
        #dibujar el recangulo
        pg.draw.rect(screen, pg.Color('red'), fruit_rect)
        
    def randomize(self):
        #crear posicion de la fruta
        self.x = random.randint(0,cell_num-1)
        self.y = random.randint(0,cell_num-1)
        self.pos = Vector2(self.x, self.y)

class BOARD:
    def __init__(self) -> None:
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            #Reposicionar la fruta
            self.fruit.randomize()
            
            #Crecer la serpiente
            self.snake.add_block()
            
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
            
    def game_over(self):
        pg.quit()
        sys.exit()
        
    def check_fail(self):
        #CHECK PARA CHOQUE EN LAS PAREDES
        #check para saber si la cabeza golpea la paredes laterales
        if not (0 <= self.snake.body[0].x < cell_num):
            self.game_over()
            
        #check para saber si la cabeza golpea la paredes superior e inferior
        if not (0 <= self.snake.body[0].y < cell_num):
            self.game_over()
            
        #CHECK PARA CHOQUE CONTRA EL CUERPO DE LA SERPIENTE
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
                
    def draw_score(self):
        score_text = str((len(self.snake.body)-3)*10)
        score_surface = game_font.render(score_text,False,pg.Color('white'))
        score_x = 20
        score_y = cell_size * cell_num - 40
        score_rect = score_surface.get_rect(topleft = (score_x,score_y))
        screen.blit(score_surface,score_rect)
            
pg.init()
cell_size = 40
cell_num = 20
game_font = pg.font.Font(None,25)
screen = pg.display.set_mode((cell_num*cell_size,cell_num*cell_size))
clock = pg.time.Clock()

tablero = BOARD()

SCREEN_UPDATE = pg.USEREVENT
pg.time.set_timer(SCREEN_UPDATE, 150)

#En este bucle se dibujan todos los elementos por pantalla
while True:
    
    #Para cerrar el juego se necesita un "event loop" que detecte cuando se cierre la ventana
    for event in pg.event.get():
        #detecta cuando se cierre la ventana
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
            
        if event.type == SCREEN_UPDATE:
            tablero.update()
            
        #Cambiar la dirección de la serpiente
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and tablero.snake.body[1] != tablero.snake.body[0] + Vector2(0,-1):
                tablero.snake.direction = Vector2(0,-1)
            if event.key == pg.K_DOWN and tablero.snake.body[1] != tablero.snake.body[0] + Vector2(0,1):
                tablero.snake.direction = Vector2(0,1)
            if event.key == pg.K_LEFT and tablero.snake.body[1] != tablero.snake.body[0] + Vector2(-1,0):
                tablero.snake.direction = Vector2(-1,0)
            if event.key == pg.K_RIGHT and tablero.snake.body[1] != tablero.snake.body[0] + Vector2(1,0):
                tablero.snake.direction = Vector2(1,0)
                
    screen.fill(pg.Color('black'))
    tablero.draw_elements()  
    pg.display.update()
    clock.tick(60)  #ajusta el framerate maximo a 60