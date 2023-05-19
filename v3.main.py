import pygame
import os
import random
import pygame.mixer

# Initialisiere Pygame
pygame.init()

# Pygame-Mixer initialisieren
pygame.mixer.init()

# Einstellungen
hitbox = False
sound_volume = 0.5


# Pfad zum Ordner, in dem sich das Soundfile befindet
sounds_folder = os.path.join(os.getcwd(), 'sounds')

# Pfad zum Soundfile
score_sound_path = os.path.join(sounds_folder, 'score_sound.mp3')
backround_sound_path = os.path.join(sounds_folder, 'background_music.mp3')
powerup_sound_path = os.path.join(sounds_folder, 'powerup_sound.mp3')
button_sound_path = os.path.join(sounds_folder, 'button_sound.mp3')
game_over_sound_path = os.path.join(sounds_folder, 'game_over_sound.mp3')


# Lade Sounds
pygame.mixer.music.load(backround_sound_path)
score_sound = pygame.mixer.Sound(score_sound_path)
game_over_sound = pygame.mixer.Sound(game_over_sound_path)
powerup_sound = pygame.mixer.Sound(powerup_sound_path)
button_sound = pygame.mixer.Sound(button_sound_path)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(sound_volume)

#Lade Images
background_image_path = os.path.join('graphics', 'background_mountain.png')
background_clouds_image_path = os.path.join('graphics', 'background_clouds.png')
background_image = pygame.image.load(background_image_path)
background_clouds_image = pygame.image.load(background_clouds_image_path)

# Definiere Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Definiere Fenstergröße
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

# Geschwindigkeiten
comet_vel = 10
dino_speed = 10

# Hintergrund Scalieren
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Definiere die Hintergrund-Position
background_x = 0
background_y = 0

# Definiere die Hintergrund-Geschwindigkeit
background_speed = 0.5

# Definiere FPS
FPS = 60
clock = pygame.time.Clock()

# Definiere den Score
score = -1
font = pygame.font.Font(None, 36)

# Definiere den Dateipfad
highscore_file = "highscore.txt"
eggs_count_file = "eggs_count.txt"

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


# Lade den aktuellen Highscore aus der Datei
def load_eggs_count():
    if os.path.exists(eggs_count_file):
        with open(eggs_count_file, "r") as file:
            try:
                return int(file.read())
            except ValueError:
                return default_highscore
    else:
        return default_highscore

# Speichere den Highscore in der Datei
def save_eggs_count(eggs_count):
    with open(eggs_count_file, "w") as file:
        file.write(str(eggs_count))
        file.flush()
        file.close()

# Lade den aktuellen Highscore
highscore = load_highscore()

# Lade die Anzahl Eier
eggs_count = load_eggs_count()

# Definiere den Text für den Score
def draw_score():
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))

# Definiere den Text für den Score
def draw_eggs_count():
    text = font.render("Eggs: " + str(eggs_count), True, BLACK)
    screen.blit(text, (10, 35))

# Definiere den Text für das Powerup
def draw_speed_powerup_text():
    
    global timer

    # Zeige die verbleibende Zeit an
    rest_time = round(10 - timer / 1000, 1) 

    # Änder die Zeit Rot wenn man weniger als 3 sek hat
    if int(rest_time) <= 2:
        text_color = RED
    else:
        text_color = BLACK

    text1 = font.render("2x Speed ", True, BLACK)
    text2 = font.render(str(rest_time) + " sek", True, text_color)
    screen.blit(text1, (380, 10))
    screen.blit(text2, (380, 38))


def draw_protection_powerup_text():
    
    global timer

    # Zeige die verbleibende Zeit an
    rest_time = round(10 - timer / 1000, 1) 

    # Änder die Zeit Rot wenn man weniger als 3 sek hat
    if int(rest_time) <= 2:
        text_color = RED
    else:
        text_color = BLACK

    text1 = font.render("Protecion ", True, BLACK)
    text2 = font.render(str(rest_time) + " sek", True, text_color)
    screen.blit(text1, (380, 10))
    screen.blit(text2, (380, 38))


