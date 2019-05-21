from collections import namedtuple
from random import choice, shuffle
import os
from time import sleep, time
import curses
import shutil

def clear_screen():
  os.system('cls' if os.name == 'nt' else 'clear')

class Shots:
  def __init__(self, filename='shots.txt'):
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
        display_text = '\n'
        display_text += '{}: {} '.format(shot.number,shot.name).center(lw, '=')
        display_text += '\n'
        display_text += shot.ingredients.center(lw)
        display_text += '\n'
        display_text += ''.center(lw, '=')

      clear_screen()
      print(display_text)

def main(win):
  win.nodelay(True)
  shots = Shots()
  while 1:
    try:
      key = win.getkey()
      if key == os.linesep:
        break
      shots.choose_random_shots()
    except Exception as e:
      pass

curses.wrapper(main)
