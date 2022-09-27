import pygame
import sys
import pandas as pd
from copy import deepcopy
from random import choice
from Figure import *
from Color import Color

name_display = 'НАРУТО ТОП'
fon_tetris_default_path = 'img/back_tetris.png'
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]
pygame.init()
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

keyboard_arrow = {'down': pygame.K_DOWN,
                             'rotate': pygame.K_UP,
                             'left': pygame.K_LEFT,
                             'right': pygame.K_RIGHT}

keyboard_wasd = {'down': pygame.K_s,
                 'rotate': pygame.K_w,
                 'left': pygame.K_a,
                 'right': pygame.K_d}

clock = pygame.time.Clock()

class TetrisHandler:

    VALUES_CURRENT_FIGURE = 1
    VALUES_OCCUPIED_FIELD = -1
    VALUES_FREE_FIELD = 0

    def __init__(self, screen, x_coord=0, y_coord=0, width_field=300, height_field=600, width_cell=-1, height_cell=-1, count_block_to_width=10, keyboard_settings = keyboard_arrow,
                 count_block_height=20, fon_path=fon_tetris_default_path, file_record='records.csv',  FPS=60, name_player='Volodya', surname_player='Bugagash', fon_endgame='game_over.jpg'): # coordinates - take from left high cell

        self.screen = screen
        self.x_coord_field = x_coord
        self.y_coord_field = y_coord

        self.width_field = width_field
        self.height_field = height_field
        self.count_block_width = count_block_to_width
        self.count_block_height = count_block_height
        self.keyboard_settings = keyboard_settings
        if width_cell==-1 or height_cell==-1:
            self.width_cell, self.height_cell=width_field//self.count_block_width,height_field//self.count_block_height
        else:
            self.width_cell, self.height_cell = width_cell, height_cell#width_field//self.count_block_width,height_field//self.count_block_height

        self.__fon_path = fon_path
        self.is_pause = False
        self.is_lose = False

        self.__figure_rect = pygame.Rect(0, 0, self.width_cell - 2, self.height_cell - 2)

        self.__figures = [Figure(self.x_coord_field, self.y_coord_field,fig_pos, Color[i], self.width_cell, self.height_cell) for i, fig_pos in enumerate(figures_pos)]


        self.__full_lines = 0
        self.__score = 0

        self.figure, self.next_figure = self.get_figure(), self.get_figure()
        self.file_record = file_record

        self.width_menu = self.screen.get_width()-self.width_field
        self.height_menu = self.height_field
      #  self.x_coord_menu = self.x_coord_field+self.width_field
     #   self.y_coord_menu = self.y_coord_field
