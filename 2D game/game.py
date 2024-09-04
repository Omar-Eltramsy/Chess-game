import pygame as pg
import time
pg.init()
win = pg.display.set_mode((720, 480))
pg.display.set_caption("Justice chess")

# update walk
walkRight = [pg.image.load('R1.png'), pg.image.load('R2.png'), pg.image.load('R3.png'), pg.image.load('R4.png'), pg.image.load('R5.png'), pg.image.load('R6.png'), pg.image.load('R7.png'), pg.image.load('R8.png'), pg.image.load('R9.png')]
walkLeft = [pg.image.load('L1.png'), pg.image.load('L2.png'), pg.image.load('L3.png'), pg.image.load('L4.png'), pg.image.load('L5.png'), pg.image.load('L6.png'), pg.image.load('L7.png'), pg.image.load('L8.png'), pg.image.load('L9.png')]
bg = pg.image.load('bg.jpg')
standing = pg.image.load('standing.png')
fbs = pg.time.Clock()
score=0
# ----------------------------------------------
#           Class for players
# ----------------------------------------------
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isjump = False
        self.jumpcount = 10
        self.left = False
        self.right = False
        self.walkcount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y+11, 29, 52)

    def draw(self, win):
        if self.walkcount + 1 >= 27:
            self.walkcount = 0
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            elif self.right:
                win.blit(walkRight[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y+11, 29, 52)  
        #pg.draw.rect(win, (255, 0, 0), self.hitbox, 2)
    
    def hit(self):
        self.x=60
        self.y=410
        self.walkcount=0
        font1=pg.font.SysFont("comicsans",100)
        text=font1.render('-5',1,(255,0,0))
        win.blit(text,((720/2)-(text.get_width()/2),240))
        pg.display.update()
        i=0
        while i<100:
            pg.time.delay(10)
            i+=1
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    i=301
                    pg.QUIT()
# ----------------------------------------------
#               Class for enemy
# ----------------------------------------------
class enemy(object):
    walkRight = [pg.image.load('R1E.png'), pg.image.load('R2E.png'), pg.image.load('R3E.png'), pg.image.load('R4E.png'), pg.image.load('R5E.png'), pg.image.load('R6E.png'), pg.image.load('R7E.png'), pg.image.load('R8E.png'), pg.image.load('R9E.png'), pg.image.load('R10E.png'), pg.image.load('R11E.png')]
    walkLeft = [pg.image.load('L1E.png'), pg.image.load('L2E.png'), pg.image.load('L3E.png'), pg.image.load('L4E.png'), pg.image.load('L5E.png'), pg.image.load('L6E.png'), pg.image.load('L7E.png'), pg.image.load('L8E.png'), pg.image.load('L9E.png'), pg.image.load('L10E.png'), pg.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkcount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y+2, 31, 57)
        self.health=10
        self.visible=True
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkcount + 1 >= 33:
                self.walkcount = 0  # walkcount
            if self.vel > 0:
                win.blit(self.walkRight[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            else:
                win.blit(self.walkLeft[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            pg.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,50,10))
            pg.draw.rect(win,(0,125,0),(self.hitbox[0],self.hitbox[1]-20,50-(5*(10-self.health)),10))

            self.hitbox = (self.x + 17, self.y+2, 31, 57)
            #pg.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        
# to move the character
# ----------------------- 
    def move(self):
        if self.vel > 0:  # Moving right
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0  
        else:  # Moving left
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount = 0  
    def hit(self):
        if self.health>0:
            self.health-=1
        else:
            self.visible=False
        print("ana 2drabt")
# -----------------------
#      for bullets
# -----------------------
class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pg.draw.circle(win, self.color, (self.x, self.y), self.radius)  

# -----------------------
#     Window sitting
# -----------------------
def window():
    win.blit(bg, (0, 0))
    text=font.render("Score:"+ str(score),1,(0,0,0))
    win.blit(text,(550,10))
    man.draw(win)
    evil.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pg.display.update()

# ----------------------- 
#       Main loop
# -----------------------
font=pg.font.SysFont('comicsans',30,True)
man = player(350, 400, 10, 64)
evil = enemy(0, 400, 10, 64, 680)
bullets = []
shootloop=0
running = True
while running:
    fbs.tick(27)
    if man.hitbox[1]<evil.hitbox[1]+evil.hitbox[3] and man.hitbox[1]+man.hitbox[3]>evil.hitbox[1]:
        if man.hitbox[0]+man.hitbox[2] >evil.hitbox[0] and man.hitbox[0]< evil.hitbox[0]+evil.hitbox[2]:
            man.hit()
            score-=5    
    if shootloop>0:
        shootloop+=1
    if shootloop>3:
        shootloop=0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    for bullet in bullets:
        if bullet.y-bullet.radius<evil.hitbox[1]+evil.hitbox[3] and bullet.y+bullet.radius>evil.hitbox[1]:
            if bullet.x -bullet.radius >evil.hitbox[0] and bullet.x-bullet.radius< evil.hitbox[0]+evil.hitbox[2]:
                evil.hit()
                score+=1    
                bullets.pop(bullets.index(bullet))

        if bullet.x < 720 and bullet.x > 0:
            bullet.x += bullet.vel
        else: 
            bullets.pop(bullets.index(bullet))

    key = pg.key.get_pressed()
    if key[pg.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif key[pg.K_RIGHT] and man.x < 720 - man.width:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkcount = 0

    if not man.isjump:
        if key[pg.K_SPACE]:
            facing = -1 if man.left else 1
            # if len(bullets) < 10:
            #     bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0,0,0), facing))
            if len(bullets)<5:
                bullets.append(projectile(round(man.x+man.width // 2),round(man.y+man.height // 2),6,(0,0,0),facing))
        shootloop=1
        if key[pg.K_UP]:
            man.isjump = True
            man.right = False
            man.left = False
            man.walkcount = 0
    else:
        if man.jumpcount >= -10:
            man.y -= (man.jumpcount * abs(man.jumpcount)) * 0.5
            man.jumpcount -= 1
        else:
            man.jumpcount = 10
            man.isjump = False
    window()

pg.quit()
