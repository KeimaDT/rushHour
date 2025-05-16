import pygame
import sys
import copy  # Pour effectuer des copies profondes

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600  # Fenêtre de 800x600
GRID_SIZE = 8  # Taille de la grille 8x8
GRID_WIDTH = 600  # Taille de la grille en pixels
CELL_SIZE = GRID_WIDTH // GRID_SIZE  # Taille d'une cellule
BUTTON_AREA_WIDTH = WIDTH - GRID_WIDTH  # Espace pour les boutons

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BROWN = (139, 69, 19)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
LIME = (50, 205, 50)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
NAVY = (0, 0, 128)
TEAL = (0, 128, 128)
OLIVE = (128, 128, 0)
MAROON = (128, 0, 0)
INDIGO = (75, 0, 130)
VIOLET = (238, 130, 238)
TURQUOISE = (64, 224, 208)
BEIGE = (245, 245, 220)
SALMON = (250, 128, 114)
CHOCOLATE = (210, 105, 30)


# Définition des boutons
BUTTON_WIDTH = 180
BUTTON_HEIGHT = 50
BUTTON_X = GRID_WIDTH + (BUTTON_AREA_WIDTH - BUTTON_WIDTH) // 2
buttons = [
    pygame.Rect(BUTTON_X, 50 + i * 70, BUTTON_WIDTH, BUTTON_HEIGHT) for i in range(5)
]
button_texts = ["Easy", "Medium", "Hard", "Reset", "Solution"]

# Paramètres de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rush Hour")

def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect_x = x * CELL_SIZE
            rect_y = y * CELL_SIZE
            color = GRAY if (x == 0 or x == GRID_SIZE - 1 or y == 0 or y == GRID_SIZE - 1) and not (x == 7 and y == 3) else WHITE
            pygame.draw.rect(screen, color, (rect_x, rect_y, CELL_SIZE, CELL_SIZE))

    for x in range(0, GRID_WIDTH + 1, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, GRID_WIDTH))
    for y in range(0, GRID_WIDTH + 1, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (GRID_WIDTH, y))

class Vehicle:
    def __init__(self, name, x, y, width, height, orientation, color):
        self.name = name  # Nom unique du véhicule
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.orientation = orientation
        self.color = color
        self.selected = False
        
    def draw(self):
        """ Dessine le véhicule sur l'écran """
        # Rectangle principal (fond)
        pygame.draw.rect(screen, self.color, (self.x * CELL_SIZE, self.y * CELL_SIZE, self.width * CELL_SIZE, self.height * CELL_SIZE))
    
        # Bordure intérieure si sélectionné
        if self.selected:
            border_thickness = 3  # Épaisseur intérieure
            pygame.draw.rect(
                screen,
                (0, 0, 0),  # Noir
                (self.x * CELL_SIZE, self.y * CELL_SIZE, self.width * CELL_SIZE, self.height * CELL_SIZE),
                width=border_thickness
            )

    def move(self, dx, dy, other_cars):
        """ Déplace le véhicule dans la direction spécifiée (avant ou arrière) """
        
        if not self.is_position_valid(dx, dy, other_cars):
            return

        if self.orientation == "h" and dx != 0:
            self.x += dx
        elif self.orientation == "v" and dy != 0:
            self.y += dy
    
    def is_position_valid(self, dx, dy, other_cars):
        """ Vérifie si le véhicule peut se déplacer sans entrer en collision avec d'autres véhicules. """
        new_x = self.x + dx
        new_y = self.y + dy

        for i in range(self.width):
            for j in range(self.height):
                check_x = new_x + i
                check_y = new_y + j

                if (check_x, check_y) == (7, 3):
                    continue

                if check_x == 0 or check_x == GRID_SIZE - 1 or check_y == 0 or check_y == GRID_SIZE - 1:
                    return False

                for other_car in other_cars:
                    for i2 in range(other_car.width):
                        for j2 in range(other_car.height):
                            if (check_x, check_y) == (other_car.x + i2, other_car.y + j2):
                                return False

        return True

class Car(Vehicle):
    def __init__(self, name, x, y, orientation, color):
        width = 2
        height = 1
        if orientation == "v":
            width, height = height, width
        super().__init__(name, x, y, width, height, orientation, color)

class Truck(Vehicle):
    def __init__(self, name, x, y, orientation, color):
        width = 3
        height = 1
        if orientation == "v":
            width, height = height, width
        super().__init__(name, x, y, width, height, orientation, color)

class RedCar(Car):
    def __init__(self, x, y, orientation, color):
        super().__init__("red", x, y, orientation, color)
    
    def has_reached_exit(self):
        return self.x == 7 and self.y == 3

    
