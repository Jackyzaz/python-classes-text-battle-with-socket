from character import Hero
from weapon import hammer, short_bow, iron_sword

choices = ["⚔️ Warrior", "🛡️ Paladin", "🏹 Archer"]


class Warrior(Hero):
    def __init__(self, name):
        super().__init__(name=name, health=100, classname=choices[0])
        self.equip(iron_sword)


class Paladin(Hero):
    def __init__(self, name):
        super().__init__(name=name, health=200, classname=choices[1])
        self.equip(hammer)


class Archer(Hero):
    def __init__(self, name):
        super().__init__(name=name, health=50, classname=choices[2])
        self.equip(short_bow)