def draw_multiplier_powerup_text():
    
    global timer

    # Zeige die verbleibende Zeit an
    rest_time = round(10 - timer / 1000, 1) 

    # Änder die Zeit Rot wenn man weniger als 3 sek hat
    if int(rest_time) <= 2:
        text_color = RED
    else:
        text_color = BLACK

    text1 = font.render("2x Eggs ", True, BLACK)
    text2 = font.render(str(rest_time) + " sek", True, text_color)
    screen.blit(text1, (380, 10))
    screen.blit(text2, (380, 38))




# Erstelle das Fenster
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Like a Dino")

# Lade das Dinosaurier-Bild
dino_image_path = os.path.join('graphics', 'dino.png')
dino_image = pygame.image.load(dino_image_path)
dino_image = pygame.transform.scale(dino_image, (200, 200))


class Dino:
    def __init__(self, x, y, speed):
        self.image = dino_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = "right"

        # Erstelle separate Hitbox mit der gleichen Position wie der Dino
        self.hitbox1 = pygame.Rect(self.rect.x + 80, self.rect.y + 30, self.rect.width // 2 - 20, self.rect.height - 60)
        self.hitbox2 = pygame.Rect(self.rect.x - 30, self.rect.y + 140, self.rect.width // 2 - 60, self.rect.height - 170)

    def draw(self):
        if self.direction == "right":
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, (self.rect.x, self.rect.y))

        # Zeichne die Hitbox
        if hitbox:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox1, 2)
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox2, 2)

    def update(self):
        # Maustaste abrufen
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0]:  # Linke Maustaste gedrückt
            # Mausposition abrufen
            mouse_x, _ = pygame.mouse.get_pos()

            if mouse_x < SCREEN_WIDTH / 2:
                # Maus befindet sich auf der linken Seite des Bildschirms
                self.rect.x -= self.speed
                self.direction = "left"
                self.hitbox1.x = self.rect.x + 40
                self.hitbox2.x = self.rect.x + 120
            else:
                # Maus befindet sich auf der rechten Seite des Bildschirms
                self.rect.x += self.speed
                self.direction = "right"
                self.hitbox1.x = self.rect.x + 80
                self.hitbox2.x = self.rect.x + 40

            # Begrenzung der Dino-Bewegung auf den Bildschirmrand
            self.rect.x = max(20, min(self.rect.x, SCREEN_WIDTH - self.rect.width - 20))

            # Aktualisierung der Hitbox-Positionen
            if self.direction == "left":
                self.hitbox1.x = self.rect.x + 40
                self.hitbox2.x = self.rect.x + 120
            else:
                self.hitbox1.x = self.rect.x + 80
                self.hitbox2.x = self.rect.x + 40

        # Aktualisiere die Position der Hitbox
        self.hitbox1.y = self.rect.y + 30
        self.hitbox2.y = self.rect.y + 140

def draw_comet():
    # Definiere die Grösse des Komets
    random_size = random.randint(50, 100)
    comet_size = [random_size, random_size]

    # Lade das Kometen-Bild
    comet_image_path = os.path.join('graphics', 'comet.png')
    comet_image = pygame.image.load(comet_image_path)
    comet_image = pygame.transform.scale(comet_image, (comet_size))

    return comet_image

class Comet:
    def __init__(self, x, y, speed):
        self.image = comet_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # Zeichne die Hitbox
        if hitbox:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = 0


# Wähle eins der Powerups
def choose_powerup():
    print("test")
     # Liste der Power-Ups
    powerups = ["speed_power_up.png", "speed_power_up.png", "multiplier_power_up.png","protection_power_up.png"] 
    powerup = random.choice(powerups)  # Zufällige Auswahl eines Power-Ups
    return powerup

def draw_powerup():
    global selected_powerup
    # Definiere die Grösse des Powerups
    powerup_size = [50, 50]
    selected_powerup = choose_powerup()
    # Lade das Powerup-Bild
    powerup_image_path = os.path.join('graphics', selected_powerup)
    powerup_image = pygame.image.load(powerup_image_path)
    powerup_image = pygame.transform.scale(powerup_image, (powerup_size))

    return powerup_image

class Powerup:
    def __init__(self, x, y, speed):
        self.image = powerup_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # Zeichne die Hitbox
        if hitbox:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def update(self):
        self.rect.y += self.speed

powerup_active = False
powerup_timer = 0