cars1 = [
    RedCar(1, 3, 'h', RED),
    Car("blue", 5, 1, 'h', BLUE),
    Truck("yellow", 3, 1, 'v', YELLOW),
    Truck("green", 6, 4, 'v', GREEN),
    Truck("orange", 1, 4, 'h', ORANGE),
]

cars2 = [
    RedCar(1, 3, 'h', RED),
    Car("blue", 4, 1, 'v', BLUE),
    Car("green", 6, 1, 'v', GREEN),
    Car("orange", 6, 3, 'v', ORANGE),
    Car("purple", 4, 4, 'h', PURPLE),
    Car("pink", 2, 6, 'h', PINK),
    Car("brown", 5, 5, 'v', BROWN),
    Truck("cyan", 1, 1, 'h', CYAN),
    Truck("magenta", 1, 5, 'h', MAGENTA),
    Truck("lime", 3, 2, 'v', LIME),
]

cars3 = [
    RedCar(2, 3, 'h', RED),
    Car("blue", 1, 1, 'h', BLUE),
    Car("green", 3, 1, 'v', GREEN),
    Car("orange", 1, 6, 'h', ORANGE),
    Car("purple", 5, 5, 'v', PURPLE),
    Car("pink", 6, 5, 'v', PINK),
    Truck("brown", 1, 2, 'v', BROWN),
    Truck("cyan", 1, 5, 'h', CYAN),
    Truck("magenta", 4, 4, 'h', MAGENTA),
    Truck("lime", 4, 1, 'v', LIME),
]


# Listes de données en jeu (modifiables)
cars1_data = copy.deepcopy(cars1)
cars2_data = copy.deepcopy(cars2)
cars3_data = copy.deepcopy(cars3)

cars = []
reset = 0
selected_car = None # Variable pour la voiture sélectionnée

# Liste des mouvements à exécuter pour la solution
moves1 = [
    ("blue", "left", 1),
    ("green", "up", 3),
    ("orange", "right", 3),
    ("yellow", "down", 3),
    ("red", "right", 3),
    ("yellow", "up", 3),
    ("orange", "left", 1),
    ("green", "down", 3),
    ("red", "right", 3)
]

moves2 = [
    ("orange", "down", 2),
    ("green", "down", 2),
    ("blue", "down", 1),
    ("cyan", "right", 3),
    ("lime", "up", 1),
    ("purple", "left", 3),
    ("lime", "down", 1),
    ("cyan", "left", 3),
    ("blue", "up", 1),
    ("green", "up", 2),
    ("brown", "up", 4),
    ("orange", "up", 2),
    ("magenta", "right", 3),
    ("pink", "left", 1),
    ("lime", "down", 2),
    ("red", "right", 3),
    ("lime", "up", 2),
    ("magenta", "left", 1),
    ("orange", "down", 1),
    ("red", "right", 3)
]

moves3 = [
    ("magenta", "left", 2),
    ("pink", "up", 4),
    ("purple", "up", 4),
    ("orange", "right", 4),
    ("magenta", "right", 2),
    ("cyan", "right", 3),
    ("orange", "right", 3),
    ("brown", "down", 2),
    ("red", "left", 1),
    ("green", "down", 4),
    ("red", "right", 1),
    ("blue", "right", 1),
    ("brown", "up", 3),
    ("magenta", "left", 3),
    ("lime", "down", 1),
    ("purple", "down", 1),
    ("pink", "down", 1),
    ("blue", "right", 3),
    ("lime", "up", 1),
    ("magenta", "right", 3),
    ("brown", "down", 3),
    ("red", "left", 1),
    ("green", "up", 4),
    ("red", "right", 1),
    ("brown", "up", 3),
    ("magenta", "left", 3),
    ("cyan", "left", 3),
    ("lime", "down", 3),
    ("pink", "down", 2),
    ("purple", "down", 2),
    ("red", "right", 5)
]

# Fonction pour vérifier si l'utilisateur clique sur une voiture
def check_car_click(x, y):
    global selected_car
    for car in cars:
        if car.x <= x < car.x + car.width and car.y <= y < car.y + car.height:
            selected_car = car  # Sélectionner la voiture
            car.selected = True
        else:
            car.selected = False  # Deselect the car if it's not clicked

def draw_buttons():
    """Affiche les boutons sur la partie droite de l'écran."""
    font = pygame.font.Font(None, 36)
    for i, button in enumerate(buttons):
        pygame.draw.rect(screen, LIGHT_GRAY, button)
        pygame.draw.rect(screen, BLACK, button, 2)
        text = font.render(button_texts[i], True, BLACK)
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)

def move_car(name, direction, steps):
    global selected_car
    for car in cars:
        if car.name == name:
            # Sélectionner la voiture (comme si elle était cliquée)
            selected_car = car
            for c in cars:
                c.selected = (c == car)

            for _ in range(steps):
                other_cars = [c for c in cars if c != car]
                if direction == 'up':
                    car.move(0, -1, other_cars)
                elif direction == 'down':
                    car.move(0, 1, other_cars)
                elif direction == 'left':
                    car.move(-1, 0, other_cars)
                elif direction == 'right':
                    car.move(1, 0, other_cars)

            break


