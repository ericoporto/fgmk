import os.path

data_path = os.path.join(os.path.dirname(__file__),'data')

def path(filename):
    return os.path.join(data_path,filename)
