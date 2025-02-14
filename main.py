# ------------ imports ------------
import os
from character_subclass import (
    HeroWarrior,
    HeroArcher,
    HeroPaladin,
    EnenmyArcher,
    EnenmyPaladin,
    EnenmyWarrior,
)
from turn_base import TurnBase
import inquirer
import random


# ------------ setup ------------
def initial_stage():
    global hero, enemy, control
    choices = [
        "⚔️ Warrior (Balance)",
        "🛡️ Paladin (⬇️ATK ,⬆️DEF)",
        "🏹 Archer (⬆️ATK , ⬇️DEF)",
    ]
    questions = [
        inquirer.List(
            "choice",
            message="Select your hero class",
            choices=choices,
        ),
    ]

    selected_class = inquirer.prompt(questions)["choice"]
    if selected_class == choices[0]:
        hero = HeroWarrior(name="Hero")
    elif selected_class == choices[1]:
        hero = HeroPaladin(name="Hero")
    elif selected_class == choices[2]:
        hero = HeroArcher(name="Hero")

    # random enemy class
    enemy_class = random.choice(choices)
    if enemy_class == choices[0]:
        enemy = EnenmyWarrior(name="Enemy")
    elif enemy_class == choices[1]:
        enemy = EnenmyPaladin(name="Enemy")
    elif enemy_class == choices[2]:
        enemy = EnenmyArcher(name="Enemy")

    control = TurnBase(hero, enemy)
    print()
    print("You have select: ", selected_class)
    print("You Enemy is: ", enemy_class)
    print()
    print("Enter to continue...")
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
        print()
        print("Enemy Won!")
        input()
        break
    elif enemy.health == 0:
        print()
        print("Hero Won!")
        input()
        break

    print()
    control.input_choice()
    control.draw_hero_enemy_choice()
    control.proccess_choice()

    # -----------------------
    os.system("cls")

    hero.health_bar.draw()
    enemy.health_bar.draw()
    print()
    control.draw_hero_enemy_choice()
    print()
    print("Enter to next round")
    input()
