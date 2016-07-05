import os.path
import sys

if getattr(sys, 'frozen', False):
    data_path = os.path.join(os.environ.get("_MEIPASS2",os.path.abspath(".")),'data')
elif __file__:
    data_path = os.path.join(os.path.dirname(__file__),'data')

def path(filename):
    return os.path.join(data_path,filename)
