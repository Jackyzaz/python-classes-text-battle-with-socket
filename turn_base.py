# ------------ imports ------------
import os
import random
from character import Hero, Enemy

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

    def draw_choice(self) -> None:
        print("--------------------------------------")
        print("[R] - 🗿 Rock ")
        print("[P] - 📃 Paper")
        print("[S] - ✂️ Scissor ")
        print("--------------------------------------")

    def input_choice(self):
        self.hero_choice = ""
        while self.hero_choice == "":
            self.hero_choice = input("Enter your choice: ").upper()
            if self.hero_choice == "":
                print("❌ Please enter a choice, cannot be empty.")
            elif self.hero_choice in "RPS":
                break
            else:
                self.hero_choice = ""
                print("❌ Pleas Enter Valid Choices")

    def proccess_choice(self):
        choices = ["R", "P", "S"]
        choiceEmoji = {"R": "🗿", "P": "📃", "S": "✂️"}
        self.enemy_choice = random.choice(choices)
        print("Hero :", choiceEmoji[self.hero_choice])
        print("Enemy: ", choiceEmoji[self.enemy_choice])

        if self.hero_choice == self.enemy_choice:
            print("Tie!")
        elif self.hero_choice == "R" and self.enemy_choice == "P":
            self.enemy_win()
        elif self.hero_choice == "R" and self.enemy_choice == "S":
            self.hero_win()
        elif self.hero_choice == "P" and self.enemy_choice == "S":
            self.enemy_win()
        elif self.hero_choice == "P" and self.enemy_choice == "R":
            self.hero_win()
        elif self.hero_choice == "S" and self.enemy_choice == "P":
            self.hero_win()
        elif self.hero_choice == "S" and self.enemy_choice == "R":
            self.enemy_win()
        else:
            print("Something Error")

    def hero_win(self):
        self.hero.attack(self.enemy)

    def enemy_win(self):
        self.enemy.attack(self.hero)
