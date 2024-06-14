import pygame as pg 
from random import randrange
from random import randint
pg.init()
font = pg.font.SysFont('dejavusansmono', 25)

Window_Height_pixels = 1000
Window_Width_pixels = 1000
Tile_Size = 50
Window_Height = Window_Height_pixels // Tile_Size
Window_Width = Window_Width_pixels // Tile_Size

screen = pg.display.set_mode((Window_Width_pixels, Window_Height_pixels))

clock = pg.time.Clock()
get_random_position = lambda: [randrange(1, (Window_Width_pixels // Tile_Size)) * Tile_Size, randrange(1, (Window_Height_pixels // Tile_Size)) * Tile_Size]

# reset 
# reward 
# play(action) returns direction
# frame, state, game iteration 
# is collision change

def random_position():
    return (randrange(1, Window_Width - 1), randrange(1, Window_Height - 1))

class SnakeAgent:
    def __init__(self):
        self.length = 1
        self.head = []
        self.positions = []
        self.direction = 0
        self.lastpositionbuff = []
        self.frameiteration = 0
        self.score = 0

    def random_head_position(self):
        self.head.append(random_position())
        self.positions = self.head

    def move(self):
        self.lastpositionbuff = self.positions[-1]

        if self.direction == 0:
            self.positions.insert(0, (self.positions[0][0], self.positions[0][1] - 1))
        if self.direction == 1:
            self.positions.insert(0, (self.positions[0][0] + 1, self.positions[0][1]))
        if self.direction == 2:
            self.positions.insert(0, (self.positions[0][0], self.positions[0][1] + 1))
        if self.direction == 3:
            self.positions.insert(0, (self.positions[0][0] - 1, self.positions[0][1]))

        del self.positions[-1]
        
    def reset(self):
        self.length = 1
        self.head = []
        self.positions = []
        self.direction = 0
        self.lastpositionbuff = []
        self.random_head_position()
        self.move()
        self.score = 0

    def drawScore(self):
        screen.blit(font.render(f'Score: {self.score}', True, (255, 255, 255)), (0, 0))

class Food: 
    def __init__(self):
        self.position = []

    def add(self):
        self.position.append(random_position())

    def draw(self):
        pg.draw.rect(screen, 'red', (self.position[0] * Tile_Size, self.position[1] * Tile_Size, Tile_Size, Tile_Size))
        

def check_collision(snake, food):
    if snake.positions[0] == food.position[0]:
        snake.length += 1
        snake.positions.append(snake.lastpositionbuff)
        food.position = []
        food.add()
        snake.score += 1
        snake.drawScore()

    if snake.positions[0][0] == Window_Width or snake.positions[0][0] == -1:
        print('Game Over')
        game_reset(snake, food)

    if snake.positions[0][1] == Window_Height or snake.positions[0][1] == -1:
        print('Game Over')
        game_reset(snake, food)
        
    if snake.length > 1:
        for i in snake.positions[1:]:
            if snake.positions[0] == i:
                print('Game Over')
                game_reset(snake, food)
        

def change_direction(snake, event, food):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

        if event.type == pg.KEYDOWN:
            if (event.key == pg.K_UP or event.key == pg.K_w) and snake.direction != 2:
                snake.direction = 0
            if (event.key == pg.K_RIGHT or event.key == pg.K_d) and snake.direction != 3:
                snake.direction = 1
            if (event.key == pg.K_DOWN or event.key == pg.K_s) and snake.direction != 0:
                snake.direction = 2
            if (event.key == pg.K_LEFT or event.key == pg.K_a) and snake.direction != 1:
                snake.direction = 3

    snake.move()
    draw_grid(snake, food)
    check_collision(snake, food)

def draw_grid(snake, food):
    screen.fill((0, 0, 0))

    [pg.draw.rect(screen, 'green', (snake.positions[0][0] * Tile_Size, 
                                    snake.positions[0][1] * Tile_Size, 
                                    Tile_Size, Tile_Size))]

    for x, y in snake.positions[1:]:
        [pg.draw.rect(screen, 'blue', (x * Tile_Size, y * Tile_Size, Tile_Size, Tile_Size))]

    [pg.draw.rect(screen, 'red', (x * Tile_Size, y * Tile_Size, Tile_Size, Tile_Size)) for x, y in food.position]


def game_reset(snake, food):
    snake.reset()
    food.position = []
    food.add()
    snake.drawScore()
    draw_grid(snake, food)
    pg.display.flip()

def main():
    snake = SnakeAgent()
    SnakeAgent.random_head_position(snake)
    food = Food()
    snake.drawScore()
    Food.add(food)
    
    while True: 
        change_direction(snake, pg.event, food)
        snake.drawScore()
        pg.display.flip()
        clock.tick(10)
    
if __name__ == '__main__':
    main()