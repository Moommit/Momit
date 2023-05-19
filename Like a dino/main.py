import pygame
import os
import random
import pygame.mixer

# Initialisiere Pygame
pygame.init()

# Pygame-Mixer initialisieren
pygame.mixer.init()


# Pfad zum Ordner, in dem sich das Soundfile befindet
sounds_folder = os.path.join(os.getcwd(), 'sounds')

# Pfad zum Soundfile
score_sound_path = os.path.join(sounds_folder, 'score_sound.mp3')
backround_sound_path = os.path.join(sounds_folder,'background_music.mp3')
powerup_sound_path = os.path.join(sounds_folder, 'powerup_sound.mp3')
button_sound_path = os.path.join(sounds_folder, 'button_sound.mp3')
game_over_sound_path = os.path.join(sounds_folder, 'game_over_sound.mp3')


# Lade Sounds
pygame.mixer.music.load(backround_sound_path)
score_sound = pygame.mixer.Sound(score_sound_path)
game_over_sound = pygame.mixer.Sound(game_over_sound_path)
powerup_sound = pygame.mixer.Sound(powerup_sound_path)
button_sound = pygame.mixer.Sound(button_sound_path)

# Lade Sounds
pygame.mixer.music.play(-1)

# Definiere Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definiere Fenstergröße
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

comet_vel = 10

# Definiere FPS
FPS = 90
clock = pygame.time.Clock()

# Definiere den Score
score = -1
font = pygame.font.Font(None, 36)

# Definiere den Text für den Score
def draw_score():
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))

# Erstelle das Fenster
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Like a Dino")

# Lade das Dinosaurier-Bild
dino_image_path = os.path.join('graphics', 'dino.png')
dino_image = pygame.image.load(dino_image_path)
dino_image = pygame.transform.scale(dino_image, (200, 200))


def draw_comet():
    # Definiere die Grösse des Komets
    random_size = random.randint(40, 100)
    comet_size = [random_size, random_size]


    # Lade das Kometen-Bild
    comet_image_path = os.path.join('graphics', 'comet.png')
    comet_image = pygame.image.load(comet_image_path)
    comet_image = pygame.transform.scale(comet_image, (comet_size))

    return comet_image


class Dino:
    def __init__(self, x, y, speed):
        self.image = dino_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = "right"
        
    def draw(self):
        if self.direction == "right":
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, (self.rect.x, self.rect.y))
            
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
            self.direction = "left"
        elif keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.rect.width - 5:
            self.rect.x += self.speed
            self.direction = "right"
            
class Comet:
    def __init__(self, x, y, speed):
        self.comet_size = [70, 70]
        self.image = comet_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            
            self.rect.y = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            
# Erstelle den Dinosaurier und den Kometen
comet_image = draw_comet()
comet = Comet(random.randint(0, SCREEN_WIDTH - comet_image.get_width()), 0, comet_vel)
dino = Dino(SCREEN_WIDTH / 2 - dino_image.get_width() / 2, SCREEN_HEIGHT - dino_image.get_height(), 10)



def reset_game():
    dino.rect.x = SCREEN_WIDTH / 2 - dino_image.get_width() / 2
    dino.rect.y = SCREEN_HEIGHT - dino_image.get_height()
    comet.rect.x = random.randint(0, SCREEN_WIDTH - comet_image.get_width())
    comet.rect.y = 0
    comet_vel = 0


# Definiere den Game-Over-Bildschirm
def game_over():

    # Erstelle Text
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    # Zeige Text an
    screen.fill(WHITE)
    screen.blit(text, text_rect)

    # Zeige Button an
    button = pygame.Rect(150, 500, 200, 100)
    pygame.draw.rect(screen, BLACK, button)
    font = pygame.font.Font(None, 30)
    text = font.render("Resume", True, WHITE)
    text_rect = text.get_rect(center=button.center)
    screen.blit(text, text_rect)

    # Aktualisiere das Fenster
    pygame.display.update()

    # Schleife für die Ereignisse
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(event.pos):
                reset_game()
                return
            

# Schleife für das Spiel
running = True
while running:
    
    # Schleife für die Ereignisse
    for event in pygame.event.get():
        # Beenden, wenn das Fenster geschlossen wird
        if event.type == pygame.QUIT:
            running = False
    
    # Komet kollesion mit boden
    if comet.rect.y == 0:
        comet_image = draw_comet()
        comet = Comet(random.randint(0, SCREEN_WIDTH - comet_image.get_width()), 0, 10)
        comet.update()

        # Erhöhe Komet speed
        if comet_vel < 20:
            comet_vel += 2
        else:
            comet_vel = 30

        #score_sound.play()
        score += 1
        # Definiere die Grösse des Komets
        random_size = random.randint(40, 100)
        comet_size = [random_size, random_size]

    # Aktualisiere den Dinosaurier und den Kometen
    dino.update()
    comet.update()

    # Überprüfe Kollision zwischen Dino und Kometen
    if dino.rect.colliderect(comet.rect):
        # Setze den Score auf 0
        score = -1
        game_over_sound.play()
        game_over()

    # Zeichne den Dinosaurier und den Kometen
    screen.fill(WHITE)
    dino.draw()
    comet.draw()
    draw_score()

    # Aktualisiere das Fenster
    pygame.display.update()

    # Begrenze FPS
    pygame.time.Clock().tick(FPS)

# Beende Pygame
pygame.quit()
pygame.mixer.quit()


