import pygame
import time
from random import randint
from pygame.locals import *
pygame.init()



class Card:
    def __init__(self, pos, random_num):
        self.mark = False
        self.wrong = False
        self.highlight = False
        self.success = False  
        self.num = random_num
        self.size = 80
        self.font = pygame.font.SysFont('Arial', 25)
        self.color = black
        self.font_color = white
        self.pos = pos


    def draw(self, screen):
        if self.mark == False and self.highlight == False and self.wrong == False and self.success == False:
            pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.size, self.size))
            screen.blit(self.font.render(str(self.num), True, white), (self.pos[0]+35, self.pos[1]+25))
        elif self.mark == True:
            pygame.draw.rect(screen, mark_colour, (self.pos[0], self.pos[1], self.size, self.size))
            screen.blit(self.font.render(str(self.num), True, white), (self.pos[0]+35, self.pos[1]+25))
        elif self.success == True:
            pygame.draw.rect(screen, success_colour, (self.pos[0], self.pos[1], self.size, self.size))
            screen.blit(self.font.render(str(self.num), True, white), (self.pos[0]+35, self.pos[1]+25))
        elif self.wrong == True:
            pygame.draw.rect(screen, error_colour, (self.pos[0], self.pos[1], self.size, self.size))
            screen.blit(self.font.render(str(self.num), True, white), (self.pos[0]+35, self.pos[1]+25))
        elif self.highlight == True:
            pygame.draw.rect(screen, highlight_colour, (self.pos[0], self.pos[1], self.size, self.size))
            screen.blit(self.font.render(str(self.num), True, white), (self.pos[0]+35, self.pos[1]+25))

        

class Board:
    def __init__(self):
        self.cards = []
        self.active_board = False
        self.font = pygame.font.SysFont('Arial', 25)
        self.color = black
        self.font_color = white
        self.target_sum = self.random_sum()
        self.score_value = 0
        self.score = 'Score: ' + str(self.score_value)
        self.score_pos = (40, 960)
        self.score_size = 100
        self.lines = []
        self.wrong_card = None
        self.mission = f'___ + ___ = {self.target_sum}'
        self.mission_pos = (40, 840)
        self.mission_size = 100
        



        for y in range(10):
            self.cards.append([])
            for x in range(10):
                self.cards[y].append(Card((x*80, y*80), self.random_num()))

        for y in range(0, 11, 1):
            temp = []
            temp.append((0, y * 80))
            temp.append((800, y * 80))
            self.lines.append(temp)

        for x in range(0, 11, 1):
            temp = []
            temp.append((x*80, 0))
            temp.append((x*80, 800))
            self.lines.append(temp)


    def random_num(self):
        return randint(1,9)

    def random_sum(self):
        return randint(6,16)

    def draw(self, screen):
        for row in self.cards:
            for card in row:
                card.draw(screen)

        pygame.draw.rect(screen, self.color, (self.mission_pos[0], self.mission_pos[1], self.mission_size, self.mission_size))
        screen.blit(self.font.render(self.mission, True, white), (self.mission_pos[0], self.mission_pos[1]))

        pygame.draw.rect(screen, self.color, (self.score_pos[0], self.score_pos[1], self.score_size, self.score_size))
        screen.blit(self.font.render(str(self.score), True, white), (self.score_pos[0], self.score_pos[1]))

        for line in self.lines:
            pygame.draw.line(screen, white, line[0], line[1])



    def click(self, x, y):
        #------------------------------------------------------
        if self.active_board == False:
            self.active_board = True

            self.selection1 = self.cards[y][x]
            self.mission = f' {self.selection1.num}  + ___ = {self.target_sum}'

            self.adjacent_cards = []
            try:
                self.adjacent_cards.append(self.cards[y][x-1])
            except IndexError:
                pass
            try:
                self.adjacent_cards.append(self.cards[y][x+1])
            except IndexError:
                pass
            try:
                self.adjacent_cards.append(self.cards[y-1][x])
            except IndexError:
                pass
            try:
                self.adjacent_cards.append(self.cards[y+1][x])
            except IndexError:
                pass

            self.selection1.mark = True

            for adjacent_card in self.adjacent_cards:
                    adjacent_card.highlight = True



        elif self.active_board == True:
            
            if self.cards[y][x] in self.adjacent_cards and self.cards[y][x].num + self.selection1.num == self.target_sum:
                self.selection2  = self.cards[y][x]
                self.mission = f'{self.selection1.num} + {self.selection2.num} = {self.target_sum}'
                self.selection1.mark = False
                for adjacent_card in self.adjacent_cards:
                    adjacent_card.highlight = False
                self.score_value += (self.selection1.num+self.selection2.num)
                self.selection1.num = 0
                self.selection1.success = True
                self.selection2.num = 0
                self.selection2.success = True
                self.active_board = False
                self.score = 'Score: ' + str(self.score_value)


            elif self.cards[y][x] == self.selection1:
                self.selection1.mark = False
                for adjacent_card in self.adjacent_cards:
                    adjacent_card.highlight = False
                self.active_board = False
                self.mission = f'___ + ___ = {self.target_sum}'

            elif self.cards[y][x].num + self.selection1.num != self.target_sum or self.cards[y][x] not in self.adjacent_cards:
                self.cards[y][x].wrong = True
                self.cards[y][x].num = 0



display_width = 800
display_height = 1000

black = (10,10,30)
white = (255,255,255)
mark_colour = (48,16,42)
highlight_colour = (32,11,28)
error_colour = (245,15,60)
success_colour = (34,139,34)


screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Zahlenteppich')
clock = pygame.time.Clock()

#Background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)


end_of_game = False
board = Board()
while not end_of_game:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_of_game = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()[0]//80, pygame.mouse.get_pos()[1]//80
                board.click(pos[0], pos[1])

    
    screen.blit(background, (0,0))
    
    clock.tick(30)
    board.draw(screen)
    pygame.display.flip()

