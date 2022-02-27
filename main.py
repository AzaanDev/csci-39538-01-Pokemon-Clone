import keyboard
from termcolor import cprint
import time
import colorama
import random

colorama.init()

class Player:
    xPos = 8
    yPos = 12
    battlePokemon = None

    def __init__(self, name, gender, nature, money, pokemon, bag):
        self.pokemon = pokemon
        self.money = money
        self.bag = bag
        self.name = name
        self.gender = gender
        self.nature = nature

    def move(self, key):
        if key == 'w':
            self.yPos -= 1
        elif key == 's':
            self.yPos += 1
        elif key == 'a':
            self.xPos -= 1
        elif key == 'd':
            self.xPos += 1

        if self.xPos < 0:
            self.xPos = 0
        elif self.xPos > 9:
            self.xPos = 9
        if self.yPos <= 0:
            self.yPos = 0
        elif self.yPos > 19:
            self.yPos = 19

    def healthCheck(self):
        test = False
        for i in self.pokemon:
            if i.hp > 0:
                return int(0)
        if test is False:
            return int(1)

    def useBag(self):
        print("You have " + str(self.money) + " money!")
        print("Your Bag Contains: ")
        for i in self.bag:
            print(i)
        time.sleep(.3)
        print()
        item = input("Enter Name of Item to Use: ")
        for i in self.bag:
            if i == item and item == 'Normal Potion':
                print("Using Normal Potion")
                self.bag.remove("Normal Potion")
                self.battlePokemon.hp += 50
            elif i == item and item == "Full Restore":
                self.bag.remove("Full Restore")
                self.battlePokemon.hp = self.battlePokemon.health
            elif i == item and item == "Pokeball":
                self.bag.remove("Pokeball")
                return 1
            elif i == item and item == "Hyper Potion":
                self.bag.remove("Hyper Potion")
                self.battlePokemon.hp += 100
            if self.battlePokemon.hp > self.battlePokemon.health:
                self.battlePokemon.hp = self.battlePokemon.health
        return 0

    def swapPokemon(self):
        print("You have the following Pokemon available to swap:")
        for i in self.pokemon:
            if i.hp > 0:
                print(i.name)
        pokemon = input("Enter Name of Pokemon to select: ")
        for i in self.pokemon:
            if i.name == pokemon:
                self.battlePokemon = i


class Pokemon:
    hp = 0
    xPos = None
    yPos = None

    def __init__(self, name, nature, moves, health, gender):
        self.name = name
        self.types = nature
        self.moves = moves
        self.health = health
        self.gender = gender
        self.hp = health

    def fight(self, key):
        if key == '1':
            return self.moves[0].damage
        elif key == '2':
            return self.moves[1].damage
        elif key == '3':
            return self.moves[2].damage
        elif key == '4':
            return self.moves[3].damage

    def displayMoves(self):
        x = 1
        for i in self.moves:
            print(str(x) + ". " + i.name + " " + str(i.damage))
            x += 1


class CPU:
    battlePokemon = None
    xPos = None
    yPos = None

    def __init__(self, name, fact, reward, gift, pokemon):
        self.pokemon = pokemon
        self.reward = reward
        self.gift = gift
        self.name = name
        self.fact = fact
        self.battlePokemon = pokemon[0]

    def position(self, x, y):
        self.xPos = x
        self.yPos = y

    def healthCheck(self):
        test = False
        for i in self.pokemon:
            if i.hp > 0:
                return int(0)
        if test is False:
            return int(1)


class GridTile:
    def __init__(self, terrain, entity, xPos, yPos):
        self.terrain = terrain
        self.entity = entity
        self.xPos = xPos
        self.yPos = yPos


class AttackMoves:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage


moves = [
    AttackMoves("Overheat", 48),
    AttackMoves("Flamethrower", 38),
    AttackMoves("Dragon Claw", 29),
    AttackMoves("Wing Attack", 12),
    AttackMoves("Hydro Pump", 47),
    AttackMoves("Hydro Cannon", 50),
    AttackMoves("Flash Cannon", 37),
    AttackMoves("Bite", 12),
    AttackMoves("Hyper Beam", 39),
    AttackMoves("Dark Pulse", 26),
    AttackMoves("Hurricane", 48),
    AttackMoves("Grass Knot", 25),
    AttackMoves("Thunder", 50),
    AttackMoves("Thunderbolt", 30),
    AttackMoves("Ancient Power", 20),
    AttackMoves("Drill Peck", 15),
    AttackMoves("Zen Headbutt", 25),
    AttackMoves("Psycho Boost", 21),
    AttackMoves("Outrage", 40),
]


