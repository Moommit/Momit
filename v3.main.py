import pygame
import os
import random
import pygame.mixer

# Initialisiere Pygame
pygame.init()

# Pygame-Mixer initialisieren
pygame.mixer.init()

# Lade Sounds
pygame.mixer.music.load('background_music.mp3')
score_sound = pygame.mixer.Sound('score_sound.mp3')
game_over_sound = pygame.mixer.Sound('game_over_sound.mp3')
pygame.mixer.music.play(-1)

# Definiere Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definiere Fenstergröße
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

comet_vel = 10

# Definiere FPS
FPS = 60
clock = pygame.time.Clock()

# Definiere den Score
score = -1
font = pygame.font.Font(None, 36)

# Definiere den Highscore-Dateipfad
highscore_file = "highscore.txt"

# Definiere die Standard-Highscore-Wert
default_highscore = 0

# Lade den aktuellen Highscore aus der Datei
def load_highscore():
    if os.path.exists(highscore_file):
        with open(highscore_file, "r") as file:
            try:
                return int(file.read())
            except ValueError:
                return default_highscore
    else:
        return default_highscore

# Speichere den Highscore in der Datei
def save_highscore(highscore):
    with open(highscore_file, "w") as file:
        file.write(str(highscore))
        file.flush()
        file.close()

# Lade den aktuellen Highscore
highscore = load_highscore()

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
            pass
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
    


# Definiere den Game-Over-Bildschirm
def game_over():

    # Text Font
    font = pygame.font.Font(None, 30)

    # Erstelle Text
    font1 = pygame.font.Font(None, 50)
    text = font1.render("Game Over", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    # Zeige Text an
    screen.fill(WHITE)
    screen.blit(text, text_rect)

    # Lade den aktuellen Highscore
    highscore = load_highscore()

    # Zeige den Highscore an
    highscore_text = font.render("Highscore: " + str(highscore), True, BLACK)
    highscore_rect = highscore_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
    screen.blit(highscore_text, highscore_rect)

    # Zeige Button an
    button = pygame.Rect(150, 500, 200, 100)
    pygame.draw.rect(screen, BLACK, button)
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
        # Erhöhe Komet speed
        if comet_vel < 20:
            comet_vel += 0.2

        else:
            comet_vel = 20

        # Definiere die Grösse des Komets
        #random_size = random.randint(40, 100)
        #comet_size = [random_size, random_size]

        comet_image = draw_comet()
        comet = Comet(random.randint(0, SCREEN_WIDTH - comet_image.get_width()), 0, comet_vel)
        
        
        #score_sound.play()
        score += 1

    # Aktualisiere Highscore 

    if score > highscore:
        highscore = score
        save_highscore(highscore)

    # Aktualisiere den Dinosaurier und den Kometen
    dino.update()
    comet.update()

    # Überprüfe Kollision zwischen Dino und Kometen
    if dino.rect.colliderect(comet.rect):
        # Setze den Score auf 0
        comet_vel = 10
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



