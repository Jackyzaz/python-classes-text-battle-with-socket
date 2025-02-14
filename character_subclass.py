from character import Hero
from weapon import hammer, short_bow, iron_sword

choices = [
    "⚔️ Warrior (Balance)",
    "🛡️ Paladin (⬇️ATK ,⬆️DEF)",
    "🏹 Archer (⬆️ATK , ⬇️DEF)",
]


class HeroWarrior(Hero):
    def __init__(self, name):
        super().__init__(name=name, health=100, classname=choices[0])
        self.equip(iron_sword)


class HeroPaladin(Hero):
    def __init__(self, name):
        super().__init__(name=name, health=200, classname=choices[1])
        self.equip(hammer)


class HeroArcher(Hero):
    def __init__(self, name):
        super().__init__(name=name, health=50, classname=choices[2])
        self.equip(short_bow)


class EnenmyWarrior(Enenmy):
    def __init__(self, name):
        super().__init__(name=name, health=100, classname=choices[0])
        self.equip(iron_sword)


class EnenmyPaladin(Enenmy):
    def __init__(self, name):
        super().__init__(name=name, health=200, classname=choices[1])
        self.equip(hammer)


class EnenmyArcher(Enenmy):
    def __init__(self, name):
        super().__init__(name=name, health=50, classname=choices[2])
        self.equip(short_bow)
