import pygame
import sys

# Initialisierung von Pygame
pygame.init()

# Bildschirmgröße
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialisierung des Bildschirms
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Shop")

# Laden der Schriftarten
font = pygame.font.SysFont(None, 30)

# Artikelklasse
class Item:
    def __init__(self, name, price, image):
        self.name = name
        self.price = price
        self.image = pygame.transform.scale(image, (150, 150))  # Skalieren Sie das Bild auf eine geeignete Größe
        self.rect = self.image.get_rect()

# Laden der Artikelbilder und erstellen der Artikelobjekte
def load_items():
    items = []
    item_files = [
        {"name": "item1", "price": 10, "image": "item1.png"},
        {"name": "item2", "price": 20, "image": "item2.png"},
        {"name": "item3", "price": 30, "image": "item3.png"},
        {"name": "item4", "price": 40, "image": "item4.png"},
        # Fügen Sie hier weitere Artikel hinzu
    ]

    for item_file in item_files:
        image = pygame.image.load(item_file["image"]).convert_alpha()
        item = Item(item_file["name"], item_file["price"], image)
        items.append(item)

    return items

# Lade die Anzahl der Eier aus der Datei
def load_eggs():
    with open("eggs_count.txt", "r") as file:
        eggs = int(file.read())
    return eggs

# Speichere die aktualisierte Anzahl der Eier in der Datei
def save_eggs(eggs):
    with open("eggs.txt", "w") as file:
        file.write(str(eggs))

# Hauptshop-Funktion
def shop():
    items = load_items()  # Artikel laden
    eggs = load_eggs()  # Eieranzahl laden

    while True:
        # Ereignisse überprüfen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Linke Maustaste
                    mouse_pos = pygame.mouse.get_pos()
                    for i, item in enumerate(items):
                        item_x = (SCREEN_WIDTH - item.rect.width * 2) // 3 * (i % 2 + 1) + item.rect.width * (i % 2)
                        item_y = (SCREEN_HEIGHT // 4) + (item.rect.height + 40) * (i // 2)

                        # Kaufschaltfläche überprüfen
                        buy_button = pygame.Rect(item_x, item_y + item.rect.height + 10 + font.get_height(), item.rect.width, 50)
                        if buy_button.collidepoint(mouse_pos):
                            if eggs >= item.price:
                                eggs -= item.price
                                save_eggs(eggs)  # Eieranzahl in der Datei speichern
                                print("Item '{}' gekauft!".format(item.name))
                            else:
                                print("Nicht genug Eier!")

        # Hintergrund löschen
        screen.fill(WHITE)

        # Eieranzahl anzeigen
        eggs_text = font.render("Eggs: {}".format(eggs), True, BLACK)
        screen.blit(eggs_text, (10, 10))

        # Artikel anzeigen
        for i, item in enumerate(items):
            item_x = (SCREEN_WIDTH - item.rect.width * 2) // 3 * (i % 2 + 1) + item.rect.width * (i % 2)
            item_y = (SCREEN_HEIGHT // 4) + (item.rect.height + 40) * (i // 2)

            # Bild anzeigen
            screen.blit(item.image, (item_x, item_y))

            # Name und Preis anzeigen
            name_text = font.render(item.name, True, BLACK)
            price_text = font.render("Price: {}".format(item.price), True, BLACK)
            screen.blit(name_text, (item_x, item_y + item.rect.height + 10))
            screen.blit(price_text, (item_x, item_y + item.rect.height + 10 + name_text.get_height()))

            # Kaufschaltfläche anzeigen
            buy_button = pygame.Rect(item_x, item_y + item.rect.height + 10 + name_text.get_height() + price_text.get_height(), item.rect.width, 50)
            pygame.draw.rect(screen, BLACK, buy_button)
            buy_text = font.render("Buy", True, WHITE)
            screen.blit(buy_text, (buy_button.centerx - buy_text.get_width() // 2, buy_button.centery - buy_text.get_height() // 2))

        pygame.display.flip()

# Shop aufrufen
shop()
