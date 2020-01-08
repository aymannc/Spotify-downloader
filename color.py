from colorama import init
from termcolor import colored


def printWithCol(text, color=None, back=None, nonline=False):
    init()
    try:
        print(colored(text, color, back), end="" if nonline else "\n")
    except:
        print(colored("Non supported song", "red", back), end="" if nonline else "\n")
