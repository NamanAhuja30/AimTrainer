import math
import random
import pygame
import time



pygame.init()

width , height = 800 , 600
bgColor = (0,30,40)

lives = 3

topBarHeight = 50

labelFont = pygame.font.SysFont("comicsans" , 24)

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Aim Trainer")


targetIncrement = 700        # in milli sec
targetEvent = pygame.USEREVENT
targetPadding = 30



class Target(object):
    maxSize = 30
    growthRate = 0.2
    color = "red"
    secondaryColor = "white" 

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.growthRate >= self.maxSize:
            self.grow = False

        if self.grow:
            self.size += self.growthRate 
        else:
            self.size -= self.growthRate

    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.x,self.y), self.size)
        pygame.draw.circle(screen,self.secondaryColor,(self.x,self.y), self.size*0.8)    # this will be on top of previous circle
        pygame.draw.circle(screen,self.color,(self.x,self.y), self.size*0.6)
        pygame.draw.circle(screen,self.secondaryColor,(self.x,self.y), self.size*0.4)
    
    
    def collide(self,x,y):
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size


def Draw(screen,targets):

    screen.fill(bgColor)   #clears the screen(fills it with the specified color)

    for target in targets:
        target.draw(screen)

    


def formatTime(secs):
    milli = math.floor(int(secs*1000 % 1000) / 100)
    seconds = int(round(secs % 60 , 1))
    minutes = int(secs // 60)

    return f"{minutes: 02d}:{seconds: 02d}.{milli}"



def drawTopBar(screen , elapsedTime , targetsPressed , misses):
     
     pygame.draw.rect(screen , "grey" , (0,0,width,topBarHeight) )

     timeLabel = labelFont.render(
         f"Time: {formatTime(elapsedTime)}", 1 , "black" )
     

     speed = round(targetsPressed / elapsedTime , 1)
     speedLabel = labelFont.render(f"Speed: {speed} t/s",1,"black")

     hitsLabel = labelFont.render(f"Hits: {targetsPressed}",1,"black")

     livesLabel = labelFont.render(f"Lives: {lives - misses}" , 1 , "black")

     screen.blit(timeLabel,(5,5))
     screen.blit(speedLabel,(200,5))
     screen.blit(hitsLabel,(450,5))
     screen.blit(livesLabel,(650,5))
    
    

def endScreen(screen , elapsedTime , targetsPressed, clicks ):

    screen.fill(bgColor)

     
    timeLabel = labelFont.render(
         f"Time: {formatTime(elapsedTime)}", 1 , "white" )
     

    speed = round(targetsPressed / elapsedTime , 1)
    speedLabel = labelFont.render(f"Speed: {speed} t/s",1,"white")

    hitsLabel = labelFont.render(f"Hits: {targetsPressed}",1,"white")

    accuracy = round(targetsPressed / clicks *100 , 1)
    accuracyLabel = labelFont.render(f"Accuracy: {accuracy}%",1,"white")

    
    screen.blit(timeLabel, (getMiddle(timeLabel), 100 ) )
    screen.blit(speedLabel, (getMiddle(speedLabel), 200 ))
    screen.blit(hitsLabel, (getMiddle(hitsLabel), 300 ))
    screen.blit(accuracyLabel, (getMiddle(accuracyLabel), 400 ))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN :
                quit()
    
    


def getMiddle(surface):
    return width/2 - surface.get_width()/2



def main():

    targets = []

    pygame.time.set_timer(targetEvent,targetIncrement)  #trigger the targetEvent every targetIncrement time

    run = True

    clock = pygame.time.Clock()

    targetPressed = 0
    clicks = 0
    misses = 0
    startTime = time.time()


    while run :                                                                     #InFINITE LOOP

        clock.tick(60)     # run the while loop at 60 FPS

        click = False

        mousePos = pygame.mouse.get_pos()

        elapsedTime = time.time() - startTime

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False
                break

            if event.type == targetEvent:
                x = random.randint(targetPadding , width - targetPadding)
                y = random.randint(targetPadding + topBarHeight , height - targetPadding )
                target = Target(x,y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0 :
                targets.remove(target)
                misses += 1

            if click and target.collide(*mousePos):
                targets.remove(target)
                targetPressed += 1
        
        if misses >= lives :
            endScreen(screen,elapsedTime,targetPressed,clicks)


        Draw(screen,targets)
        drawTopBar(screen , elapsedTime , targetPressed , misses)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()



