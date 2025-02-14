# ------------ imports ------------
import os
from character import Hero, Enemy
from character_subclass import Warrior, Archer, Paladin
from turn_base import TurnBase
import inquirer
import random
from weapon import hammer, iron_sword, short_bow


# ------------ setup ------------
def initial_stage():
    global hero, enemy, control
    choices = ["⚔️ Warrior", "🛡️ Paladin", "🏹 Archer"]
    questions = [
        inquirer.List(
            "choice",
            message="Select your hero class",
            choices=choices,
        ),
    ]

    selected_class = inquirer.prompt(questions)["choice"]
    if selected_class == "⚔️ Warrior":
        hero = Warrior(name="Hero")
    elif selected_class == "🛡️ Paladin":
        hero = Paladin(name="Hero")
    elif selected_class == "🏹 Archer":
        hero = Archer(name="Hero")

    # random enemy class
    enemy_class = random.choice(choices)
    if enemy_class == "⚔️ Warrior":
        enemy = Enemy(name="Enemy", health=100, weapon=iron_sword, classname=choices[0])
    elif enemy_class == "🛡️ Paladin":
        enemy = Enemy(name="Enemy", health=200, weapon=hammer, classname=choices[1])
    elif enemy_class == "🏹 Archer":
        enemy = Enemy(name="Enemy", health=50, weapon=short_bow, classname=choices[2])

    control = TurnBase(hero, enemy)
    print()
    print("You have select: ", selected_class)
    print("You Enemy is: ", enemy_class)

    input()


# ------------ game loop ------------
os.system("cls")

hero = None
enemy = None
control = None
initial_stage()
while True:
    # default Hero

    os.system("cls")

    hero.health_bar.draw()
    enemy.health_bar.draw()
    if hero.health == 0:
        print("Enemy Won!")
        input()
        break
    elif enemy.health == 0:
        print("Hero Won!")
        input()
        break

    # control.draw_choice()
    print()
    control.input_choice()
    control.proccess_choice()
    # -----------------------
    os.system("cls")

    hero.health_bar.draw()
    enemy.health_bar.draw()
    print()
    # control.draw_choice()
    control.proccess_choice()
    input()
