from .Color import Color
from .Typer import Typer
import random

class ProgressBar:
    
    def __init__(self, iteration: int, total: int, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r", ending = '\n') -> None:        
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        color = [Color.WHITE, Color.RED, Color.GREEN, Color.BLUE, Color.CYAN, Color.MAGENTA, Color.YELLOW]
        normal = ' ' * (length - filledLength)
        bar = f'{color[random.randint(0, len(color) - 1)]}{fill * filledLength}{normal}'
        Typer.Print(f'\r{prefix} |{bar}{Color.WHITE}| {Color.GREEN}{percent}% {Color.WHITE}Progress', Refresh=True) if printEnd == '\r' else Typer.Print(f'\r{prefix} |{bar}{Color.WHITE}| {Color.GREEN}{percent}% {Color.WHITE}Progress', Enter=True)
        if iteration == total: 
            bar = f'{Color.GREEN}{fill * filledLength}{normal}'
            Typer.Print(f'\r{prefix} |{bar}{Color.WHITE}| {Color.GREEN}{percent}% {Color.WHITE}{suffix}', Refresh=True) if ending == '\r' else Typer.Print(f'\r{prefix} |{bar}{Color.WHITE}| {Color.GREEN}{percent}% {Color.WHITE}{suffix}', Enter=True)