import pygame, sys, subprocess, os
from button import Button
import Game

pygame.init()

info = pygame.display.Info()

# Set the screen dimensions based on the display information
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

# Create the game window
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

# Sets background and Size
BACKGROUND = pygame.image.load("assets/Alive.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/murder.ttf", size)

def play():
    python_executable = sys.executable
    subprocess.run([python_executable, "Game.py"])
    
alpha_value = 0 #the transparency of the label behind the text

def main_menu():
    while True:
        SCREEN.blit(BACKGROUND, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("", True, "#FF0000")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, 200))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png").convert_alpha(), pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90), 
                            text_input="PLAY", font=get_font(300), base_color="#d90d0d", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png").convert_alpha(), pos=(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2 + 300), 
                            text_input="QUIT", font=get_font(300), base_color="#d90d0d", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        PLAY_BUTTON.image.set_alpha(alpha_value)
        QUIT_BUTTON.image.set_alpha(alpha_value)
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()