import os, glob
from .parse_all import *

__copyright__    = 'Copyright (C) 2022 BoronSpoon'
__version__      = '1.3.39b'
__license__      = 'MIT License'
__author__       = 'boronspoon'
__author_email__ = 'rayanticlimactic@gmail.com'
__url__          = 'http://github.com/BoronSpoon/vern'

__all__ = [
    #os.path.split(os.path.splitext(file)[0])[1] for file in glob.glob(os.path.join(os.path.dirname(__file__), '*.py')) if '__' not in file
    'Vern'
]