def draw_egg():
    # Definiere die Grösse des Eis
    egg_size = [40, 50]

    # Lade das Ei-Bild
    egg_image_path = os.path.join('graphics', 'egg_image.png')
    egg_image = pygame.image.load(egg_image_path)
    egg_image = pygame.transform.scale(egg_image, (egg_size))

    return egg_image


class Egg:
    def __init__(self, x, y, speed):
        self.image = egg_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # Zeichne die Hitbox
        if hitbox:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def update(self):
        pass

# Erstelle den Dinosaurier, den Kometen und das Powerup und das Ei
comet_image = draw_comet()
egg_image = draw_egg()
comet = Comet(random.randint(0, SCREEN_WIDTH - comet_image.get_width()), 0, comet_vel)
dino = Dino(SCREEN_WIDTH / 2 - dino_image.get_width() / 2, SCREEN_HEIGHT - dino_image.get_height(), dino_speed)
egg = Egg(random.randint(0, SCREEN_WIDTH - egg_image.get_width()), SCREEN_HEIGHT - 80, comet_vel)
powerup_status = False


def update_powerup():
    powerup_image = draw_powerup()
    return powerup_image

powerup_image = update_powerup()
powerup = Powerup(random.randint(0, SCREEN_WIDTH - powerup_image.get_width()), 0, 7)




# Definiere Powerupstatus
multiplier_active = False
protection_active = False


# Definiere Powerup Interval
powerup_pr = [11000, 20000]
pr_value1 = powerup_pr[0]
pr_value2 = powerup_pr[1]
powerup_timer = 0
powerup_interval = random.randint(1000, pr_value2)
timer1 = 0


# Definiere Ei spawn Interval
egg_pr = [1000, 2000]
egg_value1 = egg_pr[0]
egg_value2 = egg_pr[1]
egg_timer = 0
egg_interval = random.randint(egg_value1, egg_value2)



# Reset das Ei

def reset_egg():
        global egg_timer, egg_interval, egg_invisible
        egg_invisible = False
        egg_timer = 0
        egg_interval = random.randint(egg_value1, egg_value2)           


def reset_game():

    global timer, powerup_status

    global powerup_timer 
    global powerup_interval
    powerup.rect.y = 0

    # Musik fortsetzen
    pygame.mixer.music.unpause()

    # Definiere Powerup Interval
    powerup_timer = 0
    powerup_interval = random.randint(1000, 10000)

    reset_egg()

    timer = 0
    dino.speed = dino_speed
    powerup_status = False

    dino.rect.x = SCREEN_WIDTH / 2 - dino_image.get_width() / 2
    dino.rect.y = SCREEN_HEIGHT - dino_image.get_height()
    comet.rect.x = random.randint(0, SCREEN_WIDTH - comet_image.get_width())
    comet.rect.y = 0
           

def update_screen():

    global background_x, background_y
    # Zeichne den Hintergrund
    screen.fill(WHITE)


    # Bewege den Hintergrund
    background_x -= background_speed

    # Zeichne den Hintergrund auf das Fenster
    screen.blit(background_clouds_image, (background_x, background_y))
    screen.blit(background_clouds_image, (background_x + SCREEN_WIDTH, background_y))
    screen.blit(background_image, (0, 0))
    screen.blit(background_image, (0, 0))


    # Überprüfe, ob der Hintergrund aus dem Fenster verschwunden ist
    if background_x <= -SCREEN_WIDTH:
        background_x = 0

    # Zeichne den Dinosaurier
    dino.draw()

    # Zeichne den Kometen
    comet.draw()

