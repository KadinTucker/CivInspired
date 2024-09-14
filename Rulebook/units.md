# Units

Units are representations of a civilisation's deployed military forces. 

Units have a location in the world, a strength rating, a skill rating, and a number of hitpoints, or pips, up to a maximum of 20.

### Movement

Units can move from one location to another, with better ability to move with better logistical infrastructure. 

The maximum movement of a unit is greatly boosted by:
 - Open, more easily traversed terrain;
 - Territory under friendly control;
 - Already explored (mapped) land;
 - Built infrastructure, including roads and harbours.

#### Attrition

When units move through hostile territory, including unconquered territory or territory of an enemy civilisation, they suffer some damage, representing a combination of low availability of supplies and potential enemy and/or barbarian skirmishers. Units also suffer attrition every turn they stay in enemy territory. 

Attrition is reduced by having more advanced technology or by conquering the territory and "setting up camp". 

### Combat

When two enemy units fight each other, a battle occurs. The strength and skill ratings of the two units determine how they fight.

#### Strength

The relative strength values of the two units determine how many hits are dealt for each hit received. 

For example, if one unit, Unit I, has a strength of 1 and another, Unit II, has a strength of 2, then for each 1 damage dealt by Unit I, Unit II will deal 2 damage. 

In a single bout of combat, a maximum total of 10 damage can be dealt. Less than 5 damage will be dealt in the case of one unit reaching 0 hitpoints. In this case, only as much damage is dealt as is necessary to bring the unit to 0 hitpoints, and the other unit takes an amount of damage in proportion to how much damage is dealt this way. For example, if Unit I has a strength of 1 and 4 hitpoints, while Unit II has a strength of 2 and 20 hitpoints, then ordinarily Unit I should deal 3 damage while Unit II deals 7 damage (damages are rounded). However, Unit I can only take 4 of the 7 total damage. To keep the proportions correct, Unit II deals only 4 damage, and Unit I then deals only 2 damage. 

#### Skill

The skill values of the two units determines any "free bouts" that occur before the main battle. If one unit has higher skill than the other, then that unit gets a number of "free bouts" to attack the other unit without taking damage. 

In a free bout, the two units fight according to their strength value, but the unit dealing a free bout takes none of the damage it would receive. For example, if Unit I has a strength of 4 and Unit II has a strength of 6 and Unit I gets one free bout, then Unit I deals 4 damage and would take 6 damage, but it does not take this damage. Then the two units fight: Unit I deals 4 damage and Unit II deals 6 damage. In total, Unit I deals 8 damage and Unit II deals 6 damage. 

If after a free bout one of the units would die, the battle ends. 

The number of free bouts that occur equals the amount by which the more skilled unit's skill exceeds the other. If Unit I has 2 skill and Unit II has 1, then Unit I gets one free bout. If Unit I has 2 skill and Unit II has 4 skill, then Unit II gets 2 free bouts against Unit I. 

Wounded skilled units may deal reduced damage on their free bouts. If during the free bout the damage the unit would take would "kill" the unit, the overall damage dealt during the bout is reduced as it would be during an ordinary bout. For example, if Unit I would have only 3 hitpoints remaining, then during the free bout it could only take 3 damage, and thus would only deal 2 damage. Then Unit I would also only deal this 2 damage during its free bout.

Skill makes units much, much stronger, and high skill is reserved for technologically advanced units, and "elite" units that have special training and equipment. 

#### Estimating Army Strength

Without any skill differences in units, the strength of an army equals the total hitpoints times the strength value. Whoever has the higher strength is favoured to win an all-out war.

With skill differences factored in, for each skill above the "standard" amount, a unit has one more than that many times higher strength. A unit with 1 skill above the enemy's "standard" amount, that unit can be considered to have double the strength. A unit with 2 skill above the "standard" can be considered to have triple the strength. 

### Conquering

Units can be used to conquer territory, which causes the unit to be damaged. 

The cost to conquer a territory depends on the unit's strength, and the defensive strength of the territory. Conquering a territory happens as though the unit needs to deal 10 damage to the territory in a combat, and the unit thus takes as much damage as it would in combat with a defending unit with the defensive strength of the territory. 

A group of units may conquer a territory even if it would cost 20 hitpoints or more, provided that the pooled number of hitpoints is high enough.

The cost of conquering a territory is summarised in the following table:

| Unit Strength | Territory Defensive Strength | Hitpoint Cost to Conquer | Example Situation                                           |
|---------------|------------------------------|--------------------------|-------------------------------------------------------------|
| 1             | 1                            | 10                       | Basic soldier conquering neutral territory                  |
| 2             | 1                            | 5                        | Equipped soldier conquering neutral territory               |
| 2             | 2                            | 10                       | Equipped soldier conquering rival territory                 |
| 10            | 1                            | 1                        | Technologically advanced soldier conquering neutral territory |
| 1             | 2                            | 20                       | Basic soldier conquering rival territory                    |

Skill is not accounted for when conquering territories. 