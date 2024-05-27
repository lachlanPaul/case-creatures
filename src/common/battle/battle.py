"""
    Manages the battle display, math and decision-making.

    "I've left behind my friends, my family, the only thing left for me is this. The battlefield"
"""
import random

from src.player_info import player_save_data as player
from src.common.battle import move_creature_types
from src.common.battle.moves import Move
from src.common.creatures import Creature
from src.common.menu.battle_menu import BattleMenu
from src.common.menu.text_box import TextBox


def get_first_conscious_creature():
    """Looks for the first creature in the team that is conscious and returns its index"""
    for i, creature in enumerate(player.team):
        if creature.current_health != 0:
            return i

    return 0


class Battle:
    def __init__(self, screen, enemy):
        self.player_inventory = player.inventory
        self.player_team = player.team
        self.player_current_creature_index = get_first_conscious_creature()
        self.player_current_creature = None

        self.enemy = enemy
        self.enemy_team = enemy.team
        self.enemy_current_creature_index = 0
        self.enemy_current_creature = self.enemy_team[self.enemy_current_creature_index]

        self.player_action = None
        self.enemy_action = None

        self.menu = BattleMenu(self, screen)

        self.set_current_creatures()
        self.turn()

    """
        Changes the current creature variables for easier use
    """
    def set_current_creatures(self):
        self.player_current_creature = self.player_team[self.player_current_creature_index]
        self.enemy_current_creature = self.enemy_team[self.enemy_current_creature_index]

    def use_attack(self, attacker: Creature, victim: Creature, attack: Move):
        victim.current_health - self.calculate_damage(attacker, victim, attack)
        if victim.current_health < 0:
            victim.current_health = 0

        if random.randint(0, 100) < attack.chance_of_poison and not victim.cannot_be_poisoned:
            victim.is_poisoned = True

        if random.randint(0, 100) < attack.chance_of_paralysis:
            victim.is_paralysed = True

        if random.randint(0, 100) < attack.chance_of_sleep:
            victim.is_sleeping = True

        self.menu.announce_attack_effectiveness(victim, attack)


    def calculate_damage(self, attacker: Creature, victim: Creature, attack: Move):
        attacker_level = attacker.level
        attacker_attack_power = attacker.attack
        attack_dam = attack.base_dam
        victim_defense = victim.defense

        # Deal a tiny bit more damage if the attacker has the same type as their attack
        if attack.move_type == attacker.creature_type:
            same_type_bonus = 1.5
        else:
            same_type_bonus = 1

        type_modifier = move_creature_types.type_modifier(victim.creature_type, attack.move_type)
        spicy_number = random.randint(217, 255)

        # Shamelessly stolen from https://www.math.miami.edu/~jam/azure/compendium/battdam.htm
        return ((((((((
                                  2 * attacker_level / 7) * attacker_attack_power * attack_dam) / victim_defense) / 50) + 2) * same_type_bonus) * type_modifier / 20) * spicy_number) / 255

    """
        Decides the enemy's action, and does the actions in the correct order
    """
    def turn(self):
        # TODO: Decide enemy action
        self.enemy_action = random.choice(self.enemy_current_creature.moves)

        priority = {
            self.player_action: self.player_current_creature.speed, #tackle:40
            self.enemy_action: self.enemy_current_creature.speed #run:30
        }

        print(priority)

        for i in priority.copy().values():
            if isinstance(i, Move) or (isinstance(i, Move) and i.hits_first):
                priority[i] = 99999


        values = list(priority.values())
        print(values)
        print("dad", priority)
        if values[0] == values[1]:
            # Return to original state if they both are meant to be first.
            # This'll also mean that if they're both doing a non move, it'll be sorted by the current creature speed.
            # I don't care so we'll let it happen
            priority = {
                self.player_action: self.player_current_creature.speed,
                self.enemy_action: self.enemy_current_creature.speed
            }

        # Sorts the dict by the speed values
        priority = dict(sorted(priority.items(), key=lambda item: item[1], reverse=True))
        print(priority)

        for j in priority.keys():
            if isinstance(j, Move):
                attacker = self.enemy_current_creature if j is self.enemy_action else self.player_current_creature
                victim = self.player_current_creature if attacker is self.enemy_action else self.enemy_current_creature
                self.use_attack(attacker, victim, j)