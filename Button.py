import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((800, 600))
class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width, height, color=(255,255,0))


    def setCords(self,x,y):
        self.rect.topleft = x,y

    def pressed(self,mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False
def main():
    button = Button(0,0, 200,200) #Button class is created
    button.setCords(0,0) #Button is displayed at 200,200
    pygame.draw.rect(screen,(244,244,0),button)
    while 1:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if button.pressed(mouse):   #Button pressed method is called
                    print ('button hit')
main()
