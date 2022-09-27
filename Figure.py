import pygame

from copy import deepcopy
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

class Figure:
    def __init__(self, x_coord, y_coord, fig_pos, color='red', width=15, height=15, init_position = (5,1)): #coord in grid
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.fig_pos = fig_pos
        self.color = color

        self.width = width
        self.height = height
        self.rects = [pygame.Rect(x + init_position[0], y + init_position[1], 1, 1) for x, y in fig_pos]
        self.figure_rect = pygame.Rect(0, 0, self.width - 2, self.height - 2)

    def __getitem__(self, item):
        return self.rects[item]

    def from_grid_to_pixel(self, grid_x, grid_y):
        return self.x_coord+(grid_x*self.width), self.y_coord+(grid_y*self.height) #return coordinates left-down point

    def move(self, action, check_border_func):
        figure_old = deepcopy(self.rects)
        for i in range(4):
            self.rects[i].x += action
            if not check_border_func(self.rects[i]):
                self.rects = deepcopy(figure_old)
                break

    def rotate(self, check_border_func):
        center = self.rects[0]
        figure_old = deepcopy(self.rects)
        for i in range(4):
            x = self.rects[i].y - center.y
            y = self.rects[i].x - center.x
            self.rects[i].x = center.x - x
            self.rects[i].y = center.y + y
            if not check_border_func(self.rects[i]):
                self.rects = deepcopy(figure_old)
                break

    def draw_figure(self, screen):
        for i in range(4):
            self.figure_rect.x, self.figure_rect.y = self.from_grid_to_pixel(self.rects[i].x, self.rects[i].y)

            pygame.draw.rect(screen, self.color, self.figure_rect)

if __name__=='__main__':
    pass