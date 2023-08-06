from robot.api.deco import keyword
from robot.api import Error

class Text():
    ###Return text divide ###
    def split_text(self, text:str, lengh:int=6):
        try:
            return text[0:lengh]
        except Exception as e:
            raise Error(e)