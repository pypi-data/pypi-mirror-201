from robot.api.deco import keyword
from robot.api import Error


class ViaText():
    ###Return text divide ###
    @keyword(name="Split Text")
    def split_text(self, text:str, lengh:int=6):
        try:
            return text[0:lengh]
        except Exception as e:
            raise Error(e)