import random
import yaml

from robot.api import Error
from yaml.loader import SafeLoader

class FileYaml():
    ### Load data file yaml  ###
    def read_yaml_file(self, filename):
        absolute_path = f'{filename}.yaml'
        try:
            with open(absolute_path) as f:
                return yaml.load(f, Loader=SafeLoader)
        except Exception as e:
            raise Error(e)

class Text():
    ### Split text informations $text and $length cut  ###
    def split_text(self, text, length, start=0):
        try:
            return str(text)[start: int(length)]
        except Exception as e:
            raise Error(e)

### Cut text informations $separator and $length cut  ###
    def cut_text(self, text, separator, maxsplit):
        try:
            return str(text).rsplit(separator, -1)[maxsplit]
        except Exception as e:
            raise Error(e)

class Number():
    ### choose number in range the numbers  ###
    def choose_number(self, obj):
        try:
            return random.randrange(1, obj)
        except Exception as e:
            raise Error(e)
