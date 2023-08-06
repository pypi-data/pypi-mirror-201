import random

from robot.api import Error

class ViaNumber():
    ### Choose number in range ###
    def choose_number(self, stopNumber):
        try:
            return random.randrange(1, stopNumber)
        except Exception as e:
            raise Error(e)