class Map:
    map = []

    def __init__(self, rows=20, cols=10):
        for i in range(rows):
            arr = []
            for j in range(cols):
                arr.append(GridTile("Grass", None, i, j))
            self.map.append(arr)

    def getEntity(self, xPos, yPos):
        return self.map[yPos][xPos].entity

    def addEntity(self, entity, xPos, yPos):
        self.map[yPos][xPos].entity = entity

    def update(self, player):
        for i in self.map:
            for j in i:
                if type(j) == str:
                    None
                if type(j.entity) == Player:
                    j.entity = None
                    if self.map[player.yPos][player.xPos].entity is None:
                        self.map[player.yPos][player.xPos].entity = player
                    else:
                        player.yPos += 1
                        self.map[player.yPos][player.xPos].entity = player

    def display(self):
        print()
        for i in self.map:
            for j in i:
                if j.entity is None and j.terrain == "Grass":
                    cprint("* ", 'green', end='')
                elif j.entity == "Full Restore":
                    cprint("Full Restore ", 'blue', end='')
                elif j.entity == "Healer":
                    cprint("Healer", 'blue', end='')
                elif type(j.entity) == Player:
                    cprint(j.entity.name + " ", 'magenta', end='')
                else:
                    cprint(j.entity.name + " ", 'red', end='')
            print()


