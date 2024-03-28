"""
    Manages the battle display, math and decision-making.

    "I've left behind my friends, my family, the only thing left for me is this. The battlefield"
"""
import random

from src.common.battle import move_creature_types
from src.common.battle.moves import Move
from src.common.creatures import Creature
from src.common.menu.text_box import TextBox


class Battle:
    def __init__(self, opponent):
        self.starting_text = TextBox(f"{opponent.full_name} {opponent.wants_to_battle}")

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
        return ((((((((2 * attacker_level / 7) * attacker_attack_power * attack_dam) / victim_defense) / 50) + 2) * same_type_bonus) * type_modifier / 20) * spicy_number) / 255
