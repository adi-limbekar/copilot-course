clues = [
    "There is a faint scorch mark on the wall that whispers of a long-ago blaze.",
    "There is a hidden note folded tight, its ink faded by time and secrecy.",
    "There is a shattered glass fragment that hints at a hurried exit.",
    "There is a damp footprint that suggests someone passed through in the dark.",
    "There is a lingering scent of smoke that recalls an intense moment.",
    "There is a loose floorboard that covers a story left unresolved.",
    "There is a faint echo of footsteps that implies someone left in haste.",
    "There is a forgotten object that belonged to a presence now gone.",
    "There is a cracked mirror reflecting a memory of what once occurred.",
    "There is a threadbare curtain that hid something worth remembering."
]

sense_exp = [
    "You see candlelight trembling on cold stone and shadows that move without wind.",
    "You hear a distant drip echoing through corridors long abandoned.",
    "You smell old incense mingled with the faint sweetness of dried lavender.",
    "You touch the rough iron of a door handle that has been turned by many hands.",
    "You sense a chill on your neck as if someone unseen watched from the darkness.",
    "You see a tapestry fluttering though no breeze stirs the air.",
    "You hear soft footsteps fading into the depths of the hall.",
    "You smell smoke from a hearth that has not burned in years.",
    "You touch a crack in the wall and feel the cold breath of hidden passageways.",
    "You sense a pulse of quiet urgency, like the room itself holds its breath.",
    "You see a single cobweb glinting in the light of a distant torch.",
    "You hear a whisper of silk and something moving just beyond sight."
]

from enum import Enum
from abc import ABC, abstractmethod
import random


class encounter_outcome(Enum):
    CONTINUE = 'CONTINUE'
    END = 'END'


EncounterOutcome = encounter_outcome


class Encounter(ABC):
    @abstractmethod
    def run_encounter(self):
        """Run the encounter and return an EncounterOutcome."""
        pass

class DefaultEncounter(Encounter):
    def __init__(self):
        self.generator = SenseClueGenerator()

    def run_encounter(self):
        senseclue = self.generator.pull_random_item()
        print(senseclue)
        return EncounterOutcome.CONTINUE


class TreasureEncounter(Encounter):
    def run_encounter(self):
        print("You found the treasure! You have won the game!")
        return EncounterOutcome.END


class RedWizard(Encounter):
    def __init__(self):
        self.game_rules = {
            "Fireball": ["Ice Shard", "Lightning Bolt"],
            "Ice Shard": ["Wind Gust", "Earthquake"],
            "Wind Gust": ["Lightning Bolt", "Fireball"],
            "Lightning Bolt": ["Earthquake", "Ice Shard"],
            "Earthquake": ["Fireball", "Wind Gust"]
        }

    def run_encounter(self):
        print("\nA Red Wizard appears! Engage in a spell battle to proceed.")
        print("Spell Rules: Fireball melts Ice Shard and evaporates Lightning Bolt,")
        print("             Ice Shard freezes Wind Gust and shatters Earthquake,")
        print("             Wind Gust extinguishes Lightning Bolt and fuels Fireball,")
        print("             Lightning Bolt splits Earthquake and superheats Ice Shard,")
        print("             Earthquake quenches Fireball and grounds Wind Gust.\n")

        choices = list(self.game_rules.keys())

        while True:
            user_choice = input("Choose your spell (Fireball, Ice Shard, Wind Gust, Lightning Bolt, Earthquake): ").strip()
            if user_choice not in choices:
                print("Invalid spell. Please choose from: Fireball, Ice Shard, Wind Gust, Lightning Bolt, Earthquake.")
                continue

            wizard_choice = random.choice(choices)
            print(f"You cast: {user_choice}")
            print(f"The Red Wizard casts: {wizard_choice}")

            if user_choice == wizard_choice:
                print("The spells clash and cancel each other out! Cast again.\n")
                continue

            if wizard_choice in self.game_rules[user_choice]:
                print("Your spell prevails! The Red Wizard has been vanquished from this castle.\n")
                return EncounterOutcome.CONTINUE
            else:
                print("The Red Wizard's spell overpowers yours! You have been vanquished from this castle.\n")
                return EncounterOutcome.END