# Definiere den Game-Over-Bildschirm
def game_over():

    # Musik pausieren
    pygame.mixer.music.pause()

    # Text Font
    font = pygame.font.Font(None, 30)

    # Erstelle Text
    font1 = pygame.font.Font(None, 50)
    text = font1.render("Game Over", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 -30))

    # Zeige Text an
    #screen.fill(WHITE)
    screen.blit(text, text_rect)

    # Lade den aktuellen Highscore
    highscore = load_highscore()

    # Zeige den Highscore an
    highscore_text = font.render("Highscore: " + str(highscore), True, BLACK)
    highscore_rect = highscore_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
    screen.blit(highscore_text, highscore_rect)

    # Zeige den Score an
    highscore_text = font.render("Score: " + str(score), True, BLACK)
    highscore_rect = highscore_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 55))
    screen.blit(highscore_text, highscore_rect)

    # Zeige Restart-Button an
    restart_button = pygame.Rect(150, 500, 200, 100)
    pygame.draw.rect(screen, BLACK, restart_button)
    restart_text = font.render("Restart", True, WHITE)
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, restart_text_rect)

    # Zeige Start-Bildschirm-Button an
    start_screen_button = pygame.Rect(30, 30, 150, 50)
    pygame.draw.rect(screen, BLACK, start_screen_button)
    start_screen_text = font.render("Home", True, WHITE)
    start_screen_text_rect = start_screen_text.get_rect(center=start_screen_button.center)
    screen.blit(start_screen_text, start_screen_text_rect)

    # Aktualisiere das Fenster
    pygame.display.update()

    # Schleife für die Ereignisse
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                if restart_button.collidepoint(event.pos):
                    reset_game()
                    update_screen()
                    return
                    
                elif start_screen_button.collidepoint(event.pos):
                    reset_game()
                    start_screen()
                    return

def draw_hitbox_status():
    hitbox_text = font.render(f"Hitbox: {hitbox}", True, BLACK)
    hitbox_text_rect = hitbox_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    screen.blit(hitbox_text, hitbox_text_rect)

def start_screen():


    global hitbox, highscore
    # Text Font
    font = pygame.font.Font(None, 30)

    # Erstelle Text
    font1 = pygame.font.Font(None, 50)
    text = font1.render("Like a Dino", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))

    # Zeige Text an
    screen.fill(WHITE)
    screen.blit(text, text_rect)

    # Lade den aktuellen Highscore
    highscore = load_highscore()

    # Zeige Button an
    button = pygame.Rect(150, 500, 200, 70)
    pygame.draw.rect(screen, BLACK, button)
    text = font.render("Start", True, WHITE)
    text_rect = text.get_rect(center=button.center)
    screen.blit(text, text_rect)

    # Zeige den Egg count
    draw_eggs_count() 

    # Zeige den Highscore an
    highscore_text = font.render("Highscore: " + str(highscore), True, BLACK)
    highscore_rect = highscore_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
    screen.blit(highscore_text, highscore_rect)
 
    hitbox_button = pygame.Rect(150, 650, 200, 50)
    pygame.draw.rect(screen, BLACK, hitbox_button)
    start_screen_text = font.render(f"Hitbox: {hitbox}", True, WHITE)
    start_screen_text_rect = start_screen_text.get_rect(center=hitbox_button.center)
    screen.blit(start_screen_text, start_screen_text_rect)
        

    # Aktualisiere das Fenster
    pygame.display.update()

    # Schleife für die Ereignisse
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_sound.play()
                if button.collidepoint(event.pos):
                    reset_game()
                    return
                elif hitbox_button.collidepoint(event.pos):
            
                    hitbox = not hitbox  # Ändere den Wert der globalen hitbox-Variable
                    print(hitbox)

                        
collision_timer = 0  # Timer für die Kollisionsdauer   

egg_invisible = False

# Startbildschirm anzeigen
start_screen()

