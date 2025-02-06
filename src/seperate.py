
#open file
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
from IPython.display import display

def open_file():
    df = pd.read_csv('debug.csv' , sep=',')
    return df
## determine segments


### write files
def write_file(dataframe, path):
    #asdf
    pd.dataframe.to_csv(path)


def split_dataframes(input_dataframe):
    dataframes = []
    while(True):
        new_dataframe = pd.DataFrame()
        #always include  first few cols

        #take title of col, and clean it
        title = input_dataframe.columns[5][0]
        print(title)
        #move right until col doesnt match
        #create dataframe from all matching cols
        #continue until col is blank
        exit()


def median(input_list):
    output_list = input_list
    return output_list

def mode(input_list):
    output_list = input_list
    return output_list

def mean(input_list):
    output_list = input_list
    return output_list

df = open_file()

df.style
display(df)
print(tabulate(df, headers = 'keys', tablefmt = 'psql'))

split_dataframes(df)

df