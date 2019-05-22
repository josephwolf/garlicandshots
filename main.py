from collections import namedtuple
from random import choice, shuffle
from time import sleep, time
from gpiozero import Button
import shutil
import os

def clear_screen():
  os.system('cls' if os.name == 'nt' else 'clear')

class Shots:
  def __init__(self, filename='./shots.txt'):
    self.shots = self.list_of_shots(filename)
    shuffle(self.shots)

  @staticmethod
  def list_of_shots(filename):
    Shot = namedtuple('shot', ('number', 'name', 'ingredients'))
    shots = []
    with open(filename) as f:
      for row in f:
        row = row.strip('\n')
        new_shot = Shot(*row.split(';'))
        shots.append(new_shot)

    return shots

  def random_shots(self, k=1):
    return [choice(self.shots) for _ in range(k)]

  def choose_random_shots(self, duration=2, delay=0.08, k=1):
    lw = shutil.get_terminal_size((80, 20)).columns
    time_to_end = time() + duration

    while time() < time_to_end:
      sleep(delay)
      shots = self.random_shots(k)

      for shot in shots:
        display_text = ' '.center(lw, ' ')*3
        display_text += ' {}: {} '.format(shot.number,shot.name).center(lw, '=')
        display_text += ' '.center(lw, ' ')
        display_text += shot.ingredients.center(lw)
        display_text += ' '.center(lw, ' ')
        display_text += ''.center(lw, '=')
        display_text += ' '.center(lw, ' ')*4

      clear_screen()
      print(display_text)


shots = Shots()
button = Button(25)

print("Created by Joey Wolf")
print("github: https://github.com/josephwolf")
print("Press the button to start!")

while True:
  try:
    if button.is_pressed:
      shots.choose_random_shots()
  except KeyboardInterrupt:
    pass
    