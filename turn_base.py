# ------------ imports ------------
import os
import random
from character import Hero, Enemy
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
        choices = ["A", "C", "D"]

        self.enemy_choice = random.choice(choices)

    def draw_hero_enemy_choice(self):
        choiceEmoji = {"A": "🗡️", "C": "💥", "D": "🛡️"}
        print("Hero :", choiceEmoji[self.hero_choice])
        print("Enemy: ", choiceEmoji[self.enemy_choice])
        if self.hero_choice == self.enemy_choice:
            print("Tie!")
        elif self.hero_choice == "A" and self.enemy_choice == "C":
            self.print_hero_win()
        elif self.hero_choice == "C" and self.enemy_choice == "D":
            self.print_hero_win()
        elif self.hero_choice == "D" and self.enemy_choice == "A":
            self.print_hero_win()
        else:
            self.print_enemy_win()

    def proccess_choice(self):
        if self.hero_choice == self.enemy_choice:
            print("Tie!")
        elif self.hero_choice == "A" and self.enemy_choice == "C":
            self.hero_win()
        elif self.hero_choice == "C" and self.enemy_choice == "D":
            self.hero_win()
        elif self.hero_choice == "D" and self.enemy_choice == "A":
            self.hero_win()
        else:
            self.enemy_win()
            print("Something Error")

    def hero_win(self):
        self.hero.attack(self.enemy)

    def enemy_win(self):
        self.enemy.attack(self.hero)

    def print_hero_win(self):
        self.hero.print_attack(self.enemy)

    def print_enemy_win(self):
        self.enemy.print_attack(self.hero)
