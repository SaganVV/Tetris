from TetrisHandler import *
from tkinter import *

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
clock = pygame.time.Clock()



class Tetris:
    def __init__(self, width, height, name1, surname1, name2='', surname2=''):
        self.width = width
        self.height = height
        self.name1 = name1
        self.surname1 = surname1
        self.name2 = name2
        self.surname2 = surname2
    def two_player_game(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('TETRIS')
        tetris1 = TetrisHandler(self.screen, x_coord=self.width//6, y_coord=0, width_field= self.width // 3,
                                    height_field=self.height, width_cell=-1, height_cell=-1, count_block_to_width=10,
                                    keyboard_settings=keyboard_wasd,
                                    count_block_height=20, fon_path=fon_tetris_default_path, file_record='records.csv',
                                    FPS=60, name_player=self.name1, surname_player=self.surname1)

        tetris2 = TetrisHandler(self.screen, x_coord=self.width//2, y_coord=0, width_field=self.width // 3,
                                    height_field=self.height, width_cell=-1, height_cell=-1, count_block_to_width=10,
                                    keyboard_settings=keyboard_arrow,
                                    count_block_height=20, fon_path=fon_tetris_default_path, file_record='records.csv',
                                    FPS=60, name_player=self.name2, surname_player=self.surname2)
        tetris1.initialize()
        tetris2.initialize()
        self.is_paused = False

        # pygame.mixer.music.load('soundtrack.mp3')
        # pygame.mixer.music.play(-1)

        main_font = pygame.font.SysFont('arial', 35)
        font = pygame.font.SysFont('arial', 12)
        fon_menu = pygame.image.load('fon_for_menu2.jpg')
        fon_menu = pygame.transform.scale(fon_menu, (self.width // 6, self.height))
        title_tetris = main_font.render('TETRIS', True, pygame.Color('red'))
        while True:

            self.screen.blit(fon_menu, (0, 0))
            self.screen.blit(fon_menu, (5*self.width//6, 0))
            # self.screen.blit(title_tetris, (self.tetris.width_field + self.tetris.x_coord_field, 0))
            self.screen.blit(font.render(f'Score:{tetris1.get_score()}', True, pygame.Color('green')),
                              (0, tetris1.y_coord_field + self.height // 2))
            self.screen.blit(font.render(f'Name:{tetris1.name_player} {tetris1.surname_player}', True, pygame.Color('green')),
                              (0, tetris1.y_coord_field + self.height // 2-20))
            self.screen.blit(font.render(f'Score:{tetris2.get_score()}', True, pygame.Color('green')),
                              (5*self.width//6, tetris2.y_coord_field + self.height // 2))
            self.screen.blit(font.render(f'Name:{tetris2.name_player} {tetris2.surname_player}', True, pygame.Color('green')),
                              (5*self.width//6, tetris2.y_coord_field + self.height // 2-20))
            # #    self.screen.blit()
            self.screen.blit(font.render(f'Best results:', True, pygame.Color('green')),
                              (0,
                               tetris1.y_coord_field + 2 * self.height // 3))
            self.screen.blit(font.render(f'Best results:', True, pygame.Color('green')),
                              (tetris2.x_coord_field + self.width // 3,
                               tetris2.y_coord_field + 2 * self.height // 3))
            self.screen.blit(font.render(f'{tetris1.get_max_score()}', True, pygame.Color('green')),
                              (0,
                               tetris1.y_coord_field + 2 * self.height // 3 + 10))
            self.screen.blit(font.render(f'{tetris1.get_max_score()}', True, pygame.Color('green')),
                              (tetris2.x_coord_field + self.width // 3,
                               tetris2.y_coord_field + 2 * self.height // 3 + 10))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_paused = not self.is_paused

            if not self.is_paused:

                if not tetris1.break_game():
                    tetris1.draw_next_figure(10 , 3 * self.height // 13)
                    tetris1.step(events)
                else:


                    tetris1.draw_end_game()

                if not tetris2.break_game():
                    tetris2.draw_next_figure(5*self.width//6, 3 * self.height // 13)
                    tetris2.step(events)
                else:

                    tetris2.draw_end_game()
                if tetris1.break_game() and tetris2.break_game():
                    tetris1.set_record()
                    tetris1.draw_end_game()
                    tetris2.set_record()
                    tetris2.draw_end_game()
                    break
            pygame.display.flip()
            clock.tick((tetris1.FPS+tetris2.FPS)//2)
        need_kill_window = False
        main_font = pygame.font.SysFont("arial", 60)
        if tetris1.get_score()>tetris2.get_score():
            self.screen.blit(font.render(f'Win {tetris1.name_player} {tetris1.surname_player} with score {tetris1.get_score()}', True, pygame.Color('blue')), (self.width//2, self.height//2))
        else:
            self.screen.blit(
                font.render(f'Win {tetris2.name_player} {tetris2.surname_player} with score {tetris2.get_score()}',
                            True, pygame.Color('blue')), (self.width // 2, self.height // 2))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        need_kill_window = True
            if need_kill_window:
                break


            clock.tick((tetris1.FPS+tetris2.FPS)//2)
        name1 = self.name1
        surname1 = self.surname1
        name2 = self.name2
        surname2 = self.surname2
        del self
        pygame.display.quit()
        pygame.mixer.music.stop()
        Menu(500,500).menu(Tetris(800, 750, name1, surname1, name2, surname2))
    def one_player_game(self):

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('TETRIS')
        tetris = TetrisHandler(self.screen, x_coord=0, y_coord=0, width_field=2*self.width//3, height_field=self.height, width_cell=-1, height_cell=-1, count_block_to_width=10, keyboard_settings = keyboard_arrow,
                 count_block_height=20, fon_path=fon_tetris_default_path, file_record='records.csv', FPS=60, name_player=self.name1, surname_player=self.surname1)
        tetris.initialize()
        self.is_paused = False

        # pygame.mixer.music.load('soundtrack.mp3')
        # pygame.mixer.music.play(-1)

        main_font = pygame.font.SysFont('arial', 35)
        font = pygame.font.SysFont('arial', 15)
        fon_menu = pygame.image.load('fon_for_menu2.jpg')
        fon_menu = pygame.transform.scale(fon_menu, (self.width//3, self.height))
        title_tetris = main_font.render('TETRIS', True, pygame.Color('red'))
        while True:

            self.screen.blit(fon_menu, (2*self.width//3, 0))
            self.screen.blit(title_tetris, (tetris.width_field + tetris.x_coord_field, 0))
            self.screen.blit(font.render(f'Score:{tetris.get_score()}', True, pygame.Color('green')),
                              (tetris.x_coord_field+2*self.width//3, tetris.y_coord_field+self.height // 2))
        #    self.screen.blit()
            self.screen.blit(font.render(f'Best results:',  True, pygame.Color('green')),
                             (tetris.x_coord_field+2*self.width//3,tetris.y_coord_field+2*self.height // 3))
            self.screen.blit(font.render(f'{tetris.get_max_score()}', True, pygame.Color('green')),
                             (tetris.x_coord_field+2*self.width//3,tetris.y_coord_field+2*self.height // 3+10))
            self.screen.blit(font.render(f'Name:{tetris.name_player} {tetris.surname_player}', True, pygame.Color('green')),
                              (2*self.width//3, tetris.y_coord_field + self.height // 2-20))


            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_paused = not self.is_paused

            if not self.is_paused:

                if not tetris.break_game():
                    tetris.draw_next_figure(self.width // 2+40, 3*self.height // 13)
                    tetris.step(events)

                else:

                    tetris.set_record()
                    tetris.draw_end_game()
                    break
            pygame.display.flip()
            clock.tick(tetris.FPS)

        need_kill_window = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        need_kill_window = True
            if need_kill_window:
                break


            clock.tick(tetris.FPS)
        name1 = self.name1
        surname1 = self.surname1
        name2 = self.name2
        surname2 = self.surname2
        del self
        pygame.display.quit()
        pygame.mixer.music.stop()
        Menu(500,500).menu(Tetris(800, 750, name1, surname1, name2, surname2))
class Menu(Tk):
        def __init__(self, width_window, height_window):
            super().__init__()
            self.width = width_window
            self.height = height_window
            self.geometry(f'{width_window}x{height_window}')
        def menu(self, tetris):
            def one_player():

            #    self.registration_menu(tetris)
                self.destroy()
                tetris.one_player_game()
            def two_player():
                self.destroy()
              #  self.registration_menu(tetris)
                tetris.two_player_game()
            but_play_one = Button(self, text="1 Player mode",
                                           bg='red', command=one_player)
            width_button = self.width//2
            height_button = 40
            but_play_one.place(x=self.width//2-width_button//2, y=20, width=width_button, height=height_button)
            but_player_2 = Button(self, text="2 Player mode",
                                           bg='red', command=two_player)
            but_player_2.place(x=self.width // 2 - width_button // 2, y=100, width=width_button, height=height_button)

class RegistrationForm(Tk):
    def __init__(self, width_window, height_window):
        super().__init__()
        self.width = width_window
        self.height = height_window
        self.geometry(f'{width_window}x{height_window}')
    def form(self):
        def get_text():
            name = name_entry.get()
            surname = surname_entry.get()
            self.destroy()
            Menu(self.width, self.height).menu(Tetris(800,750, name, surname, name, surname))

        label_name = Label(text="Name: ", fg="#eee", bg="#333")
        label_name.place(x=self.width//2-50, y=100)
        name_entry = Entry(self)
        name_entry.place(x=self.width//2, y=100, width=150, height=20)

        label_surname = Label(text="Surname: ", fg="#eee", bg="#333")
        label_surname.place(x=self.width // 2 - 60, y=200, height=20)
        surname_entry = Entry(self)
        surname_entry.place(x=self.width//2, y=200, width=150, height=20)
        apply = Button(self, text="Apply",
                                           bg='red', command=get_text)
        apply.place(x=3*self.width//4, y=3*self.height//4, width=40, height=20)
if __name__=='__main__':
    # app = Menu(500, 500)
    # #app.registration_menu(Tetris(800, 500))
    # app.menu(Tetris(800, 750))
    # app.mainloop()
    reg = RegistrationForm(500,500)
    reg.form()
    reg.mainloop()