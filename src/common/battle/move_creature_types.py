from enum import Enum


class Types(Enum):
    BASIC = 0
    FURNITURE = 1
    ELECTRICAL = 2
    TOOL = 3


def type_modifier(victim_type, attack_type):
    """
        Gives a type modifier based on if an attack is strong against the victim

        Basic: No strengths or weaknesses
        Furniture: Weak to Electrical, strong against Tool
        Electrical: Weak to Tool, strong against Furniture
        Tool: Weak to Furniture, strong against Electrical

        :return: 0(no damage), 2.5(not effective), 5(no effect), 10(effective), 20(very effective)
    """

    NO_DAM = 0
    NOT_EFFECTIVE = 2.5
    NO_EFFECT = 5
    EFFECTIVE = 10
    VERY_EFFECTIVE = 20

    match victim_type:
        case Types.FURNITURE:
            if attack_type == Types.ELECTRICAL:
                return EFFECTIVE
            elif attack_type == Types.TOOL:
                return NOT_EFFECTIVE
        case Types.ELECTRICAL:
            if attack_type == Types.TOOL:
                return EFFECTIVE
            elif attack_type == Types.FURNITURE:
                return NOT_EFFECTIVE
        case Types.TOOL:
            if attack_type == Types.FURNITURE:
                return EFFECTIVE
            elif attack_type == Types.ELECTRICAL:
                return NOT_EFFECTIVE

    # Default return value if the types don't have any special interaction
    return NO_EFFECT


