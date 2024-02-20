import pygame
import random
f = open("keyterm.txt","r")
termsAndDefinitions = []
for i in range(25):
    line = (f.readline())
    termsAndDefinitions.append(line.split(':'))
f.close()

pygame.init()

#COLORS/FONT/INITIALISATION
black = (0,0,0)
white = (255,255,255)

font = pygame.font.SysFont("Arial",15)

user_text = ""
getIndex = False
game_state = "running"
score = 0
scoreIncrement = False


#DISPLAY
width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
running = True

#IMAGES
catImage = pygame.image.load('images/cat.png')
appleImage = pygame.image.load('images/apple.png')

#OBJECTS
class Cat(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10
        self.hitbox = (self.x, self.y + 20, 100, 80)
    def draw(self, screen):
        screen.blit(catImage, (self.x, self.y))
        self.hitbox = (self.x, self.y + 20, 100, 80)

class Apple(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.hitbox = (self.x,self.y,50,50)
    def draw(self, screen):
        self.vel = 10
        screen.blit(appleImage,(self.x,self.y))
        self.hitbox = (self.x,self.y,50,50)
#MAIN

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def scoreMessage(msg, x, y, size):
    regText = pygame.font.Font("freesansbold.ttf", size)
    textSurf, textRect = text_objects(msg, regText)
    textRect.center = (x, y)
    screen.blit(textSurf, textRect)

def display_answer(event):
   global game_state, scoreIncrement
   if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            scoreIncrement = False
            game_state = "running"

def draw_answer(user_text):
    global index, game_state, score, scoreIncrement
    if user_text.title() == termsAndDefinitions[index][0]:
        cow = font.render("Correct! \n (press return to continue)", True, (255, 255, 255))
        screen.blit(cow, (200,200))
        if scoreIncrement == False:
            score += 1
            scoreIncrement = True
    else:
        cow = font.render(f"Incorrect, answer is {termsAndDefinitions[index][0]} \n (press return to continue)", True, (255, 255, 255))
        screen.blit(cow, (200,200))
    pygame.display.update()
 


def question(game_state, user_text, event):
    global getIndex
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            getIndex = False
            game_state = "display answer"
        elif event.key == pygame.K_BACKSPACE:
            user_text = user_text[:-1]
        else:
            user_text += event.unicode
    return game_state, user_text

def draw_question():
    global getIndex, index
    if getIndex == False:
        index = random.randint(0, 24)
        getIndex = True
    max_width = 115 
    max_lines = 3  

    question = termsAndDefinitions[index][1]
    lines = []
    words = question.split()
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_width:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    
    lines.append(current_line)

    if len(lines) > max_lines:
        lines = lines[:max_lines]
    
    y = 200
    for line in lines:
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (50, y))
        y += text_surface.get_height()
    InputText = font.render(user_text, True, (255, 255, 255))
    screen.blit(InputText, (200,y + 10))


def main():
    global game_state, user_text, score
    running = True
    appleRate = 60
    appleCounter = 0
    cat = Cat(width//2,450)
    apple = None

    while running:
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == "waiting for input":
                game_state, user_text = question(game_state, user_text, event)
            elif game_state == "display answer":
                display_answer(event)

        if game_state == "waiting for input":
            draw_question()
        if game_state == "display answer":
            draw_answer(user_text)
    
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and cat.x > cat.vel - 5:
            cat.x -= cat.vel
        if keys[pygame.K_RIGHT]:
            cat.x += cat.vel
        if game_state == "running":
            appleCounter += 1
            if appleCounter == appleRate:
                appleCounter = 0
                xstart = random.randint(100,width - 100)
                ystart = 0
                apple = Apple(xstart,ystart)
                apple.draw(screen)
            
            if apple:
                ystart += apple.vel
                apple = Apple(xstart,ystart)
                apple.draw(screen)
                if (apple.hitbox[0] >= cat.hitbox[0] - 20) and (apple.hitbox[0] <= cat.hitbox[0] + 70):
                    if cat.hitbox[1] - 100 <= apple.hitbox[1] <= cat.hitbox[1] - 40:
                            apple = None
                            game_state = "waiting for input"
                            print("Score:", score)
                
                if ystart >= height:
                    apple = None

        text = font.render("Score: " + str(score), True, white)
        screen.blit(text, (10, 10))
        cat.draw(screen)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()

main()