class Game:
    player = Player("Azaan", "Male", "Funny", 5000, [], ["Pokeball", "Pokeball", "Pokeball", "Pokeball", "Normal Potion"])
    cpu = CPU("Godrick", "Likes to eat soup with a fork", 10000, "Hyper Potion",
              [Pokemon("Deoxys", "Psychic", [moves[8], moves[16], moves[17], moves[12]], 85, "Female"),
               Pokemon("Rayquaza", "Dragon", [moves[18], moves[3], moves[10], moves[14]], 120, "Female"),
               Pokemon("Mewtwo", "Psychic", [moves[5], moves[3], moves[9], moves[14]], 85, "Female")])
    zapdos = Pokemon("Zapdos", "Eletric", [moves[12], moves[3], moves[4], moves[15]], 100, "Male")
    Articuno = Pokemon("Articuno", "Ice", [moves[12], moves[6], moves[7], moves[15]], 150, "Female")
    Moltres = Pokemon("Moltres", "Fire", [moves[12], moves[8], moves[4], moves[1]], 120, "Female")
    map = Map()
    cpu.yPos = 7
    cpu.xPos = 7
    zapdos.yPos = 4
    zapdos.xPos = 4
    Moltres.yPos = 8
    Moltres.xPos = 2
    Articuno.yPos = 15
    Articuno.xPos = 9
    map.addEntity(player, player.xPos, player.yPos)
    map.addEntity(cpu, cpu.xPos, cpu.yPos)
    map.addEntity(zapdos, zapdos.xPos, zapdos.yPos)
    map.addEntity(Articuno, Articuno.xPos, Articuno.yPos)
    map.addEntity(Moltres, Moltres.xPos, Moltres.yPos)

    map.addEntity("Full Restore", 0, 0)
    map.addEntity("Healer", 0, 10)
    mode = 0

    def __init__(self):
        self.starting()
        while True:
            if self.mode == 1:
                self.movement()
            elif self.mode == 2:
                self.battle()

    def starting(self):
        pokemon = [Pokemon("Charizard", "Fire", [moves[0], moves[1], moves[2], moves[3]], 78, "Male"),
                   Pokemon("Blastoise", "Water", [moves[4], moves[5], moves[6], moves[7]], 100, "Male"),
                   Pokemon("Tornadus", "Flying", [moves[8], moves[9], moves[10], moves[11]], 79, "Female")]
        print("Selected a Pokemon")
        print("1. " + pokemon[0].name + " " + pokemon[0].types + " " + str(pokemon[0].health) + " " + pokemon[0].gender)
        print("2. " + pokemon[1].name + " " + pokemon[1].types + " " + str(pokemon[1].health) + " " + pokemon[1].gender)
        print("3. " + pokemon[2].name + " " + pokemon[2].types + " " + str(pokemon[2].health) + " " + pokemon[2].gender)
        while self.mode == 0:
            if keyboard.is_pressed('1'):
                print("Selected " + pokemon[0].name)
                self.player.pokemon.append(pokemon[0])
                self.mode = 1
            elif keyboard.is_pressed('2'):
                print("Selected " + pokemon[1].name)
                self.player.pokemon.append(pokemon[1])
                self.mode = 1
            elif keyboard.is_pressed('3'):
                print("Selected " + pokemon[2].name)
                self.player.pokemon.append(pokemon[2])
                self.mode = 1
        self.player.battlePokemon = self.player.pokemon[0]

    def inputs(self, inputVal):
        print()
        if inputVal == 'e' and self.map.getEntity(self.player.xPos, self.player.yPos - 1) is not None:
            entity = self.map.getEntity(self.player.xPos, self.player.yPos - 1)
            if entity == 'Full Restore':
                self.map.addEntity(None, self.player.xPos, self.player.yPos - 1);
                self.player.bag.append("Full Restore")
            elif entity == 'Healer':
                for i in self.player.pokemon:
                    i.hp = i.health
                print("Healing all Pokemon!")
                time.sleep(1)
            elif type(entity) == CPU or Pokemon:
                if self.player.healthCheck() == 0:
                    self.mode = 2
        elif inputVal == 'w' or 's' or 'd' or 'a':
            self.player.move(inputVal)
            self.mode = 1

    def movement(self):
        self.map.display()
        key = keyboard.read_key()
        if key == 'a' or 'w' or 's' or 'd' or 'e':
            self.inputs(key)
            time.sleep(0.1)
            self.map.update(self.player)
            self.map.display()

    def battle(self):
        entity = self.map.getEntity(self.player.xPos, self.player.yPos - 1)
        if self.player.healthCheck() == 1:
            self.mode = 1
            print("You Have Lost the Battle!")
            if type(entity) == Pokemon:
                entity.hp = entity.health
            else:
                for i in entity.pokemon:
                    i.hp = i.health
            time.sleep(.3)
            return

        currentPokemonFight = None
        if type(entity) == Pokemon:
            currentPokemonFight = entity
        if type(entity) == CPU:
            if entity.battlePokemon.hp > 0:
                currentPokemonFight = entity.battlePokemon
            else:
                for pokemon in entity.pokemon:
                    if pokemon.hp > 0:
                        currentPokemonFight = pokemon
                        break

        if self.player.battlePokemon.hp <= 0:
            for pokemon in self.player.pokemon:
                if pokemon.hp > 0:
                    self.player.battlePokemon = pokemon
                    break

        print("Player: " + self.player.name)
        print("Pokemon: " + self.player.battlePokemon.name + " " + str(self.player.battlePokemon.hp) + "/" + str(
            self.player.battlePokemon.health))
        print("5. Run")
        print("6. Fight")
        print("7. Use Bag")
        print("8. Change Pokemon")
        print()
        print("Enemy Pokemon: " + currentPokemonFight.name + " " + str(currentPokemonFight.hp) + "/" + str(
            currentPokemonFight.health))
        print()
        time.sleep(.3)
        key = keyboard.read_key()
        if key == '5' or '6' or '7' or '8':
            if key == '5':
                print("You ran away!")
                self.mode = 1
                if type(entity) == Pokemon:
                    entity.hp = entity.health
                else:
                    for i in entity.pokemon:
                        i.hp = i.health
                time.sleep(.3)
            elif key == '6':
                self.player.battlePokemon.displayMoves()
                time.sleep(.2)
                key = keyboard.read_key()
                if key == '1' or '2' or '3' or '4':
                    print(key)
                    currentPokemonFight.hp -= self.player.battlePokemon.fight(key)
                    print("Attacked " + currentPokemonFight.name + " for " + str(
                        self.player.battlePokemon.fight(key)) + " damage!")
                    if type(entity) == CPU:
                        if self.cpu.healthCheck() == 1:
                            self.mode = 1
                            print("You Have Won the Battle!")
                            print("You Have Recieved " + str(self.cpu.reward) + ". " + self.cpu.gift + " as a gift.")
                            self.player.money += self.cpu.reward
                            self.player.bag.append(self.cpu.gift)
                            self.map.addEntity(None, self.cpu.xPos, self.cpu.yPos)
                            time.sleep(0.5)
                            return
                    elif type(entity) == Pokemon and entity.hp < 0:
                        print(entity.name + " is Defeated!")
                        self.map.addEntity(None, entity.xPos, entity.yPos)
                        self.mode = 1
                        time.sleep(0.5)
                        return
                    randomNum = str(random.randint(1, 4))
                    self.player.battlePokemon.hp -= currentPokemonFight.fight(str(randomNum))
                    print()
                    print("You were Attacked by " + currentPokemonFight.name + " for " + str(
                        currentPokemonFight.fight(str(randomNum))) + " damage!")
            elif key == '7':
                if self.player.useBag() == 1:
                    if type(entity) == Pokemon:
                        if entity.hp < 30:
                            print("Capturing Pokemon! ")
                            time.sleep(.3)
                            print("You have captured " + entity.name)
                            self.player.pokemon.append(entity)
                            self.map.addEntity(None, entity.xPos, entity.yPos)
                            self.mode = 1
                            time.sleep(0.5)
                            return
            elif key == '8':
                self.player.swapPokemon()


def main():
    game = Game()


if __name__ == "__main__":
    main()
