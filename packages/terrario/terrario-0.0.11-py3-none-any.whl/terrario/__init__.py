import sys

sys.path.append("/terrario/src/terrario")
sys.path.append("/src/terrario")
sys.path.append("/terrario")
sys.path.append(".")

from Classes.game import Game


def run():
    Game()