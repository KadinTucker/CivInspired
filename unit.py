

HITPOINTS = 20
BOUT_DAMAGE = 10

class Unit:

    def __init__(self, owner, x, y, strength, skill):
        self.x = x
        self.y = y
        self.owner = owner

        self.strength = strength
        self.skill = skill

        self.hp = HITPOINTS


def bout(unit1, unit2):
    damage1 = BOUT_DAMAGE * unit2.strength / (unit1.strength + unit2.strength)
    damage2 = BOUT_DAMAGE * unit1.strength / (unit1.strength + unit2.strength)
    if damage1 > unit1.hp:
        damage1 = unit1.hp
        damage2 = damage1 * unit1.strength / unit2.strength
    if damage2 > unit2.hp:
        damage2 = unit2.hp
        damage1 = damage2 * unit2.strength / unit1.strength
    return int(damage1), int(damage2)

def combat(unit1, unit2):
    # First, check for skill differences
    if unit1.skill > unit2.skill:
        for _ in range(unit1.skill - unit2.skill):
            damage1, damage2 = bout(unit1, unit2)
            unit2.hp -= damage2
    elif unit2.skill > unit1.skill:
        for _ in range(unit2.skill - unit1.skill):
            damage1, damage2 = bout(unit1, unit2)
            unit1.hp -= damage1
    damage1, damage2 = bout(unit1, unit2)
    unit1.hp -= damage1
    unit2.hp -= damage2


def main():
    # Test function
    unit1 = Unit(None, 0, 0, 3, 1)
    unit2 = Unit(None, 0, 0, 2, 2)
    for _ in range(4):
        combat(unit1, unit2)
        print("Unit I has %s hitpoints, Unit II has %s hitpoints." % (unit1.hp, unit2.hp))


if __name__ == '__main__':
    main()
