import pygame
import math
import random
#Dimensions of the canvas
sh = 773
sw = 800

#Loading the images into variables
bg = pygame.image.load("ElementsPics/bg.png")
alien = pygame.image.load("ElementsPics/AlienShip.png")
asteroidL = pygame.image.load("ElementsPics/asteroidL.png")
asteroidM = pygame.image.load("ElementsPics/asteroidM.png")
asteroidS = pygame.image.load("ElementsPics/asteroidS.png")
star = pygame.image.load("ElementsPics/Star.png")
playerShip = pygame.image.load("ElementsPics/StarShip.png")

#Setting the title of the game
pygame.display.set_caption('Asteroids')
win = pygame.display.set_mode((sw,sh))

clock = pygame.time.Clock() #Clock Variable 
gameover = False

#Player class to define the Features of the Spaceship
class Player(object):
    def __init__(self): #init method to initialize the variables
        self.img = playerShip
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = sw//2
        self.y = sw//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x+self.cosine*self.w//2, self.y-self.sine*self.h//2)

    def draw(self, win): #draw method to draw the spaceship onto the window
        win.blit(self.rotatedSurf, self.rotatedRect)

    def rotateLeft(self):
        self.angle +=7
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x+self.cosine*self.w//2, self.y-self.sine*self.h//2)

    def rotateRight(self):
        self.angle -=7
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x+self.cosine*self.w//2, self.y-self.sine*self.h//2)

    def goForward(self):
        self.x += self.cosine * 6
        self.y -= self.sine *6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x+self.cosine*self.w//2, self.y-self.sine*self.h//2)
    
    def teleport(self):
        if self.x > sw+50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = sw
        elif self.y < -50:
            self.y = sh + 50
        elif self.y >sh + 50:
            self.y = 0


#class to define the bullets of the spaceship
class Bullet(object):
    def __init__(self):#init method to initialize the variables
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s  = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self): #to check the bullets leaving the screen 
        if self.x < -50 or self.x > sw or self.y > sh or self.y < -50:
            return True

class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = asteroidS
        elif self.rank == 2:
            self.image = asteroidM
        elif self.rank == 3:
            self.image = asteroidL
        self.w = 50 * rank
        self.h = 50 * rank
        self.randPoint = random.choice([(random.randrange(0, sw-self.w), random.choice([-1*self.h - 5, sh + 5])), (random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.randPoint
        
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sw//2:
            self.ydir = 1
        else:
            self.ydir = 1
        
        self.xv = self.xdir * random.randrange(1,3)
        self.yv = self.ydir * random.randrange(1,3)
    def draw(self,win):
        win.blit(self.image, (self.x, self.y))

def redrawGameWindow():
    win.blit(bg,(0,0))
    player.draw(win)
    for a in asteroids:
        a.draw(win)
    for b in playerBullets:
        b.draw(win)
    pygame.display.update()

run = True

player = Player()
playerBullets = []
asteroids = []

count = 0

while run:
    clock.tick(60)
    count +=1

    if not gameover:
        if count%50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroids.append(Asteroid(ran))
        player.teleport()
        for b in playerBullets:
            b.move()
            if b.checkOffScreen():
                playerBullets.pop(playerBullets.index(b))
        for a in asteroids:
            a.x += a.xv
            a.y += a.yv
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.goForward()
        if keys[pygame.K_a]:
            player.rotateLeft()
        if keys[pygame.K_d]:
            player.rotateRight()
 
            

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False
        if event.type == pygame.KEYDOWN: #The KEYDOWN keyword mentions to the interpreter about the key being held down
            if event.key == pygame.K_SPACE:
                if not gameover:
                    playerBullets.append(Bullet())

    redrawGameWindow()
pygame.quit()

