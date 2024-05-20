import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = Inventory()

    def take_damage(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0

class Enemy:
    def __init__(self, name, health, attack_damage):
        self.name = name
        self.health = health
        self.attack_damage = attack_damage

    def take_damage(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Puzzle:
    def __init__(self, description, solution):
        self.description = description
        self.solution = solution

class Room:
    def __init__(self, name, description, enemies=None, items=None, puzzle=None):
        self.name = name
        self.description = description
        self.enemies = enemies or []
        self.items = items or []
        self.puzzle = puzzle

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def remove_enemy(self, enemy):
        self.enemies.remove(enemy)

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

class Level:
    def __init__(self, name, rooms):
        self.name = name
        self.rooms = rooms

class Game:
    def __init__(self, player, levels):
        self.player = player
        self.levels = levels
        self.current_level = 0

    def start(self):
        print("Welcome to Mystic Quest!")
        self.play_level(self.current_level)

    def play_level(self, level_index):
        if level_index < len(self.levels):
            level = self.levels[level_index]
            print(f"\n--- Level {level.name} ---")
            for room in level.rooms:
                self.play_room(room)
            print(f"\n--- End of Level {level.name} ---")
            self.current_level += 1
            if self.current_level < len(self.levels):
                next_level_input = input("Press enter to continue to the next level...")
                if next_level_input.strip() == "":
                    self.play_level(self.current_level)
        else:
            print("Congratulations! You completed Mystic Quest.")

    def play_room(self, room):
        print(f"\nYou entered {room.name}. {room.description}")

        if room.puzzle:
            self.solve_puzzle(room.puzzle)

        if room.enemies:
            self.battle_enemies(room)

        if room.items:
            self.collect_items(room)

    def solve_puzzle(self, puzzle):
        print(f"\nYou encounter a puzzle: {puzzle.description}")
        print("Enter your answer:")
        user_answer = input().strip().lower()
        while user_answer != puzzle.solution:
            print("Incorrect answer. Try again:")
            user_answer = input().strip().lower()
        print("Congratulations! You solved the puzzle.")

    def battle_enemies(self, room):
        print("\nEnemies attack!")
        for enemy in room.enemies:
            while enemy.is_alive() and self.player.is_alive():
                player_attack = random.randint(5, 15)
                enemy_attack = random.randint(5, 15)
                self.player.take_damage(enemy_attack)
                enemy.take_damage(player_attack)
                print(f"{self.player.name} attacks {enemy.name} for {player_attack} damage.")
                print(f"{enemy.name} attacks {self.player.name} for {enemy_attack} damage.")
                if not enemy.is_alive():
                    print(f"{enemy.name} defeated!")
                    room.remove_enemy(enemy)
                    break
                if not self.player.is_alive():
                    print("Game over! You've been defeated.")
                    exit()

    def collect_items(self, room):
        print("\nYou find some items:")
        for item in room.items:
            print(f"- {item.name}: {item.description}")
            self.player.inventory.add_item(item)

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

def generate_puzzle():
    descriptions = [
        "What has keys but can't open locks?",
        "What has a head and a tail but no body?",
        "I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?"
    ]
    solutions = [
        "keyboard",
        "coin",
        "echo"
    ]
    index = random.randint(0, len(descriptions) - 1)
    return Puzzle(descriptions[index], solutions[index])

level1_rooms = [
    Room("Forest", "A dense forest filled with mysterious creatures.",
         [Enemy("Goblin", 20, 5), Enemy("Wolf", 30, 8)],
         [Item("Potion", "Restores health.")],
         generate_puzzle()),
    Room("Cave", "A dark and eerie cave.",
         [Enemy("Bat", 15, 7)],
         [Item("Key", "Unlocks a hidden door.")],
         generate_puzzle())
]

level2_rooms = [
    Room("Village", "A peaceful village surrounded by mountains.",
         [Enemy("Orc", 40, 10)],
         [Item("Scroll", "Contains ancient wisdom.")],
         generate_puzzle()),
    Room("Mountain", "Steep cliffs and treacherous paths.",
         [Enemy("Yeti", 60, 15)],
         [Item("Rope", "Helps in climbing.")],
         generate_puzzle())
]

level3_rooms = [
    Room("Underground", "A labyrinth of tunnels and chambers.",
         [Enemy("Minotaur", 80, 20)],
         [Item("Map", "Shows the way out.")],
         generate_puzzle()),
    Room("Throne Room", "The lair of the final boss.",
         [Enemy("Dragon", 100, 25)],
         [Item("Treasure", "A chest full of gold.")],
         generate_puzzle())
]

level1 = Level("1", level1_rooms)
level2 = Level("2", level2_rooms)
level3 = Level("3", level3_rooms)

player_name = input("Enter your name: ")
player = Player(player_name)

game = Game(player, [level1, level2, level3])
game.start()

