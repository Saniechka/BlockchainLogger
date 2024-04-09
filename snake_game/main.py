import pygame
from pygame.locals import *
import time
import random
import logging




logger = logging.getLogger('snake_logger')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('snake.log')
file_handler.setLevel(logging.INFO)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)


file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)

console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


critical_logger = logging.getLogger('critical_logger')
critical_logger.setLevel(logging.ERROR)  

critical_file_handler = logging.FileHandler('critical.log')
critical_file_handler.setLevel(logging.CRITICAL)

critical_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
critical_file_handler.setFormatter(critical_formatter)

critical_logger.addHandler(critical_file_handler)



SIZE=40
STEP_SIZE = 40
BACKGROUND_COLOR =(110,110,5)


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x= random.randint(0,14)*SIZE 
        self.y= random.randint(0,14)*SIZE 







class Snake:
    def __init__(self,parent_screen, length):
        self.parent_screen = parent_screen
        self.length= length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x=[SIZE]*length
        self.y=[SIZE]*length
        self.direction='down'
    
    def draw(self):
        self.parent_screen.fill((110,110,5))  
        for i in range(self.length) :    
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'
        

    def move_right(self):
        self.direction = 'right'
        
    
    def move_up(self):
        self.direction = 'up'
        
    
    def move_down(self):
        self.direction = 'down'
        
    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] =self.x[i-1]
            self.y[i] =self.y[i-1]
        if self.direction == 'up':
            self.y[0]-=STEP_SIZE
            
        if self.direction == 'down':
            self.y[0]+=STEP_SIZE
            
        if self.direction == 'left':
            self.x[0]-=STEP_SIZE
           
        if self.direction == 'right':
            self.x[0]+=STEP_SIZE
        self.draw()
            
        
       


class Game:  
    def __init__(self):
        pygame.init()
        logger.info(" NEW Game")
        critical_logger.critical("NEW GAME")
        self.surface = pygame.display.set_mode((600,600))
        #self.surface.fill((110,110,5))
        self.snake = Snake(self.surface,5)
        self.snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()

    # apple colission
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def score(self):
        font=pygame.font.SysFont('arial',30)
        score = font.render(f"Score:{self.snake.length-2}",True,(200,200,200))
        self.surface.blit(score,(500,10)) # change for making 




    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.score()
        pygame.display.flip()


        ## eating apple
        if self.is_collision(self.snake.x[0],self.snake.y[0], self.apple.x, self.apple.y):
            logger.info('EAT_APPLE')
            self.snake.increase_length()
            self.apple.move()

        # eate snake xd
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                critical_logger.critical('EAT_SNAKE')
                logger.info('EAT SNAKE')
                raise("game over xd")
        
        if (
        self.snake.x[0] < 0 or 
        self.snake.x[0] >= 600 or 
        self.snake.y[0] < 0 or 
        self.snake.y[0] >= 600
    ):
            logger.info('Sciana')
            critical_logger.critical('SCIANA')
            raise Exception("game over xd")
                


    def game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        logger.info(f"Game is over! Your score is {self.snake.length}")
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()


    def reset(self):
        logger.info('RESTART. NEW GAME')
        critical_logger.critical("RESTART")
        self.snake = Snake(self.surface,4)
        self.apple = Apple(self.surface)
        


    def run(self):
        running = True
        pause =False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:

                    if event.key == K_RETURN:
                        pause = False
                        self.reset()
                    if event.key == K_ESCAPE:
                            running = False
                
                    if not pause:
                        
                    
                        if event.key == K_UP:
                            self.snake.move_up()
                            logger.info('UP')   

                        if event.key == K_DOWN:
                            self.snake.move_down()
                            logger.info('DOWN')   

                        if event.key == K_RIGHT:
                            self.snake.move_right()
                            logger.info('RIGHT')   

                        if event.key == K_LEFT:
                            self.snake.move_left()
                            logger.info('LEFT')   
    
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                logger.info('GAME_OVER')
                critical_logger.critical('GAME_OVER')
                pause =True    
                
            time.sleep(.4)

    
if __name__ =="__main__":
    game= Game()
    game.run()
