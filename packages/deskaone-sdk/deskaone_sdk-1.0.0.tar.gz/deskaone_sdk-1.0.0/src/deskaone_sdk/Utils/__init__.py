__version_code__    = '1.0.0'
__version__         = int(__version_code__.replace('.', ''))

from os import urandom
import random
import string
from .Timer import Timer, Color, Typer
from .Reset import Reset
from .Crypto import Crypto
from .ProgressBar import ProgressBar
from .AWSViker import AWSViker
from .UserAgent import UserAgent
from .Reverse import Reverse
from .Random import Random