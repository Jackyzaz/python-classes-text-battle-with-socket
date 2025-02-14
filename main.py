# ------------ imports ------------
import os
from character import Hero, Enemy
from weapon import short_bow, iron_sword
from turn_base import TurnBase
import time

# ------------ setup ------------
hero = Hero(name="Hero", health=100)
hero.equip(iron_sword)
enemy = Enemy(name="Enemy", health=100, weapon=short_bow)
control = TurnBase(hero, enemy)
# ------------ game loop ------------
while True:

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