# Schleife für das Spiel
running = True
while running:

    # Erhöhe den Timer
    powerup_timer += clock.get_time()


    # Schleife für die Ereignisse
    for event in pygame.event.get():
        # Beenden, wenn das Fenster geschlossen wird
        if event.type == pygame.QUIT:
            running = False


    # Komet Kollesion mit Boden
    if comet.rect.y == 0:
        # Erhöhe Komet speed
        if comet_vel < 17:
            comet_vel += 0.2

        if score > 80 and comet_vel < 25:
            comet_vel += 0.1

        comet_image = draw_comet()
        comet = Comet(random.randint(0, SCREEN_WIDTH - comet_image.get_width()), 0, comet_vel)

        score += 1

    # Aktualisiere Highscore
    if score > highscore:
        highscore = score
        save_highscore(highscore)


    update_screen()

        

    # Überprüfe, ob die Zeit für das Zeichnen des Powerups erreicht ist
    if powerup_timer >= powerup_interval:
        # Zeichne das Powerup
        powerup.draw()
        # Aktualisiere das Powerup
        powerup.update()

    # Überprüfe, ob die Zeit für das Zeichnen des Eis erreicht ist
    egg.draw()

        
    if egg_timer >= egg_interval and egg_invisible == False:
        egg_invisible = True
        new_x = random.randint(0, SCREEN_WIDTH - egg_image.get_width())
        new_y = SCREEN_HEIGHT - 80

        # Überprüfe Kollision mit dem Spieler
        while dino.rect.collidepoint(new_x, new_y) or comet.rect.collidepoint(new_x, new_y):
            new_x = random.randint(0, SCREEN_WIDTH - egg_image.get_width())

        egg.rect.x = new_x
        egg.rect.y = new_y
    

    if egg_invisible == False:
        egg_timer += clock.get_time()
        egg.rect.x =   -80
        egg.rect.y = (SCREEN_HEIGHT - 80)


    # Überprüfe Powerup Kollesion mit Boden
    if powerup.rect.y > SCREEN_HEIGHT:
        print("test")
        powerup_image = update_powerup()
        powerup = Powerup(random.randint(0, SCREEN_WIDTH - powerup_image.get_width()), 0, 7)
        powerup.rect.x = random.randint(0, SCREEN_WIDTH - comet_image.get_width())
        powerup.rect.y = 0
        powerup_timer = 0
        powerup_interval = random.randint(1000, 6000)
        
 


    # Überprüfe auf Kollision mit Powerup
    if dino.hitbox1.colliderect(powerup.rect) or dino.hitbox2.colliderect(powerup.rect):
        powerup_sound.play()
        powerup_status = True
        powerup.rect.x = random.randint(0, SCREEN_WIDTH - comet_image.get_width())
        powerup.rect.y = 0
        powerup_timer = 0
        powerup_interval = random.randint(pr_value1, pr_value2)



    # Überprüfe auf Kollision mit Ei
    if dino.hitbox1.colliderect(egg.rect) or dino.hitbox2.colliderect(egg.rect):
        if collision_timer == 0:
            collision_timer = pygame.time.get_ticks()  # Starte den Timer bei der ersten Kollision
        
        if pygame.time.get_ticks() - collision_timer >= 100:  # Überprüfe, ob 500 ms vergangen sind
            #powerup_sound.play()
            if multiplier_active == True: 
                eggs_count += 3
            else:
                eggs_count += 1
            save_eggs_count(eggs_count)
            reset_egg()
            collision_timer = 0  # Setze den Timer zurück, um für die nächste Kollision zu starten

        

    # Überprüfe auf Kollision mit Ei und Comet
    if comet.rect.colliderect(egg.rect):
        game_over_sound.play()
        reset_egg()

    # Spawne Powerups
    if powerup_status == True:
        if selected_powerup == "speed_power_up.png":
            timer += clock.get_time()
            dino.speed = dino_speed * 2
            draw_speed_powerup_text()
 
        elif selected_powerup == "multiplier_power_up.png":
            multiplier_active = True
            timer += clock.get_time()
            draw_multiplier_powerup_text()
        else:
            protection_active = True
            timer += clock.get_time()
            draw_protection_powerup_text()

    
    if timer > 10000:
        # Wähle ein neues Powerup
        multiplier_active = False
        protection_active = False
        powerup_image = update_powerup()
        powerup = Powerup(random.randint(0, SCREEN_WIDTH - powerup_image.get_width()), 0, 7)
        timer = 0
        dino.speed = dino_speed
        powerup_status = False


    # Aktualisiere den Dinosaurier
    dino.update()

    # Aktualisiere den Kometen
    comet.update()



    # Überprüfe auf Kollision
    if dino.hitbox1.colliderect(comet.rect) or dino.hitbox2.colliderect(comet.rect):
        if protection_active == True:
            comet_image = draw_comet()
            comet = Comet(random.randint(0, SCREEN_WIDTH - comet_image.get_width()), 0, 7)
        else:
            game_over_sound.play()
            game_over()
            score = 0
            comet_vel = 10

    # Zeichne den Score
    draw_score()   


    # Aktualisiere das Fenster
    pygame.display.update()

    # Begrenze die Framerate
    clock.tick(FPS)

# Beende Pygame
pygame.quit()




