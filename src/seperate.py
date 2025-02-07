
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
    value = []
    amounts = []
    for item in input_list:
        if item not in value:
            value.append(item)
    for colour in value:
        total = input_list.count(colour)
        amounts.append(total)
        
    maxFreq = max(amounts)
    maxFreqIndex = amounts.index(maxFreq)
    mode = value[maxFreqIndex]
    

    return mode

def mean(input_list):
    total = 0
    for item in input_list:
        total += item
    average = total / len(input_list)
    return average

df = open_file()



alsdjkfasjk = [1,2,2,2,3,4,4,5,6,7,8]

print(mode(alsdjkfasjk))