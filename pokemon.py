from random import randint
from time import sleep

class Pokemon:
    def __init__(self, name, level, species):
        """Class to represent a Pokemon

        Args:
            name (string): friendly name of pokemon
            level (float): the "power level"
            species (string): the type of pokemon, such as "fire", "water", 
                etc...
        """
        
        self.name = name
        self.level = level
        self.species = species

        # base defaults
        self.starting_health = 1000
        self.atk_strength = 100 * self.level
        self.element = None
        self.resistance = {}
        
        # flags and stateful information
        self.current_health = self.starting_health
        self.knocked_out = False
        
    def __repr__(self):
        return f"[{self.level}][{self.current_health}] {self.name}"

    # Things that all pokemon can do
    def levelUp(self, ammt):
        self.level += ammt
        self.atk_strength = self.level * 100
        self.resetHealth()

    def avoided(self, element, factor):
        threshold = self.resistance[element] * factor
        if randint(1, 100) < threshold:
            return True
        return False

    def takeDamage(self, ammt):
        if not self.knocked_out:
            base, element = ammt
            if self.avoided(element, 75):
                print(f"{self.name} dodged!")
                return False
            else:
                damage = base * self.resistance[element]

                self.current_health -= damage
                print(f"It dealt {damage} damage!")

                if self.current_health < 0:
                    self.knocked_out = True
                    self.current_health = 0
                    print(f"{self} is knocked out!!")

                return True
        else:
            return False
    
    def heal(self, ammt):
        self.current_health += ammt
        if self.current_health > 0:
            self.knocked_out = False

    def resetHealth(self):
        self.current_health = self.starting_health

    def revive(self):
        if self.knocked_out:
            self.current_health = (0.90/self.level) * self.starting_health
    
    # Stuff we can do to other pokemon, or "Abilities"
    def reviveOther(self, pokemon):
        if self.level > 2:
            pokemon.revive()
        else:
            print("Must be level 2 to use reviveOther!")

    def attack(self, pokemon, extra=0):
        if pokemon.knocked_out:
            return True
        if self.knocked_out:
            return False
        else:
            print(f"{self} is attacking {pokemon}!")
            ammt = (self.atk_strength + extra, self.element)
            pokemon.takeDamage(self, ammt)
            return False

class Firetype(Pokemon):
    def __init__(self, name, level, species="fire"):
        super().__init__(name, level, species)
        self.starting_health = (1.4 * 1000) + (self.level * 500)
        self.current_health = self.starting_health
        self.element = "fire"
        self.resistance = {
            "fire": 0.8,
            "water": 0.3,
        }

        self.pheonixUsed = 0

    def takeDamage(self, ammt, pokemon):
        if not self.knocked_out:
            base, element = ammt
            if self.avoided(element, 75):
                print(f"{self.name} dodged!")
                return False
            else:
                damage = base * self.resistance[element]

                self.current_health -= damage
                print(f"It dealt {damage} damage!")

                if self.current_health < 0:
                    self.knocked_out = True
                    self.current_health = 0
                    print(f"{self} is knocked out!!")

                return True
        else:
            while True:
                use_pheonix = input(f"{self.name}, Use Pheonix? [y/n]: ")
                if use_pheonix == "y":
                    self.pheonix(pokemon)

    def pheonix(self, pokemon):
        if not self.pheonixUsed < self.level:
            print(f"{self.name} used pheonix on {pokemon}!")
            self.revive()
            # As the firetypes level increases, the number of uses for this
            # ability is increased, yet potency is decreased
            self.attack(pokemon, extra=350/self.level)
            self.pheonixUsed += 1

class Watertype(Pokemon):
    def __init__(self, name, level, species="water"):
        super().__init__(name, level, species)
        self.starting_health = (1.2 * 1000) + (self.level * 500)
        self.current_health = self.starting_health
        self.element = "water"
        self.resistance = {
            "fire": 0.69,
            "water": 0.92,
        }
    
    def medic(self, pokemon):
        # TODO: Add way for water type pokemon to heal all other
        # pokemon in the trainers deck by an ammount based on its
        # level
        pass

def dramaticEffect(p1, p2):
    print("Starting Simulation!\n\n\n")
    print(p1)
    sleep(1)
    print("VS".center(140, "-"))
    sleep(2)
    print(p2)
    sleep(2)
    print("\n\n\nBEGIN!!!!\n\n\n\n")
    sleep(3)

def simulateFight(p1, p2, turns=100, dramatic=False):
    
    if dramatic:
        dramaticEffect(p1, p2)

    for i in range(turns):
        print(f"Turn {i+1}!")
        if p1.attack(p2):
            print(f"{p1.name} wins!")
            break
        if p2.attack(p1):
            print(f"{p2.name} wins!")
            break
