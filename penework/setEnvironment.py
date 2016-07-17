import os

from lib.core.common import setPaths
from lib.core.data import paths


def setEnv():

    paths.PENEWORK_ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
    setPaths()


if __name__ == '__main__':

    setEnv()