#        self.fon_menu_path = fon_menu_path

        self.is_break = False

        self.__speed = 80
        self.anim_count = 0
        self.anim_limit = 2000
        self.FPS = FPS
        self.name_player = name_player
        self.surname_player = surname_player
        self.game_over_image = pygame.image.load(fon_endgame)
        self.game_over_image = pygame.transform.scale(self.game_over_image, (self.width_field, self.height_field))
    def __size_square(self):
        return self.width_field//self.count_block_width, self.height_field//self.count_block_height
    def from_pixel_to_grid(self, pix_x, pix_y):
        return (self.x-self.x_coord)//self.count_block_width, (self.y-self.y_coord)//self.count_block_height
    def from_grid_to_pixel(self, grid_x, grid_y):
        width_cell, height_cell = self.__size_square()
        return self.x_coord_field+(grid_x*width_cell), self.y_coord_field+(grid_y*height_cell) #return coordinates left-down point

    def initialize(self):

        self.field = [[0 for i in range(self.count_block_width)] for j in range(self.count_block_height)]


        self.__fon = pygame.image.load(self.__fon_path)
        self.__fon = pygame.transform.scale(self.__fon, (self.width_field, self.height_field))
        self.screen.blit(self.__fon, (self.x_coord_field, self.y_coord_field))


        self.__draw_border()

        pygame.display.flip()



    def __draw_field(self, grid_x, grid_y):
        pygame.draw.rect(self.screen, self.COLOR_DICT[self.array_field[grid_x, grid_y]],
                         pygame.Rect(*self.from_grid_to_pixel(grid_x, grid_y), *self.__size_square()))
        pygame.display.flip()

    def __draw_border(self):
             for num_line,line in enumerate(self.field):
                 for num_col, cell in enumerate(line):
                    pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(*self.from_grid_to_pixel(num_col, num_line), self.width_cell, self.height_cell), width=1)

    def draw_all_field(self):
        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if col:
                    try:
                        self.__figure_rect.x, self.__figure_rect.y = self.from_grid_to_pixel(x, y)
                        pygame.draw.rect(self.screen, col, self.__figure_rect)
                    except:
                        continue

    def get_max_score(self):
        try:
            with open(self.file_record,'r') as file:
                records = pd.read_csv(self.file_record)
                idxmax = records['Score'].idxmax()
                result = records.iloc[idxmax].values
                if result[2]>self.__score:
                    return result[0]+' '+result[1]+': '+str(result[2])
                else:
                    return self.name_player+' '+self.surname_player+':'+str(self.__score)
        except:
            return self.__score

    def get_score(self):
        return self.__score
    def set_record(self):
        with open(self.file_record, 'a') as file:
            file.write('\n'+self.name_player+','+self.surname_player+','+str(self.__score))

    def get_figure(self):
        return  deepcopy(choice(list(self.__figures)))

    def draw_next_figure(self, x_coord, y_coord):
        figure_rect = deepcopy(self.__figure_rect)
        figure_rect.width = 2*self.__figure_rect.width//3
        figure_rect.height = 2 * self.__figure_rect.height// 3
        for i in range(4):
            figure_rect.x = self.next_figure[i].x * 2*self.width_cell//3 + x_coord
            figure_rect.y = self.next_figure[i].y * 2*self.height_cell//3 + y_coord  # +self.height_menu
            pygame.draw.rect(self.screen, self.next_figure.color, figure_rect)
       # pygame.display.flip()
    def draw_end_game(self):

        self.screen.blit(self.game_over_image, (self.x_coord_field, self.y_coord_field))
        pygame.display.flip()
    def check_borders(self, cell): # cell is element self.figure

        if cell.x < 0 or cell.x > self.count_block_width - 1:
            return False
        elif cell.y > self.count_block_height-1 or cell.y<0 or self.field[cell.y][cell.x]:
            return False
        return True
    def count_and_del_full_lines(self, anim_speed):
        line, lines = self.count_block_height - 1, 0

        for row in range(self.count_block_height - 1, -1, -1):
            count = 0
            for i in range(self.count_block_width):
                if self.field[row][i]:
                    count += 1
                self.field[line][i] = self.field[row][i]
            if count < self.count_block_width:
                line -= 1
            else:
                anim_speed += 30
                lines += 1
        return lines, anim_speed

    def score_by_deleted_lines(self, count_lines):
        return 2**count_lines

    def break_game(self):
        for i in range(self.count_block_width // 2 - 2, self.count_block_width // 2 + 2):
            try:
                if self.field[0][i] != 0:

                    return True
            except:

                return True
        return False

    def step(self, events):
        self.screen.blit(self.__fon, (self.x_coord_field, self.y_coord_field))


        self.__draw_border()
        dx, rotate, escape_pushed = 0, False, False
        for i in range(self.__full_lines):
            pygame.time.wait(200)
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == self.keyboard_settings['left']:
                    dx = -1
                    # print(dx)
                elif event.key == self.keyboard_settings['right']:
                    dx += 1
                    # print(dx)
                elif event.key == self.keyboard_settings['down']:
                    self.anim_limit = 40
                elif event.key == self.keyboard_settings['rotate']:
                    rotate = True
                elif event.key == pygame.K_ESCAPE:
                    escape_pushed = True

        if escape_pushed:
            pass
            #break

        if dx != 0:
            self.figure.move(dx, self.check_borders)

        self.anim_count += self.__speed
        if self.anim_count > self.anim_limit:
            self.anim_count = 0
            figure_old = deepcopy(self.figure)

            for i in range(4):
                self.figure[i].y += 1
                if not self.check_borders(self.figure[i]):
                    for i in range(4):
                        self.field[figure_old[i].y][figure_old[i].x] = self.figure.color

                    self.figure = self.next_figure
                    self.next_figure = self.get_figure()
                    self.anim_limit = 2000
                    break

        if rotate:
            self.figure.rotate(self.check_borders)

        lines, self.__speed = self.count_and_del_full_lines(self.__speed)

        if lines >= 1:

            self.__score += self.score_by_deleted_lines(lines)

        self.figure.draw_figure(self.screen)
      #  self.draw_next_figure()
        self.draw_all_field()


      #      break
        pygame.display.flip()

    def main(self):

        main_font = pygame.font.SysFont("arial", 28)
        font = pygame.font.SysFont('arial',20)

        title_tetris = main_font.render('TETRIS', True, pygame.Color('red'))
        escape_pushed=False
        while True:

            self.screen.blit(self.__fon, (self.x_coord_field, self.y_coord_field))
        #    self.screen.blit(self.__fon_menu, (self.x_coord_menu, self.y_coord_menu))
            self.screen.blit(title_tetris, (self.width_field + self.x_coord_field, 0))
#            self.screen.blit(font.render(f'Score:{self.__score}', True, pygame.Color('green')), (self.x_coord_menu, self.y_coord_menu+self.height_menu//2))
#            self.screen.blit(font.render(f'Best results:{self.get_max_score()}',True, pygame.Color('green')),(self.x_coord_menu, self.y_coord_menu+3*self.height_menu//4))
        #    self.screen.blit(font.render(f'{self.get_max_score()}',True, pygame.Color('green')),(self.x_coord_menu+self.width_menu//2, self.y_coord_menu+3.3*self.height_menu//4))
        #    self.screen.blit(font.render('Next figure',True, pygame.Color('green')),(self.x_coord_menu, self.y_coord_menu+self.height_menu//6))
            self.__draw_border()

            self.step(pygame.event.get())
            if self.break_game():
                self.set_record()
                break
            pygame.display.flip()
            clock.tick(self.FPS)


if __name__=='__main__':
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(name_display)
    pygame.mixer.music.load('soundtrack.mp3')
    pygame.mixer.music.play(-1)
    tetris1 = TetrisHandler(screen, 0,0, 300 , 600, keyboard_settings=keyboard_arrow)
    tetris2 = TetrisHandler(screen, 300,0, 300 , 600, keyboard_settings=keyboard_wasd)
    #tetris1.initialize()

   # for i in range(100000000):
        #tetris1.draw_pause_field()
    tetris1.main()
    # tetris2.initialize()
    # while True:
    #     event = pygame.event.get()
    #     if not tetris1.break_game():
    #         tetris1.step(event)
    #     else:
    #         tetris1.set_record()
    #         break
    #     if not tetris2.break_game():
    #         tetris2.step(event)
    #  #   tetris1.step(event)
    # #tetris.main()
    #     clock.tick(60)
