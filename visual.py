import pygame
from pygame.locals import *
from game import MergeBricks
import numpy as np
import time

BACKGROUND = (30,30,30)
GRID = (200,200,200)

class App:
    def __init__(self):
        self.env = MergeBricks()
        self._running = True
        self._display_surf = None
        self.width  = 600
        self.px_offset = 20
        self.height = self.width+(self.width) // max(self.env.width, self.env.height)
        self.size=(self.width,self.height)
        
        self.color_dict = {}
        # Calculate the position to center the grid in the upper 2/3rd of the screen
        self.offset_x = int(self.px_offset/2)
        self.offset_y = int(self.px_offset/2)
        
        self.cell_size = (self.width - self.px_offset) // max(self.env.width, self.env.height)
        self.grid_size = self.cell_size * max(self.env.width, self.env.height)

        self.start_time = time.time()
        self.timer_stopped = False
        self.end_time = time.time()
        

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not self.env.end:
                mouse_x, mouse_y = event.pos
                grid_y = (mouse_x - self.offset_x) // self.cell_size
                grid_x = (mouse_y - self.offset_y) // self.cell_size

                # Ensure the coordinates are within the grid bounds
                if 0 <= grid_x < self.env.width and 0 <= grid_y < self.env.height:
                    print(f"Clicked on square at coordinates: ({grid_x}, {grid_y})")
            
                    self.env.step((grid_x,grid_y))
            
            

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill(BACKGROUND)  # White background
        self.draw_grid()  # Draw the grid
        self.draw_env()
        self.draw_details()
        if self.env.end:
            self.draw_end_screen()

        # Your existing game rendering code goes here

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def draw_grid(self):
        # Draw border
        pygame.draw.rect(self._display_surf, GRID, (self.offset_x, self.offset_y, self.grid_size, self.grid_size), 2)

        for x in range(self.offset_x, self.offset_x + self.grid_size, self.cell_size):
            pygame.draw.line(self._display_surf, GRID, (x, self.offset_y), (x, self.offset_y + self.grid_size), 1)

        for y in range(self.offset_y, self.offset_y + self.grid_size, self.cell_size):
            pygame.draw.line(self._display_surf, GRID, (self.offset_x, y), (self.offset_x + self.grid_size, y), 1)
    
    def draw_env(self):
        for y in range(self.env.height):
            for x in range(self.env.width):
                if self.env.world[y, x] == 0:
                    continue

                val = self.env.world[y, x]

                if val not in self.color_dict:
                    new_color = (np.random.randint(0, 256) for _ in range(3))
                    self.color_dict[val] = tuple(new_color)

                c = self.color_dict[val]

                rect_x = (self.offset_x + x * self.cell_size) + 10
                rect_y = (self.offset_y + y * self.cell_size) + 10

                pygame.draw.rect(self._display_surf, c, (rect_x, rect_y, self.cell_size - 20, self.cell_size - 20))

                font = pygame.font.Font(None, 36)
                val = int(val)
               # Render black text with a slight offset
                text_surface = font.render(str(val), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(rect_x + (self.cell_size - 20) // 2 + 2, rect_y + (self.cell_size - 20) // 2 + 2))
                self._display_surf.blit(text_surface, text_rect)
            
                # Render white text in the center
                text_surface = font.render(str(val), True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(rect_x + (self.cell_size - 20) // 2, rect_y + (self.cell_size - 20) // 2))
                self._display_surf.blit(text_surface, text_rect)
    
    def draw_details(self):
        # Draw user's score at the bottom center
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.env.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.width // 2, (5 * self.height // 6)+30))
        self._display_surf.blit(score_text, score_rect)

        # Draw timer under the score
        elapsed_time = int(time.time() - self.start_time) if not self.env.end else int(self.end_time - self.start_time)
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_text = font.render(f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(center=(self.width // 2, (11 * self.height // 12)+10))
        self._display_surf.blit(timer_text, timer_rect)

        # Draw rectangle of the next value at the bottom left
        next_value = self.env.next  # Assuming you have a method to get the next value
        if next_value is not None:
            next_rect_x = 10
            next_rect_y = 5 * self.height // 6
            next_rect_size = 50

            pygame.draw.rect(self._display_surf, (0, 0, 0), (next_rect_x, next_rect_y, next_rect_size, next_rect_size), 2)  # Black outline
            pygame.draw.rect(self._display_surf, self.color_dict[next_value], (next_rect_x + 2, next_rect_y + 2, next_rect_size - 4, next_rect_size - 4))

            # Draw text inside the rectangle
            next_text = font.render(str(next_value), True, (255, 255, 255))
            next_text_rect = next_text.get_rect(center=(next_rect_x + next_rect_size // 2, next_rect_y + next_rect_size // 2))
            self._display_surf.blit(next_text, next_text_rect)
            
    def draw_end_screen(self):
        # Stop the timer
        if not self.timer_stopped:
            self.timer_stopped = True
            self.end_time = time.time()
            self.e_time = self.end_time-self.start_time
            print(f"Game Over! Your final score is {self.env.score}. Time played: {self.e_time:.2f} seconds")

        # Draw dark gray rectangle over the entire screen with 70% opacity
        dark_gray = (50, 50, 50)
        end_screen_rect = pygame.Surface(self._display_surf.get_size(), pygame.SRCALPHA)
        end_screen_rect.fill((dark_gray[0], dark_gray[1], dark_gray[2], 178))  # 70% opacity
        self._display_surf.blit(end_screen_rect, (0, 0))

        # Display "END of GAME", user's score, and time played
        font = pygame.font.Font(None, 48)
        end_text = font.render("END of GAME", True, (255, 255, 255))
        score_text = font.render(f"Your final score: {self.env.score}", True, (255, 255, 255))
        time_text = font.render(f"Time played: {self.e_time:.2f} seconds", True, (255, 255, 255))

        end_rect = end_text.get_rect(center=(self.width // 2, self.height // 3))
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
        time_rect = time_text.get_rect(center=(self.width // 2, 2 * self.height // 3))

        self._display_surf.blit(end_text, end_rect)
        self._display_surf.blit(score_text, score_rect)
        self._display_surf.blit(time_text, time_rect)

        pygame.display.flip()  # Update the display
        


    def on_execute(self):
        clock = pygame.time.Clock()
        if self.on_init() is False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            clock.tick(60)
        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
