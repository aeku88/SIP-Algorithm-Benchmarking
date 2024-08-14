import threading, pygame
from utilities import colors


class Timer:
    def __init__(self, position, font_path='fonts/Montserrat-LightItalic.ttf'):
        self.current_time = 0
        self.position = position
        self.font_path = font_path

        self.should_stop = False
        self.timer_thread = threading.Thread(target=self.step, args=[])
        self.clock = pygame.time.Clock()
        self.start_time = 0
        self.text = None

    def start(self):
        self.timer_thread = threading.Thread(target=self.step, args=[])
        self.start_time = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks() - self.start_time
        self.should_stop = False
        self.timer_thread.start()

    def step(self):
        while True:
            if self.should_stop:
                break

            self.current_time = round((pygame.time.get_ticks() - self.start_time) / 1000, 2)
            self.clock.tick(60)

    def reset(self):
        self.timer_thread = threading.Thread(target=self.step, args=[])

    def draw(self, display_surface):
        font = pygame.font.Font(self.font_path, 18)
        if self.text is not None:
            display_surface.fill(colors.C_WHITE, pygame.Rect(self.position, self.text.get_rect().size))
        self.text = font.render("Runtime: " + str(round(self.current_time, 2)) + 's', True, colors.C_BLACK)
        display_surface.blit(self.text, self.position)

    def stop(self):
        if not self.should_stop:
            self.should_stop = True
            self.timer_thread.join()