class BlueWizard(Encounter):
    def __init__(self):
        self.win_map = {
            "Staff": "Crystal",
            "Crystal": "Tome",
            "Tome": "Staff"
        }

    def run_encounter(self):
        print("\nA Blue Wizard appears! Challenge the wizard to a magical duel.")
        print("Game Rules: Staff crushes Crystal, Crystal shatters Tome, Tome binds Staff.\n")

        choices = list(self.win_map.keys())

        while True:
            user_choice = input("Choose your move (Staff, Crystal, Tome): ").strip().title()
            if user_choice not in choices:
                print("Invalid move. Please choose Staff, Crystal, or Tome.")
                continue

            wizard_choice = random.choice(choices)
            print(f"You choose: {user_choice}")
            print(f"The Blue Wizard chooses: {wizard_choice}\n")

            if user_choice == wizard_choice:
                print("It's a draw! The duel continues...\n")
                continue

            if self.win_map[user_choice] == wizard_choice:
                print("Your move defeats the Blue Wizard! The Red Wizard has been vanquished from this castle.\n")
                return EncounterOutcome.CONTINUE

            print("The Blue Wizard's move overpowers yours! You have been vanquished from this castle.\n")
            return EncounterOutcome.END

class RandomItemSelector:
    def __init__(self, items):
        self.items = list(items)
        self.used_items = []

    def add_item(self, item):
        self.items.append(item)

    def pull_random_item(self):
        if not self.items:
            self.used_items.clear()
            return None

        available_items = [item for item in self.items if item not in self.used_items]

        if not available_items:
            self.reset()
            available_items = list(self.items)

        selected = random.choice(available_items)
        self.used_items.append(selected)
        return selected

    def reset(self):
        self.used_items.clear()


class SenseClueGenerator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SenseClueGenerator, cls).__new__(cls)
            cls._instance.clue_selector = RandomItemSelector(clues)
            cls._instance.sense_selector = RandomItemSelector(sense_exp)
        return cls._instance

    def get_senseclue(self):
        clue = self.clue_selector.pull_random_item()
        sense = self.sense_selector.pull_random_item()
        if clue and sense:
            return f"{clue} {sense}"
        return clue or sense or ""

    def pull_random_item(self):
        return self.get_senseclue()


class Room:
    def __init__(self, name, encounter):
        self.name = name
        self.encounter = encounter

    def visit_room(self):
        return self.encounter.run_encounter()


rooms = [
    Room("Great Hall", DefaultEncounter()),
    Room("Armory", DefaultEncounter()),
    Room("Library", DefaultEncounter()),
    Room("Chapel", DefaultEncounter()),
    Room("Tower Chamber", DefaultEncounter()),
    Room("Dungeon", DefaultEncounter())
]


class Castle:
    def __init__(self, rooms):
        self.room_selector = RandomItemSelector(rooms)

    def select_door(self):
        door_count = random.randint(2, 4)
        print(f"\nYou stand before {door_count} doors.")

        while True:
            choice = input(f"Choose a door number between 1 and {door_count}: ")
            if not choice.isdigit():
                print("Invalid input. Please enter a number.")
                continue

            door_number = int(choice)
            if 1 <= door_number <= door_count:
                print(f"You open door {door_number}...\n")
                return door_number

            print(f"Please choose a door between 1 and {door_count}.")

    def next_room(self):
        self.select_door()
        room = self.room_selector.pull_random_item()
        print(f"You arrive in the {room.name}.")
        return room.visit_room()

    def reset(self):
        self.room_selector.reset()


class Game:
    def __init__(self, rooms):
        self.castle = Castle(rooms)

    def play_game(self):
        print("Welcome to the Castle Adventure!")
        print("Your objective is to navigate through the castle and find the treasure.")
        print("Choose doors wisely and explore each room.\n")

        while True:
            outcome = self.castle.next_room()
            if outcome == EncounterOutcome.END:
                self.castle.reset()
                print("\nGame Over!")
                play_again = input("Would you like to explore a different castle? (yes/no): ").strip().lower()
                if play_again != 'yes':
                    break
                print("Starting a new adventure...\n")

# add a Treasure Room with a Treasure Encounter to the rooms list
rooms.append(Room("Treasure Room", TreasureEncounter()))

# create a room called “The Red Wizard’s Lair” with the Red Wizard Encounter and add it to the rooms list
rooms.append(Room("The Red Wizard’s Lair", RedWizard()))

# create a room called “The Blue Wizard’s Lair” with the Blue Wizard Encounter and add it to the rooms list
rooms.append(Room("The Blue Wizard’s Lair", BlueWizard()))

game = Game(rooms);
game.play_game()