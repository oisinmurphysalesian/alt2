#open file
import pandas as pd

def open_file():
    df = pandas.read_csv('data.csv' , sep=',')

## determine segments


### write files
def write_file(dataframe, path):
    #asdf
    dataframe.to_csv(path)