def handle_button_click(index):
    global cars, selected_car, reset, cars1_data, cars2_data, cars3_data

    if index == 0:  # Easy
        reset = 1
        cars = cars1_data  # On récupère la progression
        selected_car = None

    elif index == 1:  # Medium
        reset = 2
        cars = cars2_data
        selected_car = None

    elif index == 2:  # Hard
        reset = 3
        cars = cars3_data
        selected_car = None

    elif index == 3:  # Reset du niveau courant
        selected_car = None
        if reset == 1:
            cars1_data = copy.deepcopy(cars1)
            cars = cars1_data
        elif reset == 2:
            cars2_data = copy.deepcopy(cars2)
            cars = cars2_data
        elif reset == 3:
            cars3_data = copy.deepcopy(cars3)
            cars = cars3_data
            
    elif index == 4:  # Solution bouton
        moves = []
        if reset == 1:
            moves = moves1
            
        if reset == 2:
            moves = moves2
            
        if reset == 3:
            moves = moves3
        
        handle_button_click(3)
        selected_car = None
    
        for name, direction, steps in moves:
            for _ in range(steps):
                # Déplacement étape par étape
                for car in cars:
                    if car.name == name:
                        dx, dy = 0, 0
                        if direction == 'up':
                            dy = -1
                        elif direction == 'down':
                            dy = 1
                        elif direction == 'left':
                            dx = -1
                        elif direction == 'right':
                            dx = 1
                        car.move(dx, dy, [c for c in cars if c != car])
                        break

                # Affichage et pause après chaque mouvement
                screen.fill(WHITE)
                draw_grid()
                draw_buttons()
                for c in cars:
                    c.draw()
                pygame.display.update()
                pygame.time.delay(100)  # 300 ms de pause entre chaque déplacement

def show_victory_screen():
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 48)

    while True:
        screen.fill((200, 255, 200))  # Fond vert clair

        # Texte de victoire
        text = font.render("Victory !", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(text, text_rect)

        # Bouton "Play Again"
        play_again_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 60)
        pygame.draw.rect(screen, (100, 200, 100), play_again_rect)
        play_again_text = small_font.render("Play Again", True, (0, 0, 0))
        screen.blit(play_again_text, play_again_text.get_rect(center=play_again_rect.center))

        # Bouton "Exit"
        exit_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 80, 300, 60)
        pygame.draw.rect(screen, (200, 100, 100), exit_rect)
        exit_text = small_font.render("Exit", True, (0, 0, 0))
        screen.blit(exit_text, exit_text.get_rect(center=exit_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    return "restart"
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def main():
    global game_won
    clock = pygame.time.Clock()

    running = True
    selected_car = None  # Aucune voiture sélectionnée au début

    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_buttons()

        # Dessiner toutes les voitures
        for car in cars:
            car.draw()  # Appeler la méthode draw() de chaque voiture

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifie si une voiture a été cliquée
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for car in cars:
                    if car.x * CELL_SIZE <= mouse_x < (car.x + car.width) * CELL_SIZE and \
                       car.y * CELL_SIZE <= mouse_y < (car.y + car.height) * CELL_SIZE:
                        # Désélectionner la voiture précédente si elle existe
                        if selected_car:
                            selected_car.selected = False
                        # Sélectionner la voiture cliquée
                        selected_car = car
                        car.selected = True  # Marquer la voiture comme sélectionnée
                        break
                
                for i, button in enumerate(buttons):
                    if button.collidepoint(mouse_x, mouse_y):
                        handle_button_click(i)

            if event.type == pygame.KEYDOWN and selected_car:
                # Gérer les déplacements avec les touches fléchées ou ZQSD
                other_cars = [car for car in cars if car != selected_car]  # Liste des autres voitures
                if event.key == pygame.K_UP or event.key == pygame.K_z:  # Haut (Z ou Flèche Haut)
                    selected_car.move(0, -1, other_cars)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:  # Bas (S ou Flèche Bas)
                    selected_car.move(0, 1, other_cars)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_q:  # Gauche (Q ou Flèche Gauche)
                    selected_car.move(-1, 0, other_cars)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # Droite (D ou Flèche Droite)
                    selected_car.move(1, 0, other_cars)
        
        # Vérifie si la RedCar a atteint la sortie après chaque déplacement
        red_car = next((car for car in cars if isinstance(car, RedCar)), None)
        if red_car and red_car.has_reached_exit():
            print("La voiture rouge a atteint la sortie ! Vous avez gagné.")
            result = show_victory_screen()
            if result == "restart":
                handle_button_click(3)
                main()
                return
            running = False


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()