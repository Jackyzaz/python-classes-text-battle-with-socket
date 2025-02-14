# ------------ imports ------------
import os
import random
from character import Hero, Enemy
from pprint import pprint
import inquirer

# ------------ setup ------------
os.system("")


# ------------ class setup ------------
class TurnBase:
    def __init__(self, hero: Hero, enemy: Enemy):
        self.hero_choice = ""
        self.enemy_choice = ""
        self.hero = hero
        self.enemy = enemy

    def update(self) -> None:
        self.current_value = self.entity.health

    def input_choice(self):
        self.hero_choice = ""
        choices = ["🗡️ Attack", "💥 Counter", "🛡️ Defense"]
        choicesMap = {choices[0]: "A", choices[1]: "C", choices[2]: "D"}
        questions = [
            inquirer.List(
                "choice",
                message="What size do you need?",
                choices=choices,
            ),
        ]
        self.hero_choice = choicesMap[inquirer.prompt(questions)["choice"]]

    def proccess_choice(self):
        choices = ["A", "C", "D"]
        choiceEmoji = {"A": "🗡️", "C": "💥", "D": "🛡️"}
        self.enemy_choice = random.choice(choices)
        print("Hero :", choiceEmoji[self.hero_choice])
        print("Enemy: ", choiceEmoji[self.enemy_choice])

        if self.hero_choice == self.enemy_choice:
            print("Tie!")
        elif self.hero_choice == "A" and self.enemy_choice == "C":
            self.hero_win()

        elif self.hero_choice == "A" and self.enemy_choice == "D":
            self.enemy_win()
        elif self.hero_choice == "C" and self.enemy_choice == "D":
            self.hero_win()
        elif self.hero_choice == "C" and self.enemy_choice == "A":
            self.enemy_win()
        elif self.hero_choice == "D" and self.enemy_choice == "C":
            self.enemy_win()
        elif self.hero_choice == "D" and self.enemy_choice == "A":
            self.hero_win()
        else:
            print("Something Error")

    def hero_win(self):
        self.hero.attack(self.enemy)

    def enemy_win(self):
        self.enemy.attack(self.hero)
